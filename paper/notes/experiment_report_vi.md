# Kết quả pipeline liên kết và đề xuất bỏ ICL

**Ngày:** 11/08/2026 · **Cấu hình:** K=5 client, non-IID Dirichlet α=0,5, T=1 vòng, 3 seed
**Student:** Qwen2.5-1.5B-Instruct · **Teacher:** Qwen2.5-Coder-7B-Instruct (4-bit, đóng băng)
**Đo trên:** toàn bộ Spider dev (n=1.034), greedy decoding, chỉ số EX (execution accuracy)
**Kiểm định:** McNemar ghép cặp chính xác, trên dự đoán từng câu của cùng 1.034 câu hỏi

Báo cáo trả lời hai câu hỏi: **(A)** pipeline đề xuất có hiệu quả không và từng
thành phần đóng góp gì, **(B)** có nên giữ In-Context Learning không.

---

## 1. Hệ thống làm gì

Nhiều bên giữ cơ sở dữ liệu riêng, không chia sẻ dữ liệu thô. Mỗi bên tự huấn
luyện một mô hình nhỏ 1,5 tỷ tham số trên dữ liệu của mình, rồi **chỉ gửi bản
vá trọng số (LoRA adapter)** lên máy chủ. Máy chủ gộp các bản vá thành một mô
hình chung, sau đó dùng một **mô hình 7 tỷ tham số làm "giáo viên"** dạy lại mô
hình chung — giáo viên chỉ được chạm vào **kho dữ liệu công khai** (BIRD),
không bao giờ chạm dữ liệu riêng của bất kỳ bên nào.

Bốn thành phần xếp chồng:

```text
client tự huấn luyện  →  gộp liên kết (FedAvg)  →  học câu SQL của giáo viên (SeqKD)  →  học phân phối xác suất của giáo viên (reverse-KL)
```

---

## 2. (A) Kết quả pipeline đề xuất

Chạy trên **3 seed độc lập** (0, 1, 2). Mỗi seed huấn luyện lại toàn bộ 5
client và chạy lại cả hai bước máy chủ.

### 2.1 Kết quả hệ đầy đủ

| Chặng | seed 0 | seed 1 | seed 2 | Trung bình | Độ lệch chuẩn |
|---|---:|---:|---:|---:|---:|
| Mô hình 1,5B chưa huấn luyện | 50,00 | 50,00 | 50,00 | 50,00 | — |
| Client tự huấn luyện + gộp liên kết | 57,35 | 57,45 | 59,77 | 58,19 | 1,37 |
| + học câu SQL của giáo viên (SeqKD) | 61,32 | 62,28 | 59,48 | 61,03 | 1,42 |
| **+ học phân phối xác suất (reverse-KL)** | 63,35 | 62,48 | 62,38 | **62,74** | **0,53** |

**Hệ đầy đủ đạt 62,74 ± 0,53, tăng 12,74 điểm so với mô hình gốc, và không một
dòng dữ liệu nào rời khỏi chủ sở hữu.** Độ lệch chuẩn 0,53 qua 3 seed cho thấy
kết quả này ổn định.

Đối chiếu: gom hết dữ liệu về một chỗ huấn luyện tập trung đạt **68,28**; bản
thân giáo viên 7B đạt **78,72**. Hệ liên kết lấp được khoảng 70% khoảng cách
tới trần tập trung.

### 2.2 Gỡ từng thành phần: cái gì đứng vững qua 3 seed

| Thành phần bị gỡ | Mức sụt từng seed | Trung bình | Độ lệch | p |
|---|---|---:|---:|---:|
| **Toàn bộ chưng cất tại máy chủ** | 6,00 / 5,03 / 2,61 | **−4,55** | 1,75 | **0,046** |
| Chỉ reverse-KL (giữ SeqKD) | 2,03 / 0,20 / 2,90 | −1,71 | 1,38 | 0,165 |
| Chỉ SeqKD (giữ phần liên kết) | 3,97 / 4,83 / −0,29 | −2,84 | 2,74 | 0,215 |

**Bước chưng cất tại máy chủ là thành phần duy nhất chứng minh được giá trị qua
nhiều seed** (−4,55 điểm khi gỡ, p = 0,046). Đây là kết quả chắc chắn.

**Việc tách bước đó thành hai tầng thì chưa tách được.** Reverse-KL hơn SeqKD
trung bình 1,71 điểm nhưng dao động từ 0,20 đến 2,90 tuỳ seed; SeqKD thậm chí
**âm ở seed 2**. Với 3 seed, một hiệu ứng 1,71 với độ lệch 1,38 về mặt toán học
không thể đạt ý nghĩa thống kê — cần khoảng 7 seed. **Đây là câu hỏi chưa được
trả lời, không phải câu trả lời phủ định.**

