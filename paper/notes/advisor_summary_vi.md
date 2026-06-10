# Tóm tắt đề tài FedICL-SQL để advisor review

## 1. Mục tiêu đề tài

Đề tài hướng đến bài toán **Federated Learning + In-Context Learning + Teacher-KD cho Text-to-SQL**. Mục tiêu là xây dựng một framework cho phép nhiều tổ chức/công ty sử dụng **Small Language Model (SLM)** để chuyển câu hỏi từ ngôn ngữ tự nhiên sang SQL với hiệu năng tiệm cận LLM, nhưng vẫn giữ được **privacy** và **chi phí triển khai thấp**.

Mỗi tổ chức giữ database/schema và dữ liệu huấn luyện tại local. Server không nhận raw data, private schema hay private examples. Các client chỉ gửi **LoRA weight deltas** đã được bảo vệ qua secure aggregation/mã hóa, và có thể thêm differential privacy nếu Stage B đo được trade-off rõ ràng.

## 2. Bài toán và dữ liệu

Dataset chính là **Spider** của Yale. Mỗi example gồm:

- câu hỏi tự nhiên;
- gold SQL query;
- `database_id`;
- SQLite database tương ứng trong folder database để có thể execute query.

Paper đánh giá bằng hai metric chính:

- **EM (Exact Match):** so khớp SQL prediction với gold SQL ở mức query/structure.
- **EX (Execution Accuracy):** execute predicted SQL và gold SQL trên cùng database, rồi so sánh kết quả trả về.

Trong Text-to-SQL, **EX** thường quan trọng hơn vì hai SQL khác nhau về cú pháp vẫn có thể trả về cùng một kết quả đúng.

## 3. Federated data simulation

Spider không phải dataset federated tự nhiên, nên paper tạo federated setting bằng cách chia theo **database/schema**, không chia random từng câu hỏi.

Quy trình chia data:

1. Tạo danh sách các database ID.
2. Chia database thành các nhóm disjoint:
   - public set `X`;
   - private database pools cho từng client;
   - held-out databases để test cross-schema generalization.
3. Dùng Dirichlet distribution để chia **DB/domain** cho các client, thay vì chia từng question.

Cách chia này hợp lý với đời thực hơn: mỗi công ty/tổ chức thường có database/schema/domain riêng, không phải cùng một database rồi chia ngẫu nhiên câu hỏi.

Ví dụ split `3c-a1.0-s0` nghĩa là:

```text
3c     = 3 clients / 3 organizations
a1.0   = Dirichlet alpha = 1.0, mức non-IID vừa phải
s0     = random seed = 0
```

Split này đảm bảo schema-disjoint giữa public `X`, private client pools và held-out schemas, tránh leakage giữa teacher/KD data, local client training và cross-schema test data.

## 4. Kiến trúc FedICL-SQL

Framework gồm các thành phần chính:

```text
LLM teacher
+ local SLM students
+ federated LoRA aggregation engine
+ schema-aware ICL
```

### 4.1 LLM Teacher trên server

Server dùng LLM mạnh, dự kiến **Qwen2.5-72B-Instruct**, để chạy trên public set `X`. Teacher sinh:

- reasoning steps;
- SQL query;
- metadata như execution validity/execution correctness.

Teacher outputs được execute-validate. Trong simulation với Spider, vì có gold SQL, paper có thể giữ những teacher targets có execution result khớp với gold. Kết quả được cache thành `teacher_targets.csv`.

Teacher **không truy cập private data/schema của client** và **không chạy mỗi inference query**. Vai trò của teacher là **offline/training-time KD**, giúp giảm chi phí và tránh leak private query/schema.

### 4.2 Public set `X`

`X` là tập public NL-to-SQL, disjoint với private client data. `X` có hai vai trò:

- làm **KD medium**: client học từ teacher reasoning + SQL trên `X`;
- làm nguồn tạo **ICL Hub demos**: các demo public/teacher-generated có thể được dùng trong prompt/retrieval.

Vì `X` là public, việc dùng teacher trên `X` không vi phạm privacy của client.

### 4.3 Local SLM tại client

Mỗi client có:

- local schema/database riêng;
- private examples `Q_i`;
- local retriever;
- local SLM, ví dụ Phi-3-mini/Gemma/TinyLlama.

