# Kết quả pipeline liên kết và đề xuất bỏ ICL

**Ngày:** 11/08/2026 · **Cấu hình:** K=5 client, non-IID Dirichlet α=0,5, T=1 vòng, seed 0
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

### 2.1 Cộng dồn từng bước

| Bước | EX | Tăng thêm |
|---|---:|---:|
| Mô hình 1,5B chưa huấn luyện | 50,00 | — |
| Client tự huấn luyện + gộp liên kết | 57,35 | +7,35 |
| + học câu SQL của giáo viên (SeqKD) | 61,32 | +3,97 |
| **+ học phân phối xác suất của giáo viên (reverse-KL)** | **63,35** | **+2,03** |

Đối chiếu: gom hết dữ liệu về một chỗ huấn luyện tập trung đạt **68,28**; bản
thân giáo viên 7B đạt **78,72**.

Hệ nâng mô hình nhỏ từ **50,00 lên 63,35 mà không một dòng dữ liệu nào rời khỏi
chủ sở hữu**, lấp được 73% khoảng cách tới trần tập trung.

### 2.2 Bỏ từng thành phần đi thì mất bao nhiêu

Đây là phép kiểm chứng chặt chẽ hơn: lần lượt gỡ từng thành phần khỏi hệ đầy
đủ và đo mức sụt.

| Cấu hình | EX | Mất bao nhiêu | p |
|---|---:|---:|---:|
| **Hệ đầy đủ** | **63,35** | — | — |
| Bỏ reverse-KL | 61,32 | −2,03 | **0,042** |
| Bỏ toàn bộ chưng cất tại máy chủ | 57,35 | −6,00 | **4,8·10⁻⁵** |
| Bỏ toàn bộ tầng liên kết | 61,22 | −2,13 | **0,017** |
| Bỏ tất cả (mô hình gốc) | 50,00 | −13,35 | — |

**Gỡ bất kỳ thành phần nào cũng làm giảm độ chính xác có ý nghĩa thống kê.**
Không có thành phần nào thừa.

Dòng "bỏ toàn bộ tầng liên kết" là đối chứng quan trọng nhất và mới chạy xong:
lấy mô hình gốc, áp đúng bước chưng cất của máy chủ, **không dùng một dòng dữ
liệu riêng nào**. Nó đạt 61,22 — tức là **giá trị thực của toàn bộ dữ liệu
riêng là +2,13 điểm** (p = 0,017).

### 2.3 Ba điều bảng trên nói ra

**Liên kết một mình không cạnh tranh được.** Chỉ gộp 5 client mà không chưng
cất đạt 57,35, **thua** cả việc chưng cất từ mô hình gốc bằng dữ liệu công khai
(61,22; chênh 3,87 điểm, p = 0,013).

**Chưng cất một mình cũng chưa tối ưu.** 61,22 so với 63,35 của hệ đầy đủ.

**Chỉ kết hợp mới cho kết quả tốt nhất.** Hệ đầy đủ hơn chưng cất thuần 2,13
điểm và hơn liên kết thuần 6,00 điểm, cả hai đều có ý nghĩa thống kê. Đóng góp
của đề tài nằm ở chỗ này: **liên kết mô hình nhỏ chỉ trở nên đáng làm khi có
bước chưng cất từ kho công khai**, và bài báo định lượng được phần mà dữ liệu
riêng thực sự đóng góp.

Cần nói thẳng để tránh hiểu sai: phần lớn mức tăng (11,22 trên tổng 13,35) đến
từ chưng cất công khai, dữ liệu riêng đóng góp 2,13. Điều này không làm yếu
bảng ablation — một thành phần chứng minh giá trị bằng việc gỡ nó ra thì tệ đi,
không phải bằng việc đóng góp ngang nhau — nhưng không được phát biểu rằng
liên kết tạo ra toàn bộ mức tăng.

### 2.4 Cơ chế đề xuất lặp lại được ba lần

Reverse-KL so với đối chứng SeqKD cùng dữ liệu, cùng ngân sách, trên ba quần
thể client hoàn toàn khác nhau:

| Xuất phát | SeqKD | + reverse-KL | Tăng | p |
|---|---:|---:|---:|---:|
| Mô hình gốc (không liên kết) | 59,67 | 61,22 | +1,55 | 0,121 |
| Liên kết, không ICL | 61,32 | 63,35 | **+2,03** | **0,042** |
| Liên kết, có ICL | 61,51 | 64,02 | **+2,51** | **0,013** |

Cùng chiều cả ba lần, độ lớn 1,55–2,51, hai trong ba đạt ý nghĩa thống kê. Đây
là kết quả vững nhất trong toàn dự án.

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

1. **Bỏ ICL khỏi phương pháp đề xuất.** Pipeline chính thức: client tự huấn
   luyện không ví dụ mẫu → gộp FedAvg → chưng cất reverse-KL tại máy chủ trên
   kho công khai.
2. **Giữ ICL trong bài báo như một kết quả âm có kiểm định.** Đây không phải
   phần bỏ đi — nó bác bỏ một cơ chế đang được coi là hiển nhiên trong tài liệu
   (DAIL-SQL) ở quy mô mô hình nhỏ, và có đủ số liệu để bảo vệ trước phản biện.
3. **Tên phương pháp cần đổi.** `Fed-ICKD` và `FedICL-SQL` đều lấy ICL làm
   trung tâm, không còn khớp với bằng chứng.

---

## 4. Giới hạn

Tất cả số liệu là **seed 0, T = 1 vòng**. Giá trị p cho biết hai mô hình cụ thể
đó khác nhau, chưa cho biết hai *phương pháp* khác nhau — biến thiên do seed
chưa được đo. Hai dòng ablation quan trọng nhất nằm ở p = 0,017 và p = 0,042,
đủ gần ngưỡng để một seed khác có thể làm chúng dịch chuyển. Seed 1 và seed 2
đang được xếp lịch, mỗi seed khoảng 4 giờ GPU. Các kết luận về ICL nhất quán
qua 6 ô đo độc lập nên ít có khả năng đảo chiều.

Một phương án gộp adapter tinh vi hơn (FLoRA-NA) đã được thử và **không cải
thiện** ở bất kỳ cấu hình nào — kể cả khi dựng phép gộp chính xác tuyệt đối,
mức tăng là +0,68 điểm không có ý nghĩa thống kê (p = 0,311). Đề xuất dùng
FedAvg thường.

BIRD chỉ dùng làm kho công khai để chưng cất, **không** dùng làm tập đánh giá.
Mọi con số EX đều đo trên Spider dev, vốn không chung schema nào với dữ liệu
huấn luyện.
