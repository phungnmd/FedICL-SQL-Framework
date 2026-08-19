# DAIL-SQL vs CodeS — Prompt & Retrieval Methods

Tóm tắt kỹ thuật prompt construction + demo retrieval của 2 paper tham chiếu, để
tra cứu khi viết §3 Method hoặc §2 Related Work. Cả 2 đã implement trong
`fedicl-sql` (`--retrieval`, `--schema-style`) — xem cuối file.

- DAIL-SQL: [9] trong `system_architecture.md`/`CLAUDE.md`, file nguồn
  `paper/references/md/[9]-DAIL-SQL.md`.
- CodeS: chưa có số `[n]` cố định trong danh sách chính (không nhầm với [10]
  = KID). arXiv 2402.16347, SIGMOD 2024, GitHub `RUCKBReasoning/codes`. Entry
  ngắn đã có ở `related_papers.md`; file này mở rộng chi tiết prompt method.

---

## 1. DAIL-SQL

Không có model riêng — thuần prompt-engineering, cắm vào bất kỳ LLM nào (họ
test GPT-3.5, GPT-4, LLaMA, Vicuna, Alpaca). 3 trục quyết định:

### 1.1 Question representation
Benchmark 5 kiểu biểu diễn schema/prompt trên Spider-dev zero-shot:
Basic Prompt, Text Representation, **Code Representation (DDL `CREATE TABLE`
đầy đủ)**, OpenAI Demonstration Prompt, Alpaca SFT Prompt. **Code
Representation thắng ổn định nhất** ở mọi LLM — do model pretrain trên code
đã quen cú pháp DDL.

### 1.2 Example selection — "DAIL Selection"
Kết hợp 2 tín hiệu:
- **Masked Question Similarity (MQS)**: mask token khớp schema (bảng/cột) +
  giá trị cell trong câu hỏi thành placeholder, rồi so cosine embedding —
  tránh retrieval bias theo tên bảng/cột cụ thể.
- **Query-similarity gate**: sinh trước 1 SQL nháp cho câu hỏi target (draft
  pass), skeleton hoá, giữ lại demo có SQL-skeleton Jaccard-similar với
  skeleton nháp đó ở ngưỡng τ (mặc định 0.85) — ưu tiên demo có *cấu trúc SQL*
  giống câu trả lời dự kiến, không chỉ giống câu hỏi.

### 1.3 Example organization
Xếp demo theo thứ tự similarity **tăng dần**, demo giống nhất nằm **cuối cùng**
— sát câu hỏi thật nhất, tận dụng recency bias của LLM.

**Đặc điểm quan trọng:** không có schema filter, không có value retriever —
vì target là LLM lớn (context to), Spider DB nhỏ, không cần nén/cắt schema.

---

## 2. CodeS

Có model riêng (StarCoder incremental-pretrain trên corpus SQL-centric, 1B–15B)
+ pipeline prompt construction riêng, dùng được cả SFT lẫn ICL.

### 2.1 Prompt construction (§6, 3 phần độc lập)

1. **Schema filter** — 1 classifier nhỏ train riêng theo dataset, chấm
   relevance bảng/cột theo câu hỏi, giữ top-k1 bảng + top-k2 cột/bảng. Lúc
   train: dùng gold SQL để đảm bảo bảng/cột đúng luôn có mặt, pad thêm
   bảng/cột random cho đủ ngưỡng (mô phỏng noise của filter thật lúc test).
   Giải quyết vấn đề bảng rộng/nhiều bảng (đặc thù BIRD, không phải Spider).
2. **Value retriever** — BM25 lọc thô hàng trăm giá trị nghi ngờ trong toàn
   DB, rồi LCS (longest common substring) tính khớp tinh với câu hỏi, giữ giá
   trị khớp nhất → khối `matched values:` trong prompt. Coarse-to-fine để
   tránh chạy LCS trên hàng triệu giá trị (BIRD có DB tới 116.5M giá trị).
3. **Metadata** — mỗi cột: type, comment (tên cột tự nhiên từ `tables.json`,
   không phải tên cột gốc), 2 representative values
   (`SELECT DISTINCT col LIMIT 2`), primary/foreign keys.

