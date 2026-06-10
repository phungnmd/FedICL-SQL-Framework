# Báo cáo dễ hiểu về kế hoạch FedICL-SQL

**Ngày cập nhật:** 2026-06-09 (đã tích hợp các sửa sau review góc nhìn PhD data science)  
**Dựa trên:** `todo.md` và `detailed_plan.md`

## 1. Mục tiêu của đề tài

Đề tài **FedICL-SQL** muốn xây dựng một hệ thống giúp nhiều tổ chức cùng cải thiện mô hình chuyển câu hỏi tự nhiên sang câu SQL, nhưng không phải chia sẻ dữ liệu riêng, lược đồ cơ sở dữ liệu, hay ví dụ nội bộ của từng tổ chức.

Nói đơn giản:

- Mỗi tổ chức có dữ liệu và schema riêng.
- Mỗi tổ chức dùng một mô hình nhỏ chạy cục bộ để sinh SQL.
- Máy chủ có một mô hình lớn đóng vai trò giáo viên.
- Mô hình lớn dạy các mô hình nhỏ thông qua tập dữ liệu công khai và cơ chế huấn luyện liên kết.
- Các bên chỉ gửi phần cập nhật trọng số đã bảo vệ riêng tư, không gửi dữ liệu gốc.

Mục tiêu cuối cùng là chứng minh rằng cách này:

- chính xác hơn so với từng tổ chức tự chạy mô hình nhỏ riêng lẻ,
- rẻ hơn và nhẹ hơn so với dùng mô hình lớn cho mọi truy vấn,
- bảo vệ riêng tư tốt hơn so với gom toàn bộ dữ liệu về một nơi.

## 2. Ý tưởng hệ thống hiện tại

Hướng thiết kế đã được chỉnh lại vào ngày **2026-06-09**.

Hướng đúng hiện tại là:

1. Máy chủ dùng **LLM Teacher** như Qwen2.5-72B để tạo SQL chất lượng cao trên một tập truy vấn công khai `X`.
2. Mỗi client dùng **SLM Student** như Phi-3-mini để học từ kết quả của teacher.
3. Client huấn luyện nhẹ bằng **LoRA** trên máy của mình, gồm **hai phần**: học trên **data riêng `Qᵢ`** (supervised) **và** học từ teacher trên **public set `X`** (KD).
4. Client gửi **LoRA delta**, tức phần cập nhật trọng số, về server.
5. Server dùng **FedAvg hoặc FedProx** để gộp các cập nhật thành một **Global SLM**.
6. Global SLM được gửi lại cho các client dùng ở vòng tiếp theo.
7. In-Context Learning vẫn được dùng, nhưng chủ yếu là cục bộ tại client để chọn ví dụ cùng schema hoặc liên quan schema.

Điểm quan trọng: hệ thống không chia sẻ private schema, private rows, hay private demos giữa các client.

🔴 **Lưu ý kỹ thuật cốt lõi:** phần học trên data riêng `Qᵢ` là **bắt buộc**. Nếu mọi client chỉ học trên cùng `X` với cùng teacher target, các LoRA delta sẽ giống hệt nhau → FedAvg không thêm gì → federation trở nên vô nghĩa và RQ1 không thể đúng. Data riêng làm mỗi client khác nhau → FedAvg mới gộp được kỹ năng SQL của nhiều tổ chức (đúng cơ chế FedCoLLM [8]).

## 3. Những việc đã làm

### 3.1 Đã xây dựng pipeline đơn lẻ

Phần P0 đã hoàn thành. Đây là nền móng trước khi làm federated learning.

Đã có:

- cấu trúc repo cho `data`, `retrieval`, `prompts`, `models`, `eval`, `experiments`,
- loader cho Spider,
- hàm lấy DDL từ SQLite database,
- mô hình student Phi-3-mini,
- retriever dùng `BAAI/bge-small-en-v1.5` và FAISS,
- prompt theo cấu trúc Light-SQL,
- đánh giá bằng Execution Accuracy và Exact Match,
- script chạy thử pipeline từ câu hỏi tự nhiên sang SQL.

Kết quả sanity check:

- câu hỏi: “How many singers do we have?”
- SQL dự đoán: `SELECT count(*) FROM singer`
- EX: PASS
- EM: PASS

Kết quả chạy thử 50 câu trên Spider dev:

- **EX = 78.0%**
- **EM = 48.0%**

Điều này cho thấy pipeline một client đã chạy được và có kết quả nền đủ tốt để phát triển tiếp.

### 3.2 Đã thử hướng federated demo-store nhưng loại bỏ

Đã có một thử nghiệm P1 lần đầu:

- chia Spider thành 3 client,
- tạo cơ chế chia dữ liệu theo database,
- tạo held-out workload,
- tạo demo store chung,
- thử chia sẻ demo đã mask giữa các client,
- chạy thử end-to-end.

