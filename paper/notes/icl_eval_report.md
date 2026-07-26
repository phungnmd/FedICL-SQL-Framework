# Báo cáo đánh giá In-Context Learning (ICL) trong hệ Text-to-SQL liên kết

**Ngày:** 2026-07-26 · **Phạm vi:** toàn bộ kết quả đo đã có + việc cần đo thêm
**Đối tượng đọc:** người ngoài dự án — báo cáo tự chứa, không cần đọc tài liệu khác
**Nguồn số:** quét trực tiếp 103 dòng kết quả trong `experiments/*/results/*/metrics.json`

---

## 1. Hệ thống này làm gì

Bài toán: sinh câu lệnh SQL từ câu hỏi tiếng Anh (Text-to-SQL), trong bối cảnh
**dữ liệu không được tập trung** — nhiều bên (bệnh viện, ngân hàng, phòng ban)
mỗi bên giữ CSDL riêng, không chia sẻ dữ liệu thô cho nhau.

Cách giải quyết gồm ba lớp:

1. **Mô hình nhỏ (1,5 tỷ tham số)** được huấn luyện tại chỗ ở từng bên. Chỉ có
   trọng số adapter (bản vá nhẹ của mô hình) được gửi lên máy chủ, không có
   dữ liệu nào rời khỏi bên đó.
2. **Máy chủ gộp** các adapter lại thành một mô hình chung.
3. **Mô hình lớn (7 tỷ tham số) đóng vai "giáo viên"** ở máy chủ, dạy lại cho
   mô hình chung bằng cách chưng cất tri thức — nhưng chỉ được phép chạm vào
   một **kho dữ liệu công khai**, không bao giờ chạm dữ liệu riêng.

**In-Context Learning (ICL)** là kỹ thuật đưa vài ví dụ mẫu (câu hỏi + câu SQL
đúng) vào ngay trong prompt để mô hình bắt chước. "k=3" nghĩa là đưa 3 ví dụ.
ICL nằm trong tên gọi của phương pháp, nên câu hỏi trọng tâm của báo cáo này là:
**ICL thực sự đóng góp bao nhiêu, ở đâu, và đã đo đủ chưa?**

---

## 2. Thông số cố định của mọi thí nghiệm

Mọi con số trong báo cáo đều dùng cấu hình dưới đây trừ khi ghi rõ khác.

| Hạng mục | Giá trị |
|---|---|
| Mô hình học sinh (nhỏ) | Qwen2.5-1.5B-Instruct, fp16 |
| Mô hình giáo viên (lớn) | Qwen2.5-Coder-7B-Instruct, đóng băng, nén 4-bit khi cần |
| Cách tinh chỉnh | LoRA — hạng 16, hệ số 32, gắn vào tầng attention + MLP |
| Tham số huấn luyện | 1 epoch · batch 1 × tích luỹ 16 (batch hiệu dụng 16) · learning rate 2e-4 · độ dài tối đa 2560 token |
| Tập đánh giá | Spider dev — **1.034 câu hỏi**, đóng băng, lược đồ CSDL không trùng tập huấn luyện |
| Tập đánh giá phụ (độ bền) | Spider-Realistic (508 câu) · Spider-DK (535 câu) · Spider-Syn (đã chuẩn bị, chưa dùng) |
| Chỉ số chính | **EX** = độ chính xác thực thi (chạy SQL sinh ra, so bảng kết quả với đáp án) |
| Chỉ số phụ | **EM** = khớp chính xác thành phần câu lệnh |
| Kho dữ liệu công khai cho chưng cất | 3.873 bản ghi BIRD, do giáo viên tự sinh và đã lọc qua thực thi |
| Bộ mã hoá câu (cho tìm ví dụ) | BAAI/bge-small-en-v1.5 |
| Ngưỡng lọc cấu trúc của DAIL | 0,85 |
| Phần cứng | 1× RTX A5000 24 GB |
| Số hạt giống ngẫu nhiên (seed) | **0 cho gần như toàn bộ** — xem cảnh báo §7 |

---

## 3. Từ điển tên gọi

Báo cáo dùng tên dễ hiểu. Cột bên phải là tên nội bộ trong mã nguồn, để truy
nguyên khi cần.

### 3.1 Các mô hình được đánh giá

