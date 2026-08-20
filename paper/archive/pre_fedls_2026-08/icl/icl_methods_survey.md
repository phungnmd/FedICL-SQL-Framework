# ICL cho Text-to-SQL — Tổng hợp phương pháp & bản đồ so sánh giữa các paper

> Viết 2026-07-11. Mục đích: một chỗ duy nhất tra cứu các phương pháp ICL
> (chọn demo, nguồn demo, tổ chức prompt, chính sách dùng demo) khi viết
> §2 Related Work / §5 Analysis. Kèm bản đồ "paper nào compare paper nào"
> với số thật, và đối chiếu với kết quả nội bộ của repo này.
>
> Chi tiết kỹ thuật DAIL vs CodeS đã có riêng ở `dail_vs_codes_prompt_methods.md`
> — file này không lặp lại, chỉ đặt cả hai vào bức tranh chung.

---

## 1. Taxonomy — 4 trục quyết định của một hệ ICL

Mọi phương pháp ICL text-to-SQL khác nhau trên 4 trục độc lập:

| Trục | Câu hỏi | Các lựa chọn đã thấy trong lit |
|---|---|---|
| **A. Cách chọn demo** | rank demo theo tín hiệu gì? | question embedding thô → masked question (DAIL) → skeleton câu hỏi (CodeS, De-semanticization) → dual question+query sim (DAIL) → AST của SQL (ASTRES) → schema-link graph (DCG-SQL) → learned retriever (MARLO) |
| **B. Nguồn demo** | demo lấy từ đâu? | train pool cross-domain (mặc định mọi người) → synthetic in-domain (ODIS) → tự sinh cho chính test question (SAFE-SQL) |
| **C. Tổ chức prompt** | demo trình bày thế nào? | thứ tự (DAIL: giống nhất đặt cuối) · số lượng k · demo có mang schema riêng không (CodeS: có; DAIL: không) |
| **D. Chính sách dùng** | dùng demo LÚC NÀO? | uniform (mọi query — mặc định toàn bộ lit) → **gated/selective (chỉ khi draft không đáng tin — finding của repo này, chưa thấy paper nào làm)** |

Điểm mấu chốt cho paper của mình: **toàn bộ literature dồn vào trục A** (chọn
demo tốt hơn), trục D thì chưa paper nào làm. Data nội bộ (LAB_LOG
2026-07-09/10 — phạm vi hẹp: Spider dev, 1 seed/arm, chủ yếu Qwen) quan sát
thấy uniform ICL net âm trên các arm đã FT/KD đã test, còn exec-gate dương
6/6 arm. Đây là **quan sát trong phạm vi test hiện tại, chưa đủ để khẳng định
thành luật** — nhưng khoảng trống trục D trong lit là thật, và là chỗ mình đứng.

---

## 2. Từng phương pháp — tóm tắt 1 đoạn

### DAIL-SQL — [9] trong repo (arXiv 2308.15363, VLDB 2024)
Thuần prompt engineering, cắm vào LLM bất kỳ. Chọn demo bằng **dual
similarity**: masked-question embedding (mask tên bảng/cột → placeholder) +
query-similarity gate (draft SQL trước, skeleton hoá, giữ demo có skeleton
Jaccard ≥ τ). Demo format `question + SQL` trơn, không DDL. Là ICL method
**locked** của architecture (`system_architecture.md` §5.2). Cần 1 draft pass
→ đắt gấp đôi khi chạy uniform, nhưng **trong exec-gate của mình draft k=0 có
sẵn → chi phí phụ ≈ 0**.

**So sánh trong paper (đọc kỹ, verify ar5iv):**

- *Selection benchmark nội bộ* (Spider dev, GPT-4, 1-shot EX): Random 41.7 →
  Question Similarity 53.3 → **Masked** Question Similarity 58.2 → DAIL
  Selection **62.1** (3-shot 69.1, 5-shot 71.9). Pattern giữ trên GPT-3.5 /
  text-davinci-003 / Vicuna-33B. ⚠️ Đây là số lit trực tiếp cho câu hỏi A5
  "question-sim thường vs DAIL" — nhưng đo trên **base/API model chưa FT**;
  cột FT-model + trong-gate vẫn chỉ repo mình có.
