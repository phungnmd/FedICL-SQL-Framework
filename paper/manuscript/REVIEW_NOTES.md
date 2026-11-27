# Lưu ý cần review

File này ghi trong lúc viết manuscript, để bạn review sau. Mỗi mục nói
ở đâu, vấn đề gì, tôi đề xuất gì. Bạn trả lời trong chat hoặc ghi thẳng
vào cột "Quyết định"; mục đã xong được chuyển xuống phần "Đã xong".
Chi tiết của từng section nằm ở file ghi chép của section đó
(Section 3: `briefs/03_method_notes_editor.md`).

Cập nhật: 2026-11-27. Từ 2026-11-27 draft của một section được commit
ngay khi xong hai round sửa, không chờ bạn đọc (bạn quyết định
2026-11-27); các mục dưới đây vẫn chờ bạn review.

Giọng văn đổi hướng (bạn quyết định 2026-11-27): draft của cả tám
section đang ở giọng lab và sẽ được viết lại từ brief dạng mới, bản
hiện tại giữ ở tag `draft-v1-2026-11-27`. Các mục B (câu chữ) của
draft cũ hết hiệu lực khi section của nó được viết lại; các mục về số
liệu, claim và hình vẫn còn. Việc cần bạn duyệt trước khi viết lại:
A32.

| Section | Trạng thái | Mục của nó | Ghi chép |
|---|---|---|---|
| 3, Method | commit `05c0853` | A1 đến A5, B1 đến B8 | `briefs/03_method_notes_editor.md` |
| 4, Experimental setup, Appendix A và B | draft, commit `715db32` | A14, B11 đến B14, C10 đến C16, phần D | `briefs/04_setup_notes_editor.md` |
| 5, Results | draft, commit `42b2baf`; khoảng 1,730 từ (thêm hai test ở 5.4, 2026-11-27), 42 số chờ GPU | A15 đến A17, B15 đến B17, C17 đến C25, phần D | `briefs/05_results_notes_editor.md` |
| 2, Related work | draft, commit `d9cad1c`; 893 từ, 39 references | A21 đến A23, B18 đến B23, C26 đến C28, phần D | `briefs/02_related_notes_editor.md` |
| 6, Ablation study | draft, hai round xong; 927 từ; ba hàng chờ GPU chưa có câu trong text (hàng không có preference term sau 4 rounds; 0 và 3 warm-up rounds trên BIRD dev), mỗi hàng cần khoảng 20 từ khi về | A25, B24 đến B28, C29 đến C36, phần D | `briefs/06_ablation_notes_editor.md` |
| 1, Introduction, abstract, keywords | draft, hai round xong; khoảng 1,000 từ (writer đếm 1,047 trong PDF), abstract 241 từ, 41 references; title chờ bạn chọn (A28) | A28 đến A30, B29 đến B32, C39 đến C42, phần D | `briefs/01_intro_notes_editor.md` |
| 7, Discussion and limitations; 8, Conclusion | draft, hai round xong, thêm một lần sửa theo quyết định của bạn (2026-11-27); 894 và 198 từ trong PDF (tối đa 900 và 200) | B34 đến B36, C37 đến C39, C41, C43, C44, phần D | `briefs/07_discussion_notes_editor.md` |

## A. Cần bạn quyết định

| # | Ở đâu | Vấn đề | Đề xuất | Quyết định |
|---|---|---|---|---|
| A1 | Section 3.3, đoạn cuối | Hai người đọc lạnh đều thấy lý do của warm-up rounds thiếu một bước: nó cho thấy gold SQL cần cho một số câu hỏi, chưa cho thấy vì sao phải ở các round trước. Tôi đã cho writer thêm bước đó: sau warm-up, ít câu hỏi hơn không có sample đúng khi preference round đầu sample. Số đếm từ round records đã commit: BIRD 4,035 của 9,428 (pretrained model), 3,220 (1 warm-up), 2,698 (2 warm-up); Spider 1,074 của 8,659, rồi 573. Method không in số. Đây là phát biểu mới, chưa có trong `CLAIMS.md` | Giữ. Thêm một hàng vào `CLAIMS.md` (không nói gì về EX) và hai macro cho Section 6. Không viết "nhiều câu hỏi sinh pair hơn": điều đó chỉ đúng trên BIRD (4,857 lên 5,877); trên Spider số câu hỏi sinh pair giảm (4,454 xuống 4,013; số câu hỏi có cả hai label, tính cả các database không có row, là 5,951 xuống 5,192) | |
| A3 | Section 3, độ dài | Sau bản nháp đầu tôi hạ độ dài brief xin từ 1,490 (trần 1,650) xuống 1,420 (trần 1,490), thấp hơn mức "10% dưới outline" bạn đã quyết. Lý do: Fig. 1, Algorithm 1 và bốn công thức chiếm khoảng 1.85 trang, plan tính 1.5. Section 3 hiện khoảng 4.3 trang, ngân sách 4.0; tổng plan là 24.6 của 25 trang | Chấp nhận khoảng 4.3 trang. Khi biết tổng số trang, lấy phần dư từ Appendix B (0.6 trang, plan đã định chuyển sang supplementary trước tiên) | |
| A4 | Fig. 1 | Ba chỗ trong hình lệch với văn bản; tôi chưa sửa vì bạn dặn không đụng hình khi chưa quyết. (1) Ghi chú "Only LoRA adapters travel", trong khi Section 3.1 nói adapter và một số nguyên, "and nothing else"; caption không nói gì về điểm này, nên hình và văn bản đang lệch nhau. (2) Bước 4 viết L = L_DPO + L_NLL, không có λ và ký hiệu khác Eq. (4); caption giờ nối hai cách gọi. (3) "2 FedAvg rounds" và "N = 10" là số gõ tay trong hình, không theo macro | Sửa nhãn (1) thành adapter và số pairs. Để (2) và (3) như cũ. Nói "sửa" thì tôi đổi nhãn, không đụng bố cục | |
| A5 | Section 3.4, M = 2 | Cả hai người đọc muốn một lý do về hiệu quả, không chỉ về chi phí; paper không có ablation theo M (`CLAIMS.md`, mục 7, điểm 8 đã quyết: chỉ nói lý do chi phí) | Giữ như đã quyết. Một preference round với M = 10 trên BIRD tốn khoảng một ngày GPU (ước lượng từ 283 phút training ở M = 2), tôi không đề xuất chạy | |
| A14 | Section 4, độ dài | Sau hai round, Section 4 có 1,337 từ (trần 1,250 theo rule "số từ của outline là mức trên") và khoảng 3.1 trang (plan 2.3). Hai cold read đòi thêm fact: quy tắc partition, hardness của BIRD train, nguồn của hai recipe, hàng nào được test. Writer liệt kê sáu chỗ cắt (81 từ) trong `briefs/04_setup_notes.md` | Cắt ba chỗ không mất nội dung (khoảng 50 từ, còn khoảng 1,290): vai trò của seed và quy tắc rút lại partition đã có trong Table B1, câu về Table 6 thì chính bảng đã ghi hai hàng tham chiếu. Giữ ba chỗ còn lại (IID vẫn khác cỡ; alpha nhỏ thì lệch mạnh; tên các level). Chấp nhận vượt trần khoảng 40 từ | |
| A15 | Section 5.4, so sánh cùng compute trên BIRD | Brief bạn duyệt viết: A2 và A4 là câu trả lời cho "FedAvg SFT với cùng compute". Writer chỉ ra điều này chỉ đúng trực tiếp trên Spider: bốn round của method tốn 2 x 124 + 203 + 109 = 560 phút client time, năm round FedAvg SFT tốn khoảng 620 và EX thấp hơn 4.28. Trên BIRD bốn round của method tốn 2 x 173 + 470 + 391 = 1,207 phút, bằng khoảng bảy round FedAvg SFT, còn FedAvg SFT chỉ chạy tới round 4. Tôi đã sửa brief: câu nối chỉ nói FedAvg SFT không tăng sau round 3, so sánh trực tiếp chỉ nêu cho Spider, không in tổng phút. Nếu muốn có so sánh cùng client time trên BIRD: thêm FedAvg SFT round 5 đến 7 trên BIRD (ước lượng 173 phút mỗi round, khoảng 8.7 giờ train, chưa kể evaluation). Queue tôi không đổi | |
| A16 | Section 5.4, số mới ngoài `CLAIMS.md` | Cold read hỏi: câu "the gain comes from queries that now execute" chỉ dựa trên tổng. Tôi tính bảng chuyển outcome từ predictions đã commit (FedAvg SFT so với method, cùng 4 rounds; macro `\fact{moved.*}`). BIRD dev: trong 153 câu chỉ method đúng, 75 câu trước là execution error và 78 câu là incorrect result (Spider test: 67 và 83). Trong 268 execution error của FedAvg SFT trên BIRD, 107 câu giờ chạy được nhưng trả kết quả sai (Spider: 51 của 173). Tức là method sửa incorrect result cũng nhiều như sửa execution error; incorrect result không giảm vì execution error cũ chuyển sang. Câu cũ trong brief là của tôi, vượt C2 của `CLAIMS.md`; tôi đã sửa brief và đưa các số này cho writer. Bạn quyết định: giữ các số này trong 5.4 và ghi vào `CLAIMS.md`, hay bỏ. Section 7 ("hai loại round bỏ hai loại lỗi khác nhau") nên đọc lại theo bảng này | |
| A17 | Claim C3 (Section 5.4, đoạn hai) | Tôi đối chiếu C3 với test suite trên Spider dev (từ predictions và điểm TS đã commit; chi tiết ở `LAB_LOG.md`, 2026-11-26). Prediction đúng theo EX nhưng đọc table/column khác gold phần lớn bị test suite loại, ở mọi hàng: method 17 qua của 48, FedAvg SFT 14 của 49; nhóm đọc cùng table/column thì qua 711 của 755 và 689 của 728. Trên Spider dev gain theo TS của method (+25 câu) đến từ nhóm thứ nhất (+22), và nhóm thứ hai không lớn hơn với method (48 so với 49). Nhóm thứ hai chỉ lớn lên trên Spider test (103 so với 83) và BIRD dev (191 so với 136), hai set không có test suite. Vậy: (1) kết quả TS của 5.3 không đỡ được C3, câu nối tôi xin ở note 5 round 1 phải bỏ; (2) trên BIRD dev chưa biết bao nhiêu phần của nhóm thứ hai là đúng thật. Tính theo cặp câu hỏi, gain 95 câu trên BIRD gồm 60 câu ở nhóm thứ nhất và 35 câu ở nhóm thứ hai ("55 của 95" trong `CLAIMS.md` là thay đổi kích thước nhóm, khoảng 20 câu cả hai hàng đều đúng nhưng đổi nhóm). Đề xuất: không in C3 như một điểm mạnh cho tới khi có kiểm chứng trên BIRD dev; kiểm chứng rẻ nhất là đọc một mẫu của 52 câu chỉ method đúng thuộc nhóm thứ hai (database BIRD dev có trên Mac). Nếu phần lớn đúng thật, C3 quay lại kèm bằng chứng; nếu không, ta biết cỡ thật của gain trên BIRD (ít nhất 60 câu, 3.9 điểm, ở nhóm thứ nhất). Bạn quyết định: giữ C3 kèm số kiểm chứng của Spider dev, bỏ C3 khỏi paper, hay kiểm chứng trên BIRD trước | |
| A21 | SKT-SQL (JIIS 2025, `yi2025sktsql`) | Không đọc được bài: Springer chặn, các API không trả abstract; chỉ có abstract của một preprint khác tên. Tôi để paper này ngoài brief. JIIS hiện chỉ còn GradeSQL trong Section 2 (đọc bản arXiv) | Nếu bạn muốn cite thêm bài của JIIS, gửi tôi PDF của SKT-SQL, tôi thêm một hàng fact. KGRFL (IEEE, `xu2024kgrfl`) cũng chỉ đọc được abstract; brief giới hạn nó ở một mệnh đề | |
| A22 | Table 1, thêm hàng cho federated RL with verifiable rewards? | Cold read (major): Table 1 bỏ PubSwap và Fed-GRPO, hai work federated train trên output của chính model với reward kiểm chứng được (Fed-GRPO có code generation); câu novelty đúng vì cột cuối nói "pairs", loại RL ra theo định nghĩa. Text của 2.3 có nêu hai work này, bảng thì không. Hàng của Table 1 do bạn chốt trong `OUTLINE.md` nên tôi chưa cho writer thêm | Thêm một hàng "PubSwap, Fed-GRPO" (federated có, Text-to-SQL không) và đổi cột cuối thành "trains on the model's own outputs, renewed in training". Khi đó \method khác hai work này ở task và ở label từ execution trên database của client, đúng với `CLAIMS.md` rule 7. Ô "labels from execution" của hàng này: Fed-GRPO chỉ viết reward là "whether the extracted answer matches the ground truth or whether the code is right or not" (phần Training details của appendix; tôi đọc trong bản arXiv), không nói có chạy test hay không, nên ô đó là "answer check" kèm table note, không phải dấu tick. Cold read 2 (reader khác, độc lập) lặp lại điểm này ở mức major và thêm: bảng cũng bỏ Liu et al. (Text-to-SQL có, label từ execution có, pairs là output của chính model nhưng dựng một lần), nên chỉ \method có đủ mọi dấu tick. Tôi đề xuất thêm cả hai hàng: "Liu et al." với ô cuối "own outputs, fixed" và "PubSwap, Fed-GRPO"; khi đó cột cuối tách được ba mức (từ dataset, output của model dựng một lần, output của model dựng lại mỗi round) và bảng không còn đọc như dựng để \method thắng. Reader cũng muốn hai cột reference model và NLL term; tôi không đề xuất, bảng sẽ quá rộng và hai điểm đó Section 3.4 đã nói. Round 2 không đụng tới hàng của bảng; nếu bạn đồng ý, writer thêm hàng trong một lần sửa riêng theo quyết định của bạn | |
| A23 | Section 2.3, có cite work về aggregation của LoRA trong federated learning? | Cả hai cold read (minor) đều nêu: 2.3 viết "each client trains an adapter and the server averages the adapters" như chuyện đã xong, trong khi trung bình riêng A và B không bằng trung bình của tích BA, và có hẳn một nhánh nghiên cứu về việc này (reader nêu FedIT, FFA-LoRA, FLoRA). \method chỉ trao đổi LoRA adapter và Section 6 có hàng về trọng số của server average, nên reviewer về FL dễ hỏi | Thêm một câu ở 2.3 với hai citation (FFA-LoRA và FLoRA là hai ứng viên; tôi chưa đọc lại hai bài này, sẽ cho helper dựng fact row từ chính bài trước khi viết), nói ta dùng plain averaging như OpenFedLLM và FederatedScope-LLM. Reference list khi đó khoảng 41 đến 42 entry (hiện 38, Pang et al. quay lại ở round 2, Lanchantin et al. sẽ được cite ở Section 6). Bạn quyết định có thêm hay không | |
| A25 | Section 6, kiểm định trên execution error (tôi đã thêm, bạn có thể bỏ) | Cold read Section 6 (major): đoạn về preference term dựa trên số đếm execution error chưa được kiểm định. Tôi thêm vào generator đúng phép exact McNemar của Section 4.6, áp cho biến "prediction của câu hỏi kết thúc bằng execution error", hàng "Without the preference term" so với method ở 3 rounds: BIRD dev 36 câu chỉ lỗi ở method, 182 câu chỉ lỗi ở hàng kia, p = 1.1e-24; Spider test 41 và 95, p = 4.2e-6 (macro `\errpval`, `\errpadj`). Sau cold read 2 (reader chê chỉ test một chiều) tôi thêm test đối xứng trên incorrect result (`\wrpval`): BIRD dev 198 câu chỉ là incorrect result ở method, 80 câu chỉ ở hàng kia, p = 1.0e-12 (method có nhiều incorrect result hơn, significant); Spider test 89 và 69, p = 0.13. Bốn test này vào family "text" (15 lên 19); p hiệu chỉnh của so sánh gold SQL (B8) từ 0.058 thành 0.065; không giá trị hiệu chỉnh nào đổi phía so với 0.05. Section 4.6 chỉ nói test trên "paired predictions" nên Section 6 nói rõ trong một mệnh đề | Ba lựa chọn: (a) cả hai test, như hiện tại; (b) không test nào, chỉ in số đếm; (c) chỉ test execution error. Tôi khuyên (a): claim B4 ("the error counts carry the claim") có kiểm định trong khi chênh lệch EX của hàng này không significant, và hai loại prediction sai được xử lý như nhau (test một chiều thì reviewer bắt được, cold read 2 đã bắt). Nếu chọn (b), bỏ `ERR_TESTS` trong `tools/paper_numbers.py` và hai ngoặc đơn trong đoạn đó | 2026-11-27: giữ (a), cùng quyết định với A31 |
| A28 | Title | Ba ứng viên của writer: (1) "FedLS-SQL: Federated Fine-Tuning for Text-to-SQL with Execution Labels from the Clients' Databases"; (2) "FedLS-SQL: Federated Preference Optimization with Client-Side Execution Labels for Text-to-SQL"; (3) "FedLS-SQL: Learning from Query Execution on Client Databases in Federated Training of Text-to-SQL Models". `main.tex` vẫn để "title to be set" | Tôi khuyên (1): trọng tâm là execution labels từ database của client, phần kết quả ủng hộ chắc nhất. (2) đặt trọng tâm vào preference optimization, trong khi chênh EX của preference term so với chỉ NLL chưa significant (C29) | 2026-11-27: "FedLS" là tên tạm của bản cũ; tên method và title sẽ đổi sau, bạn đặt. Chưa làm gì: `main.tex` giữ "title to be set"; tên là một dòng `\method` trong `macros.tex` |
| A29 | "LS" trong FedLS-SQL là gì? | Text, abstract và title đều không giải thích; cả hai cold read của Section 1 đều hỏi | Bạn cho biết; tôi đưa vào Section 1 (một mệnh đề ở chỗ đặt tên method) | 2026-11-27: không cần giải thích "LS": tên sẽ đổi (xem A28) |
| A32 | `TERMS.md`, `OUTLINE.md` Section 3 | Giọng mới kể method theo component, không theo thứ tự thời gian của một lần train. Heading hiện tại: 3.1 Setting and notation, 3.2 Overview, 3.3 Warm-up rounds, 3.4 A preference round, 3.5 What a round costs a client. `TERMS.md` chỉ đặt tên cho round, chưa đặt tên cho component | Heading: 3.1 Problem Formulation; 3.2 Framework Overview; 3.3 Supervised Warm-Up; 3.4 Client-Side Execution Labeling (sampling và execution label); 3.5 On-Policy Preference Pair Construction; 3.6 Preference Optimization Objective (preference term, NLL term, reference model là global model của round); 3.7 Aggregation and Client Cost. Thêm vào `TERMS.md` bốn tên: client-side execution labeling, on-policy pair construction, preference objective (cả loss), execution-derived supervision (tín hiệu từ execution label); cho phép dạng ghép "client databases" thay "the databases of a client". Các tên cũ (warm-up round, preference round, execution label, preference pair, reference model) giữ nguyên | |

