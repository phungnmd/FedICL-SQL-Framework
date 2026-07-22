# Related Papers — Key References

## FT + ICL Interaction

### Fine-Tuned In-Context Learners for Efficient Adaptation
- **arXiv**: 2512.19879
- **Link**: https://arxiv.org/abs/2512.19879
- **Core idea**: SFT trên k-shot format (không phải single examples). Inference cũng dùng k-shot → không format mismatch.
- **Exact format**:
  ```
  "Next example: " + x₁ + y₁ + ... + xₖ + yₖ + x_target + y_target
  ```
  Loss tính trên **tất cả** `yᵢ` (mọi demo response), không chỉ target cuối.
- **k tested**: {1, 3, 5, 10, 15, 30}. Plateau ở k≈5.
- **Models**: Gemma-2 (2B, 9B, 27B), Qwen-3 (0.6B, 1.7B, 4B).
- **Datasets**: Big Bench Hard (23 tasks), NLP classification (11 tasks), translation — **không có NL2SQL**.
- **Key results** (BBH, Gemma-2 27B, 150 examples):
  - ICL+FT: **81.8%** | FT-only: 72.6% | ICL-only: 64.2%
- **⚠️ CRITICAL — LoRA FT vẫn NEGATIVE**:
  BBH average: LoRA ICL+FT → 68.8% → **67.6%** (giảm). Full FT mới work.
- **⚠️ NL2SQL caveat**: Task của paper là classification/reasoning, không phải structured SQL generation. Format specialization mạnh hơn nhiều với NL2SQL → ngay cả k-shot SFT format có thể không đủ.
- **Why still relevant**: Confirm mechanism; fix yêu cầu full FT (không LoRA) VÀ loss trên tất cả demo responses.

---

### FIAT: Fusing learning paradigms with Instruction-Accelerated Tuning
- **arXiv**: 2309.04663
- **Link**: https://arxiv.org/abs/2309.04663
- **Authors**: Xinyi Wang, John Wieting, Jonathan H. Clark (Google DeepMind)
- **Core idea**: Fuse FT + ICL bằng SFT trên instruction-accelerated data (prompt engineering + chain-of-thought) với parameter-efficient tuning.
- **Method**: Dùng ICL-style reasoning (CoT từ large model) làm SFT data cho small model. Kết hợp paradigm thay vì chọn một.
- **Why relevant**: Template cho cách combine FT và ICL mà không bị negative gain. Related work cho phần methodology FedICL-SQL.
- **Key result**: Better than both ICL-only và FT-only ở 100–10,000 training examples.

---

## FT + Retrieval trên Spider/BIRD

### LitE-SQL: A Lightweight and Efficient Text-to-SQL Framework
- **arXiv**: 2510.09014
- **Link**: https://arxiv.org/abs/2510.09014
- **Published**: EACL 2026 Findings
- **GitHub**: https://github.com/shengminp/LitE-SQL
- **Core idea**: FT (SFT + execution-guided RL) + vector-based schema/example retriever. Cả hai chạy cùng nhau tại inference.
- **Method**:
  - Schema Retriever: vector DB pre-computed schema embeddings, hard-negative contrastive training
  - SQL Generator: 2-stage — SFT rồi execution-guided RL, tự-correct không cần multi-candidate
- **Why relevant**: Closest existing work kết hợp FT + ICL/retrieval trên Spider. Centralized baseline để so sánh với federated version của FedICL-SQL.
- **Key result**: Spider 1.0 → **88.45% EX**, BIRD → 72.10% EX. Best among 7B FT-based methods.

---

## Mechanism: Tại sao ICL negative gain trên FT model

### Fine-Tuning Without Forgetting In-Context Learning
- **arXiv**: 2602.23197
- **Link**: https://arxiv.org/abs/2602.23197
- **Core idea**: Theoretical analysis (linear attention) chứng minh SFT phá ICL ability.
- **Mechanism**: Format specialization xảy ra ngay đầu SFT → model expect input format không có demos → thêm demos = OOD.

### Spectrum Tuning: Post-Training for Distributional Coverage and In-Context Steerability
- **arXiv**: 2510.06084
- **Link**: https://arxiv.org/abs/2510.06084
- **Core finding**: "Current post-training hurts LLMs' in-context steerability." SFT giảm khả năng dùng context để override prior.
- **Solution**: Post-training method giữ ICL steerability trong khi maintain safety.

---

## FT-only trên Spider/BIRD (<7B)

### DTS-SQL: Decomposed Text-to-SQL with Small Large Language Models
- **arXiv**: 2402.01117
- **Link**: https://arxiv.org/abs/2402.01117
- **Core idea**: 2-step decomposed FT: step 1 = schema linking, step 2 = SQL gen. Mỗi step dùng 7B (DeepSeek/Mistral).
- **Key result**: Matches GPT-4 few-shot ICL performance. Spider + Spider-SYN, +3–7% EX.

### CodeS: Towards Building Open-source Language Models for Text-to-SQL
- **arXiv**: 2402.16347
- **Link**: https://arxiv.org/abs/2402.16347
- **Published**: SIGMOD 2024
- **GitHub**: https://github.com/RUCKBReasoning/codes
- **Local copy**: `paper/references/pdf/Natural Language to SQL/15-2024-CodeS- Towards Building Open-source Language Models for Text-to-SQL.pdf` (md: same path under `md/`)
- **Model sizes**: 1B, 3B, 7B, 15B
- **Core idea**: Incremental pre-training trên SQL-centric corpus + SFT. Bi-directional data augmentation + strategic prompt construction.
- **Key result**: Competitive với GPT-4 trên Spider + BIRD, 10x–100x smaller.
- **Đã implement trong `fedicl-sql`**: §6.3 schema metadata (`--schema-style codes`), §6.2 matched values, §8.2 question-pattern retriever (`--retrieval codes`). Chi tiết: `paper/notes/dail_vs_codes_prompt_methods.md`. Không dùng số `[10]` (đã gán cho KID) — xem note ở đầu `dail_vs_codes_prompt_methods.md`.

### SLM-SQL: An Exploration of Small Language Models for Text-to-SQL
- **arXiv**: 2507.22478
- **Link**: https://arxiv.org/abs/2507.22478
- **GitHub**: https://github.com/CycloneBoy/slm_sql
- **Model sizes**: 0.5B, 1.5B
- **Core idea**: SFT + RL post-training + corrective self-consistency.
- **Key result**: BIRD dev — 0.5B: 56.87%, 1.5B: **67.08%**. BIRD test — 1.5B: **70.49%**.
- **Why relevant**: Exact model size range (0.5B–1.5B) = FedICL-SQL student SLM range.

### Optimizing Small Language Models for NL2SQL via Chain-of-Thought Fine-Tuning
- **arXiv**: 2603.22942
- **Link**: https://arxiv.org/abs/2603.22942
- **Core idea**: CoT data làm SFT → small Qwen model.
- **Key result**: SFT baseline 36% → CoT-SFT **54.5%**. Large models (Gemini 2.5) gain nothing; small models gain a lot.
- **Why relevant**: Validates CoT distillation signal cho SLM FT — aligns với FedICL-SQL KD approach.