- *Organization benchmark*: Full-Information (demo mang schema) vs SQL-only
  vs DAIL Organization (question+SQL, bỏ schema) — DAIL Org thắng về
  hiệu quả token; khớp kết quả with_schema nội bộ của mình.
- *End-to-end systems*: DIN-SQL, C3/STRIKE, CBR-ApSQL.
- *LLM phủ*: GPT-4/3.5/davinci + LLaMA/LLaMA-2 (7–70B), Vicuna, Falcon,
  CodeLLaMA — nhưng toàn zero-FT.

### CodeS (arXiv 2402.16347, SIGMOD 2024)
Model riêng (StarCoder pretrain tiếp trên corpus SQL) + pipeline prompt:
schema filter, value retriever (BM25+LCS), metadata schema. Retrieval ICL:
POS-tag skeleton (nltk) + SimCSE, `max(sentsim(q,q'), sentsim(skel,skel'))`,
single-pass (không cần draft). Demo **có mang schema riêng**. Đã port vào
`fedicl-sql` (`--retrieval codes`, `--schema-style codes`).

### ACT-SQL (arXiv 2310.17342, EMNLP 2023 Findings)
Auto-CoT cho text-to-SQL: tự sinh chain-of-thought cho demo, chọn demo bằng
hybrid similarity. Xuất hiện làm baseline trong cả DCG-SQL lẫn SAFE-SQL.
Hướng CoT đã bị repo này drop (2026-07-07) — chỉ cite.

### DIN-SQL (arXiv 2304.11015, NeurIPS 2023)
Decomposed ICL: chia bài toán thành schema-linking → classification →
generation → self-correction, mỗi bước prompt riêng với demo cố định
(không retrieval động). Baseline phổ biến; yếu hơn các method retrieval động
trên model nhỏ (số ở §3).

### PTD-SQL (arXiv 2409.14082, EMNLP 2024) — *thêm vì là baseline của SAFE-SQL*
Partition train data theo loại query (aggregation, join, nested...), soạn
"targeted drilling" demo riêng cho từng partition — demo chọn theo **loại
bài**, không theo similarity liên tục. GPT-4o Spider dev 85.7 (SAFE table).
Góc nhìn khác trên trục A: phân loại rời rạc thay vì ranking.

### DEA-SQL (arXiv 2402.10671, ACL 2024 Findings) — *baseline của SAFE-SQL*
Workflow decomposed kiểu DIN nâng cấp: information determination (bỏ thông
tin thừa) → phân loại bài → prompt theo loại → self-correction + active
learning. GPT-4o Spider dev 85.6 (SAFE table). Họ hàng DIN, không phải
retrieval động.

### C3 (arXiv 2307.07306) — *baseline zero-shot chuẩn*
Zero-shot ChatGPT: Clear Prompting + Calibration with Hints + Consistent
Output (self-consistency voting). Spider test 82.3 **không cần demo nào** —
mốc quan trọng: zero-shot tốt đã ~82 trên GPT-class, làm mọi gain ICL trên
API-model khó diễn giải; trên student 1.5B của mình khoảng trống lớn hơn nhiều.

### SENSE (arXiv 2408.03256) — *nghi là "Syn-SQL" trong bảng SAFE-SQL, chưa verify*
"Synthesizing Text-to-SQL Data from Weak and Strong LLMs".
SFT model mở trên data synthetic (strong LLM sinh + weak LLM sinh lỗi làm
preference data). BIRD: hơn DAIL-SQL+GPT-4 5.98pp test. Thuộc trục "thay ICL
bằng SFT trên synthetic data" — liên quan Text2SQL-Flow, và là ref khi bàn
pool `P` synthetic.