| Tên trong báo cáo | Mô tả | Tên nội bộ |
|---|---|---|
| **Mô hình A — tốt nhất hiện tại** | Tinh chỉnh Spider → chưng cất từ giáo viên trên dữ liệu công khai → tinh chỉnh Spider lần hai | `kd_then_spider_ft` |
| **Mô hình B — đối chứng ngân sách** | Tinh chỉnh Spider hai lần, **không** chưng cất. Cùng số bước huấn luyện với A, dùng để tách riêng công của chưng cất | `spider_ft2` |
| **Mô hình C — bản chưng cất thử nghiệm** | Chưng cất một giai đoạn từ mô hình gốc. *Toàn bộ bảng ICL cũ đo trên mô hình này* | `central_rkd` |
| **Mô hình C′** | Như C nhưng chưng cất từ đáp án nhiễu thay vì đáp án chuẩn | `central_kid` |
| **Mô hình D — tinh chỉnh thuần** | Chỉ tinh chỉnh, không chưng cất, huấn luyện **không có** ví dụ mẫu | `qwen1b_ft_no_icl` |
| **Mô hình E — huấn luyện kèm ví dụ** | Như D nhưng lúc huấn luyện **có** đưa ví dụ mẫu vào prompt | `qwen1b_ft_icl_k3` |
| **Giáo viên 7B** | Mô hình lớn, không tinh chỉnh, chỉ dùng để tham chiếu trần | `teacher` |
| **Mô hình gốc (4 dòng)** | Chưa huấn luyện gì: Qwen 0,5B · Qwen 1,5B · Gemma-2 2B · Llama-3.2 1B | `*_base` |

### 3.2 Các phương pháp chọn ví dụ mẫu

| Tên trong báo cáo | Cơ chế | Tên nội bộ |
|---|---|---|
| **Ngẫu nhiên** | Bốc bừa từ kho ví dụ. Dùng làm đối chứng — nếu phương pháp tinh vi không thắng được cái này thì nội dung ví dụ không quan trọng | `random` |
| **Giống câu hỏi** | Nhúng câu hỏi thành vector, lấy k câu gần nhất | `question` |
| **DAIL** | Che tên bảng/cột trong câu hỏi rồi mới đo độ giống, cộng thêm bước lọc theo cấu trúc câu SQL. Tốn thêm một lượt sinh nháp | `dail_select` |
| **CodeS** | Đo độ giống trên "khung" câu hỏi (bỏ từ mang nghĩa cụ thể), một lượt duy nhất | `codes` |
| ~~Kỹ năng (Skills)~~ | Nhờ một LLM viết tóm tắt "kỹ năng cần dùng" rồi tìm theo tóm tắt đó. **Đã gỡ khỏi mã nguồn 2026-07-26, chưa từng chạy** — xem §6 | ~~`ss`~~ |

### 3.3 Cách trình bày ví dụ trong prompt

| Tên trong báo cáo | Nội dung mỗi ví dụ | Tên nội bộ |
|---|---|---|
| **Gọn** (mặc định) | Chỉ câu hỏi + câu SQL | `never_schema` |
| **Che định danh** | Câu SQL bị che tên bảng/cột. **Đã lập trình, chưa chạy** | `skeleton` |
| **Đầy đủ** | Kèm cả cấu trúc bảng của CSDL trong ví dụ | `with_schema` |

### 3.4 Chính sách sử dụng ví dụ — *khi nào* thì đưa ví dụ vào

| Tên trong báo cáo | Cơ chế | Tên nội bộ |
|---|---|---|
| **Luôn dùng** | Mọi câu hỏi đều kèm ví dụ | `uniform` (k>0, không cổng) |
| **Chỉ khi nháp lỗi** | Sinh nháp không ví dụ trước; chỉ khi SQL nháp chạy lỗi mới sinh lại có ví dụ | `--icl-gate exec` |
| **Khi lỗi hoặc thiếu tự tin** | Như trên, cộng thêm điều kiện xác suất mô hình thấp. **Đã lập trình, chưa chạy** | `--icl-gate conf` |
| **Bỏ ví dụ, bỏ phiếu** (mặc định hiện tại) | Không dùng ví dụ. Sinh 8 lời giải khác nhau, chạy cả 8, lấy đáp án được nhiều phiếu nhất theo *kết quả thực thi* | `--overlay sc` |

---

## 4. ICL có thể cắm vào bốn chỗ — trạng thái từng chỗ

| Chỗ | Mô tả | Trạng thái |
|---|---|---|
| **① Giáo viên sinh đáp án** | Khi mô hình 7B tạo dữ liệu dạy học trên kho công khai, có kèm ví dụ mẫu không? | **ĐÃ ĐÓNG.** Đo 2026-07-19: không kèm ví dụ thắng ở cả ba chỉ số. Loại bỏ |
| **② Ngữ cảnh lúc chưng cất** | Prompt mà mô hình nhỏ nhìn thấy trong lúc học từ giáo viên | **CHƯA ĐO LẦN NÀO.** Hiện đặt k=0. Vướng kỹ thuật: bộ nhớ đệm logit của giáo viên được dựng ở k=0, muốn k=3 phải dựng lại từ đầu |
| **③ Huấn luyện tại chỗ ở mỗi bên** | Prompt lúc mô hình nhỏ tự học trên dữ liệu riêng | Đặt k=0. Có số cũ ở chế độ tập trung, **chưa có số nào ở chế độ liên kết** |
| **④ Lúc suy luận (chạy thật)** | Prompt lúc trả lời người dùng | Mặc định hiện tại: bỏ ví dụ, dùng bỏ phiếu 8 mẫu. **Toàn bộ bảng k=3 hiện có nằm ở đây, nhưng đo dưới chế độ đã bị thay thế** |