## B. Cần bạn đọc lại câu chữ

Đọc trong `sections/03_method.tex` hoặc `build/main.pdf` (bản sửa vòng
2). Sau hai vòng, phần còn lại do bạn sửa hoặc bảo tôi sửa chỗ nào là
cơ học.

| # | Ở đâu | Đọc để kiểm gì |
|---|---|---|
| B1 | Section 3.4, đoạn cuối (CodeLutra) | Câu "The contribution of FedLS-SQL is to bring this execution-based supervision into federated training, where only a client can compute it". Đây là chỗ Method nói paper nhận cái gì là của mình; kiểm xem có đúng ý bạn và có khớp contribution 1 trong `CLAIMS.md` không. "First" và "to our knowledge" để dành cho Section 1. Câu "The rest are settings" đã bỏ (bạn, 2026-11-26: trung thực quá mức cần thiết); xem mục D, điểm 9 |
| B2 | Section 3.4, đoạn cuối | Câu "the same λ then weighs the NLL term less against the preference term than in CodeLutra, by a factor of \|y+\|". Đúng về số học; người đọc thứ hai coi việc không nói là nói quá mức độ theo CodeLutra. λ không còn trong danh sách "We follow CodeLutra in" |
| B3 | Section 3.1, đoạn cuối | Cái gì ở lại client, giờ được gọi tên (samples, execution results, execution labels, preference pairs). Các từ này xuất hiện ở 3.1 trước khi 3.4 định nghĩa chúng. So với contribution 2 trong `CLAIMS.md` |
| B4 | Section 3.3, đoạn cuối | Câu mới về lý do warm-up: "which leaves fewer questions without a correct sample than the pretrained model does", và "Section 6 reports these counts" (mục A1) |
| B5 | Section 3.4, đoạn reference model và đoạn về câu hỏi không sinh pair | Hai đoạn cả hai người đọc phải đọc hai lần ở bản trước; đã viết lại ở vòng 2, chưa có người đọc lạnh nào đọc bản mới |
| B6 | Section 3.4 | Việc client gửi số pairs lên server giờ chỉ nói ở Section 3.1 ("one integer, its aggregation weight") và ở Algorithm 1, dòng 13; văn bản 3.4 chỉ nói trọng số là số pairs |
| B7 | Section 3.4 | "Empty sample" không còn được nhắc: nó là sample incorrect theo quy tắc chung. Chi tiết này có thể để ở Appendix B |
| B8 | Section 3.4 | "CodeLutra constructs ten" viết bằng chữ, không qua macro (là fact của paper được trích, không phải setting của ta) |
| B9 | Section 3.4, đoạn cuối, "where CodeLutra sums it" | Helper đọc lại CodeLutra (arXiv v3, bản TMLR): Eq. (3) viết log-likelihood của cả response; paper không nói gì về chuẩn hoá theo độ dài. "CodeLutra sums it" là cách ta đọc công thức, không phải điều CodeLutra viết, và code của họ có thể lấy trung bình theo token. Đề xuất đổi thành một câu bám vào công thức, kiểu "where CodeLutra's objective takes the log-likelihood of the whole query (its Eq. 3)", và kiểm code của CodeLutra nếu có công bố. Câu "by a factor of \|y+\|" (mục B2) phụ thuộc điểm này |
| B10 | Section 3.4, "constructed once, as in FedDPO" | OpenFedLLM viết "each client holds a preference dataset" và không mô tả bước nào sinh lại pairs; reference model "fixed throughout the FL process" thì được viết rõ. "Constructed once" là cách ta đọc; cited-work audit ở bước W11 sẽ xét câu này |
| B11 | Section 4.2, đoạn cuối | "A preference round constructs no pair for some of them: ..." Bản round 1 viết "in any round"; bỏ đi thì hai loại câu hỏi này đọc như là tất cả các câu hỏi không sinh pair, trong khi câu hỏi có sample toàn đúng hoặc toàn sai cũng không sinh pair ở round đó. Đề xuất: thêm lại "in any round" |
| B12 | Section 4.2, "Its parser cannot read most queries of BIRD train" | Code ghi tỉ lệ cho BIRD dev (85%); database của BIRD train không có trên Mac nên tỉ lệ trên BIRD train chưa đo. Đếm query có cú pháp ngoài grammar của Spider (backtick, CAST, CASE, IIF...) được 2,319 của 9,428, chỉ là cận dưới. Đề xuất: viết "many queries of BIRD", hoặc đo trên server (script CPU, không đụng GPU queue) |
| B13 | Section 4.2, setup IID | "assigns each client the same number of databases", còn Table 2 in 29 đến 30 (146 database, 5 client). Đề xuất: "an equal share" hoặc để nguyên |
| B14 | Section 4.5, vai trò của seed | Câu nói seed quyết định thứ tự training example và sampling; seed còn quyết định khởi tạo adapter và việc ghép pair. Table B1 đã có đủ bốn thứ. Đề xuất: cắt mệnh đề này (writer cũng đề nghị cắt cho độ dài) |
| B15 | Section 5.4, đoạn về hai nhóm prediction đúng (C3) | Bản round 2 chỉ còn: tiêu chí, bốn cặp số đếm, câu "The counts are taken for each method separately..." (writer thêm, để reader không tự trừ ra 55 của 95), và câu "EX establishes correctness on the evaluation database only". Đoạn kết ở một giới hạn của bằng chứng, không có gì đỡ. Số phận của đoạn theo quyết định ở A17 |
| B16 | Section 5.4, đoạn đầu | Trên BIRD dev execution errors tăng ở preference round thứ hai (102 lên 128); text nêu số, không nói vì sao. Bảng chuyển outcome round 3 sang round 4 có (723 incorrect result: 56 thành đúng, 54 thành execution error) nhưng chưa là macro. Muốn in thì tôi thêm macro |
| B17 | Section 5.1, đoạn cuối | "a fifth round, which we train on Spider only and use in Section 5.4": round 5 của FedAvg SFT được giới thiệu ở Results; Section 4.4 nói mọi hàng federated có T = 4. Đề xuất: khi Section 4 sửa lần cuối, thêm một mệnh đề ở 4.4 và bỏ mệnh đề ở 5.1 |
| B18 | Tên "FL4SP" | Paper của Zhang et al. không tự gọi là FL4SP (từ này không xuất hiện trong paper); đó là tên trong notes, `CLAIMS.md` và `OUTLINE.md`. Brief Section 2 yêu cầu viết "Zhang et al." và gọi re-weighting của họ là Lorar | Giữ như brief; Section 1 cũng viết "Zhang et al." | |
| B19 | `CLAIMS.md`, wording rule 7: "federated DPO for human preferences (OpenFedLLM)" | Đúng với HH-RLHF. Với UltraFeedback paper chỉ nói "the response with the highest score" trong bốn response của các LLM, không nói ai chấm. Brief viết "preference datasets for helpfulness and harmlessness" | Giữ như brief; Section 1 dùng cùng cách nói | |
| B20 | Table 1, ô "pairs constructed anew" của FedDPO | Brief ghi "no: each client holds its preference dataset". OpenFedLLM không viết câu nào nói pairs không được dựng lại; paper chỉ không mô tả bước sinh hay gán nhãn lại trong các round. Cùng gốc với B10 | Giữ "no" kèm lý do trong ô hoặc table note | |
| B21 | Section 2.4, câu "To our knowledge" (đoạn cuối) | Revision 2 viết: "no earlier method combines federated training with execution labels and renewed pairs of the model's own outputs". Câu bạn duyệt trong brief là "no earlier method does so [trains a Text-to-SQL model with federated learning] with ...". Bản mới bỏ giới hạn Text-to-SQL, tức rộng hơn scope của `CLAIMS.md` rule 7 ("its scope is federated training for Text-to-SQL"). Writer đổi vì cả hai cold read chê câu cũ đúng theo định nghĩa (work federated Text-to-SQL duy nhất trước đó dùng SFT). Theo các fact row, câu rộng vẫn đúng với những work đã đọc (FedDPO: pairs từ dataset; Wu et al.: pairs sinh một lần ở server; PubSwap, Fed-GRPO: reward, không có pairs), nhưng phạm vi tìm của ta là federated fine-tuning của LLM, không phải mọi federated work về code | Hai round đã hết nên tôi không sửa. Bạn chọn: (a) giữ câu rộng và nới rule 7; (b) trả lại scope "for Text-to-SQL" (an toàn, đúng rule 7). Tôi nghiêng về (b) nếu chưa search thêm federated code generation | |
| B22 | Section 2.2, đoạn CodeLutra: "the scale of the DPO term" và "the uniform pairing" | "the scale of the DPO term" chỉ beta; Section 3.4 gọi beta là "the strength of the constraint toward the reference model", nên hai chỗ nói khác nhau về cùng một setting. "the uniform pairing" chỉ được giải thích ở Section 3.4. Đoạn này tả method khoảng 60 từ trước Section 3 và dùng "global model", "warm-up rounds of FedAvg SFT", "NLL term" (doubt 1 của writer) | Đọc lại khi Section 1 xong; nếu Section 1 không giới thiệu các từ này thì đoạn cần gọn lại | |
| B23 | Section 2.2, "Section 6 varies all three of these choices" | Dựa vào mô tả hàng ablation trong `OUTLINE.md` (B1 giữ pairs và reference của preference round đầu; B3 bỏ NLL term). Section 6 chưa viết | Section 6 đã viết: pairs và reference được giữ cố định cùng nhau (một hàng), DPO loss alone là hàng riêng. Cold read 2 thấy "varies all three" lệch với điều đó. Đề xuất sửa ở lượt đọc toàn bài (W14) thành "varies these choices"; Section 2 đã hết hai round nên tôi không sửa câu | |
| B24 | Table 8, hai thay đổi trong generator (theo góp ý của writer Section 6) | (1) Tiêu đề block chỉ còn "4 rounds" và "3 rounds": tiêu đề cũ "2 warm-up rounds, 2 preference rounds" sai với hai hàng về warm-up (0 và 3 warm-up rounds). (2) Thêm hàng đầu "FedAvg SFT, 2 rounds" (BIRD 42.70, Spider 74.10; chỉ EX, không test): model mà mọi hàng xuất phát, để đọc được "without the NLL term" 73.59 nằm dưới điểm xuất phát 74.10 ngay trong bảng | Giữ. Nếu bạn muốn bảng như `CLAIMS.md` ghi ban đầu thì bỏ hàng này, text vẫn mang số | |
| B25 | Section 6, số câu hỏi không có sample đúng trên Spider | Cold read cộng các số của Sections 4 đến 6 và thấy thừa 16 trên Spider: số `questions_all_wrong` của round record gồm cả câu hỏi trên database không có row (58, 16 và 13 câu với 0, 2, 3 warm-up rounds), mà các câu đó đã được đếm riêng (1,759). Generator giờ bỏ chúng: 1,016, 557, 470 (trước: 1,074, 573, 483); BIRD không đổi (4,035 và 2,698). Sau khi sửa, Spider cộng đúng 8,659: 4,013 có pair, 2,327 chỉ có sample đúng, 557 không có sample đúng, 1,759 trên database không có row, 3 gold SQL lỗi. `LAB_LOG.md` các entry cũ giữ số thô | Đọc lại câu này trong Section 6 (mẫu số là 6,900 câu trên database có row) | |
| B26 | Section 6, giới hạn độ dài | Brief bạn duyệt: 790 từ, tối đa 880. Tôi nâng tối đa lên 930 ở round 1: B8 (gold SQL làm correct side) được thêm sau khi con số 880 của `OUTLINE.md` được đặt, và note round 1 yêu cầu thêm số mà reader hỏi (EX của hàng "Without the preference term", p hiệu chỉnh, độ lệch trọng số). Ở Section 2 giới hạn cứng đã làm writer cắt mất một statement | Chấp nhận 930, hoặc nói tôi cắt lại khi tính tổng số trang | |
| B27 | Section 6, đoạn về preference term | Sau round 2 đoạn mở bằng điều hàng này xác lập ("fewer predictions end in an execution error; a difference in EX is not established on either dataset"), nêu chênh EX với method kèm p hiệu chỉnh, rồi hai test trên execution error và incorrect result. Đoạn không còn nói bằng lời rằng hàng NLL-only vẫn cao hơn model trước round (44.39 so với 42.70; 75.87 so với 74.10): reader phải đọc ở hàng đầu của Table 8. Cold read 1 muốn thấy điều đó, cold read 2 chê cách nói "lies between" là xếp hạng không có test | Đọc lại đoạn này; nếu muốn nêu, thêm một mệnh đề với hai giá trị, không dùng "between" | |
| B28 | Section 6, câu đầu đoạn warm-up: "what differs is test-suite accuracy and the number of training questions without a correct sample" | Dựa trên so giá trị của Table 6 (biến thể không warm-up thấp hơn FedAvg SFT về TS trên cả ba set, không có test) và một test significant trong ba (Spider-Syn); hai câu sau nêu rõ căn cứ. Nằm trong ceiling của B5 | Đọc lại; đây là câu kết luận về warm-up mà cold read 2 đòi | |
| B29 | Câu về cost: "a preference round takes more client compute than an SFT round" | Sai với một round: preference round thứ hai trên Spider tốn 0.9 lần một SFT round (`\fact{cost.spider.pref2.ratio}`; BIRD 2.7 và 2.3, Spider 1.6 và 0.9). Writer của Section 7 phát hiện khi viết outline. Câu này nằm trong hai brief bạn duyệt (Section 1 statement 7, Section 7 limitation 4) và trong `CLAIMS.md` section 5 mục 4 ("More client compute per round"). Điều đúng: method không thêm communication, cost thêm là computation ở client; tính cả bốn round thì method tốn client time hơn FedAvg SFT trên cả hai dataset (BIRD 1,207 so với 692 phút; Spider 560 so với 496). Section 5.4 đã nói đúng như vậy | Tôi đã sửa hai brief theo cách nói của Section 5.4. `CLAIMS.md` section 5 mục 4 nên đổi thành "More client compute over the rounds (E2)"; tôi chưa sửa vì đó là file claim bạn duyệt | 2026-11-27: "CLAIM không phải chân lý, có thể sửa nếu nó không đúng". Đã sửa `CLAIMS.md` section 5 mục 4 thành "More client compute over the rounds", kèm ghi chú preference round thứ hai trên Spider là 0.9 lần |
| B30 | Section 1, danh sách contribution | Writer gộp lại để lấy chỗ: (1) quan sát kèm method, (2) kết quả kèm phân tích và cost, (3) ablation, (4) release. `CLAIMS.md` section 2 để method là contribution riêng. Contribution 1 đúng phạm vi brief ("supervision that federated fine-tuning leaves unused", "to our knowledge the first method for the federated training of Text-to-SQL models"); câu "to our knowledge" chỉ còn ở đây, không còn ở cuối đoạn gap. Hai cold read đều chê bản trước ("we identify ...") là nhận ý tưởng execution feedback về mình | Đọc lại; nếu muốn method là contribution riêng thì cần khoảng 25 từ | |
| B31 | Section 1, đoạn 7: hai kết quả ablation | "holding the pairs and the reference model fixed lowers EX on BIRD dev" (Spider test thì level, không nói ở đây) và "without the NLL term, a preference round brings no gain on Spider test" (hàng BIRD chưa commit). Mỗi câu đúng trên set nó nêu; Section 6 có cả hai set. NLL term có kết quả nhưng không có lý do của Section 3.4 (hết chỗ) | Đọc lại; nếu thấy chọn lọc thì thêm "on Spider test the two are level" (khoảng 8 từ) | |
| B32 | Section 1, đoạn 2: "for example a hospital or a bank" | Ví dụ của writer, trả lời cold read 1 (tiền đề chỉ được khẳng định). Không dựa trên nguồn nào | Giữ, đổi, hoặc bỏ | |
| B34 | Section 7.2 thiếu bốn ý của limitation trong `CLAIMS.md` section 5 | Writer bỏ vì giới hạn 780 từ: (1) cost là limitation (mục 4): Section 7 không còn câu nào, Section 8 giữ một mệnh đề "at the cost of additional computation at the clients", số ở Section 1 và 5.4; (2) seed thứ hai trên BIRD (mục 6): Section 4.5 đã hứa, Table 3 sẽ mang; (3) số pair của client phụ thuộc performance của model trên data của nó (C41): chỉ còn "a client's number of pairs" trong câu về privacy; (4) câu hỏi trên database không có row không sinh pair: Section 3.4 và 4.2 đã nêu kèm số | Chấp nhận, hoặc cho Section 7 thêm khoảng 40 từ cho (1) và (3). Paper đang 29 trang so với giới hạn 25 nên tôi khuyên chấp nhận | 2026-11-27: "nếu cần, tốt cho bài thì để, vì đây là bản draft, cần đầy đủ, và sẽ chắt lọc tiếp sau". Đã thêm lại (1), (3), (4); Section 7 nay 894 từ (giới hạn nâng lên 900). (2) seed thứ hai chưa thêm vì hàng của nó ở Table 3 còn trống. Khi chắt lọc, writer đề xuất cắt trước: số pair Spider của preference round thứ hai, câu về trọng số, khoảng cost (Section 5.4 đã in) |
| B35 | Abstract: "about half as many of its predictions end in an execution error" | Section 1, 5.4, 7.1 và 8 đều đi kèm ý "incorrect result không giảm"; Section 8 còn nói một phần query nay chạy được lại trả kết quả sai. Abstract chỉ nêu nửa có lợi. Câu của abstract đúng với số (268 và 128, 173 và 84). Writer của Sections 7, 8 đề nghị abstract mang cùng mệnh đề | Abstract 241 từ, tối đa 250: đủ chỗ cho khoảng 9 từ. Bạn quyết định; nếu thêm thì writer của Section 1 sửa một câu | 2026-11-27: bạn hỏi thêm vào có tốt hơn cho paper không. Tôi trả lời: không, giữ nguyên. Câu của abstract đúng và nay có kiểm định (A31); chênh lệch incorrect result không significant sau hiệu chỉnh trên cả hai set nên abstract không bỏ sót một kết quả; ý "không giảm" đã có ở Section 1, 5.4, 7.1 và 8. Abstract không đổi trừ khi bạn nói khác |
| B36 | Section 7.1, đoạn 2: "Nor does it rest on the preference term alone ... a difference in EX to the round with both terms is not established" | Đây là C29 viết thẳng trong paper: round chỉ có NLL term trên sample đúng cũng cao hơn model trước nó, và chênh EX với round có cả hai term chưa significant sau hiệu chỉnh. Section 8 mô tả loss có hai term, không nói cả hai đều cần | Đọc lại khi hai hàng 4 rounds của biến thể này về (đang chờ GPU); câu có thể đổi theo kết quả | |
| B37 | Sections 2.2, 3.4, 4.5: credit cho CodeLutra (bạn, 2026-11-27: "không tự nhận nhiều hơn mức cần") | Tôi (main session, không qua writer) đã viết lại hai đoạn và một câu. 2.2: bỏ câu "takes from CodeLutra its sampling settings..." và mệnh đề về số pair, NLL; còn lại CodeLutra làm gì và training ở ta chạy qua các client. 3.4: bỏ "The contribution of FedLS-SQL is to bring this ... into federated training" và "We follow CodeLutra in ..."; bỏ câu về hệ số λ so với CodeLutra. 4.5: một câu duy nhất nêu các setting theo CodeLutra (số sample, temperature, β, learning rate, pairs per update, epoch, weight decay). λ không nằm trong danh sách vì NLL term ở ta lấy trung bình theo token. Bạn đọc ba chỗ này. Nếu muốn λ cũng ghi "theo CodeLutra" thì thêm lại một mệnh đề ở 4.5 |
| B38 | Ba review ngoài của cả bản thảo (`cold_reviews/2026-11-27_0703_fit_novelty_1.md`, `_2.md`, `2026-11-27_0706_fit_novelty_codex_1.md`) | Cả ba: đủ cho CMC, JIIS sát ngưỡng. Việc còn mở từ review, chưa làm: trích ExeSQL ở 2.2 (`zhang2025exesql` đã có trong `references.bib`); một câu ở 2.3 về federated GRPO; FedAvg SFT vòng 5 đến 7 trên BIRD cho so sánh cùng client time (chưa queue); viết lại 5.4, 6, 7.1 cho bớt số trong câu văn sau khi các ô về. Chờ bạn quyết từng việc |
| B39 | Bản thảo chuyển sang template CMC (bạn, 2026-11-27) | `main.tex` là wrapper CMC (class của Tech Science Press trong `Definitions/`), wrapper Springer thành `main_jiis.tex`. Build: 28 trang (phí gồm 15 trang, vượt 13). Tôi (main session) sửa hai chỗ trong phần thân vì layout: Appendix B tách thành hai bảng (Table A1: model, federation, FedAvg SFT round; Table A2: preference round, evaluation, software), câu dẫn và hai caption viết lại theo đó; Figure A1 dùng chữ 7 pt và nhãn panel theo journal. Chờ bạn: title, khối tác giả, bốn statement (funding, author contributions, availability of data and materials, conflicts of interest) trong `sections/90_statements_cmc.tex`; caption của Fig. 1 phải ghi tên và version của AI tool nếu hình được làm bằng AI tool (quy định của CMC, `WRITING_PLAN.md` section 11 mục 2) |
| B40 | FedLS-SQL được gọi là framework, bản nhẹ (bạn, 2026-11-27) | Tôi (main session, không qua writer) sửa 5 chỗ: abstract ("We propose FedLS-SQL, a federated learning framework for Text-to-SQL that uses this signal"), Section 1 đoạn "We propose", danh sách contribution, Section 3.2 ("illustrates the framework"), câu đầu Section 8. Danh sách contribution trở lại bốn mục như brief (B30 từng gộp để lấy chỗ theo giới hạn trang của JIIS): (1) nguồn supervision bị bỏ, (2) framework, kèm "to our knowledge ... the first method for the federated training of Text-to-SQL models that uses this supervision" (phạm vi không đổi), (3) kết quả, phân tích, cost và ablation, (4) release. Method, cấu hình mặc định và các bảng không đổi; ngoài 5 chỗ đó bài vẫn viết "the method". `TERMS.md`, `CLAIMS.md` section 2 và brief Section 1 ghi theo. Title vẫn "title to be set"; ba phương án để bạn chọn: (a) "FedLS-SQL: A Federated Learning Framework for Text-to-SQL with Execution-Labeled Preference Optimization"; (b) "FedLS-SQL: Federated Fine-Tuning of Text-to-SQL Models with Execution Feedback from Client Databases"; (c) "A Federated Learning Framework for Text-to-SQL That Learns from Execution on Client Databases" |
| B41 | Ba referee report cho bản CMC (`cold_reviews/2026-11-27_1009_cmc_full_1.md`, `_2.md`, `_codex_1.md`) | Cả ba: reject vì bản thảo chưa hoàn chỉnh. Điểm mới: optimizer của preference round khác SFT round và bài chưa có hàng control. Đã sửa theo review: Section 4.2 thêm số câu hỏi BIRD có gold SQL quá time limit (87 và 92); references in DOI và arXiv id. Chờ bạn: queue hai hàng control (FedAvg SFT rounds 3 và 4 với settings của preference round; FedAvg SFT rounds 5 đến 7 trên BIRD); related work thêm self-training (STaR, RFT, ReST), ExeSQL, FedPDPO; viết lại 5.4, 6, 7.1; hàng FedDPO có ghi rõ là dùng pairs của round đầu hay không; có thêm số BIRD dev của các small model đã công bố để đặt 48.76 vào bối cảnh hay không |

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
| C10 | (Cold read Section 4, major) Không có validation split: T, T_w, learning rate được chọn trên dữ liệu nào, và baseline có được tune kỹ như method không? | Cả hai người đọc lạnh của Section 4 đều nêu là major. Paper không kể cách chọn setting (rule của bạn, 2026-11-17), nhưng nêu nguồn thì được: sau round 2, Section 4.5 nói learning rate của SFT và 3 epoch của centralized và local SFT là của recipe LoRA mà SPFT-SQL báo cho model này (appendix A.4: lr 2e-4, 3 epoch, đã kiểm trong paper), còn learning rate, 16 pairs mỗi update, 1 epoch và weight decay của preference round là của CodeLutra (Table 4, đã kiểm). T = 4 và T_w = 2 vẫn không có nguồn; người đọc thứ hai hỏi thêm FedAvg SFT có được thử learning rate thấp hơn ở round 3 và 4 không |
| C11 | FedDPO: round thứ hai train lại trên cùng pairs với cùng reference; baseline có thể yếu vì lịch train chứ không vì thiếu on-policy | Đó là FedDPO như đã công bố (dataset và reference cố định). Hàng "Fixed pairs and reference" của Table 8 (giữ NLL): BIRD thấp hơn 2.61, Spider ngang. Hàng FedDPO chưa chạy |
| C12 | Local SFT và centralized SFT train 3 epochs, FedAvg SFT 4 rounds mỗi round 1 epoch: ngân sách train khác nhau | Chưa trả lời. Section 4.4 nêu số epoch, không nêu lý do |
| C13 | 87 và 92 gold SQL của BIRD train quá time limit ở hai preference round: label phụ thuộc thời gian chạy của máy. 350 gold SQL của BIRD train lỗi khi chạy, không có lời giải thích | Chưa trả lời. Các con số in ở Section 4.1; nguyên nhân của 350 lỗi chưa được phân loại |
| C14 | Setup IID vẫn lệch: tỉ lệ câu hỏi hard 34 đến 52% (alpha 0.5: 22 đến 56%), cỡ client 1,298 đến 2,028; ba setup trên Spider có thể khác nhau ít hơn tên gọi | Section 4.2 (sau round 1) nói IID vẫn khác nhau về cỡ vì database khác cỡ; Table 2 in các khoảng |
| C15 | Mỗi setup chỉ là một lần rút partition (split seed 42); độ biến thiên theo partition không được xét | Chưa trả lời; nếu nêu thì ở Section 7 cùng limitation một seed (C9) |
| C16 | Bảng in p chưa hiệu chỉnh nhưng dấu sao theo p đã hiệu chỉnh: người đọc không kiểm được dấu sao từ bảng | Supplementary liệt kê mọi test với p đã hiệu chỉnh (`WRITING_PLAN.md`, mục 5) |
| C17 | Table 7 cho thấy bốn round của method tốn client time gấp khoảng 1.75 lần bốn round FedAvg SFT trên BIRD (1,207 so với 692 phút); FedAvg SFT thêm round thì sao? | Section 5.1 (A2): FedAvg SFT không tăng sau round 3; Section 5.4: so sánh trực tiếp trên Spider. Trên BIRD chưa có round 5 trở đi (mục A15) |
| C18 | Model 0.5B: margin nhỏ hơn (+2.10 so với +3.49); vì sao? | Paper không nêu lý do. Notes có số: FedAvg SFT của model này còn tăng ở round 4 (62.69 lên 64.09, p 0.0059), nên mức FedAvg SFT đạt tới chưa đo. Brief cũ cho phép một conjecture; tôi bỏ vì paper không in số nào đỡ nó, và in số round 3 thì mở ra câu hỏi về các round sau |
| C19 | Table 6, Spider-DK: method không warm-up (67.10) cao hơn method (63.55), chênh 3.55, p chưa hiệu chỉnh 0.032, không significant sau Holm | Bảng in ô này. Section 5.3 viết "no difference in EX is significant after the correction" và trỏ sang Section 6; brief cũ viết "EX is level with" là sai ở Spider-DK, đã sửa |
| C20 | (Cold read Section 5, major) Trên BIRD 55 của 95 câu gain đọc table hoặc column khác gold; BIRD so kết quả theo set of rows và không có test suite, nên có thể là trùng kết quả ngẫu nhiên. Table 6 cho thấy preference round có thể tăng EX mà không tăng TS (hàng không warm-up) | Spider: Section 5.3, gain theo TS gần bằng gain theo EX; trên Spider dev số prediction đúng EX nhưng sai TS là 74 với FedAvg SFT và 75 với method (tính từ Table 6). BIRD: chưa có kiểm chứng. Có thể làm: đọc tay một mẫu của nhóm thứ hai trên BIRD, hoặc trên Spider dev đếm nhóm thứ hai có bao nhiêu câu qua TS |
| C21 | (Cold read Section 5, major) T = 4 được chọn thế nào; method không được chạy quá round 4 dù hai đường còn tăng; FedAvg SFT có round 5 chỉ trên Spider | Chưa trả lời (cùng C10). Text giờ nói round 5 ở đâu ra |
| C22 | Số câu hỏi mà cả mười sample đều đúng trên BIRD nhảy từ 416 lên 3,016 sau một preference round: sample ở temperature 1 có mất đa dạng không? | Chưa trả lời; có thể đo số sample khác nhau trên mỗi câu hỏi ở hai round từ file samples |
| C23 | Client time là tổng năm client chạy lần lượt; wall-clock của một round federated là client chậm nhất | Caption Table 7 nói rõ là tổng. Chưa in thời gian theo client |
| C24 | Hàng của model chính in ba lần (Tables 3, 4, 5); với giới hạn 25 trang đây là chỗ tiết kiệm rõ nhất | Do thiết kế bảng (brief: hai hàng đầu của Table 5 là hàng chính). Bạn quyết định khi tính số trang cuối |
| C25 | (Cold read 2 Section 5, major) Preference round dùng learning rate 5e-5, SFT round dùng 2e-4, và FedAvg SFT giảm sau round 3: FedAvg SFT round 3 và 4 ở learning rate thấp có lấy lại một phần gap không? Control tự nhiên là SFT trên các sample đúng của chính client, nhưng nó nằm ở Section 6, không ở Table 3 | Section 6: hàng train trên correct samples không có preference term (cùng settings của preference round, kể cả learning rate) trả lời cả hai; hàng này chờ GPU (Table 8, `rft`). Chưa có hàng FedAvg SFT ở learning rate 5e-5. Reader thứ hai cũng xin vòng sample, label, DPO trên dữ liệu gộp làm cận trên (hàng `pooled` của Table 8, Spider) |
| C26 | (Cold read Section 2, major) Sao dùng DPO pairs mà không dùng federated GRPO cho Text-to-SQL? Section 2.1 nêu RL với execution reward cho Text-to-SQL, 2.3 nêu federated RL với verifiable reward; ghép lại là lựa chọn hiển nhiên | Paper không có hàng nào chạy federated GRPO. Chưa có câu trả lời bằng số; nếu có lý do về chi phí (số rollout, bộ nhớ 24 GB) thì đặt ở Section 3.5 hoặc 7. Cần bạn quyết có nói hay không. Cold read 2 lặp lại (major) và hỏi thêm vì sao Fed-GRPO với execution reward không phải là baseline |
| C27 | (Cold read Section 2, major) Client giữ database, gold SQL và model nên tự chạy được vòng lặp của CodeLutra; federated thêm gì? | Paper có Local SFT (Table 3) và hàng pooled clients (Table 8, chờ GPU); không có hàng "preference rounds chạy riêng ở từng client". Editor's note 2 chỉ yêu cầu Section 2 nói Section 3.4 nêu chỗ khác với CodeLutra. Cold read 2 lặp lại (major): sau 2.2 reader vẫn đọc method là "CodeLutra chạy trong FedAvg" và không thấy section nêu vấn đề nào nảy sinh khi federate CodeLutra. Round 2 chỉ sửa được chỗ pointer nói sai (liệt kê "renews the pairs" như điểm khác trong khi CodeLutra cũng làm vậy); phần còn lại là câu hỏi về contribution, trả lời ở Section 1 và 3.4 |
| C28 | (Cold read Section 2, minor) Vì sao nhiều tổ chức muốn train chung một model khi mỗi bên tự fine-tune được open model? | Việc của Section 1; ghi ở phần E. Cold read 2 lặp lại: một tổ chức tự chạy được open model nên "training at one site" chưa phải là giới hạn; cần nói một tổ chức thiếu gì mà federation cho (ví dụ in-domain examples) |
| C29 | (Cold read Section 6, major) Preference term thêm gì về EX? | Hàng "Without the preference term" (NLL term trên sample đúng của mỗi pair, không có DPO term) sau một round đạt 44.39 trên BIRD dev và 75.87 trên Spider test: từ model trước round (42.70, 74.10) nó lấy được +1.69 trong +3.52 của method trên BIRD và +1.77 trong +3.36 trên Spider. Chênh với method là -1.83 (p 0.057) và -1.59 (p 0.015), không significant sau hiệu chỉnh. Điều có kiểm định là execution error (A25). Text giờ nêu ba giá trị EX trước rồi mới đến số đếm. Hai hàng 4 rounds của biến thể này đang chờ GPU; khi về cần đọc lại claim B4. Cold read 2 (major) nói thẳng: "what the preference term demonstrably adds is executable SQL, not more correct SQL". Tôi tính bảng chuyển outcome từ predictions đã commit (hàng này sang method, 3 rounds): trên BIRD dev, trong các câu lỗi execution ở hàng NLL-only, ở method 123 câu thành incorrect result và 59 câu thành đúng; ngược lại 75 câu đúng ở hàng kia thành incorrect result ở method. Reader cũng hỏi hàng NLL-only chạy ở learning rate của preference round (5e-5), có thể under-trained. Đây là điểm yếu nhất của Section 6 trước reviewer; paper hiện trả lời bằng Section 5.4 (execution error giảm một nửa, incorrect result không giảm) và Section 7 |
| C30 | (Cold read Section 6, major) Hàng "Fixed pairs and reference" đổi pairs và reference cùng lúc; bằng chứng cho renewal chỉ có BIRD, một seed | Đúng: hàng này không tách được hai thứ, và trên Spider preference round thứ hai của chính method chỉ thêm +0.74 (p 0.093) nên "level" ở đó không nói gì. Text giờ nói rõ hai thứ được giữ cùng nhau (như FedDPO và Liu et al.). Tách hai thứ cần một hàng mới (pairs dựng lại, reference cố định): một preference round trên BIRD, khoảng 8 giờ GPU (ước lượng từ 470 phút của Table 7). Tôi không đề xuất chạy trừ khi reviewer hỏi |
| C31 | (Cold read Section 6, minor) Gold SQL làm correct side (B8) chỉ chạy với $T_w$ = 0; không nói gì về method như đề xuất, nơi 2,698 câu hỏi BIRD vẫn không có sample đúng sau warm-up | Đúng; text nói rõ là biến thể không có warm-up. Chạy cùng thí nghiệm sau warm-up là một preference round trên BIRD (khoảng 8 giờ GPU, ước lượng). Không đề xuất chạy lúc này |
| C32 | (Cold read Section 6, minor) Không có ablation theo $M$, $N$, $\beta$, $\lambda$; Section 2.2 nêu ba chỗ khác CodeLutra (warm-up, ít pair hơn, NLL trung bình theo token) nhưng chỉ warm-up được ablate | Cùng A5 (đã quyết: chỉ nêu lý do chi phí cho $M$). Reader thứ ba hỏi điều này |
| C33 | (Cold read Section 6) Hai chỗ của Section 4 mà reader không tự dựng lại được | (1) Section 4.6 nói các so sánh chỉ nêu trong text "form a family of their own" nhưng không nói family đó gồm gì (17 so sánh của Sections 5 và 6). (2) Trên BIRD, 9,428 - 5,877 - 416 - 2,698 - 350 còn 87 câu: đó là 87 gold SQL quá time limit ở preference round đầu (92 ở round hai; macro `\fact{train.bird.gold_timeout.pref1}`), Section 4.1 chỉ nêu 350 gold SQL lỗi. Section 4 đã hết hai round sửa; tôi đề xuất thêm hai mệnh đề này ở lượt đọc toàn bài (W14) |
| C35 | (Cold read 2 Section 6) Cùng một chênh lệch -2.61 xuất hiện ở hai so sánh: hàng "Fixed pairs and reference" trên BIRD dev (48.76 - 46.15) và gold SQL làm correct side (41.85 - 39.24), đều là 40 câu trong 1,534; reader nghi chép nhầm | Cả hai đúng (đã đối chiếu với `generated/numbers.md`). Text chỉ in 2.61 một lần (đoạn gold SQL); số kia nằm trong Table 8 |
| C36 | (Cold read 2 Section 6) Hàng "Clients pooled" không chỉ bỏ federation: train gộp còn đổi thành phần batch và số optimizer step | Hàng đang chờ GPU; khi về, câu của nó nói rõ cái gì giữ nguyên (số epoch, batch, learning rate) |
| C34 | (Cold read Section 6) Tên biến thể không có warm-up khác nhau ở ba chỗ: "\method, no warm-up" (Table 6), "No warm-up round" (Table 8), "no warm-up rounds" (text) | Nhãn bảng nằm trong generator; thống nhất ở lượt đọc toàn bài (W14) |
| C37 | Limitation 8 của `CLAIMS.md` nêu nguyên nhân: gain nhỏ hơn "where FedAvg SFT is still improving fast (the 0.5B model)" | Paper không in hàng nào theo round cho model 0.5B: generator chỉ có hàng 4 rounds trên Spider test, và Section 5.2 không nói nguyên nhân. Số theo round của model này chỉ có trong notes, trên Spider dev (`LAB_LOG.md`, 2026-11-23). Section 7 vì vậy chỉ nêu hai điều paper có: số warm-up rounds giữ là 2 cho mọi model, và gain với model 0.5B nhỏ hơn (Table 4). Nếu bạn muốn nêu nguyên nhân thì cần một macro từ evaluation theo round của FedAvg SFT với model đó trên Spider test (chưa có trong generator) |
| C38 | Section 7, reading "preference round đổi gì là theo loại sample sai trong pairs của nó": hàng "Fixed pairs and reference" có ủng hộ không? | Trên BIRD dev có, theo số đếm: round thứ hai train lại trên pairs của round đầu (56% pair có sample sai là execution error) kết thúc ở 91 execution error và 735 incorrect result, so với 102 và 723 sau một preference round; với pairs dựng lại (25% là execution error) là 128 và 658. Tức là pairs cũ tiếp tục giảm execution error, pairs mới giảm incorrect result. Trên Spider test hàng này không cho thấy điều đó (97 và 375 so với 84 và 384). Đây là so giá trị, không có test, và hàng này còn giữ cả reference model. Tôi cho writer dùng các số BIRD với "consistent with" và yêu cầu không bỏ qua Spider |
| C39 | (Cold read Section 1, hai lần; cold read Sections 7 và 8) Chạy SQL do model sinh trên database nội bộ của client: load, câu lệnh ghi, query chạy lâu | Code mở mọi database ở chế độ read-only (`mode=ro`, `PRAGMA query_only=ON` trong `fedls_sql/eval/sql_exec.py`) và dùng time limit của evaluation (30 s BIRD, 60 s Spider). Paper chưa nói read-only ở đâu; tôi đưa fact này vào brief Section 7 (limitation 1) cho round 2. Load trên database đang dùng thì ngoài phạm vi |
| C40 | (Cold read Section 1) Mức EX so với dòng RL: 48.76 trên BIRD dev với model 1.5B, trong khi reader nhớ SLM-SQL báo cáo mức 60 ở cùng cỡ; setup gốc có yếu không? Vì sao dùng preference pairs mà không dùng reward (cùng C26) | Paper không so mức với các hệ thống một site (chủ trương: cho thấy effect so với baseline cùng setup). Section 2.1 nêu dòng RL; Section 1 giờ ghi nhận nó. Chưa có câu nào nói vì sao chọn DPO |
| C41 | (Cold read Section 1 và Sections 7, 8) Trọng số theo số pair: client mà model sai hết hoặc đúng hết thì ít pair, tức là client khó nhất bị giảm trọng số; số pair còn tiết lộ model làm tốt đến đâu trên data của client | Section 6 so ba cách tính trọng số sau một preference round, không khác biệt significant. Section 7.2 giờ nêu số pair phụ thuộc vào performance của model trên data của client. Nếu muốn, method có thể gửi số câu hỏi thay cho số pair; đó là thay đổi method, bạn quyết |
| C42 | (Cold read Section 1) "Cùng số round" là cân communication, không cân compute; có baseline cùng client compute không? | Spider: round thứ năm của FedAvg SFT (Section 5.4), 5 round của nó tốn hơn 4 round của method và method vẫn cao hơn 4.28 điểm. BIRD: không có round thứ năm; tổng client time 1,207 so với 692 phút (khoảng 1.7 lần), con số này chưa in ở đâu. Một round FedAvg SFT thứ năm trên BIRD là khoảng 3 giờ GPU (173 phút, Table 7) cộng evaluation; tôi không đổi GPU queue |
| C43 | (Cả hai cold read của Sections 7 và 8, major) Gain trên BIRD dev có bao nhiêu là query không tương đương với gold SQL nhưng trả cùng kết quả? | Số của Section 5.4: correct predictions đọc đúng bảng và cột của gold SQL tăng 517 lên 557 (+40), đọc bảng hoặc cột khác tăng 136 lên 191 (+55), tức 55 trong net gain 95 câu nằm ở nhóm chỉ có EX trên một database kiểm tra; BIRD không có test suite. Trên Spider test thì ngược lại (+55 ở nhóm đọc đúng, +20 ở nhóm kia) và TS giữ chiều chênh lệch. Section 7.2 nêu các số này và nói thẳng gain trên BIRD không có phép kiểm chặt hơn; Section 8 nhắc lại trong một câu. Đọc bảng khác không có nghĩa là sai (join thừa, cột tương đương), paper không có breakdown. Code có fuzzer theo Zhong et al. (`fedls_sql/eval/db_fuzz.py`), đã dùng trên Spider dev (10 variant khớp suite chính thức 98.6 đến 98.9%, `LAB_LOG.md` 2026-11-23); chưa chạy trên BIRD dev. Chấm predictions của hai hàng chính trên các variant của database BIRD dev là việc CPU, không đụng GPU queue; tôi chưa đo thời gian và chưa chạy vì đây là thêm một phép đo vào paper, bạn quyết. **Bạn, 2026-11-27:** thử chạy sau, đưa số vào paper nếu kết quả tốt. Không bắt buộc: các paper trên BIRD báo cáo EX (tôi chưa mở lại từng paper để kiểm tra). Dữ kiện gần nhất trong notes: trên Spider dev, test suite chấp nhận 17 trong 48 prediction loại này của method và 14 trong 49 của FedAvg SFT (`LAB_LOG.md`, 2026-11-26), tức phần lớn nhóm này không qua phép kiểm chặt, ở cả hai model. Chạy thử không ràng buộc gì paper: kết quả không tốt thì ở lại notes, paper không in và không cần câu nào về nó. Chỗ duy nhất phụ thuộc là mệnh đề "and its gain has no stricter check" của Section 7.2 (do brief của tôi đưa vào): nó nói chưa có phép kiểm nào, nên khi đã chạy thì bỏ mệnh đề đó; "BIRD has no test suite" vẫn đúng |
| C44 | Số pairs theo loại sample sai (Section 7.1, đoạn 3) chỉ có trong text | Tám số đếm in thẳng trong câu, lần đầu xuất hiện ở Discussion (cold read 1, minor). Writer đề xuất hai cột trong Table 7 ("incorrect side: execution error", "incorrect result"); Section 7.1 khi đó trỏ tới bảng và bớt khoảng 25 từ. Table 7 là bảng generated nên phải sửa `tools/paper_numbers.py`; tôi chưa làm vì bảng thuộc Section 5 đã commit |

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
9. Hàng CodeLutra (bạn, 2026-11-26): bỏ câu "The number of pairs and
   the token average are settings, not the contribution", là nguồn của
   câu "The rest are settings" trong bản nháp; ceiling viết lại thành
   mức nói mạnh nhất được phép, không còn liệt kê điều paper không
   nhận. Rule chung nằm ở `WRITING_GUIDE.md` ("How it should read",
   "What binds" điểm 2) và `WRITING_PLAN.md`, mục 4. Cùng kiểu, chưa
   sửa, chờ bạn: câu về λ và `|y+|` (B2, B9).

