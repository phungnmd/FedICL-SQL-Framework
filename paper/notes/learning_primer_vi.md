# FedICL-SQL — Primer dễ hiểu bằng tiếng Việt

File này giải thích các khái niệm chính của đề tài **FedICL-SQL** theo cách dễ nắm trước khi đọc paper/reference. Giả định bạn đã biết cơ bản về machine learning: model, training, inference, token, embedding.

Mục tiêu của primer này không phải đi sâu toán, mà giúp bạn hiểu:

- đề tài đang giải quyết bài toán gì;
- các mảnh ghép Text-to-SQL, ICL, FL, LLM/SLM, KD liên kết với nhau như thế nào;
- sau update ngày 2026-06-09, hướng đúng của project là gì.

Ký hiệu mức độ ưu tiên:

- 🔴 Bắt buộc hiểu để làm project.
- 🟡 Cần hiểu để viết paper.
- 🟢 Biết để phòng khi bảo vệ/trả lời reviewer.

---

## 0. Bức tranh tổng thể

FedICL-SQL kết hợp 4 ý tưởng:

```text
Text-to-SQL
+ In-Context Learning
+ Federated Learning
+ LLM teacher → SLM students
```

Mô hình tổng quát:

```text
                    SERVER / CLOUD
        ┌─────────────────────────────────────┐
        │  LLM Teacher, ví dụ Qwen2.5-72B     │
        │  Shared public query set X          │
        │  Answer fusion / KD / aggregation   │
        └─────────────────▲───────────────────┘
                          │
              teacher signals / fused answers
                          │
        ┌─────────────────┴───────────────────┐
        │                                     │
   CLIENT 1                              CLIENT L
   private schema                         private schema
   private examples                       private examples
   local SLM                              local SLM
   local ICL retriever                    local ICL retriever
```

Ý tưởng chính:

- Mỗi client là một tổ chức có database riêng.
- Client **không gửi raw rows, private schemas, hoặc private examples** ra ngoài. (Client **có** gửi LoRA-delta weights đã mã hóa + DP-noise — xem §11.)
- Server có LLM lớn làm teacher.
- Client dùng SLM nhỏ để chạy rẻ hơn.
- ICL giúp SLM sinh SQL tốt hơn bằng cách đưa ví dụ phù hợp vào prompt (chạy local, RQ2).
- Federated part = **teacher-KD parametric** (client LoRA-train → server FedAvg → Global SLM), không phải share raw schema/demos.

Điểm rất quan trọng sau update 2026-06-09 (RE-ALIGNED theo Fig.1):

> 1. Không dùng global masked demo-store `G` làm trung tâm nữa — fail ở P1 attempt 1.
> 2. Engine chính là **PARAMETRIC**: client LoRA-train SLM trên **data riêng `Qᵢ` + public set `X`** (teacher SQL) → upload **LoRA deltas** → server **FedAvg → Global SLM `M_G`**. Đây đúng là cơ chế **FedCoLLM [8]** áp cho SQL (xem Fig.1: aggregation engine FedAvg/FedProx + Global SLM broadcast). (Train trên data riêng là bắt buộc — không thì FedAvg vô nghĩa.)
> 3. Demo-level KD parameter-free + Fed-ICL answer-fusion = **variant/baseline**, không phải engine chính.
> 4. ICL chạy local (RQ2), masking chỉ dùng cho retrieval.

---

## 1. 🔴 Text-to-SQL là gì?

Text-to-SQL là bài toán biến câu hỏi tự nhiên thành câu SQL chạy được trên database.

Input:

```text
Question:
"How many singers do we have?"

Schema:
CREATE TABLE singer (
  singer_id int,
  name text,
  ...
)
```

Output:

```sql
SELECT count(*) FROM singer
```

Ba khó khăn chính:

1. **Schema linking**

   Model phải nối từ trong câu hỏi với đúng bảng/cột.

   Ví dụ:

   ```text
   "cost" có thể là total_cost, price, amount, budget
   ```

2. **SQL structure**

   Model phải sinh đúng cấu trúc SQL: `JOIN`, `GROUP BY`, `ORDER BY`, nested query, aggregation.

3. **Generalization**

   Model phải làm được trên database/schema mới hoặc câu hỏi chưa thấy.

Hai metric quan trọng:

| Metric | Ý nghĩa | Ghi chú |
|---|---|---|
| EM | Exact Match, SQL predicted giống SQL gold | Quá strict, vì nhiều SQL khác nhau vẫn đúng |
| EX | Execution Accuracy, chạy SQL rồi so kết quả | Metric chính, quan trọng hơn |

Ví dụ:

```sql
SELECT count(*) FROM singer
```

và

```sql
SELECT COUNT(singer_id) FROM singer
```

có thể khác EM nhưng cùng EX nếu trả về cùng kết quả.

Dataset chính:

- **Spider:** benchmark Text-to-SQL chuẩn, nhiều database/domain.
- **Spider-Realistic:** khó hơn vì câu hỏi được paraphrase, ít nhắc trực tiếp tên cột.

---

## 2. 🔴 LLM teacher và SLM student

Trong đề tài này có hai loại model:

| Loại | Ví dụ | Vai trò |
|---|---|---|
| LLM teacher | Qwen2.5-72B, GPT-4, Llama-70B | Chính xác hơn, chạy ở server/cloud |
| SLM student | Phi-3-mini, Gemma-2B, TinyLlama | Nhỏ, rẻ, chạy ở client/local |

LLM lớn thường giỏi hơn nhưng đắt:

- cần GPU mạnh hoặc API;
- latency cao;
- khó triển khai ở từng tổ chức nhỏ.

SLM nhỏ rẻ hơn:

- có thể chạy local;
- ít VRAM hơn;
- phù hợp enterprise/on-premise.

Mục tiêu của FedICL-SQL:

> Dùng LLM teacher để truyền tri thức SQL cho nhiều SLM students, sao cho SLM chạy tốt hơn nhưng vẫn rẻ hơn LLM-only.

Đây chính là RQ3 của outline:

> LLM-to-SLM knowledge transfer có đạt trade-off tốt hơn giữa accuracy và efficiency không?

---

## 3. 🔴 In-Context Learning là gì?

ICL nghĩa là model học từ ví dụ đặt ngay trong prompt, không update weights.

Prompt Text-to-SQL thường có dạng:

```text
Instruction:
You are an SQL expert. Output only SQL.

Schema:
CREATE TABLE singer (...);
CREATE TABLE concert (...);

Examples:
Q: How many singers are there?
SQL: SELECT count(*) FROM singer

Q: List singer names.
SQL: SELECT name FROM singer

Target question:
How many concerts are there?

SQL:
```

Model nhìn instruction, schema, examples, rồi sinh SQL cho target question.

Công thức trong Light-SQL [4]:

```text
prompt = question + schema + instruction + demonstrations
```

Hay viết gọn:

```text
σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q
```

Trong đó:

- `q`: câu hỏi cần trả lời;
- `S`: schema của target database;
- `I`: instruction;
- `Q`: các demo examples.

Điểm cần nhớ:

- ICL không train model.
- Chất lượng demo quyết định rất nhiều.
- `k=1` đến `k=3` demos thường tốt.
- Quá nhiều demos có thể làm model rối hoặc vượt context.

Trong project này, ICL dùng để trả lời RQ2:

> Schema-aware ICL có giúp Text-to-SQL tốt hơn không?

---

## 4. 🔴 Retrieval: chọn demo nào để đưa vào prompt?

Không thể đưa toàn bộ examples vào prompt. Ta phải chọn vài demo phù hợp nhất.

Quy trình retrieval:

```text
1. Encode mỗi question trong example store thành vector embedding.
2. Lưu vector vào FAISS.
3. Với question mới, encode nó thành vector.
4. Tìm top-k examples gần nhất.
5. Đưa top-k examples vào prompt.
```

Ví dụ target question:

```text
"How many accounts do we have?"
```

Retriever có thể chọn demo gần:

```text
Q: How many singers are there?
SQL: SELECT count(*) FROM singer
```

vì cả hai đều có pattern `How many ...`.

Tool dùng trong project:

- `BAAI/bge-small-en-v1.5` để tạo embeddings;
- FAISS để tìm nearest neighbors;
- cosine similarity trên vector đã normalize.

---

## 5. 🔴 Masking dùng để làm gì?

Masking nghĩa là thay tên bảng/cột thật bằng token giả.

Ví dụ:

```sql
SELECT account_id, account_name FROM Accounts
```

thành:

```sql
SELECT col1, col2 FROM tbl1
```

Ban đầu project thử đưa masked demos trực tiếp vào prompt. Cách đó fail.