> **Điểm mấu chốt:** ICL hiện **không được sử dụng ở bất kỳ chỗ nào** trong
> đường ống đang chạy. Chỗ ② là nơi duy nhất còn lại mà ICL có thể chứng minh
> giá trị — và nó chưa được đo.

---

## 5. Kết quả đã đo

Tất cả: 1.034 câu hỏi Spider dev, seed 0, ví dụ trình bày **gọn**, chính sách
**luôn dùng** trừ khi ghi rõ khác. Đơn vị: EX (%).

### 5.1 Trên mô hình gốc chưa huấn luyện — ICL có giúp không?

| Mô hình gốc | Không ví dụ | Ngẫu nhiên | Giống câu hỏi | DAIL | CodeS |
|---|---:|---:|---:|---:|---:|
| Qwen 0,5B | 23,31 | **30,08** | 27,76 | 28,05 | 25,82 |
| Qwen 1,5B | 50,00 | 53,58 | 50,77 | **54,26** | 52,13 |
| Gemma-2 2B | 52,22 | 49,52 | 47,78 | 50,77 | **50,97** |
| Llama-3.2 1B | 37,33 | 35,69 | 30,46 | 35,01 | **37,23** |

**Đọc bảng:** ICL giúp mạnh trên dòng Qwen (+4 đến +7 điểm), nhưng **làm hại**
trên Gemma và Llama. Quan trọng hơn: cột "Ngẫu nhiên" ngang ngửa cột "DAIL" ở
cả bốn dòng — kiểm định thống kê cho p = 0,20–0,70, tức là **không có khác biệt
đáng kể**. Trên mô hình 0,5B, ngẫu nhiên còn *thắng* DAIL. Kết luận: đầu tư vào
việc chọn ví dụ cho khéo không mang lại gì trong dải mô hình này.

### 5.2 Trên mô hình đã huấn luyện — chính sách "luôn dùng ví dụ"

| Mô hình | Không ví dụ | Có 3 ví dụ (DAIL) | Chênh lệch |
|---|---:|---:|---:|
| Mô hình C (chưng cất) | 68,28 | 65,86 | **−2,42** |
| Mô hình C, ví dụ ngẫu nhiên | 68,28 | 66,83 | −1,45 |
| Mô hình C, ví dụ giống câu hỏi | 68,28 | 65,28 | −3,00 |
| Mô hình C, ví dụ CodeS | 68,28 | *thiếu số* | — |
| Mô hình C′ | 66,83 | 65,96 | −0,87 |
| Mô hình D (tinh chỉnh thuần) | 62,19 | 61,90 | −0,29 |
| **Mô hình E (huấn luyện KÈM ví dụ)** | 64,02 | 59,09 | **−4,93** |
| Qwen 0,5B tinh chỉnh thuần | 48,55 | 44,29 | −4,26 |
| Qwen 0,5B huấn luyện kèm ví dụ | 49,03 | 48,07 | −0,96 |
| Gemma-2 2B tinh chỉnh | 63,35 | 64,70 | **+1,35** |
| Chưng cất một giai đoạn khác (C″) | 65,47 | ❌ chưa đo | — |
| Giáo viên 7B | 78,72 | 78,53 | −0,19 |

**Đọc bảng:** sau khi mô hình đã được huấn luyện, đưa ví dụ vào prompt **hầu hết
là làm hại**. Chỉ **1/11 dòng dương** (Gemma +1,35), và nó nằm trên dòng mô hình
duy nhất mà ICL cũng có dấu bất thường ở bảng §5.1.

> **Đính chính (2026-07-26):** dòng C″ trước đây ghi 66,83 (+1,36) là **sai** —
> lần chạy đó bật chính sách "chỉ khi nháp lỗi", không phải "luôn dùng". Đã
> chuyển sang bảng §5.3. Trường `gate_pass_rate` trong file kết quả **không**
> phải chỉ báo cổng thực thi (nó là tỉ lệ đạt ngưỡng τ của DAIL) — chỉ
> `config.json → icl_gate` mới đáng tin.

