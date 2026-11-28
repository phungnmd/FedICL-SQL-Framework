# Lưu ý cần review

File này dành cho bạn và chỉ giữ hai loại việc: việc cần bạn quyết định
(phần A) và câu hỏi reviewer có thể đặt (phần C). Mục đã quyết thì xóa
khỏi đây; kết quả của nó nằm trong file nó liên quan (`CLAIMS.md`,
`OUTLINE.md`, `checks/`) và trong `LAB_LOG.md`. Số section là của
`OUTLINE.md` (bảy section).

Cập nhật: 2026-11-28.

## A. Cần bạn quyết định

| # | Ở đâu | Vấn đề | Đề xuất |
|---|---|---|---|
| A46 | Section 3; Section 1 và abstract | Hai bản sửa ngày 2026-11-28 chưa commit. Section 3: sửa giọng văn, dài thêm 15%, 25 trong 83 câu mở bằng trạng từ nối (bản đã commit: 1 trong 69); nội dung chỉ khác ở câu cuối 3.1. Section 1 và abstract: thêm so sánh với FedDPO trên BIRD dev. Cả hai có trong tag `archive/writing-workflow-2026-11-28` | Section 3: quay về bản đã commit, giữ câu cuối 3.1 mới. Section 1 và abstract: giữ |
| A47 | Section 3.4 | Warm-up là component hay bước khởi tạo? Lý do nêu trong bài là số câu hỏi không có sample đúng (4,035 xuống 2,698 trên BIRD); kết quả đo được là B5: EX không đổi, test-suite accuracy trên các bộ Spider tăng | Giữ là component. Xem lại khi hàng BIRD của B5 về |
| A48 | Cả bài | Số trang mục tiêu. Abstract, Section 1 và Section 3 đã chiếm 9,5 trang; ước lượng cả bài 25 đến 30 trang; CMC tính USD 100 mỗi trang vượt 15. Appendix cũng tính trang | Bạn cho con số; cắt ở caption, các ý lặp và đoạn kết quả của Introduction |
| A16 | Section 5.2 | Bảng chuyển outcome (`\fact{moved.*}`), chưa có trong `CLAIMS.md`. BIRD dev: trong 153 câu chỉ method đúng, 75 câu trước là execution error và 78 câu là incorrect result (Spider test: 67 và 83). Trong 268 execution error của FedAvg SFT trên BIRD, 107 câu giờ chạy được nhưng trả kết quả sai (Spider: 51 của 173) | In ở 5.2 và ghi vào `CLAIMS.md`, hoặc bỏ |
| A22 | Table 1 | Bảng bỏ PubSwap và Fed-GRPO (federated, train trên output của chính model với reward kiểm chứng được) và Liu et al. (Text-to-SQL, label từ execution, pairs dựng một lần), nên chỉ method có đủ dấu tick | Thêm hai hàng; cột cuối tách ba mức: từ dataset, output của model dựng một lần, dựng lại mỗi round. Ô "labels from execution" của Fed-GRPO là "answer check" kèm table note |
| A35 | Section 2, citation thêm | ExeSQL ở 2.2 (đã có trong `references.bib`); một câu về federated GRPO ở 2.3; aggregation của LoRA trong federated learning (FFA-LoRA, FLoRA; chưa đọc hai bài); self-training (STaR, RFT, ReST); FedPDPO | Thêm ExeSQL và câu về federated GRPO; các mục còn lại bạn chọn |
| A21 | Section 2 | SKT-SQL (`yi2025sktsql`) và KGRFL (`xu2024kgrfl`) chỉ đọc được abstract | Giới hạn mỗi bài ở một mệnh đề, hoặc bạn gửi PDF |
| A34 | Hai hàng control, chưa queue | (1) FedAvg SFT round 3 và 4 chạy với settings của preference round (learning rate 5e-5). (2) FedAvg SFT round 5 đến 7 trên BIRD để so ở cùng client time | Bạn quyết từng hàng |
| A43 | Section 5.3 | Số câu hỏi sinh pair của pretrained model chưa có macro. BIRD 4,857 lên 5,877 sau warm-up; Spider giảm 4,454 xuống 4,013 vì số câu all-correct tăng (1,427 lên 2,327). In riêng số BIRD sẽ khiến reader hiểu warm-up làm tăng số pair | In cả hai dataset ở 5.3 hoặc thêm hàng $T_w$ = 0 vào Table 8; Section 3.4 giữ nguyên |
| A41 | Fig. 2 | Hình gõ tay "N = 10"; ghi "Global model" ở mũi tên từ server (text: global adapter); loss là L_DPO + λL_NLL, hai tên này chưa được định nghĩa trong text | Sửa ba nhãn trong SVG, hoặc giữ hình và gọi tên hai term ở Eq. (4) |
| A39 | Section 4 | "cannot read most queries of BIRD train" chưa có số: 85% đo trên BIRD dev; trên BIRD train chỉ có cận dưới 2,319 của 9,428 | Viết "many queries of BIRD", hoặc đo trên server (script CPU) |
| A42 | `AGENTS.md` và `fedicl-sql/AGENTS.md` | Câu "never executes a query on the databases" sai theo nghĩa đen trên Spider: prompt đọc 3 rows mỗi bảng bằng `SELECT * FROM t LIMIT 3` | Đổi thành: FedAvg SFT không execute gold SQL hay query của model, và không execution result nào vào loss |
| A37 | Phần đầu bài và statement của CMC | Khối tác giả; bốn statement trong `sections/90_statements_cmc.tex`; caption của hình phải ghi tên và version của AI tool nếu hình làm bằng AI tool. Hai entry của `references.bib` cần bạn nhìn bằng mắt: tác giả thứ hai của SLM-SQL (arXiv và ACL Anthology ghi khác nhau); Holm (1979) không có DOI, đang cite bằng địa chỉ JSTOR | Bạn điền và chốt |

