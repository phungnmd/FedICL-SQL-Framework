# Lưu ý cần review

File này ghi trong lúc viết manuscript, để bạn review sau. Mỗi mục nói
ở đâu, vấn đề gì, tôi đề xuất gì. Bạn trả lời trong chat hoặc ghi thẳng
vào cột "Quyết định"; mục đã xong được chuyển xuống phần "Đã xong".
Chi tiết của từng section nằm ở file ghi chép của section đó
(Section 3: `briefs/03_method_notes_editor.md`).

Cập nhật: 2026-11-26. Section 3 đã commit (`05c0853`); các mục A1 đến
A5 và B1 đến B8 của nó chờ bạn review. Brief của Section 4
(`briefs/04_setup.md`) chờ bạn duyệt; các mục A6 đến A10 là của nó.

## A. Cần bạn quyết định

| # | Ở đâu | Vấn đề | Đề xuất | Quyết định |
|---|---|---|---|---|
| A1 | Section 3.3, đoạn cuối | Hai người đọc lạnh đều thấy lý do của warm-up rounds thiếu một bước: nó cho thấy gold SQL cần cho một số câu hỏi, chưa cho thấy vì sao phải ở các round trước. Tôi đã cho writer thêm bước đó: sau warm-up, ít câu hỏi hơn không có sample đúng khi preference round đầu sample. Số đếm từ round records đã commit: BIRD 4,035 của 9,428 (pretrained model), 3,220 (1 warm-up), 2,698 (2 warm-up); Spider 1,074 của 8,659, rồi 573. Method không in số. Đây là phát biểu mới, chưa có trong `CLAIMS.md` | Giữ. Thêm một hàng vào `CLAIMS.md` (không nói gì về EX) và hai macro cho Section 6. Không viết "nhiều câu hỏi sinh pair hơn": điều đó chỉ đúng trên BIRD (4,857 lên 5,877); trên Spider số câu hỏi sinh pair giảm (4,454 xuống 4,013; số câu hỏi có cả hai label, tính cả các database không có row, là 5,951 xuống 5,192) | |
| A2 | Section 6 hoặc 7 | Cả hai người đọc hỏi: sao không dùng gold SQL làm correct side ngay trong preference round cho các câu hỏi không có sample đúng. Notes có hai kết quả trên BIRD, chưa là hàng nào của paper: gold làm correct side, 1 round, 39.24 so với 41.85 (p 0.007); thêm hàng NLL trên gold, 42.37 so với 43.02 (p 0.43) | Một câu ở Section 6 với kết quả thứ nhất, cần một hàng trong `CLAIMS.md`. Không cần GPU | |
| A3 | Section 3, độ dài | Sau bản nháp đầu tôi hạ độ dài brief xin từ 1,490 (trần 1,650) xuống 1,420 (trần 1,490), thấp hơn mức "10% dưới outline" bạn đã quyết. Lý do: Fig. 1, Algorithm 1 và bốn công thức chiếm khoảng 1.85 trang, plan tính 1.5. Section 3 hiện khoảng 4.3 trang, ngân sách 4.0; tổng plan là 24.6 của 25 trang | Chấp nhận khoảng 4.3 trang. Khi biết tổng số trang, lấy phần dư từ Appendix B (0.6 trang, plan đã định chuyển sang supplementary trước tiên) | |
| A4 | Fig. 1 | Ba chỗ trong hình lệch với văn bản; tôi chưa sửa vì bạn dặn không đụng hình khi chưa quyết. (1) Ghi chú "Only LoRA adapters travel", trong khi Section 3.1 nói adapter và một số nguyên, "and nothing else"; caption không nói gì về điểm này, nên hình và văn bản đang lệch nhau. (2) Bước 4 viết L = L_DPO + L_NLL, không có λ và ký hiệu khác Eq. (4); caption giờ nối hai cách gọi. (3) "2 FedAvg rounds" và "N = 10" là số gõ tay trong hình, không theo macro | Sửa nhãn (1) thành adapter và số pairs. Để (2) và (3) như cũ. Nói "sửa" thì tôi đổi nhãn, không đụng bố cục | |
| A5 | Section 3.4, M = 2 | Cả hai người đọc muốn một lý do về hiệu quả, không chỉ về chi phí; paper không có ablation theo M (`CLAIMS.md`, mục 7, điểm 8 đã quyết: chỉ nói lý do chi phí) | Giữ như đã quyết. Một preference round với M = 10 trên BIRD tốn khoảng một ngày GPU (ước lượng từ 283 phút training ở M = 2), tôi không đề xuất chạy | |
| A6 | Section 4.1 (brief) | Section 3.4 nói hai loại câu hỏi không bao giờ sinh pair; người đọc lạnh hỏi số lượng (mục C6). Số từ round records: Spider train có 7 database không có row, 1,759 của 8,659 câu hỏi nằm trên đó (20%), cộng 3 gold SQL lỗi; BIRD train có 350 gold SQL lỗi và 87, rồi 92 gold SQL quá time limit ở hai preference rounds. Đã có macro (`\fact{train.*}`) | In các số này ở Section 4.1, một hai câu: chúng giải thích cột "questions that yield pairs" của Table 7 và người đọc cần để lặp lại thí nghiệm. Nếu bạn không muốn in, tôi bỏ statement 6 khỏi brief | |
| A7 | Section 4, chỗ đặt bốn research questions | `OUTLINE.md` đặt bốn RQ làm câu chuyển ở cuối Section 4. Brief đặt chúng ở đoạn mở đầu Section 4, trước 4.1: Section 4.1 và 4.2 gọi "RQ2", "RQ3" (chính outline viết vậy), nên RQ phải được nêu trước; một đoạn ở cuối sẽ nằm dưới heading 4.6 "Statistical test" | Giữ ở đoạn mở đầu | |
| A8 | Appendix A và B | Tôi đã lắp hai appendix. Appendix A in prompt của một câu hỏi BIRD dev và một câu hỏi Spider test, lấy từ predictions đã commit: bảng đầu tiên của schema và các dòng sau schema; `[...]` thay cho các bảng còn lại. Khoảng 0.45 trang, plan tính 0.2. In đủ hai prompt sẽ tốn khoảng 1 trang. Appendix B (bảng settings) khoảng 0.75 trang, plan tính 0.6 | Giữ bản rút gọn. Khi biết tổng số trang, Appendix B sang supplementary trước (plan đã định), prompt đầy đủ cũng có thể vào supplementary | |
| A9 | Section 4.4 và 4.5 | Section 4 mô tả cả các baseline chưa chạy: local SFT, FedProx SFT (hệ số mu chưa đặt, in `??`), FedDPO; và câu "hai hàng chính trên BIRD được train thêm một seed thứ hai" (chưa queue). Nếu hàng nào bị bỏ thì câu của nó phải bỏ theo | Viết theo plan của các hàng (`RESEARCH_STATE.md`, mục 3.4); đọc lại Section 4.4 và 4.5 khi các hàng về | |
| A10 | Section 4.2, citation của cách chia client | `references.bib` chỉ có `hsu2019noniid` cho Dirichlet partition. Code của ta theo nhánh `noniid-labeldir` của NIID-Bench (Li et al., ICDE 2022): với mỗi tier rút tỉ lệ của các client từ Dir(alpha), và client đã đủ 1/K số database thì không nhận thêm. Hsu et al. rút phân phối label cho từng client, là chiều ngược lại | Thêm entry NIID-Bench vào `references.bib` (cần bạn hoặc tôi kiểm record: tác giả, DOI) và cite nó cùng `hsu2019noniid`. Chưa làm | |

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
| C6 | Database không có row và gold SQL lỗi: các câu hỏi đó nhận label gì? | Section 3.4: không sinh pair ở mọi round; số lượng ở Section 4.1 (mục A6) |
| C7 | FedDPO baseline chạy sau 2 warm-up rounds và dùng pairs từ execution labels; FedDPO "nguyên bản" từ pretrained model thì sao? | Section 4.4 nói rõ cái gì lấy từ OpenFedLLM (pairs cố định, reference cố định, không NLL) và cái gì là của ta khi chạy nó. Hàng không warm-up của method (Table 8) là so sánh gần nhất; không có hàng FedDPO từ pretrained model |
| C8 | 20% câu hỏi train của Spider không sinh pair: preference rounds có bỏ qua các domain đó không? | Chưa trả lời. Các câu hỏi đó vẫn được học ở warm-up rounds; Section 7 (limitation 5 của `CLAIMS.md`) nói về database không có row |
| C9 | McNemar với một seed chỉ nói về mẫu câu hỏi test, không nói về độ biến thiên giữa các lần train | Section 4.6 nói test là gì; seed thứ hai cho hai hàng chính trên BIRD (chưa chạy); Section 7 nêu limitation |

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
| 4 | Cách đọc query từ output của model và cách so execution results (Section 3.4 trỏ tới đây); số câu hỏi trên database không có row và số gold SQL lỗi. Đã vào brief `briefs/04_setup.md` (Section 4.1) |
| Appendix B | Time limit, cấu hình adapter, settings của local training, và quy tắc replacement nếu Section 3.4 bỏ nó. Đã có trong `generated/tab_settings.tex` (các hàng Pairing, Time limit) |
| 5 | Thời gian ở Table 7 là tổng của các client chạy lần lượt trên một card (Section 4.5 chỉ nói simulation trên một GPU) |
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