**Phát hiện chưa được khai thác:** Mô hình E — mô hình *được huấn luyện kèm ví
dụ*, tức là ví dụ nằm trong phân phối quen thuộc của nó — lại rơi **mạnh nhất
bảng (−4,93)**. Giả thuyết "huấn luyện kèm ví dụ sẽ miễn dịch với tác hại của
ví dụ lúc chạy" bị chính số liệu này phản bác. Giả thuyết đó hiện vẫn đang được
ghi trong tài liệu thiết kế như một hướng cần thử.

### 5.2b Ma trận đầy đủ — mô hình × phương pháp chọn ví dụ (thuần, k=3)

Chỉ giải mã tham lam, **không** bỏ phiếu, **không** cổng thực thi. ✅ = đã có
số · ❌ = chưa đo. Cột "không ví dụ" là mốc so sánh của chính dòng đó.

| Mô hình (adapter) | không ví dụ | ngẫu nhiên | giống câu hỏi | DAIL | CodeS |
|---|---:|---:|---:|---:|---:|
| **A** `..._kd_bird_exmatch_then_spider_ft` | 67,31 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **B** `probe_p/central_ft_then_spider_ft` | 67,02 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **C** `kd_poc/central_rkd` | 68,28 | ✅ 66,83 | ✅ 65,28 | ✅ 65,86 | ❌ | ❌ |
| **C′** `central_kid` | 66,83 | ❌ | ❌ | ✅ 65,96 | ❌ | ❌ |
| **C″** `central_ft_then_kd_bird_exmatch` | 65,47 | ❌ | ❌ | ❌ | ❌ | ❌ |
| `central_rkd_asym` | 67,50 | ❌ | ❌ | ✅ 65,38 | ❌ | ❌ |
| **D** `icl_ladder/qwen1b/ft_no_icl` | 62,19 | ❌ | ❌ | ✅ 61,90 | ❌ | ❌ |
| **E** `qwen1b ft_icl_k3` (train kèm ví dụ) | 64,02 | ❌ | ❌ | ✅ 59,09 | ❌ | ❌ |
| Qwen 0,5B tinh chỉnh thuần | 48,55 | ❌ | ❌ | ✅ 44,29 | ❌ | ❌ |
| Qwen 0,5B train kèm ví dụ | 49,03 | ❌ | ❌ | ✅ 48,07 | ❌ | ❌ |
| Gemma-2 2B tinh chỉnh | 63,35 | ❌ | ❌ | ✅ 64,70 | ❌ | ❌ |
| Giáo viên 7B | 78,72 | ❌ | ❌ | ✅ 78,53 | ❌ | ❌ |
| Qwen 0,5B gốc | 23,31 | ✅ 30,08 | ✅ 27,76 | ✅ 28,05 | ✅ 25,82 | ❌ |
| Qwen 1,5B gốc | 50,00 | ✅ 53,58 | ✅ 50,77 | ✅ 54,26 | ✅ 52,13 | ❌ |
| Gemma-2 2B gốc | 52,22 | ✅ 49,52 | ✅ 47,78 | ✅ 50,77 | ✅ 50,97 | ❌ |
| Llama-3.2 1B gốc | 37,33 | ✅ 35,69 | ✅ 30,46 | ✅ 35,01 | ✅ 37,23 | ❌ |
| Mọi mô hình liên kết | — | ❌ | ❌ | ❌ | ❌ | ❌ |

**Độ phủ:** 4 mô hình gốc kín 4/4 cột. Mọi mô hình đã huấn luyện chỉ có **1/4
cột** (DAIL), trừ Mô hình C có 3/4. Hai mô hình mạnh nhất theo chế độ mặc định
(A, B) **trống hoàn toàn**.

Cột thứ 5 (Skills/`ss`) đã bị gỡ khỏi mã nguồn 2026-07-26 — xem §6. Nếu bổ sung
một phương pháp chọn ví dụ khác, nó chiếm chỗ cột đó.

**Lưu ý xếp hạng:** ở chế độ thuần này, Mô hình C (68,28) *cao hơn* Mô hình A
(67,31). Thứ hạng "A tốt nhất" chỉ đúng khi bật bỏ phiếu 8 mẫu. Ngoài ra C được
huấn luyện **trước** thay đổi hàm mất mát ngày 2026-07-17 (§7.3), nên C và A
không so sánh một-biến được — chúng thuộc hai dòng huấn luyện khác nhau. Nếu
bảng cuối cùng chỉ được phép có một dòng đầy đủ, chọn dòng nào là quyết định
cần cân nhắc (xem §9, Lệnh 3-thuần).

### 5.3 Chính sách "chỉ dùng ví dụ khi nháp lỗi"