### DCG-SQL (arXiv 2505.19956, ACL 2025)
Dựng **Deep Contextual schema-link Graph** giữa question và schema elements,
retrieval demo trên biểu diễn graph đó. Claim trung tâm: các method chọn demo
cũ (DAIL, ACT) gần như **không cải thiện khi LLM nhỏ** — retrieval graph của
họ mới làm ICL có ích ở small LLM (Llama 3.2-3B, DeepSeek-Coder-6.7B,
Llama 3.1-8B). **Căng trực tiếp với quan sát gate của mình** (xem §4).

**So sánh trong paper:**

- *ICL baselines*: DIN-SQL, ACT-SQL, DAIL-SQL, ASTRES. *Fine-tuned refs*:
  Graphix-T5, RESDSQL.
- *Số EX Spider dev trên small LLM (bảng đầy đủ)*:

  | Model | DIN | ACT | DAIL | DCG |
  |---|---|---|---|---|
  | Llama 3.1-8B | 67.4 | 75.0 | 71.2 | **82.1** |
  | DeepSeek-Coder-6.7B | 72.6 | 74.2 | 73.4 | **81.1** |
  | Llama 3.2-3B | 44.8 | 66.0 | 58.8 | **74.7** |

  (GPT-4: DCG 87.5 vs DAIL 82.8, ACT 83.9. Chú ý: DAIL < ACT trên cả 3 small
  model — thứ hạng selection method đảo theo model, không ổn định.)
- *Benchmarks*: Spider dev + Spider-DK/-Realistic/-Syn, BIRD (appendix) —
  rộng hơn hẳn các paper selection khác; Spider-Realistic trùng eval plan mình.
- *Ablation retrieval nội bộ*: question-embedding thô / masked-question /
  question+schema text / graph truyền thống → graph sâu của họ thắng.

### SAFE-SQL (arXiv 2502.11438, EMNLP 2025)
Bỏ hẳn retrieval từ train pool: LLM **tự sinh demo cho chính test question**
(cùng schema!), rồi lọc fine-grained theo 3 tiêu chí (semantic similarity,
structural alignment, reasoning-path quality; giữ điểm ≥ θ=8).
**Không cần execution lúc inference** → hợp constraint production của mình.
Demo cùng schema với question → schema bleed bất khả thi về cấu trúc.

**So sánh trong paper:**

- *Few-shot ICL*: DAIL-SQL, DIN-SQL, ACT-SQL, PTD-SQL, DEA-SQL.
- *Zero-shot*: C3-SQL. *SFT refs*: Syn-SQL (≈ SENSE? — id chưa verify từ
  chính PDF SAFE, đánh dấu khi cite), SQL-PaLM.
- *Số EX Spider dev (GPT-4o)*: SAFE **87.9** > PTD 85.7 > DEA 85.6 >
  DAIL 83.6. BIRD dev: SAFE 63.5 ≈ Syn-SQL 63.4.
- Lưu ý đọc số: mọi baseline đều chạy lại trên GPT-4o — so sánh cùng model,
  sạch hơn kiểu Table-5-của-CodeS; nhưng vẫn base model, không FT.

### ODIS (arXiv 2310.06302, EMNLP 2023)
Demo hybrid: out-of-domain (train pool thật) **+ synthetic in-domain** (sinh
trên chính DB đích). Finding gốc quan trọng: demo in-domain (cùng DB) là thứ
mang lại gain lớn; SQL distribution của demo quan trọng hơn surface question.
Spider +1.1 EX, KaggleDBQA +11.8 EX vs single-source. Tiền thân trực tiếp
của SAFE-SQL trên trục B.

**So sánh trong paper (verify ar5iv):**

- *Selection baselines*: Random · **SimNLQ** (question-embedding
  Sentence-BERT — chính là `--retrieval question` của mình) · **SimSQL**
  (similarity trên SQL dự đoán, BM25) · **CovSQL** (coverage-based cho demo
  synthetic) · out-of-domain-only · synthetic-in-domain-only.