Lý do:

```text
Prompt demo:
SQL: SELECT count(*) FROM tbl1

Model output:
SELECT count(*) FROM tbl1
```

Nhưng `tbl1` không tồn tại trong database thật, nên SQL không execute được.

Kết luận sau P1 attempt 1:

> Không đưa masked SQL demo trực tiếp vào prompt sinh SQL.

Cách dùng đúng hơn:

```text
Masking chỉ dùng cho retrieval similarity hoặc privacy analysis.
Prompt generation dùng unmasked demos, và demos phải schema-relevant.
```

Nói đơn giản:

- Masking giúp tìm pattern giống nhau.
- Nhưng khi model cần sinh SQL thật, nó cần thấy tên bảng/cột thật của target schema hoặc demo cùng schema.

---

## 6. 🔴 Federated Learning trong đề tài này là gì?

Federated Learning nghĩa là nhiều client cùng cải thiện hệ thống mà không gộp dữ liệu thô về một nơi.

Trong enterprise setting:

```text
Client 1: database riêng, schema riêng, examples riêng
Client 2: database riêng, schema riêng, examples riêng
Client 3: database riêng, schema riêng, examples riêng
```

Ràng buộc:

```text
Không gửi raw rows.
Không gửi private database.
Không gửi toàn bộ model weights nếu không cần.
```

RQ1 hỏi:

> FedICL-SQL có cải thiện Text-to-SQL trong federated environments không?

Nói đơn giản:

```text
Mỗi client chạy riêng lẻ
vs
Các client tham gia FedICL-SQL
```

Nếu FedICL-SQL có EX cao hơn SLM-only local, RQ1 có kết quả tích cực.

---

## 7. 🔴 Update quan trọng: P1 cũ sai ở đâu?

P1 attempt 1 dùng ý tưởng:

```text
client góp masked demos vào global store G
server aggregate G
client retrieve demos từ G
test trên held-out databases
```

Kết quả TEST A1:

| Setting | EX |
|---|---:|
| Zero-shot, G OFF | 50.0% |
| Unmasked cross-DB demos | 43.3% |
| Masked cross-DB demos, G ON | 3.3% |

Hai nguyên nhân:

1. Model copy `tbl1`, `col1` từ masked demos, làm SQL không execute được.
2. Demo từ database khác gây nhiễu vì SQL gắn chặt với schema.

Vì vậy, global masked demo-store `G` không còn là trung tâm của project.

Đây là bài học quan trọng:

> Text-to-SQL không giống classification/QA thông thường. SQL phụ thuộc rất mạnh vào schema. Không thể kỳ vọng demo từ schema bất kỳ transfer trực tiếp sang schema khác.

---

## 8. 🔴 Hướng mới: teacher-centric FedICL-SQL

Sau update 2026-06-09, hướng chính là:

```text
LLM teacher → SLM students
```

Không còn lấy masked demo-store làm federation engine chính.

Có 3 thành phần:

### 8.1 Parametric teacher-KD là engine chính (= FedCoLLM [8] cho SQL)

Server có LLM teacher. Ta dùng một shared public NL-to-SQL set `X`.

Quy trình (parametric, đúng theo Fig.1):

```text
1. Teacher (Qwen2.5-72B) sinh SQL chất lượng cao trên X (offline, cache).
2. Exec-filter: chỉ giữ teacher SQL chạy được (đây là "execution loss" của Fig.1 —
   thực ra là bước LỌC target, KHÔNG phải loss gradient).
3. Mỗi client LoRA-train SLM bằng HAI phần:
   L_i = L_sup(Qᵢ riêng) + L_KD(X công khai)
   - L_sup = CE trên (q, gold-SQL) RIÊNG của client (own schema, không rời máy)
   - L_KD  = CE(teacher) + λ·KL(τ) + β·skeleton-CE, trên X, target đã exec-filter
4. Client upload LoRA deltas (mã hóa, nén, DP-noise) — KHÔNG gửi data/schema.
5. Server FedAvg/SecureAvg các LoRA adapters → Global SLM M_G.
6. Broadcast M_G về clients.
7. Đánh giá M_G trên client own-schema held-out questions.
```