| Mô hình | Không ví dụ (sàn) | Ngẫu nhiên | Giống câu hỏi | DAIL | CodeS |
|---|---:|---:|---:|---:|---:|
| Mô hình C | 68,28 | 70,41 | **70,79** | 70,50 | 69,92 |
| Mô hình C′ | 66,83 | — | — | 69,15 | — |
| Mô hình D | 62,19 | — | — | 66,54 | 66,73 |
| Mô hình E | 64,02 | — | — | 67,02 | — |
| Qwen 0,5B tinh chỉnh thuần | 48,55 | — | — | 51,84 | — |
| Qwen 0,5B kèm ví dụ | 49,03 | — | — | 53,09 | — |
| Gemma-2 2B tinh chỉnh | 63,35 | — | — | 66,34 | — |
| Giáo viên 7B | 78,72 | — | — | **80,37** | — |

**Đọc bảng:** đổi dấu hoàn toàn. Cùng những ví dụ đó, cùng mô hình đó — dùng bừa
bãi thì hại, dùng có chọn lọc thì lợi ở **8/8 mô hình**.

Nhưng khoảng cách giữa bốn phương pháp chọn ví dụ trên Mô hình C chỉ là **0,87
điểm**, kiểm định ngẫu-nhiên-vs-DAIL cho **p = 1,00**. Phân tích sâu hơn: tập
câu được sửa đúng bởi bốn phương pháp gần như **không giao nhau** (chỉ 5/50 câu
chung cả bốn).

**Diễn giải:** thứ sửa được câu sai không phải là *kiến thức trong ví dụ*, mà là
**việc xáo trộn prompt cộng với việc kiểm tra bằng thực thi**. Ví dụ chỉ đóng
vai chất gây nhiễu. Đây là kết luận có sức nặng nhất trong toàn bộ dữ liệu.

### 5.4 Chế độ mặc định hiện tại — bỏ phiếu 8 mẫu

| Mô hình | Bỏ phiếu, không ví dụ | Bỏ phiếu, có 3 ví dụ | Chênh lệch |
|---|---:|---:|---:|
| **Mô hình A (tốt nhất)** | **75,24** | *chưa đo* | — |
| Mô hình B (đối chứng) | 73,40 | *chưa đo* | — |
| Mô hình C | 72,73 / 72,34 (hai lần chạy) | *chưa đo* | — |
| Mô hình C′ | 72,24 | *chưa đo* | — |
| Mô hình D | 70,12 | 68,28 | **−1,84** |

**Đọc bảng:** chỉ có **đúng một ô** trong toàn bộ kho kết quả kết hợp ICL với
chế độ mặc định hiện tại — và nó âm. Ô đó lại nằm trên Mô hình D (không phải mô
hình chính), một seed, và được chạy **trước** khi một lỗi sinh số ngẫu nhiên
được sửa (§7.1).

Hai lần chạy Mô hình C lệch nhau 0,39 điểm dù cùng cấu hình — đó là mức nhiễu
sàn của chế độ bỏ phiếu. Mọi chênh lệch nhỏ hơn ~0,5 điểm ở chế độ này không
đọc được.

### 5.5 Tập kiểm tra độ bền

Spider-Realistic và Spider-DK đã có hạ tầng và đã chạy, nhưng **toàn bộ ở chế độ
không ví dụ**, và chỉ trên hai mô hình phụ. **Không có một phép đo ICL nào trên
tập kiểm tra độ bền.** Spider-Syn đã chuẩn bị dữ liệu, chưa chạy lần nào.

---

## 6. Còn thiếu gì — ma trận độ phủ

| Trục khảo sát | Đã đo | Chưa đo |
|---|---|---|
| Số ví dụ k | 0 và 3 | **1, 2, 5** — chưa có đường cong nào |
| Phương pháp chọn ví dụ | Ngẫu nhiên · Giống câu hỏi · DAIL · CodeS | — (Kỹ năng/SS đã gỡ 2026-07-26; chỗ trống dành cho phương pháp sẽ chọn thêm) |
| Cách trình bày ví dụ | Gọn; Đầy đủ (chỉ trên mô hình 0,5B) | **Che định danh** — đã lập trình, 0 lần chạy; Đầy đủ trên mô hình 1,5B |
| Chính sách dùng ví dụ | Luôn dùng · Chỉ khi lỗi | **Khi lỗi hoặc thiếu tự tin** — đã lập trình, 0 lần chạy |
| Kết hợp với bỏ phiếu 8 mẫu | 1 ô duy nhất | **Gần như trống hoàn toàn** |
| Mô hình được đo | Mô hình gốc ×4, C, C′, D, E, Gemma, Giáo viên | **Mô hình A và B (hai mô hình mạnh nhất)**; **mọi mô hình liên kết** |
| Vị trí cắm ICL | ④ suy luận; ③ một phần | **② ngữ cảnh chưng cất — trống hoàn toàn** |
| Tập đánh giá | Spider dev có ICL; Realistic/DK chỉ không-ví-dụ | ICL trên Realistic/DK/Syn |
| Số seed | 0 cho tất cả; 1 cho đúng một lần chạy | **≥3 seed cho bất kỳ ô nào** |