- *Systems*: DIN-SQL (Codex 75.6 / GPT-4 82.8), LEVER 81.9, Self-Debugging
  84.1, SYNCHROMESH + SKILL-KNN (KaggleDBQA 43.0); SFT refs: T5+PICARD,
  RESDSQL+NatSQL 84.1, SmBoP, ShiP+PICARD.
- *ODIS đạt*: Codex 85.2 Spider / 54.8 KaggleDBQA; ChatGPT 81.5/52.9;
  CodeLlama 80.0/42.3.
- LLM: Codex, ChatGPT, CodeLlama — lại toàn base, không FT.

### MARLO (arXiv 2410.14049)
**Learned retriever**: train encoder align question ↔ SQL query trong một
embedding space chung, metadata-agnostic (né bias theo tên bảng/cột — cùng
động cơ với masked question của DAIL nhưng học được thay vì heuristic).
Không cần draft pass → **nhanh hơn** DAIL-style dual similarity.

**So sánh trong paper (verify ar5iv) — thang selection sạch nhất trong lit,
cùng 1 LLM (Claude 2.1), Spider dev / test EX:**

| Method | dev | test |
|---|---|---|
| Zero-shot | 67.5 | 69.0 |
| Random | 72.2 | 75.1 |
| Question Similarity (QS) | 73.5 | 75.1 |
| Masked QS (MQS, DAIL-style) | 75.3 | 78.0 |
| Skills Similarity (SS — LLM tóm tắt "skill" cần, retrieve theo đó) | 77.9 | 80.7 |
| **MARLO** | **80.8** | **81.2** |

→ Thang lit: Random < QS < MQS < SS < learned. Cùng chiều DAIL paper
(41.7 < 53.3 < 58.2 < 62.1 trên GPT-4). Vẫn: base model, không FT.

### ASTRES / AST-based ranking (arXiv 2407.03227)
Rank demo theo **AST của SQL** thay vì skeleton string Jaccard + schema
pruning. Baseline trong DCG-SQL. Cùng họ với query-sim của DAIL, tín hiệu
cấu trúc tinh hơn.

### De-semanticization + skeleton retrieval (Springer 2023)
Tiền thân của hướng skeleton: mask ngữ nghĩa domain khỏi câu hỏi, retrieve
theo skeleton. Cite làm gốc lịch sử của trục A.

### Họ federated ICL — [5] Fed-ICL, [6] IFed-ICL, FICAL (2412.08054)
ICL trong setting federated nhưng **không distill vào weights**: Fed-ICL [5]
answer-fusion parameter-free (QA); IFed-ICL [6] ICL-vector ngầm; FICAL truyền
"knowledge compendium" thay params. Khác lớp với mình (mình: ICL nhất quán
train/inference + KD server-side). Cite ở §2 nhánh federated.

### Survey nền
- Retrieved demonstrations for ICL: arXiv 2401.11624.
- Text-to-SQL in the LLM era: arXiv 2407.15186.

---

## 3. Bản đồ so sánh — paper nào compare paper nào, số thật

```
  DAIL-SQL ─ so nội bộ: Random / QuestionSim / MaskedQS / DAIL-Selection
             (+ systems: DIN-SQL, C3/STRIKE, CBR-ApSQL)

  DCG-SQL  ─ so: DAIL-SQL, ACT-SQL, DIN-SQL, ASTRES
             (+ SFT refs Graphix-T5, RESDSQL; ablation nội bộ: question-emb /
              masked-q / question+schema / graph thường)

  SAFE-SQL ─ so: DAIL-SQL, DIN-SQL, ACT-SQL, PTD-SQL, DEA-SQL, C3,
             Syn-SQL(SENSE?), SQL-PaLM — tất cả rerun trên GPT-4o

  MARLO    ─ so: Zero-shot / Random / QS / MQS(DAIL-style) / SkillsSim,
             cùng Claude 2.1 — thang selection sạch nhất lit

  ODIS     ─ so: Random / SimNLQ(question-sim) / SimSQL / CovSQL
             (+ systems: DIN-SQL, LEVER, Self-Debugging, SKILL-KNN)

  CodeS    ─ có DAIL-SQL+GPT-4 làm baseline Table 5 (Spider dev/test) + BIRD,
             nhưng chỉ HỆ-THỐNG-level (SFT CodeS vs DAIL+GPT-4 — confound
             model + SFT-vs-ICL + prompt format). KHÔNG có so sánh
             retrieval-level; ablation §8.2 chỉ so variant nội bộ.
             → duy nhất repo này có số retrieval-level DAIL-vs-CodeS (§3 dưới).
```

