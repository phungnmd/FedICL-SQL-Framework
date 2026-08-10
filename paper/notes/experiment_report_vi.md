# Đánh giá pipeline liên kết — từng thành phần đóng góp gì, và có nên giữ ICL không

**Ngày:** 10/08/2026 · **Cấu hình:** K=5 client, non-IID Dirichlet α=0,5, T=1 vòng, seed 0
**Student:** Qwen2.5-1.5B-Instruct · **Teacher:** Qwen2.5-Coder-7B-Instruct (4-bit, đóng băng)
**Đo trên:** toàn bộ Spider dev (n=1.034), greedy decoding, chỉ số EX (execution accuracy)
**Nguồn số:** `experiments/*/results/*/metrics.json`, kiểm định ghép cặp trên file dự đoán từng câu

---

## 1. Hệ thống làm gì

Nhiều bên giữ cơ sở dữ liệu riêng, không chia sẻ dữ liệu thô. Mỗi bên tự huấn
luyện một mô hình nhỏ 1,5 tỷ tham số trên dữ liệu của mình, rồi **chỉ gửi bản
vá trọng số (LoRA adapter)** lên máy chủ. Máy chủ gộp các bản vá thành một mô
hình chung, sau đó dùng một **mô hình lớn 7 tỷ tham số làm "giáo viên"** dạy
lại mô hình chung — nhưng giáo viên chỉ được chạm vào **kho dữ liệu công khai**
(BIRD), không bao giờ chạm dữ liệu riêng của bất kỳ bên nào.

Pipeline có bốn thành phần xếp chồng. Báo cáo này đo **từng thành phần đóng góp
bao nhiêu**, rồi trả lời câu hỏi cuối: có nên giữ In-Context Learning không.

---

## 2. Mỗi thành phần đóng góp bao nhiêu

Cộng dồn từ dưới lên. Mỗi dòng là kết quả của việc thêm đúng một thành phần vào
dòng ngay trên nó.

| Thành phần | EX | Giá trị thêm vào | Ý nghĩa thống kê |
|---|---:|---:|---|
| Mô hình 1,5B chưa huấn luyện | 50,00 | — | mốc sàn |
| **Client tự huấn luyện + gộp liên kết (FedAvg)** | **57,35** | **+7,35** | — |
| **+ Học từ câu SQL của giáo viên (SeqKD)** | **61,32** | **+3,97** | p = 0,010 |
| **+ Học từ phân phối xác suất của giáo viên (reverse-KL)** | **63,35** | **+2,03** | p = 0,042 |

Hai mốc đối chiếu: gom hết dữ liệu về một chỗ rồi huấn luyện tập trung
(`central_rkd`) đạt **68,28**; bản thân giáo viên 7B đạt **78,72**.

**Đọc bảng này ra sao:**

- Hệ thống nâng mô hình nhỏ từ **50,00 lên 63,35 mà không có một dòng dữ liệu
  nào rời khỏi chủ sở hữu**. Đó là toàn bộ mục đích của đề tài.
- So với trần tập trung 68,28, hệ liên kết lấp được **73% khoảng cách**; phần
  còn thiếu do liên kết là 4,93 điểm.
- Bước +7,35 gộp chung hai việc: client tự huấn luyện, và gộp liên kết. Phần
  §2.1 tách riêng hai việc đó.
- **Giáo viên đóng góp nhiều nhất, và chia làm hai tầng.** Cho student học *câu
  SQL* mà giáo viên viết ra đã cho +3,97. Cho student học thêm *phân phối xác
  suất* của giáo viên cho thêm +2,03. Tầng thứ hai chính là cơ chế đề xuất của
  bài báo.
- Con số +2,03 được đo trên **đối chứng cùng dữ liệu, cùng ngân sách huấn
  luyện** — nghĩa là nó không phải "nhờ có thêm dữ liệu", mà là giá trị riêng
  của việc chưng cất ở mức logit. Đối chứng dữ liệu thuần đã đo riêng và cho
  kết quả âm (huấn luyện trên SQL gốc của BIRD: 47,10, thấp hơn mốc sàn 50,00).
- Cơ chế này **lặp lại được**: chạy trên một bộ client hoàn toàn khác cho
  +2,51 (p = 0,013). Cùng chiều, cùng độ lớn, hai lần độc lập.

### 2.1 Gộp liên kết có hơn từng bên tự làm không