---

## 7. Cảnh báo về tính hợp lệ của số cũ

### 7.1 Lỗi seed đã được sửa ngày 2026-07-22
Trước bản vá `b5cf373`, tham số `--seed` chỉ điều khiển việc chọn tập con và
định danh checkpoint — **không reset bộ sinh số ngẫu nhiên của quá trình lấy
mẫu**. Hệ quả: mọi lần chạy chế độ bỏ phiếu trước ngày đó là *lặp lại ngẫu
nhiên*, không phải *lặp lại có kiểm soát seed*. Ảnh hưởng trực tiếp đến ô ICL
duy nhất ở §5.4 và cặp Mô hình A seed 0/seed 1.

### 7.2 Kích thước batch ảnh hưởng kết quả bỏ phiếu
Chạy batch 1 và batch nhiều rút mẫu khác nhau. Đây là lý do hai lần chạy Mô
hình C lệch 0,39 điểm. Nay đã được đưa vào chữ ký checkpoint để không lẫn.

### 7.3 Hàm mất mát đổi ngày 2026-07-17
Một thành phần trọng số trong hàm mất mát đã bị gỡ. Adapter huấn luyện trước
ngày đó **không so sánh một-biến được** với adapter mới. Một thí nghiệm ngày
2026-07-22 đã phải huấn luyện lại nhóm đối chứng vì lý do này. Luôn kiểm tra
ngày huấn luyện trước khi ghép cặp so sánh.

### 7.4 Trường ghi tên tập đánh giá bị cứng
Trường `eval_set` trong file kết quả luôn ghi cùng một chuỗi bất kể chạy trên
tập nào. Các lần chạy Spider-Realistic/DK chỉ phân biệt được qua số câu hỏi
(508 / 535). **Nên sửa** — nếu không, bảng độ bền sẽ không tự truy nguyên được.

### 7.5 Kết quả liên kết có nhiều dòng mỗi lần chạy
Các mô hình chạy ở chế độ liên kết cho một dòng kết quả cho mỗi bên tham gia,
với chênh lệch lớn giữa các bên (một trường hợp: 28,82 / 36,94 / 39,46 — lệch
10,6 điểm). Đừng gộp trung bình khi trích dẫn; chính độ lệch đó là tín hiệu
về mức độ mất cân bằng dữ liệu.

---

## 8. Kết luận

1. **ICL không được dùng ở bất kỳ đâu trong hệ thống đang chạy**, dù nó nằm
   trong tên phương pháp. Cần hoặc đo chỗ ② để có bằng chứng, hoặc đổi tên.
2. **Nội dung ví dụ không quan trọng.** Ngẫu nhiên ngang DAIL ở mọi cấu hình đã
   đo (p = 0,20 đến 1,00). Cái có tác dụng là *xáo trộn prompt + kiểm tra bằng
   thực thi*, không phải tri thức trong ví dụ.
3. **Chính sách dùng ví dụ mới là thứ đáng nghiên cứu**, không phải phương pháp
   chọn ví dụ. Dùng bừa: hại. Dùng khi nháp lỗi: lợi 8/8 mô hình. Đây là khoảng
   trống thật trong tài liệu khoa học hiện có.
4. **Toàn bộ bảng ICL hiện mô tả một cấu hình đã bị thay thế.** Cần đo lại trên
   mô hình mạnh nhất + chế độ mặc định hiện tại trước khi đưa vào bài báo.

---

## 9. Các lệnh cần chạy bổ sung

Chạy từ thư mục mã nguồn `FedICL-SQL/` (thư mục chứa `experiments/`).
Thời gian ước tính lấy từ tốc độ thực đã ghi trong các lần chạy trước.

### Nhóm P0 — bắt buộc, để bảng số khớp với hệ thống đang chạy (~3 giờ GPU)

**Lệnh 1 — sweep chính sách "khi lỗi hoặc thiếu tự tin". 0 phút GPU, chạy được ngay.**

Công cụ đã có sẵn; nó mô phỏng lại từ hai file dự đoán cũ, không cần sinh lại gì.

```bash
uv run python analysis/gate_sweep.py \
  experiments/eval_arms/results/eval_arms__s0__20260709T181318/predictions/central_rkd_gate_exec.csv \
  experiments/eval_arms/results/eval_arms__s0__20260708T191314/predictions/central_rkd_k3dail.csv
```

Kết quả: lấp ô cuối cùng của trục "chính sách dùng ví dụ" → đủ để nói đã thử cả
ba chính sách thay vì hai.

---

**Lệnh 2 — vá ô số còn thiếu trong bảng §5.2 (~10 phút).**

