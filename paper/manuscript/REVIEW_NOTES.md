# Lưu ý cần review

File này ghi trong lúc viết manuscript, để bạn review sau. Mỗi mục nói
ở đâu, vấn đề gì, tôi đề xuất gì. Bạn trả lời trong chat hoặc ghi thẳng
vào cột "Quyết định"; mục đã xong được chuyển xuống phần "Đã xong".
Chi tiết của từng section nằm ở file ghi chép của section đó
(Section 3: `briefs/03_method_notes_editor.md`).

Cập nhật: 2026-11-26, sau bản sửa vòng 2 của Section 3. Hai vòng notes
đã dùng hết; bản hiện tại chờ bạn đọc trước khi commit.

## A. Cần bạn quyết định

| # | Ở đâu | Vấn đề | Đề xuất | Quyết định |
|---|---|---|---|---|
| A1 | Section 3.3, đoạn cuối | Hai người đọc lạnh đều thấy lý do của warm-up rounds thiếu một bước: nó cho thấy gold SQL cần cho một số câu hỏi, chưa cho thấy vì sao phải ở các round trước. Tôi đã cho writer thêm bước đó: sau warm-up, ít câu hỏi hơn không có sample đúng khi preference round đầu sample. Số đếm từ round records đã commit: BIRD 4,035 của 9,428 (pretrained model), 3,220 (1 warm-up), 2,698 (2 warm-up); Spider 1,074 của 8,659, rồi 573. Method không in số. Đây là phát biểu mới, chưa có trong `CLAIMS.md` | Giữ. Thêm một hàng vào `CLAIMS.md` (không nói gì về EX) và hai macro cho Section 6. Không viết "nhiều câu hỏi sinh pair hơn": điều đó chỉ đúng trên BIRD (4,857 lên 5,877), Spider thì giảm (5,951 xuống 5,192) | |
| A2 | Section 6 hoặc 7 | Cả hai người đọc hỏi: sao không dùng gold SQL làm correct side ngay trong preference round cho các câu hỏi không có sample đúng. Notes có hai kết quả trên BIRD, chưa là hàng nào của paper: gold làm correct side, 1 round, 39.24 so với 41.85 (p 0.007); thêm hàng NLL trên gold, 42.37 so với 43.02 (p 0.43) | Một câu ở Section 6 với kết quả thứ nhất, cần một hàng trong `CLAIMS.md`. Không cần GPU | |
| A3 | Section 3, độ dài | Sau bản nháp đầu tôi hạ độ dài brief xin từ 1,490 (trần 1,650) xuống 1,420 (trần 1,490), thấp hơn mức "10% dưới outline" bạn đã quyết. Lý do: Fig. 1, Algorithm 1 và bốn công thức chiếm khoảng 1.85 trang, plan tính 1.5. Section 3 hiện khoảng 4.3 trang, ngân sách 4.0; tổng plan là 24.6 của 25 trang | Chấp nhận khoảng 4.3 trang. Khi biết tổng số trang, lấy phần dư từ Appendix B (0.6 trang, plan đã định chuyển sang supplementary trước tiên) | |
| A4 | Fig. 1 | Ba chỗ trong hình lệch với văn bản; tôi chưa sửa vì bạn dặn không đụng hình khi chưa quyết. (1) Ghi chú "Only LoRA adapters travel", trong khi Section 3.1 nói adapter và một số nguyên, "and nothing else"; caption không nói gì về điểm này, nên hình và văn bản đang lệch nhau. (2) Bước 4 viết L = L_DPO + L_NLL, không có λ và ký hiệu khác Eq. (4); caption giờ nối hai cách gọi. (3) "2 FedAvg rounds" và "N = 10" là số gõ tay trong hình, không theo macro | Sửa nhãn (1) thành adapter và số pairs. Để (2) và (3) như cũ. Nói "sửa" thì tôi đổi nhãn, không đụng bố cục | |
| A5 | Section 3.4, M = 2 | Cả hai người đọc muốn một lý do về hiệu quả, không chỉ về chi phí; paper không có ablation theo M (`CLAIMS.md`, mục 7, điểm 8 đã quyết: chỉ nói lý do chi phí) | Giữ như đã quyết. Một preference round với M = 10 trên BIRD tốn khoảng một ngày GPU (ước lượng từ 283 phút training ở M = 2), tôi không đề xuất chạy | |

## B. Cần bạn đọc lại câu chữ

Đọc trong `sections/03_method.tex` hoặc `build/main.pdf` (bản sửa vòng
2). Sau hai vòng, phần còn lại do bạn sửa hoặc bảo tôi sửa chỗ nào là
cơ học.