**Thang selection hội tụ trong lit (đều trên base model, chưa FT):**
`Random < QuestionSim < MaskedQS < structure/skill-aware (DAIL, SS, ASTRES)
< learned/graph (MARLO, DCG)` — nhất quán qua 3 paper đo độc lập (DAIL trên
GPT-4: 41.7→53.3→58.2→62.1; MARLO trên Claude 2.1: 72.2→73.5→75.3→77.9→80.8;
DCG trên 3 small LLM). Ngoại lệ: DCG đo được DAIL < ACT trên small LLM —
thứ hạng không ổn định theo model. Chưa paper nào đo thang này trên model
ĐÃ FT/distill, càng không trong gate — chỗ A5 của mình đứng.

### DCG-SQL vs baselines (Spider dev, EX)

| Model chạy | DCG-SQL | DAIL-SQL | ACT-SQL | DIN-SQL |
|---|---|---|---|---|
| Llama 3.1-8B | **82.1** | 71.2 | 75.0 | 67.4 |
| GPT-4 | **87.5** | 82.8 | 83.9 | — |

Đọc số này cẩn thận: khoảng cách DAIL↔DCG trên model nhỏ (−10.9) lớn bất
thường so với trên GPT-4 (−4.7). Claim của họ: demo-selection cũ vô dụng ở
model nhỏ. **Nhưng** setup của họ là base model chưa FT, không hề đo trên
model ĐÃ fine-tune — khác setup quan trọng khi đối chiếu với quan sát nội bộ
(vốn đo chủ yếu trên arm đã FT/KD).

### SAFE-SQL vs baselines (Spider dev, EX, GPT-4o)

| SAFE-SQL | PTD-SQL | DEA-SQL | DAIL-SQL |
|---|---|---|---|
| **87.9** | 85.7 | 85.6 | 83.6 |

(BIRD dev: SAFE 63.5 ≈ SYN-SQL 63.4.)

### MARLO (Spider, EX)
+2.9 vs generic embedding · +0.8 vs metadata-masking (DAIL-style) · latency
thấp hơn (single-pass).

### ODIS
Spider +1.1 · KaggleDBQA **+11.8** vs demo single-source. Gain lớn nhất khi
domain đích lạ — đúng logic in-domain.

### Số nội bộ repo (đọc kèm — cùng 1 stack, adapter mình train)

**Cập nhật 2026-07-12 — thang A5 đủ 4 chân, cả uniform lẫn gate, cả FT lẫn
4 base family.** Số đầy đủ + McNemar: LAB_LOG 2026-07-11 (4) và 2026-07-12;
bảng chính đã nằm trong `system_architecture.md` §5.2. Tóm tắt:

| So sánh (cùng adapter/model) | random | question | DAIL | codes |
|---|---|---|---|---|
| central_rkd 1.5B, exec-gate | 70.41 | **70.79** | 70.50 | 69.92 |
| central_rkd 1.5B, uniform k3 | **66.83** | 65.28 | 65.86 | — |
| 0.5B base, uniform k3 | **30.08** | 27.76 | 28.05 | 25.82 |
| 1.5B base, uniform k3 | 53.58 | 50.77 | **54.26** | 52.13 |
| gemma-2-2b base, uniform k3 | 49.52 | 47.78 | 50.77 | **50.97** |
| llama-3.2-1b base, uniform k3 | 35.69 | 30.46 | 35.01 | **37.23** |