Báo cáo trước ghi con số này là +2,03 với p = 0,042. Đó là kiểm định trên một
seed duy nhất, chỉ trả lời "hai *mô hình cụ thể này* có khác nhau không", không
trả lời "hai *phương pháp* có khác nhau không". Ba seed cho thấy biến thiên
giữa các seed đủ lớn để nuốt hiệu ứng đó.

### 2.3 Vì sao các bước trung gian dao động mà điểm cuối thì không

```text
seed 0:  trước server 57,35  →  máy chủ bù +6,00  →  63,35
seed 1:  trước server 57,45  →  máy chủ bù +5,03  →  62,48
seed 2:  trước server 59,77  →  máy chủ bù +2,61  →  62,38
```

**Xuất phát càng cao, bước chưng cất bù càng ít, điểm cuối gần như không đổi.**
Bước chưng cất kéo mọi thứ về khoảng 62,7 bất kể đi vào ở đâu.

Điều này có hai hệ quả. Thứ nhất, nó giải thích vì sao đo đóng góp của từng
bước phía trước lại nhiễu: bước máy chủ bù trừ cho chúng. Thứ hai, nó nói rằng
đầu tư công sức vào cải thiện tầng gộp là kém hiệu quả — đã kiểm chứng riêng
bằng thực nghiệm về phép gộp chính xác, kết quả không cải thiện.

### 2.4 Giá trị của dữ liệu riêng

Đối chứng quan trọng nhất: lấy mô hình gốc, áp đúng bước chưng cất của máy chủ,
**không dùng một dòng dữ liệu riêng nào**. Kết quả 61,22 (mới có 1 seed).

So với hệ đầy đủ 62,74, **giá trị của toàn bộ dữ liệu riêng khoảng +1,5 điểm**.
Con số này chưa được lặp lại trên nhiều seed nên chỉ là ước lượng.

Ba điều đi kèm cần nói thẳng:

- **Liên kết một mình không cạnh tranh được.** Gộp 5 client mà không chưng cất
  đạt 58,19, **thua** việc chưng cất từ mô hình gốc bằng dữ liệu công khai
  (61,22).
- **Phần lớn mức tăng đến từ kho công khai**, không phải từ dữ liệu riêng:
  khoảng 11 trên tổng 12,74 điểm. Không được phát biểu rằng liên kết tạo ra
  toàn bộ mức tăng.
- **Đóng góp nằm ở sự kết hợp.** Không nửa nào tự đủ; hệ đầy đủ hơn cả hai.
  Phát biểu đúng là: *liên kết mô hình nhỏ chỉ đáng làm khi có bước chưng cất
  từ kho công khai*.

### 2.5 Gộp liên kết có hơn từng bên tự làm không

Đo 5 adapter client của nhánh khuyến nghị (seed 0):

| | EX |
|---|---:|
| Client yếu nhất | 53,38 |
| Trung bình 5 client | 54,99 |
| Client mạnh nhất | 57,64 |
| **Model sau khi gộp** | **57,35** |

Model gộp hơn trung bình client **2,36 điểm** và chỉ kém client mạnh nhất
**0,29 điểm** — tức là ngang. Đáng chú ý: không bên nào biết trước mình là bên
mạnh, nên trong thực tế model gộp là lựa chọn tốt hơn hẳn kỳ vọng của việc tự
làm.

---

## 3. (B) Có nên giữ ICL không

**ICL ở đây là:** chèn 3 ví dụ mẫu (câu hỏi + SQL đúng, lấy từ kho riêng của
chính client đó) vào prompt để mô hình bắt chước. Kỹ thuật này nằm trong tên
phương pháp nên phải được kiểm chứng nghiêm túc.

Đã chạy **hai pipeline song song hoàn toàn** — cùng phân hoạch dữ liệu, cùng
seed, cùng kho công khai, cùng bước máy chủ, cùng ngân sách — khác đúng một
biến: client có dùng ví dụ mẫu khi huấn luyện hay không.

### 3.1 Bảng 2×2

| | Chạy không ví dụ mẫu | Chạy có 3 ví dụ mẫu | Mất khi thêm ví dụ |
|---|---:|---:|---:|
| **Huấn luyện có ICL** | 63,93 | 60,06 | **−3,87** (p = 0,003) |
| **Huấn luyện không ICL** | 62,57 | 59,48 | **−3,09** (p = 0,014) |
| Chênh lệch | +1,35 (p = 0,060) | +0,58 (p = 0,572) | |

**(1) Đưa ví dụ mẫu vào lúc chạy làm giảm độ chính xác, có ý nghĩa thống kê.**
Mất 3,87 điểm (p = 0,003). Đây là hiệu ứng ICL lớn nhất đo được, và nó âm.