Brief của Section 4 (`briefs/04_setup.md`, bạn duyệt 2026-11-26, commit
`3ebf681`) đổi mười chỗ: bốn chỗ sau khi writer trả outline, hai chỗ
(5, 6) sau khi đọc draft, bốn chỗ (7 đến 10) sau cold read:

1. Section 4.1: thêm một mệnh đề giới thiệu difficulty levels của hai
   tập evaluation, vì Table 3 báo EX theo level.
2. Section 4.2: quy tắc "client đã đủ 1/K số database thì không nhận
   thêm" là của code NIID-Bench, không có trong paper của nó; brief
   yêu cầu ghi nguồn là implementation hoặc nêu như quy tắc của ta.
3. Section 4.3: model 0.5B chạy trên Spider, DeepSeek-Coder trên Spider
   và BIRD; RQ2 không chỉ nằm trên Spider.
4. Appendix A: system message mặc định là fact của chat format của
   model chính (đã kiểm với Qwen2.5-Coder-1.5B), không nói cho mọi
   model.
5. Section 4.1: brief viết "mọi baseline và mọi ablation chạy trên
   BIRD". Sai: ablation "Clients pooled" của Table 8 chỉ chạy trên
   Spider. Brief đã sửa.
6. Section 4.4, FedDPO: thêm fact còn thiếu là các round của FedDPO
   dùng settings của preference round, với λ = 0 (cùng lệnh, thêm
   `--nll-alpha 0 --samples-from-round 1 --fixed-reference`).
