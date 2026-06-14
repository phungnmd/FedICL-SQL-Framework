# FedICL-SQL — Đề xuất chỉnh outline (xin thầy duyệt)

**Gửi:** TS. Lê Quang Hùng (corresponding) · **Từ:** [Student] · **Ngày:** 2026-06-14
**Bối cảnh:** Fig.1 (kiến trúc) + outline gốc (`fedicl_sql_outline.pdf`) của thầy là **chuẩn**. Dưới đây là **10 điểm em đề xuất đổi** so với outline đã duyệt, để de-risk 3 trụ cột (Federated / LLM-teacher / ICL) trước khi chạy thí nghiệm tốn tiền.

> ⚠️ **Cơ chế KHÔNG đổi.** Engine vẫn đúng Fig.1 100%: client train 4-loss `L = λ₁L_SQL + λ₂L_KD + λ₃L_struct + λ₄L_exec` → upload **weights only** → **FedAvg → Global SLM `M_G`**; teacher chạy public-X nuôi **cả** ICL Hub demos **và** KD targets. Các điểm dưới chỉ đổi **framing RQ / model / cách đo / trích dẫn**, không đổi kiến trúc.

| # | Điểm | Outline gốc (v1) | Đề xuất (v2) | Lý do | Thầy duyệt |
|---|---|---|---|---|---|
| 1 | **RQ1 framing** | "cải thiện performance trong môi trường federated" | `M_G` **tiến sát ceiling tập trung B3** (gap nhỏ), không chỉ `> SLM-only` | `> SLM-only` gần như chắc thắng (FedAvg gộp ~K× data) → tầm thường, reviewer bác | ✅ Duyệt |
| 2 | **RQ3 / teacher** 🔴 | (mở) "transfer có tốt hơn không" | Giữ ablation **"Without Teacher"** (gold-CE), **báo cáo delta — KHÔNG cổng pass/fail** | Trên Spider có gold, SQL teacher ⊆ gold → teacher thắng nhờ **soft-KL** (dark knowledge) + CoT, là phép so công bằng | ✅ Duyệt |
| 3 | **Ablation 3b mới** | (không có) | **Label-free KD (unlabeled-X)** — regime teacher *cần thiết* (không có gold), khớp deployment. Secondary | Chứng minh giá trị 72B ở chỗ không có nhãn | ❌ Bỏ — chưa cần thiết bây giờ |
| 4 | **Student chính** 🔴 | "e.g. Phi-3-mini / Gemma-2B / TinyLlama" | **Qwen2.5-1.5B-Instruct** primary; 3 model kia → ablation A5 | Cùng tokenizer teacher Qwen-72B → **soft-KL KD sạch, khỏi MinED**. (gốc ghi "e.g." nên không trái, nhưng cần thầy xác nhận) | ✅ Duyệt |
| 5 | **Skeleton-loss** | novelty ngang hàng | Hạ xuống **claim phụ** — chỉ nêu nếu ablation λ₃ dịch EX có CI | Token skeleton đã nằm trong `L_SQL` → phần lớn là reweight, dễ bị bắt over-claim | ↩️ Giữ V1 |
| 6 | **Privacy (DP)** | đóng góp vô điều kiện | DP là **headline chỉ nếu đo được** (báo ε vs EX); không thì → future work | Encrypted-delta + secure-agg = secure-FL chuẩn, chưa đủ novel | ↩️ Giữ V1 |
| 7 | **Benchmark 2** | Spider-Realistic "nice-to-have" | Spider-Realistic → **Tier-2 (bắt buộc)** | Q3 mong ≥2 benchmark; cùng DB, chỉ paraphrase → gần như free | ✅ Duyệt |
| 8 | **Lý thuyết hội tụ** | (ngầm dựa Fed-ICL) | Cite **McMahan/FedProx** (parametric weight-agg) | Fed-ICL chứng minh cho *answer-fusion parameter-free* — sai cơ chế, reviewer bắt | ✅ Duyệt |
| 9 | **Teacher–student collab** | (chung) | **Chỉ training-time KD**; runtime escalation → §5 future | Escalation lúc inference tốn teacher + lộ query pattern lên server (trái privacy); Fig.1 không vẽ box vote | ✅ Duyệt |
| 10 | **Teacher logits / KD** | (chưa nêu) | Teacher Qwen-72B qua **DeepInfra `top_logprobs=20`** → KD hard+soft thật ở P1; bỏ MinED/P2 | API trả logprobs → làm được soft-KL Hinton qua API, khỏi self-host | ✅ Duyệt |

**Quan trọng nhất (🔴):** #2 (teacher gate→ablation) và #4 (student Qwen-1.5B) — hai cái này định hình trụ "Large" + toàn bộ KD. Mong thầy cho ý kiến trước.

**Đề xuất phụ (không phải đổi outline, xin ý kiến):** Spider có thể bị contamination (Qwen pretrain ~2024 đã thấy Spider 2018) → bóp headroom. Cân nhắc thêm **BIRD** (2023, khó hơn) thay/bổ sung Spider-Realistic? ☐ thêm BIRD ☐ giữ Spider-Realistic

---
*Chi tiết từng điểm + `[Δ]` tag: `paper/drafts/fedicl_sql_outline_v2.md`. Cơ chế: `paper/notes/fig1_architecture.md`. Spec thực thi: `paper/notes/detailed_plan.md`.*