```bash
uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms central_rkd=artifacts/kd_poc/central_rkd/adapter \
  --k 3 --retrieval codes --batch-size 16 --seed 0
```

---

**Lệnh 3 — bảng ICL trên mô hình tốt nhất + chế độ mặc định (4 lần chạy, ~2,5 giờ).**

Đây là nhóm lệnh quan trọng nhất trong toàn bộ danh sách.

```bash
ADP=artifacts/probe_p/central_ft_then_kd_bird_exmatch_then_spider_ft/adapter

# 3a. Mốc tham chiếu: bỏ phiếu, không ví dụ (~70 phút)
uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms modelA_sc_k0=$ADP \
  --k 0 --overlay sc --sc-n 8 --batch-size 2 --seed 0

# 3b+3c. Bỏ phiếu + 3 ví dụ, hai phương pháp chọn (~35 phút mỗi lệnh)
for R in random dail_select; do
  uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --arms modelA_sc_k3_$R=$ADP \
    --k 3 --retrieval $R --overlay sc --sc-n 8 --batch-size 2 --seed 0
done

# 3d. Đối chứng greedy có ví dụ, để tách công của bỏ phiếu (~15 phút)
uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms modelA_greedy_k3=$ADP \
  --k 3 --retrieval dail_select --batch-size 16 --seed 0
```

---

**Lệnh 3-thuần — ma trận §5.2b, ICL thuần: không bỏ phiếu, không cổng (4 lần
chạy, ~1 giờ).**

Đây là bộ lệnh lấp **một dòng đầy đủ** của bảng §5.2b — đo riêng tác dụng của
ICL, tách khỏi mọi cơ chế sửa lỗi. Chạy trên Mô hình A (dòng huấn luyện hiện
hành). Mốc không-ví-dụ 67,31 đã có sẵn, không cần chạy lại.

```bash
ADP=artifacts/probe_p/central_ft_then_kd_bird_exmatch_then_spider_ft/adapter

for R in random question dail_select codes; do
  uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --arms modelA_k3_$R=$ADP \
    --k 3 --retrieval $R --demo-style never_schema \
    --batch-size 16 --seed 0
done
```

Đổi `$ADP` sang `artifacts/kd_poc/central_rkd/adapter` nếu muốn lấp dòng Mô
hình C thay vì A — khi đó chỉ cần chạy `codes` (ba cột kia đã có).

---

### Nhóm P1 — làm chắc kết luận (~4–6 giờ GPU)

**Lệnh 4 — đường cong số ví dụ k (4 lần chạy, ~2,5 giờ).**

Hiện chỉ có hai điểm (k=0 và k=3) nên không vẽ được đường. Dùng ví dụ ngẫu
nhiên vì nó rẻ nhất và đã chứng minh ngang DAIL.

```bash
ADP=artifacts/probe_p/central_ft_then_kd_bird_exmatch_then_spider_ft/adapter
for K in 1 2 5; do
  uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --arms modelA_sc_k$K=$ADP \
    --k $K --retrieval random --overlay sc --sc-n 8 --batch-size 2 --seed 0
done
```

**Lệnh 5 — lặp lại với seed khác (4 lần chạy, ~4 giờ).**

Đây là **lần đầu tiên** chạy được phép lặp có kiểm soát seed, sau bản vá §7.1.

```bash
ADP=artifacts/probe_p/central_ft_then_kd_bird_exmatch_then_spider_ft/adapter
for S in 1 2; do
  uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --arms modelA_sc_k0_s$S=$ADP --k 0 --overlay sc --sc-n 8 --batch-size 2 --seed $S
  uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --arms modelA_sc_k3_s$S=$ADP --k 3 --retrieval random --overlay sc --sc-n 8 --batch-size 2 --seed $S
done
```

---

### Nhóm P2 — lấp các trục còn trống (~3 giờ GPU)

**Lệnh 6 — cách trình bày "che định danh" (2 lần chạy, ~30 phút).**

Biến thể duy nhất của trục trình bày chưa từng đo.

```bash
ADP=artifacts/kd_poc/central_rkd/adapter
uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms modelC_skeleton_k3=$ADP \
  --k 3 --retrieval dail_select --demo-style skeleton --batch-size 16 --seed 0

uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms modelC_skeleton_k3_gate=$ADP \
  --k 3 --retrieval dail_select --demo-style skeleton --icl-gate exec --batch-size 16 --seed 0
```

**Lệnh 7 — ĐÃ HUỶ.** Trước đây là phương pháp chọn "Kỹ năng" (`--retrieval ss`).
Mã nguồn đã gỡ 2026-07-26 theo quyết định của user; phương pháp thay thế chưa
chọn. Khi có, thêm vào đây và vào `scripts/run_icl_matrix_list2.sh`.