## C. Câu hỏi reviewer có thể đặt

Từ các cold read. Ghi để khi viết section liên quan thì có câu trả lời.

| # | Câu hỏi | Paper trả lời ở đâu, còn thiếu gì |
|---|---|---|
| C1 | FedExec-SQL là gì ngoài CodeLutra chạy trong FedAvg? Client có database, gold SQL và model nên tự chạy được vòng lặp đó; federation thêm gì? | Section 1 (novelty so với FedAvg SFT và FedDPO); Section 2.2 và Table 1 (so với CodeLutra, một lần); Local SFT ở Table 3 và hàng pooled clients ở Table 4 (chờ GPU). Không có hàng "preference rounds chạy riêng ở từng client" |
| C2 | Cấu hình mặc định chỉ có một lần dựng lại pairs (hai preference round). Hàng "Fixed pairs and reference" đổi pairs và reference cùng lúc | B1 và B2: trên BIRD pairs và reference cố định thấp hơn 2.61 (p 5.7e-4), round thứ hai thêm +2.54; trên Spider ngang nhau. Tách pairs khỏi reference cần một hàng mới (khoảng 8 giờ GPU, ước lượng); chưa đề xuất chạy |
| C3 | Trọng số theo số pair giảm trọng số của client mà model sai hết hoặc đúng hết; số pair còn tiết lộ model làm tốt đến đâu trên data của client | B6: ba cách tính trọng số cho kết quả ngang nhau. Gửi số câu hỏi thay cho số pair là đổi method, bạn quyết |
| C4 | Trung bình riêng hai ma trận của LoRA không bằng trung bình tích của chúng | Chưa trả lời; chưa kiểm OpenFedLLM ở điểm này (cùng A35) |
| C5 | Preference term là tổng theo token ($\beta$ = 0.1), NLL term là trung bình theo token ($\lambda$ = 1): cân bằng giữa hai term đổi theo độ dài query | Chưa trả lời; không có ablation. NLL term của Pang et al. cũng chuẩn hoá theo độ dài |
| C6 | Câu hỏi không sinh pair không được train trong preference round: 3,551 của 9,428 câu BIRD ở preference round đầu (2,698 all-incorrect, 416 all-correct, 437 không có label); nhóm all-incorrect là các câu khó nhất | Section 3.6 nói hệ quả; B8 (gold SQL làm correct side với $T_w$ = 0 không tăng EX); A3 (gain ở mọi difficulty level); số theo round ở Table 8 |
| C7 | FedDPO chạy sau 2 warm-up rounds, trên pairs đầu của method, và round thứ hai train lại trên cùng pairs: baseline yếu vì lịch train? FedDPO từ pretrained model thì sao? | Section 4 nói cái gì lấy từ OpenFedLLM (pairs cố định, reference cố định, không NLL) và cái gì là của ta; A6; hàng "Fixed pairs and reference" (giữ NLL). Không có hàng FedDPO từ pretrained model |
| C8 | Một training seed và một lần rút partition (split seed 42); McNemar chỉ nói về mẫu câu hỏi test | Section 4 nói test là gì; seed thứ hai cho hai hàng chính trên BIRD (chưa chạy); limitation 6 |
| C9 | Không có validation split: T, $T_w$, learning rate chọn trên dữ liệu nào? Baseline có được tune như method không? Local và centralized SFT train 3 epoch, FedAvg SFT 4 round mỗi round 1 epoch | Section 4 nêu nguồn: recipe SFT của SPFT-SQL (appendix A.4: lr 2e-4, 3 epoch), settings của preference round theo CodeLutra (Table 4). T = 4 và $T_w$ = 2 không có nguồn |
| C10 | Preference round dùng learning rate 5e-5, SFT round dùng 2e-4: FedAvg SFT ở learning rate thấp có lấy lại một phần gap không? | Hàng "without the preference term" chạy cùng settings của preference round (B4). Không có hàng FedAvg SFT ở 5e-5 (A34) |
| C11 | "Cùng số round" là cân communication, không cân compute | Table 8: BIRD 879 so với 692 phút GPU, cộng 327 phút label trên CPU. Spider: 5 round FedAvg SFT tốn 620 phút so với 555 và vẫn thấp hơn 4.28. Round 5 của FedAvg SFT trên BIRD chưa chạy (A34) |
| C12 | EX nhận một query sai nếu nó trùng kết quả với gold SQL trên database đó; gain trên BIRD có bao nhiêu là thật? | C4: suite sinh cho BIRD dev, gain 4.89 dưới test-suite accuracy (6.19 dưới EX); C3 in số dưới suite cạnh số EX; D4 trên Spider; limitation 5 |
| C13 | Preference term và NLL term mỗi cái thêm gì về EX? | B4: trên BIRD ở 4 round, không có preference term thấp hơn 3.52 (significant), execution error 228 so với 128, nhưng method có nhiều incorrect result hơn. B3: bỏ NLL thì Spider thấp hơn 3.87; BIRD thấp hơn 1.24 (không significant; -0.13 dưới suite). Hàng `bird_nonll` ở 4 round đang chờ |
| C14 | Vì sao DPO pairs mà không federated GRPO với execution reward? Mức 48.76 trên BIRD dev thấp hơn các hệ SLM một site (reader nhớ mức 60) | Không có hàng GRPO; paper so trong cùng setup, không so mức. Chưa có câu nào nói vì sao chọn DPO; bạn quyết có nói hay không |
| C15 | Vì sao nhiều tổ chức train chung khi mỗi bên tự fine-tune được open model? | Section 1, đoạn 2: một tổ chức có ít database và ít cặp question-SQL |
| C16 | Label phụ thuộc time limit và máy chạy: 87 và 92 gold SQL của BIRD train quá limit ở hai preference round; 350 gold SQL lỗi khi chạy | Section 4 in các số; nguyên nhân của 350 lỗi chưa được phân loại |
| C17 | Setup IID vẫn lệch (tỉ lệ câu hard 34 đến 52%, cỡ client 1,298 đến 2,028); cột "Hard or extra" của Table 2 áp cho BIRD train, vốn dùng thang simple, moderate, challenging | Section 4.2 phải nói rõ; Appendix B có `\setting{split.hardness}`; kiểm lại tên cột của `tab_setups` |
| C18 | Bảng in p chưa hiệu chỉnh nhưng dấu sao theo p đã hiệu chỉnh; family của các so sánh chỉ nêu trong text gồm gì? | Supplementary liệt kê mọi test với p đã hiệu chỉnh; Section 4 nói family |
| C19 | Model 0.5B: margin nhỏ hơn (+2.10 so với +3.49); vì sao? | Paper không nêu lý do. Số theo round của model này chỉ có trong notes, trên Spider dev; muốn nêu thì cần macro |
| C20 | Spider-DK: method không warm-up (67.10) cao hơn method (63.55), p 0.032, không significant sau Holm | Table 7 in ô này; B5 |
| C21 | Warm-up để làm gì: trên Spider số câu sinh pair giảm sau warm-up và EX ngang với $T_w$ = 0 | Section 3.4 chỉ nói điều đúng trên cả hai dataset; Section 5.3 trả lời bằng B5 (A43, A47) |
| C22 | Số câu hỏi BIRD mà cả mười sample đều đúng nhảy từ 416 lên 3,016 sau một preference round: sample ở temperature 1 có mất đa dạng không? | Chưa trả lời; đo được từ file samples |
| C23 | Thời gian là tổng năm client chạy lần lượt trên một card, không phải wall-clock của một round | Caption Table 8 |
| C24 | Không có ablation theo $M$, $N$, $\beta$, $\lambda$; gold SQL làm correct side chỉ chạy với $T_w$ = 0 | Paper chỉ nêu lý do của $M$: số pair đặt độ dài local training. $M$ = 10 trên BIRD tốn khoảng một ngày GPU mỗi round (ước lượng) |
| C25 | Hàng "Clients pooled" không chỉ bỏ federation: train gộp đổi cả thành phần batch và số optimizer step | Khi hàng về, câu của nó nói rõ cái gì giữ nguyên |
| C26 | Preference round đổi gì là theo loại sample sai trong pairs: hàng "Fixed pairs and reference" có ủng hộ không? | Trên BIRD có, theo số đếm (pairs round đầu: 56% có sample sai là execution error; pairs dựng lại: 25%); trên Spider không. Chỉ viết "consistent with" |
| C27 | Chạy SQL do model sinh trên database nội bộ của client: load, câu lệnh ghi, query chạy lâu | Code mở database ở chế độ read-only và dùng time limit của evaluation (30 s BIRD, 60 s Spider). Paper chưa nói |
| C28 | Phần lớn gain là bớt execution error; một bộ lọc execution lúc inference (chạy query, sinh lại khi lỗi) có lấy lại gain mà không cần train không? | Chưa có trong record. Một hàng chỉ evaluate trả lời được; nếu không chạy thì nêu ở Section 6 |
| C29 | Loại câu hỏi trên database rỗng khỏi pair construction bỏ cả negative hợp lệ (execution error vẫn là execution error) | Chưa trả lời |
| C30 | Việc của lượt đọc toàn bài | Tên biến thể không warm-up khác nhau giữa các bảng và text; -2.61 xuất hiện ở hai so sánh khác nhau (cả hai đúng); hàng của model chính in ở ba bảng |