Kết quả thử nghiệm này âm tính:

- zero-shot không dùng store chung: **50.0% EX**
- dùng demo cross-schema không mask: **43.3% EX**
- dùng demo đã mask: **3.3% EX**

Lý do thất bại:

- mô hình copy token mask như `tbl1`, `col2` vào SQL nên SQL không chạy được,
- demo từ schema khác dễ làm mô hình sinh SQL sai,
- SQL phụ thuộc rất mạnh vào schema cụ thể,
- cách chia sẻ demo này không đúng với Fed-ICL gốc.

Vì vậy, hướng này đã được đánh dấu là **superseded**, chỉ giữ lại như một kết quả âm tính và bài học thiết kế.

### 3.3 Những phần có thể tái sử dụng

Dù P1 attempt 1 bị bỏ, vẫn có nhiều phần dùng lại được:

- code chia dữ liệu federated,
- code đánh giá EX/EM,
- masking utility, nhưng chỉ dùng cho retrieval hoặc privacy, không đưa SQL đã mask vào prompt,
- kinh nghiệm về schema-coupling của Text-to-SQL,
- báo cáo negative result để đưa vào phần limitation.

## 4. Hướng sẽ làm tiếp

### 4.1 P1 mới: Teacher-centric federated framework

Đây là phần quan trọng nhất tiếp theo.

Cần làm:

- **chia Spider thành 3 pool schema-tách-rời:** public `X` / private mỗi client / held-out — không pool nào trùng DB, tránh rò rỉ dữ liệu (leakage),
- tạo tập công khai `X` gồm các câu hỏi NL-to-SQL dùng để teacher tạo nhãn,
- kết nối hoặc chạy LLM teacher,
- để teacher tạo SQL đúng (exec-filter: bỏ SQL không chạy được) và có thể có reasoning,
- cho từng client LoRA-train SLM trên **data riêng `Qᵢ` + public `X`** (KD từ teacher),
- client gửi LoRA delta về server,
- server FedAvg các delta để tạo Global SLM,
- gửi Global SLM lại cho các client,
- đánh giá xem Global SLM có tốt hơn SLM local-only không (≥3 seed, có test ý nghĩa thống kê).

Câu hỏi make-or-break:

> Global SLM học từ teacher qua federated LoRA có tăng EX so với SLM-only không, đồng thời rẻ hơn LLM-only không? Và có vượt được "null" (một client train một mình trên `X`) để chứng minh FedAvg thật sự có ích không?

Nếu câu trả lời là có, đề tài có trục kết quả chính.

### 4.2 P2: Nâng cấp knowledge distillation

Sau khi P1 mới chạy được, sẽ thêm các kỹ thuật KD mạnh hơn:

- logit-level KD,
- soft target từ teacher,
- MinED để xử lý khác biệt tokenizer giữa teacher và student,
- so sánh sequence-level KD với logit-level KD.

P2 không phải nền móng đầu tiên nữa. Nó là phần nâng cấp sau khi P1 teacher-KD chạy ổn.

### 4.3 P3: Chạy các baseline

Cần có các mô hình hoặc cấu hình so sánh:

- LLM-only: dùng teacher trực tiếp,
- SLM-only: mỗi client tự chạy mô hình nhỏ trên data riêng, không federation, không teacher,
- **Centralized-FT: gom toàn bộ data riêng, train MỘT SLM (không federation)** — đây là trần thật sự của method parametric; reviewer sẽ hỏi "FedAvg mất bao nhiêu so với train tập trung",
- centralized ICL: gom dữ liệu về một nơi + ICL, upper bound vi phạm privacy,
- without ICL: bỏ in-context examples,
- FedAvg-LoRA: federated learning không có teacher,
- Fed-ICL adapted to SQL: baseline gần nhất từ Fed-ICL.

Các baseline này giúp chứng minh từng phần của hệ thống có đóng góp thật.

### 4.4 P4: Đánh giá và tạo bảng/hình

Cần tạo các bảng và hình chính:

- T1: kết quả EX/EM trên Spider và Spider-Realistic,
- T2: độ hiệu quả về latency, VRAM, FLOPs,
- T3: chi phí truyền thông mỗi vòng,
- F2: đường hội tụ qua các round,
- F3: tương quan accuracy và cost,
- F4: ảnh hưởng của mức độ non-IID,
- F5: đánh giá privacy bằng prompt-extraction attack (chạy **khi bật DP**, report (ε, EX-cost)).

🔴 Mọi số liệu trong bảng cần **trung bình ± độ lệch chuẩn qua ≥3 seed**; các so sánh make-or-break cần **test ý nghĩa thống kê** (paired bootstrap / McNemar). temp=0 chỉ cố định decode, không thay cho variance.