→ dail-vs-random không significant ở đâu cả (p=0.20–1.00). **Không tồn tại
regime nào selection sophistication trả tiền** trong stack của mình. Repair
sets trong gate gần như disjoint giữa các bộ demo (all-4 chung 5/50) —
attribution: perturbation + exec-verify, không phải demo knowledge.

---

## 4. Đối chiếu với finding nội bộ — mình đứng đâu

1. **Cả lit đo ICL trên base/API model chưa FT.** DCG-SQL, SAFE-SQL, DAIL,
   ODIS — tất cả prompt model chưa fine-tune trên task. Quan sát nội bộ
   (phạm vi hẹp: Spider dev, 1 seed/arm, Qwen 0.5B/1.5B/7B + 1 arm Gemma):
   uniform ICL net âm trên các arm đã FT/KD đã test; gemma_ft +1.35 là ngoại
   lệ. **Chưa đủ phạm vi (1 dataset, 1 seed, 2 family) để khái quát "ICL giúp
   base, hại FT"** — ghi nhận là pattern cần kiểm chứng thêm (nhiều seed,
   Spider-Realistic, thêm family). Câu hỏi "ICL còn ích gì sau khi student đã
   FT/distill" vẫn chưa paper nào đụng — §5 khai thác dưới dạng phân tích
   per-arm có số, không phát biểu thành luật.

2. **DCG-SQL là paper phải phản biện trực tiếp** khi viết: reviewer sẽ nói
   "họ đã làm ICL work cho small LLM rồi". Trả lời: (a) small của họ = 3–8B
   base, không FT; (b) dail_select của mình đã là structural gate τ=0.85 mà
   73% broken rows vẫn có demo đúng shape trong prompt — bottleneck không
   phải chọn demo; (c) gate của mình lật dấu ở cả 7B teacher, thứ DCG không
   giải thích được.

3. **SAFE-SQL/ODIS là hướng build duy nhất đáng cân nhắc thêm** (trục B —
   đổi nguồn demo, diệt schema bleed tận gốc, không cần exec, federated-fit:
   client tự sinh trên schema riêng). Tier-2/3, cần advisor. MARLO/DCG (trục
   A) = cite + argue, không build — data mình nói trục A không phải đòn bẩy.

4. **Trục D (gated/selective ICL) trống trong lit** — không paper nào trong
   danh sách này gate việc CÓ đưa demo vào prompt hay không theo độ tin của
   draft. Execution-guided repair (MAC-SQL refiner, RSL-SQL retry-until-
   nonempty) là họ hàng gần nhất nhưng họ sửa SQL bằng vòng lặp reflection,
   không điều khiển sự hiện diện của demo. Vị trí novelty của mình nằm đây +
   phân tích "khi nào ICL giúp student đã distill".

---

## 5. Việc rút ra (đã nêu ở LAB_LOG/session, gom lại cho tiện)

- [ ] A5 mở rộng: chạy `--retrieval question` (uniform + gate) trên
      central_rkd → lấp cột trống §3; thang random/question/dail/codes.
- [ ] Mở rộng phạm vi trước khi viết bất kỳ câu khái quát ICL-sau-FT nào:
      nhiều seed, Spider-Realistic, thêm model family; recheck gemma_ft +1.35.
- [ ] Cite: DAIL, CodeS, ACT, DIN, DCG, SAFE, ODIS, MARLO, ASTRES, PTD-SQL,
      DEA-SQL, C3, SENSE, Fed-ICL/IFed-ICL/FICAL, 2 survey. Phản biện DCG
      theo §4.2.
- [ ] Verify danh tính "Syn-SQL" trong bảng SAFE-SQL (nghi = SENSE
      2408.03256) từ chính PDF SAFE trước khi cite.
- [ ] Quyết định (advisor): có build synthetic in-domain demos
      (SAFE/ODIS-style) làm Tier-2/3 không.