**Lệnh 8 — trình bày ví dụ "đầy đủ" trên mô hình 1,5B (~20 phút).**

Hiện chỉ đo trên mô hình 0,5B chưa huấn luyện.

```bash
uv run python experiments/eval_arms/run.py --pool-mode centralized \
  --arms modelC_withschema_k3=artifacts/kd_poc/central_rkd/adapter \
  --k 3 --retrieval dail_select --demo-style with_schema --batch-size 16 --seed 0
```

**Lệnh 9 — ICL trên tập kiểm tra độ bền (4 lần chạy, ~2 giờ).**

Đây là chỗ hợp lý nhất để ICL còn có ích: khi phân phối dữ liệu lệch khỏi tập
huấn luyện. Tài liệu khoa học báo mức tăng lớn nhất chính ở tình huống này.

```bash
ADP=artifacts/probe_p/central_ft_then_kd_bird_exmatch_then_spider_ft/adapter
for TEST in processed_data/SPIDER_REALISTIC/test.csv \
            processed_data/SPIDER_DK/test.csv; do
  for K in 0 3; do
    uv run python experiments/eval_arms/run.py --pool-mode centralized \
      --test-csv $TEST --arms modelA_robust_k$K=$ADP \
      --k $K --retrieval random --overlay sc --sc-n 8 --batch-size 2 --seed 0
  done
done
```

---

### Nhóm P3 — chỗ duy nhất ICL còn có thể chứng minh giá trị

**Lệnh 10 — ngữ cảnh lúc chưng cất (chỗ ② ở §4). Chi phí cao, cần quyết định trước.**

Đây là **điểm duy nhất còn lại** nơi ICL có thể biện minh cho tên phương pháp.
Không chạy được ngay: bộ nhớ đệm logit giáo viên hiện tại chỉ hợp lệ ở k=0, và
bộ kiểm tra sẽ báo lỗi dừng nếu cấu hình lệch. Hai bước, theo thứ tự:

```bash
# Bước 1 — dựng lại bộ nhớ đệm logit giáo viên ở k=3 (nhiều giờ, chạy nền)
uv run python scripts/build_teacher_logit_cache.py \
  --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv \
  --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit \
  --k-teacher 3 --retrieval dail_select --demo-style never_schema \
  --embedder BAAI/bge-small-en-v1.5 --tau 0.85 \
  --out artifacts/teacher_logit_cache/rkd_k3_full --seed 0

# Bước 2 — chưng cất lại với ngữ cảnh k=3, mọi thứ khác giữ nguyên
uv run python experiments/client_train/run.py \
  --client processed_data/BIRD/bootstrap_full_exmatch/train.csv \
  --kd-direction rkd \
  --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit \
  --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k3_full \
  --init-adapter artifacts/icl_ladder/qwen1b/ft_no_icl/adapter \
  --out artifacts/probe_p/kd_ctx_k3/adapter \
  --epochs 1 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0
```

Sau đó đánh giá bằng Lệnh 3a với adapter mới, so với Mô hình A.

Kỳ vọng thấp — giáo viên tự nó cũng không hưởng lợi từ ví dụ (78,53 so với
78,72). Nhưng kết quả âm ở đây **vẫn là kết quả công bố được**: "ICL không giúp
ngay cả ở kênh chưng cất" là câu trả lời sạch sẽ cho câu hỏi về tên phương pháp.

> **Cần quyết định trước khi chạy Lệnh 10:** hoặc (a) chấp nhận chi phí và báo
> cáo dù kết quả âm, hoặc (b) bỏ cụm "In-Context" khỏi tên phương pháp. Giữ
> nguyên tên mà không có ô số nào là vị thế yếu nhất trong ba lựa chọn.

---

### Nếu chỉ có một buổi chạy máy

Lệnh 1 (0 phút) → Lệnh 2 (10 phút) → Lệnh 3 (2,5 giờ).

Ba lệnh này biến bảng ICL từ chỗ *mô tả một hệ thống đã bị thay* thành *bảng hợp
lệ cho hệ thống đang chạy*, đồng thời đóng trục chính sách. Mọi thứ còn lại là
làm dày thêm.

---

### Lưu ý về thứ tự công việc

Kế hoạch hiện hành đang khoá hành động kế tiếp vào việc chạy thử hệ liên kết
(2 bên → 8 bên), và ghi rõ *"ICL tạm hoãn"*. Danh sách trên nên xếp **sau** đợt
đó — ngoại trừ Lệnh 1 và Lệnh 2, đủ rẻ để chèn vào bất kỳ khe trống nào. Riêng
Lệnh 10 là câu hỏi cấp bài báo chứ không phải cấp kết quả, nên thời điểm chạy
phụ thuộc vào quyết định (a)/(b) ở trên.