🔴 **Vì sao BẮT BUỘC có L_sup (train trên data riêng):** nếu mọi client chỉ train trên cùng tập `X` với cùng teacher target → các LoRA delta giống hệt nhau → `FedAvg ≈ một client train một mình` → federation vô nghĩa → RQ1 chết. Phần data riêng `Qᵢ` làm delta mỗi client KHÁC nhau → FedAvg mới gộp được kỹ năng SQL của nhiều tổ chức vào `M_G`. Đây đúng là cơ chế FedCoLLM [8] (client có data riêng; `X` chỉ là môi trường KD).

Vì sao không vướng tường schema của attempt 1: KD dạy **kỹ năng SQL tổng quát** (JOIN/agg/nesting), không phải schema cụ thể. Schema-specific do **local ICL** lo lúc inference. Weights mang skill, không mang schema.

⚠️ **`skeleton-CE` (Structure loss) là gì:** weighted CE trên các token cấu trúc SQL (`SELECT/FROM/JOIN/WHERE/GROUP BY/agg`), bỏ identifier. Phạt việc sai *hình dạng* query. Đây là CE bình thường → backprop được. KHÔNG phải AST-edit-distance (rời rạc, không backprop được). Novelty của ta = exec-filter-trong-vòng-federated + skeleton loss; **execution-guidance bản thân nó là prior art**, đừng claim là mới.

Điểm privacy:

- `X` là public/shared, không phải private examples của client.
- Client không gửi raw rows / private schema.
- Chỉ LoRA deltas (mã hóa + DP) ra khỏi client — xem §11.

**Lưu ý cơ chế:** FedAvg-LoRA + Global SLM = **FedCoLLM [8]**. KHÔNG phải FedMKT [7] — [7] share *logits* (logit-space), không FedAvg weights; [7] dùng cho P2 (logit-KD + MinED).

### 8.2 Local schema-aware ICL cho RQ2

Mỗi client vẫn dùng ICL local:

```text
target question
+ target schema
+ retrieved local demos
→ SLM sinh SQL
```

Masking chỉ dùng cho retrieval nếu cần. Prompt dùng unmasked demos.

### 8.3 Fed-ICL answer fusion là baseline parameter-free (KHÔNG phải engine chính)

Fed-ICL [5] không share demos. Nó share answers.

Quy trình variant:

```text
1. Server có shared query.
2. Mỗi client dùng model/local context để trả lời.
3. Server fuse các answers bằng vote/Fusion-LM/execution vote.
4. Kết quả fused được dùng ở round sau.
```

Điểm khác với P1 cũ:

```text
P1 cũ: share demos
Plan mới: share answers hoặc teacher signals
```

---

## 9. 🟡 Knowledge Distillation là gì?

Knowledge Distillation, viết tắt KD, là cách để model nhỏ học từ model lớn.

Trong project này:

```text
Teacher = LLM lớn
Student = SLM nhỏ
```

Có ba mức KD (từ chính → phụ → nâng cao):

### 9.1 Sequence/LoRA KD — engine chính, P1′ (= FedCoLLM [8])

Student **LoRA-train** trên **data riêng `Qᵢ` (supervised) + public set `X` (KD từ teacher)**. Đây là engine chính, làm **trước** (đúng Fig.1).

```text
L_i = L_sup(Qᵢ)  +  L_KD(X)
  L_sup: CE trên (q, gold-SQL) RIÊNG của client     ← làm delta mỗi client KHÁC nhau
  L_KD : CE(teacher SQL, exec-filtered) + λ·KL + β·skeleton-CE  trên X
→ FedAvg các adapters → Global SLM M_G
```

🔴 Nhắc lại: thiếu `L_sup` (chỉ train trên `X`) → mọi delta giống nhau → FedAvg vô nghĩa → RQ1 chết. Data riêng là thứ làm federation có ý nghĩa.

Cần: LoRA adapter (`peft`), 4-bit quantization (QLoRA). **Không** cần logit alignment (vì train trên SQL string, không phải token logits).

### 9.2 Demo-level KD — variant parameter-free (so sánh rẻ)

Teacher SQL dùng như demonstration/ICL example cho student, **không train weights**. Đơn giản, dùng làm comparator rẻ cho 9.1.

```text
Teacher SQL trên X → đưa vào ICL prompt làm high-quality demo
Không update weights
```

### 9.3 Logit-level KD + MinED — P2 enhancement (= FedMKT [7])