Prompt mẫu (Fig.2/Fig.4 CodeS):
```
table movie , columns = [ movie.mid ( int | primary key | comment : movie id | values : 101 , 102 ) , ... ]
foreign keys :
rating.mid = movie.mid
matched values :
reviewer.name ( Sarah Martinez )
Question: ...
```

### 2.2 Few-shot ICL retriever (§8.2) — đã verify bằng source code thật

Paper viết "stripping entities" — **verify bằng GitHub
(`RUCKBReasoning/codes/text2sql_few_shot.py`) cho thấy khác**: không dùng NER,
dùng **POS-tag masking qua nltk** (`extract_skeleton()`):
- Token có tag `NN, NNP, NNS, NNPS, CD, SYM, FW, IN` → mask thành `_`.
- Một số token dấu câu (`$ '' ( ) , -- . :`) bị loại hẳn.
- Còn lại (verb, wh-word, conjunction...) giữ nguyên → thành "skeleton" câu hỏi.

Score chọn demo (`np.maximum(...)` trong code, Eq.4 trong paper):
```
score = max( sentsim(question, demo_question),
             sentsim(question_skeleton, demo_question_skeleton) )
```
Encoder: SimCSE (`princeton-nlp/sup-simcse-roberta-base`), không phải
sentence-transformers thường.

**ICL prompt của CodeS CÓ chứa schema** — mỗi demo tự mang `schema_sequence +
content_sequence` (matched values) của **chính DB nó**, không chỉ (question,
SQL) trơn; target cũng có schema+matched-values riêng ở cuối, không SQL (để
model sinh).

### 2.3 SFT (không chỉ ICL)
Input = db_prompt (schema filter + value retriever + metadata) ⊕ question,
target = SQL. Inference: beam search 4 candidate, chọn candidate đầu tiên
**chạy được** (executable) làm output cuối — không chỉ lấy top-1 mù quáng.

---

## 3. So sánh trực tiếp

| | DAIL-SQL | CodeS |
|---|---|---|
| Loại | kỹ thuật prompt thuần, cắm vào LLM bất kỳ | model riêng + pipeline prompt riêng |
| Schema representation | DDL đầy đủ (Code Representation thắng benchmark) | metadata nén (type\|PK\|comment\|values) |
| Cắt bớt schema? | không | có (schema filter, cho DB rộng — BIRD) |
| Value grounding | không | có (matched values, BM25+LCS) |
| Demo selection | Masked Question Similarity + skeleton query-sim gate (cần 1 draft-SQL pass) | POS-tag skeleton (nltk) + SimCSE, max của 2 similarity, single-pass |
| Demo có mang schema? | tùy ablation (mặc định KHÔNG — tránh cross-schema bleed) | CÓ, mặc định — mỗi demo tự mang schema+matched-values riêng |
| Target dùng cho | LLM lớn, ICL-only, không finetune | model nhỏ, SFT là chính, ICL là fallback |

**Không có so sánh số liệu trực tiếp giữa 2 phương pháp** — 2 paper không chạy
chung 1 base LLM. CodeS's Table 5/6 so SFT-CodeS với DAIL-SQL+GPT-4 nhưng
confound nhiều biến (fine-tune vs ICL-only, size model, không chỉ khác prompt).

---

## 4. Implement trong `fedicl-sql`

Commit `4e790f4` (2026-07-09):
- `--retrieval codes` — port `extract_skeleton()` thật (không phải NER), dùng
  `bge-small` encoder (không phải SimCSE, giữ nhất quán với `dail_select`/
  `question` để so sánh công bằng retrieval-strategy, không lẫn encoder).
- `--schema-style codes` — metadata (type\|PK\|comment\|values+FK), Spider-scoped
  (bỏ schema-filter classifier — không cần cho DB nhỏ; bỏ BM25, brute-force
  substring match trực tiếp — DB đủ nhỏ).
- `demo_style=with_schema` giờ nhận `schema_style` — demo tự mang
  schema+matched-values riêng theo đúng style target, khớp thiết kế CodeS
  §8.2 (trước đó hardcode DDL, bug đã sửa).

Chưa implement: schema-filter classifier (CodeS §6.1) — quyết định bỏ vì
Spider DB nhỏ (≤28 bảng), ablation gốc của CodeS cũng cho thấy phần này chủ
yếu cứu BIRD.