## 6. Vì sao mình thấy khác lit — lý thuyết ICL (research 2026-07-12)

Ba mảnh lit lý thuyết giải thích trọn bộ hiện tượng nội bộ (selection vô
dụng, ICL chết sau FT, dấu ICL theo family). Dùng làm anchor §2/§5.

1. **TR vs TL (Pan et al. 2305.09731; dynamics 2406.14022).** ICL = hai cơ
   chế: *Task Recognition* (nhận task/format từ demo — có từ 350M, KHÔNG cải
   thiện khi demo tốt hơn hay nhiều hơn) và *Task Learning* (học mapping mới
   từ demo — chỉ emerge ở model lớn, mới hưởng lợi từ selection). Student
   0.5–2B của mình = TR-only regime → random ≈ DAIL là **dự đoán của theory**.
   Toàn bộ thang selection trong lit (§3) đo trên GPT-4/Claude/Codex/GPT-4o =
   TL-capable — không mâu thuẫn, khác regime.
2. **Demos không cần đúng (Min et al. 2202.12837).** Label random gần như
   không giảm hiệu năng ICL — demo chủ yếu cung cấp format + label space +
   input distribution. Khớp: random demos thắng DAIL trên 0.5B base (30.08
   vs 28.05); question-sim tệ nhất 3/4 family (near-duplicate câu hỏi +
   schema sai = kênh copy độc nhất, còn format thì demo nào cũng cấp được).
3. **FT giết ICL — có chứng minh (2602.23197, 02/2026).** Trên linear
   attention: FT tối ưu zero-shot loss làm suy giảm few-shot ability về mặt
   cấu trúc. Hai lối ra actionable: (i) FT giới hạn vào value matrix (freeze
   query/key) giữ được ICL → gợi ý ablation LoRA target-modules; (ii) thêm
   auxiliary few-shot loss khi FT → few-shot phục hồi. Chú ý: random-k
   injection mặc định của `build_examples` (n ~ U{0..k}) chính là dạng (ii)
   — đọc lại `ft_icl_k3` dưới lens này: k0 floor tốt hơn (64.02 vs 62.19) +
   phục hồi mạnh nhất trong gate (+7.93) = tín hiệu yếu ủng hộ.
4. **Chính [9] đã thấy và bỏ ngỏ.** Quote nguyên văn DAIL-SQL: *"after
   fine-tuning we also observe a decrease in in-context learning capability,
   which requires further study."* — §5 của mình là "further study" đó.
   Mở đầu §5 bằng quote này.

**Quyết định ICL policy cho paper (2026-07-12, ba tầng):** client training
k=0 · client inference = verifier-gated retry, fallback question-sim ·
teacher distill context = DAIL k_teacher=3 (ablate 0 — quyết chữ "IC" trong
tên Fed-ICKD, kỳ vọng thấp). Selection method không phải contribution;
§5 analysis + usage policy (trục D) mới là.

## Link nhanh

| Paper | arXiv |
|---|---|
| DAIL-SQL [9] | 2308.15363 |
| CodeS | 2402.16347 |
| ACT-SQL | 2310.17342 |
| DIN-SQL | 2304.11015 |
| DCG-SQL | 2505.19956 |
| SAFE-SQL | 2502.11438 |
| ODIS | 2310.06302 |
| MARLO | 2410.14049 |
| ASTRES / AST ranking | 2407.03227 |
| PTD-SQL | 2409.14082 |
| DEA-SQL | 2402.10671 |
| C3 | 2307.07306 |
| SENSE | 2408.03256 |
| FICAL | 2412.08054 |
| Survey ICL retrieval | 2401.11624 |
| Survey text-to-SQL LLM | 2407.15186 |
| TR vs TL (theory) | 2305.09731 |
| TR/TL pre-training dynamics | 2406.14022 |
| Demos: labels don't matter | 2202.12837 |
| FT-forgets-ICL (linear attention) | 2602.23197 |
| Many-shot ICL | 2404.11018 |