Câu hỏi tự nhiên: nếu một bên cứ tự huấn luyện rồi dùng luôn model của mình,
có thua model gộp không. Đo trên 5 adapter client (số dưới đây thuộc nhánh có
ICL — phép đo tương ứng cho nhánh không ICL chưa chạy, khoảng 1 giờ GPU):

| | EX |
|---|---:|
| Client yếu nhất | 50,97 |
| Trung bình 5 client | 53,21 |
| Client mạnh nhất | **56,29** |
| Model sau khi gộp (FedAvg) | **54,45** |

Câu trả lời trung thực: **model gộp hơn 4 trên 5 client, nhưng thua client mạnh
nhất 1,84 điểm** (p = 0,164 — không có ý nghĩa thống kê). Nó chỉ hơn client yếu
nhất một cách có ý nghĩa (+3,48, p = 0,009).

Khoảng cách 1,84 điểm này đã được truy nguyên đến tận cùng. Hai giả thuyết được
kiểm tra, một bị bác bỏ và một được xác nhận.

**Giả thuyết 1 — lỗi gộp LoRA. Bị bác bỏ.** Phép gộp trung bình từng thừa số
cho $\bar{B}\bar{A} \neq \sum_i w_i B_i A_i$, một sai số đã biết trong tài liệu
(FedEx-LoRA, FLoRA, Fed-SB đều nhằm sửa nó). Đã dựng tổng chính xác từ chính 5
adapter đó, không cần huấn luyện lại:

| Cách gộp | rank | sai số tích | EX | so với FedAvg | p |
|---|---:|---:|---:|---:|---:|
| Trung bình từng thừa số (đang dùng) | 16 | 0,069 | 54,45 | — | — |
| FLoRA-NA | 16 | 0,066 | 54,45 | 0,00 | — |
| Xấp xỉ rank-16 tối ưu | 16 | tối thiểu | 54,26 | −0,19 | 0,851 |
| **Tổng chính xác** | 80 | **0** | 55,13 | +0,68 | 0,311 |

Dòng thứ ba là mấu chốt: nó cùng mục tiêu với dòng thứ tư nhưng bị giữ ở rank
16, và cho **đúng số không**. Nên phần +0,68 của tổng chính xác đến từ việc
adapter to gấp 5, không phải từ việc sửa sai số. Bốn cách gộp trải sai số từ
0,069 xuống 0 cho EX trong dải 0,87 điểm, không cách nào đạt ý nghĩa thống kê.

**Giả thuyết 2 — hiệu ứng trọng số của tập test. Được xác nhận.** Chỉ số EX
chuẩn của Spider cân mỗi database theo số câu hỏi. Tính lại với mỗi database
cân bằng nhau:

| | EX theo câu hỏi | EX theo database |
|---|---:|---:|
| Client 5 | **56,29** (hạng 1) | 58,21 (hạng 3) |
| Model gộp (FedAvg) | 54,45 | **58,25** (hạng 2) |
| Tổng chính xác | 55,13 | **58,62** (hạng 1) |
| Client 1 | 53,29 | 57,43 |
| Client 2 | 52,51 | 56,79 |
| Client 3 | 53,00 | 56,31 |
| Client 4 | 50,97 | 55,30 |

**Thứ hạng đảo ngược.** Cân bằng theo database thì model gộp đã ngang hoặc hơn
mọi client lẻ. Client 5 mạnh đúng ở những database lớn nhất — `world_1` (120
câu, chiếm 11,6% tập test), `dog_kennels` (82), `tvshow` (62), `pets_1` (42).
Bốn database trên tổng số 20 đã chiếm hơn toàn bộ khoảng cách 1,84 điểm.

Ba dữ kiện phụ khớp với cách đọc này:

- **Model gộp bằng trung bình theo database cộng 1,24 điểm.** Nó hành xử đúng
  như một phép trung bình lành mạnh; một phép gộp hỏng sẽ rơi *xuống dưới* mức
  trung bình đó.
- **Tập test hoàn toàn không chung schema với tập huấn luyện** — 20 database
  test, 146 database train, giao rỗng. Không client nào từng thấy database nào
  trong tập test, nên đây là khác biệt về khả năng chuyển giao, không phải ghi
  nhớ.