7. Mọi ceiling viết lại thành mức nói mạnh nhất được phép, theo rule
   của bạn ở commit `0a90b1b`; không ô nào còn liệt kê điều paper không
   nhận (ví dụ "not realistic", "does not report variance over seeds",
   "no state of the art"). Bản nháp đầu không in câu phủ định nào thuộc
   loại này.
8. Section 4.1: cách đọc query viết thành ba bước theo đúng thứ tự của
   code (`extract_sql`); Section 4.3: "cùng settings cho ba model" sai
   ở một điểm, giới hạn độ dài training sequence của DeepSeek-Coder là
   8,704 token (7,168 ở model chính).
9. Section 4.2: thêm lý do lệch theo query complexity (với database
   nguyên vẹn, client ở setup nào cũng khác nhau về domain và schema;
   cấu trúc SQL là thứ mang sang được database chưa thấy, và EX được
   báo theo đúng các level đó; từ `FEDERATED_DATA_SETUP.md`, 3.3) và
   nhận xét rằng client của setup IID vẫn khác nhau về cỡ.
10. Section 4.4 và 4.6: hàng Local SFT cho K model, mỗi model chấm trên
    cả tập evaluation, in mean kèm client thấp nhất và cao nhất; mỗi
    hàng được test với hàng tham chiếu của bảng (FedAvg SFT ở các bảng
    của Section 5, method ở bảng của Section 6), hai hàng của seed thứ
    hai được test với nhau.