Cũng cần chạy 5 ablation:

- bỏ ICL,
- bỏ federated learning,
- bỏ teacher LLM,
- thay đổi số demo retrieval `k`,
- thay đổi student model.

### 4.5 P5: Viết paper song song

Không cần chờ toàn bộ kết quả mới viết.

Có thể viết trước:

- phần Method,
- phần Related Work,
- phần Introduction.

Các phần cần chờ kết quả:

- Experiments,
- Abstract,
- Conclusion.

### 4.6 P6: Review và submit

Cuối cùng sẽ:

- tự review như reviewer,
- kiểm tra claim nào cũng có bảng hoặc hình chứng minh,
- chuẩn hóa format IAJIT,
- chuẩn bị code release,
- submit bài.

## 5. Trạng thái hiện tại

Tóm tắt ngắn:

- P0 đã xong.
- P1 attempt 1 đã chạy nhưng thất bại và đã bị loại.
- Hướng nghiên cứu đã được chỉnh lại theo Fig. 1.
- Hướng chính hiện tại là **LLM Teacher → SLM Student bằng LoRA + FedAvg**.
- Việc quan trọng tiếp theo là hiện thực P1 mới và chứng minh Global SLM tốt hơn local SLM.

## 6. Cách giải thích đề tài trong báo cáo ngắn

Có thể trình bày đề tài như sau:

> Chúng tôi xây dựng FedICL-SQL, một framework federated learning cho bài toán Text-to-SQL. Trong hệ thống này, mỗi tổ chức giữ dữ liệu và schema riêng tại chỗ, dùng một mô hình nhỏ để sinh SQL. Server có mô hình lớn đóng vai trò teacher, tạo tri thức SQL trên tập dữ liệu công khai. Mỗi client huấn luyện LoRA trên **dữ liệu riêng của mình kết hợp với tín hiệu distillation từ teacher trên tập công khai**, sau đó gửi phần cập nhật trọng số đã bảo vệ riêng tư về server. Server tổng hợp các cập nhật bằng FedAvg để tạo Global SLM và gửi lại cho các client. Cách này hướng tới việc tăng độ chính xác so với SLM local-only, giảm chi phí so với LLM-only, và tránh chia sẻ dữ liệu nhạy cảm.

## 7. Việc cần ưu tiên ngay

Thứ tự ưu tiên gần nhất:

1. Chốt cách chia 3 pool schema-tách-rời (public `X` / private / held-out), tránh leakage.
2. Chốt tập public `X`.
3. Chốt cách truy cập teacher 72B: API hay local GPU. (Lưu ý: giờ cần GPU cho **training** LoRA, nặng hơn P0 vốn chỉ inference.)
4. Implement teacher target generation + exec-filter.
5. Implement LoRA training cho student trên **data riêng + public `X`**.
6. Implement FedAvg cho LoRA delta.
7. Chạy thử với 3 client, ≥3 seed.
8. So sánh Global SLM với SLM-only **và** với null (1 client train trên `X`) + Centralized-FT.
9. Ghi lại kết quả (kèm độ lệch chuẩn + p-value) để quyết định có tiếp tục P2 logit-KD hay không.

## 8. Lưu ý khi viết paper

Không nên nói rằng hệ thống không truyền model weights. Thực tế hệ thống có truyền weight updates, cụ thể là LoRA deltas.

Nên nói chính xác:

- không truyền raw data,
- không truyền private schema,
- không truyền private demos,
- chỉ truyền LoRA delta đã mã hóa, nén, và có thể thêm DP noise.

Cũng không nên nói masking chắc chắn tăng accuracy. Theo Light-SQL, masking có thể làm giảm accuracy; trong đề tài này masking chủ yếu là công cụ privacy hoặc retrieval, không phải điểm chính để tăng EX.

Thêm vài lưu ý sau lần review (góc nhìn reviewer PhD):

- **Đừng claim "execution-guided" là mới.** Exec-guidance cho SQL đã có nhiều (exec-guided decoding, RL-with-exec-reward). Cái mới của ta = **lọc target KD theo execution trong vòng federated** + **structure loss theo skeleton-token** (CE có trọng số trên token cấu trúc, backprop được — KHÔNG phải AST-edit-distance).
- **DP chỉ là contribution nếu đo được** — phải có đường (ε, EX-cost) + F5 attack khi DP bật. Nếu không đo, để DP là future work.
- **Cross-schema generalization (RQ2):** vẫn giữ là claim chính (đúng outline), nhưng làm qua **skill của Global SLM + local ICL**, KHÔNG qua share demo cross-schema (đường đó đã fail ở attempt-1).
- **Ceiling đúng cho method parametric = Centralized-FT** (gom data train 1 model), không phải Centralized-ICL.