| # | Ở đâu | Đọc để kiểm gì |
|---|---|---|
| B1 | Section 3.4, đoạn cuối (CodeLutra) | Câu "The contribution of FedLS-SQL is to bring this execution-based supervision into federated training, where only a client can compute it", rồi "The rest are settings". Đây là chỗ Method nói paper nhận cái gì là của mình; kiểm xem có đúng ý bạn và có khớp contribution 1 trong `CLAIMS.md` không. "First" và "to our knowledge" để dành cho Section 1 |
| B2 | Section 3.4, đoạn cuối | Câu "the same λ then weighs the NLL term less against the preference term than in CodeLutra, by a factor of \|y+\|". Đúng về số học; người đọc thứ hai coi việc không nói là nói quá mức độ theo CodeLutra. λ không còn trong danh sách "We follow CodeLutra in" |
| B3 | Section 3.1, đoạn cuối | Cái gì ở lại client, giờ được gọi tên (samples, execution results, execution labels, preference pairs). Các từ này xuất hiện ở 3.1 trước khi 3.4 định nghĩa chúng. So với contribution 2 trong `CLAIMS.md` |
| B4 | Section 3.3, đoạn cuối | Câu mới về lý do warm-up: "which leaves fewer questions without a correct sample than the pretrained model does", và "Section 6 reports these counts" (mục A1) |
| B5 | Section 3.4, đoạn reference model và đoạn về câu hỏi không sinh pair | Hai đoạn cả hai người đọc phải đọc hai lần ở bản trước; đã viết lại ở vòng 2, chưa có người đọc lạnh nào đọc bản mới |
| B6 | Section 3.4 | Việc client gửi số pairs lên server giờ chỉ nói ở Section 3.1 ("one integer, its aggregation weight") và ở Algorithm 1, dòng 13; văn bản 3.4 chỉ nói trọng số là số pairs |
| B7 | Section 3.4 | "Empty sample" không còn được nhắc: nó là sample incorrect theo quy tắc chung. Chi tiết này có thể để ở Appendix B |
| B8 | Section 3.4 | "CodeLutra constructs ten" viết bằng chữ, không qua macro (là fact của paper được trích, không phải setting của ta) |

## C. Câu hỏi reviewer có thể đặt

Từ hai bài đọc lạnh. Không cần quyết định ngay; ghi để khi viết các
section sau có câu trả lời.

| # | Câu hỏi | Paper trả lời ở đâu |
|---|---|---|
| C1 | FedLS-SQL là gì ngoài CodeLutra chạy trong FedAvg? | Section 1, Section 2 và Table 1 mang lập luận; Section 3.4 nói khác biệt nào là đóng góp |
| C2 | Với 4 rounds chỉ có một lần sample lại; "on-policy" có thấy được không? | Section 6, B1 và B2 (BIRD: pairs và reference cố định thấp hơn 2.61, p 5.7e-4; Spider: ngang nhau) |
| C3 | Trọng số theo số pairs nghiêng về client có nhiều câu hỏi "nửa đúng nửa sai"; có chủ ý không? | Section 6, B6: ba cách đặt trọng số cho kết quả ngang nhau |
| C4 | Lấy trung bình hai ma trận của LoRA riêng rẽ không bằng trung bình tích của chúng | Chưa trả lời. Một mệnh đề là đủ nếu có nguồn đã kiểm làm như vậy; tôi chưa kiểm OpenFedLLM ở điểm này |
| C5 | NLL lấy trung bình theo token còn preference term là tổng: cân bằng giữa hai term phụ thuộc độ dài query | Chưa trả lời; không có ablation |
| C6 | Database không có row và gold SQL lỗi: các câu hỏi đó nhận label gì? | Section 3.4: không sinh pair ở mọi round; số lượng cần có ở Section 4 |

## D. Brief của Section 3 đã đổi sau khi bạn duyệt

Bạn duyệt `briefs/03_method.md` ở commit `3638801`. Các thay đổi sau đó
(xem `git diff 3638801 -- briefs/03_method.md`):

1. Độ dài: mục A3.
2. Statement 3 của Section 3.3 (cái warm-up round bỏ sót) gộp vào
   statement 1 của Section 3.2, để ý đó chỉ nói một lần.
3. Section 3.1, statement 4: gọi tên cái gì ở lại client; bỏ
   "everything derived".
4. Section 3.3, statement 2: thêm bước lập luận của mục A1.
5. Section 3.4, labeling: query được đọc từ output và kết quả được so
   như ở evaluation (Section 4 định nghĩa); "empty sample"; chỉ sample
   hoàn chỉnh mới được chạy; "database không có row" nghĩa là không
   bảng nào có row.
6. Section 3.4, pairs: hai lần rút độc lập; cùng một pair có thể lặp;
   quy tắc replacement có thể để ở Appendix B.
7. Section 3.4, aggregation: lý do của trọng số (lượng dữ liệu client
   đã train trong round) và con trỏ tới Section 6.
8. Hàng CodeLutra: khác biệt về bản chất, cái nào là đóng góp, hệ quả
   của trung bình theo token đối với λ.

## E. Việc chuyển sang các section sau

| Section | Phải mang |
|---|---|
| 4 | Cách đọc query từ output của model và cách so execution results (Section 3.4 trỏ tới đây); số câu hỏi trên database không có row và số gold SQL lỗi |
| Appendix B | Time limit, cấu hình adapter, settings của local training, và quy tắc replacement nếu Section 3.4 bỏ nó |
| 6 | Số câu hỏi không có sample đúng, có và không có warm-up (mục A1); so sánh trọng số; câu về gold SQL trong preference round nếu bạn đồng ý mục A2 |
| 7 | Client phải chạy được SQL trên database của mình (Section 3.5 không còn nói) |

## F. Còn mở từ trước

Từ `paper/notes/WRITING_PLAN.md`, mục 11.

1. JIIS: 25 trang tính trong class nào, và review model (hỏi editorial
   office). Hiện viết trong `sn-jnl`, không ẩn danh.
2. Fig. 1 theo quy định của Springer Nature về hình tạo bằng AI: bạn vẽ
   lại, hoặc bạn coi nó là flow chart.
3. Journal nào nộp trước (plan giả định JIIS).
4. Tác giả, funding, competing interests chưa điền.
5. Hai entry của `references.bib` cần xem bằng mắt: tác giả thứ hai của
   SLM-SQL; Holm (1979) không có DOI.

## Đã xong

Chưa có mục nào.