**(2) Huấn luyện có ví dụ mẫu KHÔNG bảo vệ được khỏi (1) — điểm quyết định.**
Lý lẽ của DAIL-SQL, cũng là lý lẽ duy nhất từng biện minh cho việc cho client
huấn luyện kèm ví dụ, dự đoán mô hình huấn luyện không ví dụ sẽ sụp đổ khi gặp
ví dụ còn mô hình huấn luyện có ví dụ thì không. Thực tế **ngược lại**: mô hình
huấn luyện không ví dụ mất *ít hơn* (−3,09 so với −3,87). Tương tác đi sai
chiều.

Ba mô hình độc lập, ba công thức huấn luyện khác nhau, đều mất khoảng 3 điểm
khi gặp ví dụ mẫu. **Hình phạt này là thuộc tính của mô hình 1,5B, không phải
của cách huấn luyện.** Không có cách huấn luyện nào chữa được nó.

**(3) Nếu triển khai có ví dụ mẫu, huấn luyện có ICL mua được đúng số không.**
60,06 so với 59,48, chênh 0,58 điểm, p = 0,572.

**(4) Huấn luyện có ICL còn làm mô hình gộp kém đi.** Trước bước máy chủ, nhánh
không ICL đạt 57,35 còn nhánh ICL chỉ 54,45 — kém **2,90 điểm, p = 0,008**, kèm
nhiều lỗi thực thi hơn (258 so với 236).

### 3.2 Cái giá phải trả

| | Không ICL | Có ICL | Tỉ lệ |
|---|---:|---:|---:|
| Thời gian huấn luyện 5 client | 4.100 giây | 9.651 giây | **2,35×** |
| Độ dài prompt khi chạy | 1.568 ký tự | 2.175 ký tự | **+38,7%** |
| Thời gian mỗi câu hỏi | 0,289 giây | 1,224 giây | **4,2×** |
| Hạ tầng tại mỗi bên | không cần | phải lưu và đánh chỉ mục kho ví dụ riêng | — |

### 3.3 Đề xuất

Bốn kiểm định đều cùng một hướng, không có ô nào ủng hộ ICL:

| Bằng chứng | Giá trị | p |
|---|---:|---:|
| Huấn luyện có ICL làm mô hình gộp kém đi | −2,90 | 0,008 |
| Ví dụ mẫu lúc chạy làm giảm độ chính xác | −3,87 | 0,003 |
| Huấn luyện có ICL không bảo vệ được (bác bỏ DAIL-SQL) | sai chiều 0,78 | — |
| Ở chế độ triển khai có ví dụ, hai nhánh như nhau | +0,58 | 0,572 |

Cộng thêm chi phí 2,35× khi huấn luyện và 4,2× khi chạy.

Kết luận về ICL dựa trên 6 ô đo độc lập với hiệu ứng 3–4 điểm, lớn gấp đôi
biến thiên giữa các seed đo được ở §2. Khác với phần phân rã thành phần, phần
này không bị đe doạ bởi việc thêm seed.

1. **Bỏ ICL khỏi phương pháp đề xuất.** Pipeline chính thức: client tự huấn
   luyện không ví dụ mẫu → gộp FedAvg → chưng cất tại máy chủ trên kho công
   khai.
2. **Giữ ICL trong bài báo như một kết quả âm có kiểm định.** Đây không phải
   phần bỏ đi — nó bác bỏ một cơ chế đang được coi là hiển nhiên trong tài liệu
   (DAIL-SQL) ở quy mô mô hình nhỏ, và có đủ số liệu để bảo vệ trước phản biện.
3. **Tên phương pháp cần đổi.** `Fed-ICKD` và `FedICL-SQL` đều lấy ICL làm
   trung tâm, không còn khớp với bằng chứng.

---

## 4. Giới hạn

**Số seed.** Phần §2 dùng 3 seed; phần §3 (ICL) dùng 1 seed nhưng 6 ô đo độc
lập với hiệu ứng lớn. Với 3 seed, chỉ những hiệu ứng lớn hơn khoảng 4 điểm mới
đạt được ý nghĩa thống kê — đó là lý do bước chưng cất tổng thể qua được còn
việc tách nó thành hai tầng thì không. **Đang chạy thêm 4 seed** để đưa thiết
kế lên 7 seed; nếu hiệu ứng 1,71 điểm của reverse-KL là thật, 7 seed sẽ cho
thấy.

**Một vòng.** Toàn bộ số liệu là T = 1. Chưa đo hành vi qua nhiều vòng.

**Dòng "giá trị dữ liệu riêng" mới có 1 seed.** Đang bổ sung seed 1 và 2.

Một phương án gộp adapter tinh vi hơn (FLoRA-NA) đã được thử và **không cải
thiện** ở bất kỳ cấu hình nào — kể cả khi dựng phép gộp chính xác tuyệt đối,
mức tăng là +0,68 điểm không có ý nghĩa thống kê (p = 0,311). Đề xuất dùng
FedAvg thường.

BIRD chỉ dùng làm kho công khai để chưng cất, **không** dùng làm tập đánh giá.
Mọi con số EX đều đo trên Spider dev, vốn không chung schema nào với dữ liệu
huấn luyện.