Sau cold read lần hai (round 2), thêm bốn chỗ:

11. Section 4.2: quy tắc 1/K được áp theo từng tier (client đã đủ 1/K
    khi tới lượt một tier thì không nhận database của tier đó), nên một
    client có thể vượt 1/K; bản trước đọc như giới hạn cứng và mâu
    thuẫn với Table 2 (18 của 69 database). Hardness của BIRD train:
    parser của Spider không đọc được phần lớn query của BIRD, nên dùng
    cùng tiêu chí trên query do sqlglot parse (đã kiểm trong code).
12. Section 4.5: thêm hàng "where the recipes come from" (SPFT-SQL và
    CodeLutra, mục C10). Đây là nội dung mới so với brief bạn đã duyệt.
13. Section 4.6: câu "FedAvg SFT là hàng tham chiếu ở Section 5" sai với
    Table 6 (còn test method với bản không warm-up) và hàng Local SFT
    không có test; brief nêu lại đúng.
14. Lý do thứ hai của việc lệch theo complexity ("EX báo theo cùng
    level") chỉ đúng trên Spider; đã bỏ. Writer phát hiện.

Brief của Section 5 (`briefs/05_results.md`, bạn duyệt 2026-11-26) đổi
mười hai chỗ: hai chỗ khi Section 4 xong, bốn chỗ sau khi writer trả
outline, sáu chỗ (7 đến 12) sau draft và cold read:

1. Section 5.1: hàng "No training" là pretrained model, nói trong một
   mệnh đề (Section 4 không còn nói).
2. Caption của các bảng giải thích dấu sao và p chưa hiệu chỉnh.
3. D1 (model 0.5B): bỏ conjecture về margin nhỏ hơn (mục C18).
4. Section 5.3, hàng không warm-up: "EX is level with" đổi thành "no
   difference in EX is significant after the correction; TS thấp hơn
   trên cả ba set" (mục C19). Writer phát hiện.
5. E2: câu "more SFT rounds do not reach it" thu lại thành câu nối với
   A2 và so sánh trực tiếp trên Spider (mục A15). Writer phát hiện.
6. Table 6: các hàng là model của setup chính trên Spider (các hàng
   Spider của Table 3, và method không warm-up train trong cùng setup);
   caption nói điều đó. Brief cũ thiếu fact này.
7. E2: "labels chiếm phần lớn thời gian thêm sau training" sai ở
   preference round 2 trên BIRD (training 195 của 391 phút); đổi thành
   "training trên pairs là phần lớn nhất ở mọi preference round".
   Writer phát hiện.
8. C2: câu "the gain comes from queries that now execute and are
   correct" thay bằng các số của bảng chuyển outcome (mục A16).
9. A2: FedAvg SFT có round 5 chỉ trên Spider và text phải nói; round
   cao nhất của FedAvg SFT trên Spider là round 3 và 4.
10. Hàng không warm-up: thêm định nghĩa (T_w = 0, bốn preference round
    từ pretrained model); Section 3 và 4 không định nghĩa nó.
11. Số câu hỏi "all correct" không còn tính các câu trên database không
    có row (Spider 2,891 và 5,784 thành 2,327 và 4,623).
12. C3: bỏ quy tắc cho prediction không parse được (không prediction
    đúng nào trong các hàng được trích là không parse được).

Outline của writer khác `OUTLINE.md` ở thứ tự trong 5.1 (Table 3 đọc
trước: A1, A3, A5 và A6; rồi Fig. 2: A4 trước A2) và ở heading của 5.4
("Analysis of the predictions and cost of a round (RQ4)"); nội dung
không đổi. Thêm một mệnh đề ngoài brief ở 5.1: gain của preference
round thứ hai (BIRD +2.54, significant; Spider +0.74, không
significant), đặt cạnh việc FedAvg SFT không tăng sau round 3.

### Brief của Section 2 đã đổi sau khi bạn duyệt (2026-11-27, sau audit và cold read)

| Chỗ | Bản bạn duyệt | Nay |
|---|---|---|
| 2.2, statement 2, ceiling về Liu et al. | "the paper offers no explanation of it" | nêu setup của họ cạnh kết quả (pairs dựng một lần, chỉ DPO loss, reference cố định), không nêu nguyên nhân, và trỏ tới ablation của ta (Section 6) |
| 2.2, statement 4, CodeLutra | pointer tới Section 3.4 chỉ nói settings theo CodeLutra | pointer nói cả hai: lấy gì, và Section 3.4 nêu chỗ khác; CodeLutra là method cho code generation, đánh giá trên Text-to-SQL và data-science code |
| 2.2, statement 6 | "the party that trains holds the questions and the databases" cho cả subsection | chỉ cho các work gán nhãn bằng execution (DPO, Pang et al., Lanchantin et al. không dùng database) |
| 2.3, statement 2 | "Federated DPO" cho cả FedDPO và Wu et al. | ở Wu et al. DPO chạy ở server |
| 2.3, statement 4 | "none of these" | "none of these federated works" (LoRA có thí nghiệm trên một dataset Text-to-SQL) |
| 2.4, statement 1 | số của Zhang et al. tùy writer | nói quan hệ giữa câu hỏi của họ (client heterogeneity dưới SFT) và của ta (supervision); số chỉ giữ nếu phục vụ điều đó |
| Table 1 | không nói | các hàng mô tả method như đã công bố |

Đổi lần hai, sau cold read 2 (2026-11-27):

| Chỗ | Trước | Nay |
|---|---|---|
| 2.1, statement 1 | privacy motive của CodeS phải có | chỉ giữ nếu nói được bước nối từ "một tổ chức với API provider" sang "nhiều tổ chức không gộp được dữ liệu"; được bỏ |
| 2.2, statement 2 | "the preference need not come from annotators" | "needs no annotation beyond the gold SQL query that SFT already uses"; section không được đọc như train không có label. Ceiling thêm: hàng ablation không renewal giữ cả pairs lẫn reference model của preference round đầu, nên Section 6 xét đủ ba lựa chọn của Liu et al. |
| 2.2, statement 3 | Pang et al. và Lanchantin et al. đều nêu | Pang et al. bắt buộc (DPO + NLL loss, pairs dựng lại mỗi iteration, model của iteration trước làm reference có ở họ trước CodeLutra); câu về Lanchantin et al. được bỏ vì độ dài, key đó sẽ cite ở Section 6 |
| 2.2, statement 4 | "takes its sampling and loss settings" | lấy đúng những gì Section 3.4 ghi (số sample, temperature, beta, uniform pairing, cách chọn reference model); chỗ khác: vòng lặp chạy qua các client, warm-up rounds, ít pairs hơn, NLL term lấy trung bình theo token. Việc dựng lại pairs là điểm chung, không liệt kê như điểm khác. Một tên cho likelihood term |
| 2.2, statement 6 | "An execution label needs the database, and in federated training only the client has it" | chỉ nói các work gán nhãn bằng execution train ở một site; lập luận "label chỉ tính được ở nơi có database" thuộc Section 1 |
| 2.4, statement 1 | "ours the supervision a client learns from" | "what execution on the databases of a client adds to the gold SQL as supervision" |

### Brief của Section 6 đã đổi sau khi bạn duyệt (2026-11-27, sau cold read 1)

Bạn duyệt `briefs/06_ablation.md` ở commit `5779f42`.

| Chỗ | Bản bạn duyệt | Nay |
|---|---|---|
| Độ dài | 790 từ, tối đa 880 | khoảng 880, tối đa 930 (mục B26) |
| Các hàng là gì | mỗi hàng bỏ hoặc thay một phần | hai hàng không như vậy: "Fixed pairs and reference" giữ hai thứ cùng lúc, "Clients pooled" đổi setting |
| B1 | hàng khác method ở preference round thứ hai | thêm: hàng không cho biết chênh lệch trên BIRD đến từ pairs hay từ reference; một mệnh đề được nêu bước của preference round thứ hai (Spider +0.74, BIRD +2.54) để đọc chữ "level" trên Spider |
| B3 | một câu credit | câu đó nói rõ hai work so accuracy khi chỉ có DPO term với accuracy khi có cả hai term; cite Liu et al. ở chỗ ba lựa chọn của họ được thay đổi (lời hứa của Section 2.2) |
| B4 | số đếm execution error mang claim | ba giá trị EX trước (model trước round, hàng này, method), rồi số đếm với kiểm định của chúng (mục A25); không viết phần giảm lỗi nào "requires" preference term |
| B5 | "does not carry over ... with two it does" | vẫn là mức mạnh nhất, nhưng text nói mỗi nửa dựa vào gì: method so với biến thể có test (significant ở Spider-Syn), biến thể so với FedAvg SFT là so giá trị của Table 6. Số đếm Spider đổi (mục B25) |
| B8 | "does not raise EX" | thêm độ lớn (2.61) và p hiệu chỉnh (0.058) cạnh p chưa hiệu chỉnh |
| B6 | "the three weightings are level" | "no significant difference", kèm độ lệch lớn nhất của trọng số một client (BIRD 2.1 và 13.3 điểm phần trăm, Spider 10.8 và 9.4) |
| B7 | một câu nói hàng là gì | thêm mục đích: cùng các preference round nhưng không federated, để thấy các round mất gì khi chạy ở năm client có server average |

### Brief của Sections 1 và 7, 8 đã đổi sau khi bạn duyệt (2026-11-27, khi trả lời outline)

Bạn duyệt hai brief trong chat ngày 2026-11-27 (commit `dcab6eb` và `de149a7`).

| Chỗ | Bản bạn duyệt | Nay |
|---|---|---|
| Section 1, statement 7, câu về cost | "a preference round takes more client compute than an SFT round" | không thêm communication, cost thêm là computation ở client; nói về cả method, không về từng round (mục B29) |
| Section 7, limitation 4 | cùng câu trên | cùng cách sửa; bốn hệ số đã in ở Section 5.4 nên ở đây nêu khoảng là đủ |
| Section 7, limitation 8 | gain nhỏ hơn "where FedAvg SFT is still improving fast, as with the model of 0.5B parameters" | hai điều paper có, không nêu nguyên nhân (mục C37) |
| Section 7, statement 1, evidence | pairs theo loại và số đếm theo round của method | thêm số đếm của hàng "Fixed pairs and reference" trên BIRD dev và Spider test (mục C38) |

Sau cold read của từng section, brief đổi thêm:

| Chỗ | Bản bạn duyệt | Nay |
|---|---|---|
| Section 1, statement 4 | training với execution label ở một site: DPO (CodeLutra) | thêm dòng RL với execution reward (SLM-SQL, Think2SQL, Arctic-Text2SQL-R1), như Section 2.1; FedDPO dùng "preference datasets for helpfulness or harmlessness", không viết "human preferences" (B19) |
| Section 1, statement 6 | method trong ba câu | thêm chỗ khác với loop của CodeLutra, theo cách nói của Section 3.4 |
| Section 1, statement 7 | gain, A2, C1, một mệnh đề về cost | thêm: federation là gì, 4 rounds chia thế nào, test nào, EX cao nhất của FedAvg SFT trên BIRD dev (43.68 ở round 3, thấp hơn 5.08) |
| Section 7, statement 1 | "what a preference round changes follows what the incorrect samples of its pairs are" | chỉ còn phần đúng trên cả hai dataset: round đầu hơn nửa số pair có sample sai là execution error và round đó giảm execution error; pairs nêu bằng số đếm của cả hai loại. Không suy ra việc incorrect result giảm ở round hai từ thành phần pairs; hàng "Fixed pairs and reference" không dùng (C38) |
| Section 7, statement 4 | effect của warm-up "is seen in TS" | nói rõ cái gì có test (TS trên Spider-Syn so với method) và cái gì là so giá trị; reading phải đi kèm cách đọc khác (biến thể chạy bốn preference round thay vì hai) |
| Section 7, limitation 5 | EX có cùng giới hạn; BIRD không có test suite | thêm số của Section 5.4: trên BIRD dev, correct predictions đọc đúng bảng và cột của gold SQL 517 lên 557, đọc bảng hoặc cột khác 136 lên 191 |
| Section 7, limitations 1, 2, 3, 8 | như `CLAIMS.md` | 1: database mở read-only, có time limit (C39). 2: client lấy từ training set của một benchmark; chỉ hai preference round. 3: số pair phụ thuộc performance của model (C41). 8: không đặt model 0.5B cạnh số warm-up rounds |
| Section 8, statement 1 | method | thêm: loss có preference term và NLL term |
| Section 7, limitation 2 (sau revision 2) | "Two preference rounds are all that is studied" (câu tôi thêm ở round 2) | method không train quá 4 rounds; dòng duy nhất có hơn hai preference round là biến thể không có warm-up rounds (mục B33). Draft đã sửa theo (2026-11-27) |
| Section 5.4, C1 và C2 (2026-11-27, theo quyết định A31) | số đếm execution error và incorrect result | thêm hai test của method so với FedAvg SFT ở 4 rounds (`\errpval`, `\wrpval` với `{fedavg}{4}{k2}{4}`) |
| Section 7, statement 3 (2026-11-27, theo A31) | giảm một nửa execution error, nêu bằng số đếm | thêm hai test trên; việc giảm một nửa có kiểm định, chênh lệch incorrect result không significant sau hiệu chỉnh |
| Section 7, độ dài và limitations (2026-11-27, theo B34) | khoảng 700 từ, tối đa 780 | khoảng 860, tối đa 900; các hàng 3, 4, 5 của limitations nêu đủ (cost, số pair phụ thuộc performance, database không có row) |

Outline của writer khác brief ở thứ tự, không ở nội dung: Section 7 mở bằng statement 3 (kết quả so với FedAvg SFT, nối từ Section 5.4), rồi 1, 2, 4; Section 1 tách statement 4 thành hai đoạn (CodeLutra ở một site, rồi FedDPO và gap).

## E. Việc chuyển sang các section sau

| Section | Phải mang |
|---|---|
| 1 | Định nghĩa các abbreviation SFT, DPO, NLL, LoRA và EX ở lần dùng đầu: Section 2 dùng chúng mà không viết đầy đủ (trả lời outline của Section 2). Viết "Zhang et al.", không viết "FL4SP" (B18); nói về data của FedDPO như brief Section 2 (B19). Cite Spider và BIRD ở lần nhắc đầu (Section 2 nhắc tên mà không cite). Giới thiệu thuật ngữ "execution label" (Section 2 dùng trước khi Section 3 định nghĩa). Nói vì sao nhiều tổ chức cần train chung một model (C28). Giới thiệu "global model", "warm-up rounds" và "NLL term": đoạn CodeLutra của Section 2.2 dùng chúng trước Section 3 (B22). Privacy motive của CodeS đã ra khỏi Section 2; nếu cần thì Section 1 nói |
| 4 | Cách đọc query từ output của model và cách so execution results (Section 3.4 trỏ tới đây); số câu hỏi trên database không có row và số gold SQL lỗi. Đã vào brief `briefs/04_setup.md` (Section 4.1) |
| Appendix B | Time limit, cấu hình adapter, settings của local training, và quy tắc replacement nếu Section 3.4 bỏ nó. Đã có trong `generated/tab_settings.tex` (các hàng Pairing, Time limit) |
| Appendix B, khi các hàng GPU về | Thêm vào Table B1: settings của FedDPO, hệ số của FedProx, số epoch của Local SFT, training seed thứ hai (cold read Section 4 thấy thiếu; các run đó chưa commit) |
| 5 | Hàng "No training" không còn được giải thích ở Section 4: 5.1 nói nó là pretrained model. Caption của các bảng kết quả giải thích dấu sao và p chưa hiệu chỉnh (Section 4.6 đã bỏ câu đó). Cả hai đã vào brief. Thời gian ở Table 7 là tổng của các client chạy lần lượt trên một card (Section 4.5 chỉ nói simulation trên một GPU). Các ceiling của brief `briefs/05_results.md` đã viết lại theo rule của commit `0a90b1b` (15 ô; không còn "not robust", "no state of the art", "never ..."); nội dung claim không đổi |
| 6 | Số câu hỏi không có sample đúng, có và không có warm-up (mục A1); so sánh trọng số; câu về gold SQL trong preference round nếu bạn đồng ý mục A2 |
| 7 | Client phải chạy được SQL trên database của mình (Section 3.5 không còn nói). Một training seed và một lần rút partition là limitation nêu ở đây, một lần (C9, C15) |
| 6 (thêm, từ fact sheet Section 2) | Bốn kết quả đã công bố về likelihood term trong DPO, có locator trong `briefs/02_related_rows.md`, để đặt hàng "without the NLL term" của Table 8 vào đúng bối cảnh: CodeLutra, Table 2 (Spider 17.2 khi chỉ có DPO term, 76.6 với loss đủ); Pang et al., Table 1 (GSM8K 61.8 so với 73.1, một round); Liu et al., App. A, Table 7 (thêm SFT term trên output chỉ có SQL: 58.8 lên 60.0, họ gọi là gain hạn chế); Lanchantin et al., Sec. 4.2 (thêm NLL term không có lợi trong task của họ). Hai kết quả cuối không ủng hộ NLL term; brief Section 6 phải mang cả bốn. Section 2.2 hứa "Section 6 varies all three of these choices" (pairs dựng một lần, chỉ DPO loss, reference cố định): brief Section 6 phải nói rõ hàng B1 giữ cả pairs lẫn reference (B23). Lanchantin et al. chỉ còn được cite ở đây |
| 4.2 (lượt đọc toàn bài, W14) | "non-IID" có trong `TERMS.md` là abbreviation phải viết đầy đủ ở lần dùng đầu; Section 4.2 dùng "IID" và "non-IID" mà chưa viết đầy đủ (Sections 4.4 và 5.1 dùng lại). Section 1 không mô tả client là non-IID nên không giới thiệu từ này; chỗ viết đầy đủ là Section 4.2 (writer của Section 1 phát hiện) |
| 3.4 (đã accept; để bạn cân nhắc) | NLL term của Pang et al. cũng length-normalized (fact row K.1: "alpha times length-normalized NLL on the winner"), giống cách ta lấy trung bình theo token; Section 3.4 hiện chỉ nói "where CodeLutra sums it". Có thể thêm một mệnh đề ghi nhận Pang et al. (key đã có trong reference list sau round 2) |

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

## G. Notes lệch với paper gốc (helper Table 1, 2026-11-26)

Helper Opus đọc đủ bốn paper của Table 1; từng ô có trích dẫn và vị trí
trong `briefs/02_related_table1_rows.md`. Tôi chưa sửa các file notes;
brief của Related work sẽ dựng từ file đó, không từ notes.

| Notes | Ghi | Paper viết |
|---|---|---|
| `LITERATURE.md`, dòng 57 | FL4SP "full fine-tuning" | chỉ "finetune T5-base"; không nói full hay adapter, không in kích thước model |
| `LITERATURE.md`, dòng 59 | OpenFedLLM: Llama2-7B int8, LoRA r=32 | đó là setup instruction tuning; FedDPO dùng Wizard-Vicuna-7B-Uncensored, LoRA rank 8, alpha 16 |
| `DPO_RESEARCH.md`, dòng 168 | "every FL algorithm beats local training"; FedDPO là "DPO inside FedAvg" | trên HH-RLHF, FedProx thấp hơn local training về harmlessness (Table 9); bảng FedDPO còn chạy FedProx, SCAFFOLD, FedAvgM |
| `DPO_RESEARCH.md`, dòng 203 | ExCoT: "5.6k of the 9,428 BIRD train" | ExCoT ghi 9.2k |
| `DPO_RESEARCH.md`, dòng 56 | CodeLutra: "base model" | bảng checkpoint ghi Llama-3-8B-Instruct (`LITERATURE.md`, dòng 525 đã ghi) |
| `LITERATURE.md`, dòng 835 đến 837 | FedDPO của OpenFedLLM "all on human preferences" | đúng với HH-RLHF; với UltraFeedback paper không nói ai chấm điểm |

Lưu ý cho Table 1: ExCoT chỉ dùng output của chính model ở các on-policy
rounds (round DPO đầu và SFT dùng output của GPT-4o), và không viết loss
thành công thức; FL4SP không có preference stage, các ô về pairs là
"not applicable"; reference model của ba paper DPO thuộc ba loại khác
nhau (đổi mỗi iteration, cố định, không nói).

Thêm từ helper thứ hai (17 paper ngoài Table 1, `briefs/02_related_rows.md`, 2026-11-26):

| Notes | Ghi | Paper viết |
|---|---|---|
| `LITERATURE.md` 1.4, Liu et al. | "SQL-only DPO lowers EX for 6 of 10 models" | đúng với greedy và Maj@16; với Pass@1 cả 10 model tăng (Table 1). Pairs dựng một lần từ SFT model, DPO 8 epoch, không có NLL term |
| `bib/report.md`, Lanchantin et al. | chỉ ghi offline, semi-online, online | paper còn ghi thêm NLL term không có lợi (Sec. 4.2) |
| `LITERATURE.md` 1.4, Think2SQL | "GRPO with EX or partial rewards" | model tốt nhất dùng partial reward (trọng số 0.85) cộng hai format term; bản arXiv v5 trỏ sang một paper TMLR mới hơn, khác tên. Entry trong `references.bib` là preprint |
| `LITERATURE.md` 1.4, Arctic | reward 1 và 0.1 | đúng; abstract của paper lại viết "solely execution correctness". Model cuối bắt đầu từ checkpoint OmniSQL |
| `bib/report.md`, SPFT-SQL | "verified synthesis plus self-play" | execution chỉ kiểm tra output của model so với SQL tổng hợp; paper không nói SQL tổng hợp được chạy trước khi dùng. Loss của self-play theo kiểu SPIN, không phải DPO |
| `LITERATURE.md` 1.22, KGRFL | "an RL-based fusion weights client models" | đúng theo abstract; abstract không nói rõ BART parser là model được train federated |
| CodeLutra (mọi notes) | gain so với SFT | paper viết "16.9% after four iterations"; Table 1 của chính nó cho 76.6 (iteration 3) so với SFT 67.9, tức 8.7 điểm |

## Đã xong

| # | Mục | Quyết định (bạn, 2026-11-27: "Duyệt 1,7,8, hoàn thiện bản draft") |
|---|---|---|
| A26 | Brief của Section 1 (`briefs/01_intro.md`) với abstract, keywords, ba ứng viên title | Duyệt, gồm bốn điểm tôi nêu: lý do train chung nêu như setting; contribution 3 không nhắc C3; tối đa hai reference mới; viết Section 1 không chờ Sections 7 và 8 |
| A27 | Brief của Sections 7 và 8 (`briefs/07_discussion.md`) | Duyệt, gồm số mới về pairs theo loại sample sai (statement 1) và các số `moved.*` (statement 3); C3 không được diễn giải |
| A30 | Con số trong abstract: 6.19 hay 5.08 | Giữ 6.19 (bạn, 2026-11-27: "ok"); Section 1 và 5.1 nêu 5.08 |
| A31 | Kiểm định cho "execution error giảm một nửa" so với FedAvg SFT | Đưa cả bốn test vào (bạn, 2026-11-27: "được"). `ERR_TESTS` trong `tools/paper_numbers.py` thêm method so với FedAvg SFT ở 4 rounds trên hai set. Execution error: BIRD dev p = 5.8e-22 (182 câu chỉ lỗi ở FedAvg SFT, 42 câu chỉ lỗi ở method), Spider test p = 6.2e-14 (118 và 29), cả hai significant sau Holm. Incorrect result: BIRD dev p = 0.007, sau Holm 0.077 (156 và 111); Spider test p = 0.37 (111 và 97); không cái nào significant sau hiệu chỉnh. Family "text" từ 19 lên 23: mọi p hiệu chỉnh trong family tăng nhẹ (so sánh gold SQL của B8 từ 0.065 thành 0.077), không giá trị nào đổi phía so với 0.05. `CLAIMS.md` C1 và C2 ghi các test này. Section 5.4 và Section 7.1 nêu test (writer sửa theo brief) |
| B33 | Section 7.2: "more than two preference rounds are not studied" không khớp Section 7.1 (lỗi từ brief của tôi) | Đã sửa trong lần sửa 2026-11-27: "has 2 preference rounds among its T = 4 rounds and is not trained further; only the variant without warm-up rounds has more" |

| # | Mục | Quyết định (bạn, 2026-11-26: "duyệt" brief Section 4) |
|---|---|---|
| A6 | Số câu hỏi không sinh pair ở Section 4.1 | In, như đề xuất (statement 6 của brief) |
| A7 | Bốn RQ ở đoạn mở đầu Section 4 | Giữ ở đoạn mở đầu |
| A8 | Appendix A in prompt rút gọn; Appendix B | Giữ bản rút gọn; khi biết tổng số trang thì Appendix B sang supplementary trước |
| A9 | Baseline chưa chạy và seed thứ hai được mô tả ở Section 4 | Viết theo plan; đọc lại 4.4 và 4.5 khi các hàng về |
| A10 | Citation NIID-Bench | Đã thêm `li2022niidbench` vào `references.bib` (record từ Crossref và arXiv API) và vào brief |
| A11 | Hai câu thêm ngoài `CLAIMS.md` trong brief Section 5 | Giữ cả hai (bạn, 2026-11-26: "duyệt" lần hai). Brief `briefs/05_results.md` đã duyệt |
| A12 | Số liệu mới cho Section 5 | Đã biết |
| A13 | Số trang: Section 4 khoảng 2.75 (plan 2.3), appendix 1.2 (plan 0.8), tổng dự kiến khoảng 25.7 của 25 | Appendix B sang supplementary như plan; quyết khi các section còn lại có số trang thật |
| | Template `section` của skill cold-review (`.claude/skills/cold-review/prompts/section.md`) | Bạn duyệt 2026-11-27. Từ Section 2, cold read của từng section chạy qua skill này (session Opus cô lập, chỉ thấy các trang của section và các trang trước nó), thay cho helper subagent |
| A2 | Gold SQL làm correct side cho câu hỏi không có sample đúng | Bạn giao tôi quyết (2026-11-27). Đưa vào: một statement (B8) ở phần warm-up của Section 6, chỉ cho BIRD dev, variant không warm-up, một preference round: 39.24 so với 41.85 (-2.61, p 0.0073; sau Holm trong family của text là 0.058, tức không significant sau correction); execution errors 219 xuống 105, incorrect results 673 lên 827. Câu trong paper: "does not raise EX". Là số trong text, không phải hàng Table 8. `CLAIMS.md` có hàng B8, macro đã sinh. Khác với notes: `RESEARCH_STATE.md` xếp đây là phần đã bỏ, không in; và run tương ứng trên Spider (đổi ba thứ cùng lúc) cao hơn 0.80 ở round 1 (p 0.21) rồi giảm ở round 2, nên paper không nói gì về Spider. Kết quả thứ hai (thêm NLL trên gold, -0.65, p 0.43) không đưa vào |
| A24 | Brief của Section 6 (`briefs/06_ablation.md`) | Bạn duyệt 2026-11-27 ("duyệt brief"). Sau đó thêm statement B8 theo quyết định A2. Writer đã khởi động |
| A18 | Brief của Section 2 (`briefs/02_related.md`) | Bạn duyệt 2026-11-27 ("duyệt brief"). Writer đã khởi động |
| A19 | Table 1, các cột | Theo brief đã duyệt: năm property của `OUTLINE.md`; không có cột model size, không có cột NLL term |
| A20 | Section 2.2, kết quả của Liu et al. | Theo brief đã duyệt: writer được nêu kết quả của họ (decoding và cỡ model của họ), không giải thích |