- **Không client nào thực sự trội.** Số database mà mỗi client thắng rải đều
  4/6/4/1/5. Client 2 thắng nhiều database nhất (6 trên 20) nhưng chỉ xếp hạng
  5. "Client mạnh nhất" không phải một tính chất ổn định của client, mà phụ
  thuộc vào phân bố kích thước database của tập test.

Kết luận: **model gộp không kém client mạnh nhất.** Trên tập test này một client
tình cờ mạnh ở đúng những database lớn nhất, và cách tính điểm theo câu hỏi
khuếch đại điều đó thành khoảng cách 1,84 điểm vốn đã không có ý nghĩa thống kê.
Giá trị của việc gộp là có thật, và giá trị của cả hệ nằm ở bước tiếp theo: trên
cùng 5 client đó, sau khi giáo viên chưng cất, model chung đạt 64,02 — hơn
client mạnh nhất **7,73 điểm**.

Hệ quả thực dụng: câu hỏi "sao không dùng FedEx-LoRA hay Fed-SB" đã có câu trả
lời bằng số. Sửa sai số gộp mà giữ nguyên rank cho −0,19 điểm; sửa triệt để
bằng cách tăng rank gấp 5 cho +0,68 điểm, không có ý nghĩa thống kê. Không có
dư địa đáng kể ở tầng này.

---

## 3. Thành phần không đóng góp: FLoRA-NA

FLoRA-NA là cách gộp adapter tinh vi hơn FedAvg, tối ưu lại các thừa số low-rank
thay vì lấy trung bình trực tiếp. Đã so trực tiếp với FedAvg trên 6 cấu hình.

Nó tái tạo tích ma trận chính xác hơn thật (sai số 0,066 so với 0,072), nhưng
**không cấu hình nào cho cải thiện EX có ý nghĩa thống kê** — hoà hoặc thua ở
mọi ô đo theo chế độ triển khai chính. Đề xuất dùng FedAvg và giữ FLoRA-NA như
một nhận xét phụ: gộp thừa số chính xác hơn không làm SQL đúng hơn.

---

## 4. Nội dung chính — có nên giữ ICL không

**ICL là gì ở đây:** chèn k=3 ví dụ mẫu (câu hỏi + SQL đúng, lấy từ kho riêng
của chính client đó) vào prompt, để mô hình bắt chước. Kỹ thuật này nằm trong
tên phương pháp, nên nó phải được kiểm chứng nghiêm túc.

Đã chạy **hai pipeline hoàn toàn song song** — cùng phân hoạch dữ liệu, cùng
seed, cùng kho công khai, cùng bước máy chủ, cùng ngân sách — khác đúng một
biến: client có dùng ví dụ mẫu khi huấn luyện hay không.

### 4.1 Bảng 2×2: huấn luyện có/không ICL × chạy có/không ICL

| | Chạy không ví dụ mẫu | Chạy có 3 ví dụ mẫu | Mất bao nhiêu khi thêm ví dụ |
|---|---:|---:|---:|
| **Huấn luyện có ICL** | 63,93 | 60,06 | **−3,87** (p = 0,003) |
| **Huấn luyện không ICL** | 62,57 | 59,48 | **−3,09** (p = 0,014) |
| Chênh lệch | +1,35 (p = 0,060) | +0,58 (p = 0,572) | |

Bốn phát hiện, đọc theo thứ tự:

**(1) Đưa ví dụ mẫu vào lúc chạy làm giảm độ chính xác — có ý nghĩa thống kê.**
Mất 3,87 điểm (p = 0,003). Đây là hiệu ứng ICL lớn nhất và chắc chắn nhất đo
được trong toàn dự án, và nó âm.

**(2) Huấn luyện có ví dụ mẫu KHÔNG bảo vệ được khỏi (1).** Đây là điểm quyết
định. Lý lẽ của DAIL-SQL — cũng là lý lẽ duy nhất từng biện minh cho việc cho
client huấn luyện kèm ví dụ — dự đoán rằng mô hình huấn luyện không ví dụ sẽ
sụp đổ khi gặp ví dụ, còn mô hình huấn luyện có ví dụ thì không. Thực tế
**ngược lại**: mô hình huấn luyện không ví dụ mất *ít hơn* (−3,09 so với
−3,87). Tương tác đi sai chiều.

Ba mô hình độc lập, ba công thức huấn luyện khác nhau, đều mất khoảng 3 điểm
khi gặp ví dụ mẫu. Kết luận: **hình phạt này là thuộc tính của mô hình 1,5B,
không phải của cách huấn luyện.** Không có cách nào huấn luyện để chữa nó.