Client LoRA-train SLM trên hai nguồn:

```text
private supervised data Q_i
+ public teacher-KD targets on X
```

Loss chính gồm:

- SQL loss trên gold SQL/private data;
- KD loss từ teacher reasoning + SQL;
- structure loss để nhấn mạnh SQL skeleton;
- execution-guided filtering cho teacher targets.

Điểm quan trọng: client phải học từ **private data của chính nó**. Nếu chỉ train trên public `X`, các client sẽ có updates gần giống nhau và FedAvg không còn nhiều ý nghĩa.

### 4.4 Federated LoRA aggregation

Sau local training, client không gửi data hay schema. Client chỉ gửi **LoRA deltas** về server. Server aggregate bằng **FedAvg/FedProx** để tạo **Global SLM `M_G`**, rồi broadcast lại cho clients ở round sau.

Quy trình này giúp các client chia sẻ "SQL generation skill" thông qua model updates, thay vì chia sẻ database/schema/examples.

### 4.5 In-Context Learning

ICL vẫn là thành phần quan trọng của framework. Khi inference, client dùng schema-aware retrieval để chọn demos phù hợp từ:

- local private examples;
- public/teacher demos từ ICL Hub.

Prompt gồm question, schema DDL, instruction và top-k demos. Masking chỉ dùng cho retrieval/de-identification nếu cần, không đưa masked SQL placeholder vào prompt cuối.

## 5. Khác với Fed-ICL prior work

Trong plan có nhắc đến **Fed-ICL** như một prior work/baseline. Fed-ICL gốc là một paper khác, làm parameter-free federated ICL:

```text
client local ICL -> gửi answer -> server fuse answer -> lặp nhiều round
```

Fed-ICL gốc không train model, không dùng teacher-KD, không FedAvg weights.

Trong paper này, Fed-ICL chỉ được adapt thành baseline:

```text
server gửi shared SQL questions
-> clients sinh SQL bằng local schema-aware ICL
-> server fuse SQL answers bằng execution vote / Fusion-LM
-> không train model, không exchange weights
```

Framework chính của FedICL-SQL vẫn là:

```text
Teacher-KD + schema-aware ICL + LoRA-based Federated Learning
```

## 6. Baselines và ablations

Paper sẽ so sánh FedICL-SQL với các baseline:

- **SLM-only:** client train/evaluate local SLM, không teacher, không federation.
- **LLM-only:** dùng LLM trực tiếp, làm accuracy ceiling nhưng cost cao.
- **FedAvg-LoRA:** federation không teacher-KD.
- **Centralized-FT:** gom toàn bộ private data để train một model, privacy-violating upper bound.
- **Fed-ICL adapted baseline:** client sinh SQL bằng local ICL, server fuse SQL answers, không train model.
- **Without ICL / Without Teacher / Without Federation:** ablations để chứng minh từng thành phần có đóng góp.

## 7. PoC trước khi chạy thực nghiệm lớn

Trước khi chạy full experiments, paper sẽ chạy một PoC nhỏ với split mặc định như `3c-a1.0-s0`:

```text
3 clients
alpha = 1.0
seed = 0
K = 2-3 rounds
1 seed
subset evaluation
no DP
```

Mục tiêu PoC là kiểm tra tín hiệu sống còn:

```text
FedICL-SQL / Global SLM M_G
> SLM-only
> X-only null baseline
```

Nếu PoC tích cực, mới mở rộng sang Stage B với:

- nhiều seeds;
- alpha sweep để kiểm tra mức non-IID;
- client-count sweep `L = {3, 5, 10}`;
- Spider-Realistic;
- đầy đủ baselines và ablations;
- significance tests cho headline results.

## 8. Kỳ vọng đóng góp

Đóng góp chính của paper là một framework federated Text-to-SQL cho phép nhiều tổ chức cùng cải thiện SLM local mà không chia sẻ dữ liệu/schema.

Framework kết hợp:

```text
Teacher-KD từ LLM mạnh
+ schema-aware ICL
+ LoRA-based Federated Learning
```

Mục tiêu là đạt accuracy gần LLM hơn SLM-only, nhưng inference/deployment rẻ hơn LLM-only và privacy tốt hơn centralized training.