Phức tạp hơn 9.1: student bắt chước **distribution/logits** của teacher (soft targets, temperature τ). Cần **tokenizer alignment MinED** [7] vì teacher (Qwen) và student (Phi) tokenize khác nhau.

Đây là **P2**, làm sau khi 9.1 đã validated.

---

## 10. 🟡 LoRA, QLoRA, quantization

Các khái niệm này phục vụ phần parametric KD.

| Khái niệm | Ý nghĩa |
|---|---|
| Quantization | Nén model weights, ví dụ 4-bit, để giảm VRAM |
| LoRA | Freeze model chính, chỉ train adapter nhỏ |
| QLoRA | LoRA trên model đã quantize 4-bit |

Vì sao cần?

```text
Phi-3-mini/Gemma/TinyLlama có thể chạy hoặc tune rẻ hơn.
Client không cần train full model.
Server có thể aggregate adapter deltas thay vì full weights.
```

Trong P1′, project ưu tiên:

```text
parametric LoRA-KD (sequence-level) + FedAvg → Global SLM   ← engine chính
```

Demo-level KD = variant rẻ; logit-KD + MinED = P2 làm sau.

---

## 11. 🟡 Privacy trong project này

Privacy claim mới (RE-ALIGNED theo Fig.1 — quan trọng):

```text
KHÔNG truyền raw rows.
KHÔNG truyền private database / private schema.
Private examples nằm local.
NHƯNG: engine parametric CÓ truyền LoRA-delta weights
       (đã mã hóa + nén + DP-noise). KHÔNG phải full weights.
```

> ⚠️ Đừng claim "no weights leave the client" — Fig.1 ghi rõ "Weights Only" upload. Claim đúng: *"no raw data/schema leaves; chỉ LoRA deltas đã mã hóa + DP-perturbed được truyền."* Boundary privacy là **data/schema** ở local, không phải weights.

DP (Differential Privacy — gradient perturbation) là cơ chế privacy first-class trong Fig.1 (DP-SGD trên LoRA deltas). Không ref nào ([5][7][8]) dùng DP → đây là novelty của ta. ⚠️ **Chỉ được claim DP là contribution NẾU đo được** — phải report đường (ε, EX-cost) + chạy F5 attack khi DP bật. Nếu không đo, hạ DP xuống "future work", đừng để là đóng góp chính.

Masking không còn là claim chính cho mọi thứ. Masking chỉ là cơ chế hỗ trợ:

- retrieval similarity;
- giảm rủi ro lộ identifier nếu cần;
- privacy analysis phụ.

Không nên claim quá mạnh như:

```text
masked demos đảm bảo privacy tuyệt đối
```

Nên claim:

```text
privacy-aware / privacy-preserving under the chosen communication protocol,
because raw rows and private schemas are not centrally pooled.
```

Nếu làm privacy experiment:

- prompt-extraction attack;
- schema reconstruction attack;
- so sánh with/without masking nếu có.

---

## 12. 🔴 RQ1, RQ2, RQ3 hiểu thế nào?

### RQ1: Federated Learning effectiveness

Câu hỏi:

```text
FedICL-SQL có cải thiện Text-to-SQL trong federated environments không?
```

So sánh:

```text
SLM-only local
vs
FedICL-SQL teacher-KD / answer fusion
```

Metric:

- EX;
- EM;
- convergence;
- communication cost.

### RQ2: In-Context Learning effectiveness

Câu hỏi:

```text
Schema-aware ICL có giúp model sinh SQL tốt hơn không?
```

So sánh:

```text
without ICL
vs
local schema-aware ICL
```

Ablation:

```text
k = 0, 1, 3, 5
```

Lưu ý:

> Không nên hiểu RQ2 là demo từ schema ngẫu nhiên phải transfer tốt sang database hoàn toàn khác. P1 attempt 1 cho thấy cách *share demo* đó không ổn.
>
> NHƯNG cross-schema generalization vẫn là **claim chính của RQ2** (đúng outline RQ2 + Fig.1 innovation #4) — chỉ là làm qua đường **khác**: `M_G` mang kỹ năng SQL tổng quát (skill transfer được), schema mới do **local ICL** trên vài demo của chính schema đó lo. Test: `M_G` EX trên held-out unseen schema vs SLM-only. Đường parametric này mới defensible; đường share-demo (attempt-1) thì không.

### RQ3: LLM-to-SLM transfer and efficiency

Câu hỏi:

```text
LLM teacher có giúp SLM student tốt hơn với chi phí thấp hơn LLM-only không?
```

So sánh:

```text
SLM-only
vs
SLM + teacher KD
vs
LLM-only
```

Metric:

- EX/EM;
- latency;
- VRAM;
- FLOPs hoặc cost proxy.

---

## 13. 🔴 Toolchain cần biết

| Tool | Dùng để làm gì |
|---|---|
| `transformers` | Load và generate với LLM/SLM |
| `sentence-transformers` / BGE | Encode text thành embedding |
| FAISS | Vector retrieval top-k demos |
| `sqlglot` | Normalize/parse SQL cho EM |
| SQLite | Execute predicted/gold SQL cho EX |
| `peft` | LoRA adapter |
| `bitsandbytes` | 4-bit quantization trên CUDA |
| Flower hoặc custom loop | Mô phỏng federated rounds |

Trong repo hiện tại, P0 đã có:

- Spider loader;
- retriever;
- prompt builder;
- student model wrapper;
- EX/EM evaluator.

P1 attempt 1 đã có thêm:

- partition;
- masking;
- aggregation;
- round-loop prototype.

Nhưng round-loop demo-store cũ cần được thay bằng P1′ theo plan mới.

---

## 14. 🟢 Glossary nhanh

| Từ | Nghĩa |
|---|---|
| Shot | Một example trong prompt |
| Zero-shot | Không có example |
| Few-shot | Có vài examples |
| Context window | Số token tối đa model đọc được |
| Temperature | Độ ngẫu nhiên khi generate, Text-to-SQL thường để 0 |
| DDL | Cách mô tả schema bằng `CREATE TABLE ...` |
| Embedding | Vector biểu diễn text |
| Retrieval | Tìm examples liên quan |
| KD | Knowledge Distillation, model nhỏ học từ model lớn |
| Logits | Điểm số trước softmax của mỗi token |
| Round | Một vòng đồng bộ trong federated setting |
| Non-IID | Dữ liệu các client khác phân phối nhau |
| Dirichlet alpha | Tham số điều khiển mức heterogeneity khi partition |

---

## 15. Đọc gì trước?

Thứ tự đọc nên là:

1. **Light-SQL [4]**

   Để hiểu single-client Text-to-SQL bằng SLM + ICL + retrieval.

2. **Outline của thầy**

   Để nhớ project không chỉ là ICL, mà là LLM-SLM federated framework.

3. **FedCoLLM [8]** ← đọc kỹ, đây là engine anchor

   LoRA-adapter FedAvg + Global SLM + KD (CE+λKL). Engine parametric của ta = FedCoLLM áp cho SQL.

4. **FedMKT [7]**

   Logit-space KD + MinED token alignment. Lưu ý: [7] share *logits*, KHÔNG FedAvg weights → dùng cho **P2**, không phải engine chính.

5. **Fed-ICL [5]**

   Answer fusion / parameter-free federated ICL = **baseline** của ta. Lưu ý: Fed-ICL share answers, không phải share SQL demos như P1 attempt 1. QA chứ không phải SQL.

6. **fig1_architecture.md + detailed_plan.md**

   Fig1.md = cơ chế kiến trúc (đọc trước để nắm engine parametric). Detailed-Plan = kế hoạch build + experiment; đọc banner REVISION 2026-06-09 trước.

---

## 16. Tóm tắt một câu

FedICL-SQL sau update nên được hiểu là:

> Một framework Text-to-SQL trong đó server LLM teacher distill kỹ năng SQL vào nhiều client SLM students: mỗi client **LoRA-train trên data riêng `Qᵢ` + public set `X` với teacher SQL**, server **FedAvg các adapters → Global SLM** (parametric, = FedCoLLM cho SQL); mỗi client dùng **schema-aware ICL local** để sinh SQL trên schema riêng. Chỉ **LoRA-delta weights (mã hóa + DP)** ra khỏi client — raw data/schema luôn ở local. Demo-level KD + Fed-ICL answer-fusion là variant/baseline parameter-free, không phải engine chính.

(Phần data riêng `Qᵢ` là bắt buộc — nếu chỉ train trên `X` thì FedAvg vô nghĩa. Mọi số liệu báo cáo cần ≥3 seed + test ý nghĩa thống kê. Baseline ceiling thật của method parametric = **Centralized-FT**, không phải Centralized-ICL.)