**(3) Nếu triển khai có ví dụ mẫu, huấn luyện có ICL mua được đúng số không.**
Cột giữa: 60,06 so với 59,48, chênh 0,58 điểm với p = 0,572 — không phân biệt
được.

**(4) Huấn luyện có ICL còn làm mô hình gộp kém đi.** Trước bước máy chủ, bản
gộp của nhánh không ICL đạt 57,35 còn nhánh ICL chỉ 54,45 — **kém 2,90 điểm,
p = 0,008**, kèm nhiều lỗi thực thi hơn (258 so với 236). Bước máy chủ sau đó
kéo nhánh ICL lên nhiều hơn chỉ vì nó xuất phát thấp hơn, nên hai đường hội tụ
về cách nhau 1,35 điểm không có ý nghĩa thống kê.

### 4.2 Cái giá phải trả

| | Không ICL | Có ICL | Tỉ lệ |
|---|---:|---:|---:|
| Thời gian huấn luyện 5 client | 4.100 giây | 9.651 giây | **2,35×** |
| Bước sinh SQL nháp để truy hồi | không cần | bắt buộc | — |
| Bộ nhớ GPU đỉnh phía client | 25,9 GB | 28,2 GB | +2,3 GB |
| Độ dài prompt khi chạy | 1.568 ký tự | 2.175 ký tự | **+38,7%** |
| Thời gian mỗi câu hỏi | 0,289 giây | 1,224 giây | **4,2×** |
| Hạ tầng tại mỗi bên khi triển khai | không cần | phải lưu và đánh chỉ mục kho ví dụ riêng | — |

---

## 5. Đề xuất: bỏ ICL khỏi phương pháp

Bốn kiểm định đều cùng một hướng:

| Bằng chứng | Giá trị | p |
|---|---:|---:|
| Huấn luyện có ICL làm mô hình gộp kém đi | −2,90 | 0,008 |
| Ví dụ mẫu lúc chạy làm giảm độ chính xác | −3,87 | 0,003 |
| Huấn luyện có ICL không bảo vệ được (bác bỏ DAIL-SQL) | sai chiều 0,78 | — |
| Ở chế độ triển khai có ví dụ, hai nhánh như nhau | +0,58 | 0,572 |

Cộng thêm chi phí 2,35× khi huấn luyện và 4,2× khi chạy.

**Đề xuất cụ thể:**

1. Bỏ ICL khỏi phương pháp đề xuất. Pipeline chính thức là: client tự huấn
   luyện không ví dụ mẫu → gộp FedAvg → chưng cất reverse-KL tại máy chủ trên
   kho công khai.
2. Giữ ICL trong bài báo như một **kết quả âm có kiểm định** ở phần thực
   nghiệm. Đây không phải phần bỏ đi — nó bác bỏ một cơ chế đang được xem là
   hiển nhiên trong tài liệu (DAIL-SQL) ở quy mô mô hình nhỏ, và có đủ số liệu
   để bảo vệ trước phản biện.
3. Tên phương pháp cần đổi. `Fed-ICKD` và `FedICL-SQL` đều lấy ICL làm trung
   tâm, không còn khớp với bằng chứng.

Đóng góp còn lại — và là đóng góp có bằng chứng mạnh nhất — là **chưng cất
reverse-KL phía máy chủ trên kho dữ liệu công khai trong bối cảnh liên kết**:
+2,03 (p = 0,042), lặp lại +2,51 (p = 0,013), đo trên đối chứng cùng dữ liệu
cùng ngân sách.

---

## 6. Giới hạn của báo cáo này

Tất cả số liệu là **seed 0, T = 1 vòng**. Giá trị p cho biết hai mô hình cụ thể
đó khác nhau, chưa cho biết hai phương pháp khác nhau — biến thiên do seed chưa
được đo. Đang chạy seed 1 và seed 2 trên nhánh khuyến nghị, mỗi seed khoảng 4
giờ GPU. Các kết luận về ICL nhất quán qua 6 ô đo độc lập nên ít có khả năng
đảo chiều; con số +2,03 thì cần khoảng tin cậy trước khi đưa vào bài báo.

BIRD chỉ được dùng làm kho công khai để chưng cất, **không** dùng làm tập đánh
giá. Mọi con số EX trong báo cáo đều đo trên Spider dev.
