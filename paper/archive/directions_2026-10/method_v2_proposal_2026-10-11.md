# Đề xuất phương pháp FedLS-SQL v2: round private on-policy được execution kiểm chứng

> **Trạng thái 11/10/2026: đóng.** Owner chốt hướng A
> ([paper_direction_2026-10-11.md](paper_direction_2026-10-11.md)). Churn A1 không ủng hộ R2 nên
> ExST không thể thành method chính (R5), và screen S1 đã bỏ khỏi hàng đợi. Hai điểm dưới đây
> đã được thay: quyết định "đi theo v2" ở mục 1, và việc viết lại luật P2.27 ở mục 2.2 (theo luật
> gốc, `teacher` fail, `server_kd` pass). Phần còn lại giữ làm tài liệu tham khảo cho thiết kế ExST.

Ngày 11/10/2026. Dựa trên P2.25–P2.28. Mọi số là seed 0, EX (%), protocol v2.
Kiểm định: exact McNemar ghép cặp, khoảng tin cậy Wald 95%.

## 1. Tóm tắt

- **Server Hinton KD đã có giá trị ở phía public và về robustness.** Ở Coder-1.5B, α=0.1,
  Hinton v1 so với FedNTD: BIRD +18.97 (p<.001), Spider không thua (cận dưới −0.89),
  Spider-DK +5.61 (p<.001), Syn +3.00, Realistic +3.74.
- **Round private đang làm mòn phần teacher đóng góp.**
  - Hinton hơn gold rất rõ ngay sau stage K: K2 Spider +3.00, BIRD +4.56.
  - Sau mỗi round private, khoảng cách này còn khoảng một nửa: A3 Spider +1.35, BIRD +1.89.
- **Phía private (Spider) bão hòa.**
  - SFT trên gold không thêm năng lực sau round 2.
  - FedNTD, giải pháp retention của v1, không giúp gì và còn làm giảm BIRD.
- **Client vẫn còn headroom lớn trên chính dữ liệu của mình (P2.28).**
  - pass@8 − greedy là 13–18 điểm.
  - 65–77% câu hỏi có SQL đúng theo execution nhưng khác gold.
- **Đề xuất:**
  - Giữ server Hinton KD, bỏ NTD.
  - Thay SFT gold ở round private bằng **ExST** (execution-verified self-training). Client sample SQL
    từ adapter global vừa nhận, chạy trên DB local, giữ các SQL đúng, rồi train trên gold cộng các SQL đó.
- **Vì sao đây là method về KD + FL, không chỉ là RFT chạy trong FL.** Mục tiêu train của ExST là
  **on-policy**, tức do chính model global sinh ra. Literature cho thấy train on-policy làm model trôi
  khỏi điểm xuất phát ít hơn và quên ít hơn SFT. Trong FL, điều đó dẫn tới hai hệ quả kiểm chứng được:
  (H1) giữ được phần tri thức teacher đưa vào ở stage K, và (H2) giảm client drift dưới non-IID.
  ExST làm đúng vai trò mà NTD định làm, đồng thời còn học thêm được ở miền private.
- **Quyết định (sửa 11/10):** không đi theo v2 làm hướng chính. ExST chạy như screen S1 có điều
  kiện dừng (luật R4, R5 trong LAB_LOG 2026-10-11).

## 2. Bằng chứng hiện có

### 2.1 P2.27: Coder-1.5B, α=0.1, model cuối (A3)

| Arm | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| base (chưa train) | 59.19 | 46.26 | 45.94 | 47.66 | 21.32 |
| FL A>A>A | 67.60 | 59.65 | 53.68 | 53.27 | 25.68 |
| FedNTD A>A[ntd]>A[ntd] | 67.79 | 57.09 | 53.38 | 51.96 | 24.32 |
| gold v1 A>K[ce]>A[ntd]>K[ce]>A[ntd] | 67.89 | 59.06 | 55.61 | 52.90 | 41.40 |
| **Hinton v1** A>K[kd]>A[ntd]>K[kd]>A[ntd] | **69.25** | **60.83** | **56.38** | **57.57** | **43.29** |
| central Spider E3 | đang chạy | | | | |
| teacher Coder-7B zero-shot | 76.69 | | | | 47.07 |

Quỹ đạo Spider / BIRD qua từng stage:

| Stage | FL | gold v1 | Hinton v1 |
|---|---|---|---|
| A1 | 65.57 / 22.62 | (chung) | (chung) |
| K1 | | 58.70 / 40.35 | 62.19 / 42.18 |
| A2 | 68.28 / 24.38 | 66.34 / 41.59 | 68.47 / 41.66 |
| K2 | | 60.54 / 39.77 | 63.54 / 44.33 |
| A3 | 67.60 / 25.68 | 67.89 / 41.40 | 69.25 / 43.29 |

### 2.2 Các so sánh chính ở model cuối (Δ EX, CI 95%, p)

| So sánh | Spider | BIRD | DK | Syn | Realistic |
|---|---|---|---|---|---|
| Hinton v1 − FedNTD | +1.45 [−0.89, 3.79], p=.26 | **+18.97**, p<.001 | **+5.61**, p<.001 | **+3.00**, p=.019 | **+3.74**, p=.037 |
| Hinton v1 − gold v1 | +1.35 [−0.70, 3.41], p=.23 | +1.89 [−0.12, 3.90], p=.076 | **+4.67**, p<.001 | +0.77, ns | +1.77, ns |
| Hinton v1 − FL | +1.64 [−0.73, 4.02], p=.20 | **+17.60**, p<.001 | **+4.30**, p=.012 | **+2.71**, p=.046 | +1.18, ns |

Không có so sánh nào mà Hinton v1 thua. Ở Coder-0.5B, α=0.5, Hinton − gold AKAKA là Spider +2.42
(p=.02). Hướng của hiệu ứng nhất quán qua hai model và hai split.

Về luật P2.27 trong LAB_LOG (sửa 11/10): theo luật cố định trước kết quả, `teacher` fail
(Spider +1.35, p=.23) và `server_kd` pass. Một comparison ghép cặp trên 1,034 câu có nửa độ rộng
CI khoảng 2-2.4 điểm, nên p<.05 trên một seed chỉ bắt được chênh lệch từ khoảng 2.5 điểm. Vì vậy,
từ seed 1, claim teacher được đánh giá bằng kiểm định gộp 3 seed (luật R7, cố định 11/10 trước
khi có kết quả seed 1). Luật cũ không được viết lại cho P2.27.

### 2.3 Round private làm mòn phần đóng góp của teacher

Hinton − gold, đo sau từng stage (cùng schedule, chỉ khác mục tiêu ở stage K):

| Sau stage | Spider | BIRD |
|---|---|---|
| K1 | **+3.48** (p=.002) | +1.83 (p=.077) |
| A2 | +2.13 (p=.043) | +0.07 |
| K2 | **+3.00** (p=.013) | **+4.56** (p<.001) |
| A3 | +1.35 (p=.23) | +1.89 (p=.076) |

Phần teacher đóng góp, tính trên nền gold, bị round private xóa khoảng một nửa hoặc hơn mỗi lần.
Đây là một dạng forgetting khác: không phải BIRD bị quên hẳn, mà là **phần riêng của teacher** bị
quên. Tổng BIRD gần như giữ nguyên (Hinton K2 → A3: −1.04, ns), nên kiểu forgetting này không lộ ra
nếu chỉ nhìn EX tuyệt đối. Riêng DK, lợi thế của Hinton vẫn rõ ở model cuối (+4.67), cho thấy không
phải mọi đóng góp đều bị xóa.

### 2.4 Những gì P2.27 bác bỏ

1. **Asymmetric forgetting kiểu 0.5B không còn ở 1.5B.** BIRD sau K2 → A3: gold +1.6, Hinton −1.04 (ns).
   Ở 0.5B mức rơi là 4–7 điểm.
2. **FedNTD không giúp.** So với FL: Spider +0.19 (ns), BIRD −1.37 (p=.044), Realistic −2.56 (p=.047).
   Cùng kết luận với P2.21–P2.24 ở 0.5B.
3. **SFT trên gold bão hòa.** FL A2 → A3: Spider −0.68 (ns). Hinton A2 − FL A2: Spider +0.19.

### 2.5 P2.28: headroom trên câu hỏi train của client

1,000 câu Spider train cố định (200 câu × 5 client). Mỗi câu có 1 SQL greedy và 8 mẫu ở T=0.7,
chấm bằng `spider_result_eq_v1`. pass@k theo công thức không chệch của Chen et al. (2021).

| Adapter (đầu round private) | greedy | pass@8 | headroom | rescue | variant | Headroom theo client |
|---|---:|---:|---:|---:|---:|---|
| FL A2 | 77.0 | 90.0 | 13.0 | 13.2 | 65.3 | 12.0 / 18.5 / 16.0 / 9.0 / 9.5 |
| gold v1 K2 | 66.9 | 84.7 | 17.8 | 18.0 | 76.8 | 22.0 / 20.5 / 22.5 / 14.0 / 10.0 |
| Hinton v1 K2 | 71.9 | 85.6 | 13.7 | 13.7 | 77.4 | 14.0 / 17.5 / 12.0 / 12.0 / 13.0 |

- **rescue:** tỉ lệ câu mà greedy sai nhưng có ít nhất 1 mẫu đúng.
- **variant:** tỉ lệ câu có ít nhất 1 mẫu đúng nhưng khác chuỗi gold (sau khi bỏ khác biệt hoa/thường,
  khoảng trắng và `;`).

Model global sinh được nhiều SQL đúng trên dữ liệu của client, nên mục tiêu on-policy luôn có sẵn và
đủ đa dạng ở mọi client. Headroom ở K2 cao hơn một phần vì stage K làm Spider bị quên, nên ExST phải
được so với một round A plain **từ cùng parent**.

## 3. Chẩn đoán

Round private trong FL có ba vấn đề:

| Vấn đề | Bằng chứng | Hệ quả |
|---|---|---|
| **P1. Làm mòn đóng góp của teacher** | Hinton − gold giảm từ +3.0/+4.6 (K2) xuống +1.4/+1.9 (A3) | Lợi ích KD ở model cuối nhỏ hơn mức teacher thực sự mang lại |
| **P2. Bão hòa ở miền private** | FL A2 → A3 −0.68; mọi arm dừng ở khoảng 67–69 Spider, teacher 76.7 | Thêm round SFT không thêm năng lực |
| **P3. Client drift dưới non-IID** | Mỗi client chỉ có 6–8 trong 20 cụm domain; mức FL thua central chờ số `central` | Chưa đo trực tiếp |

Cả ba có chung một gốc: **SFT trên gold là mục tiêu off-policy.** Mỗi câu chỉ có một cách viết,
không phải cách mà model global sẽ tự viết. Việc kéo model về target đó đẩy adapter đi xa khỏi điểm
xuất phát:
- xóa bớt những gì stage K vừa dạy (P1);
- dừng lại ở mức ghi nhớ gold, không học thêm (P2);
- và mỗi client bị kéo theo một hướng khác nhau (P3).

NTD chỉ chữa P1 bằng cách phạt việc lệch khỏi model cũ, và thực tế không có tác dụng. ExST thay
chính target: thay vì phạt việc rời xa, nó chọn target nằm sẵn gần model.

## 4. Phương pháp đề xuất: FedLS-SQL v2

### 4.1 Tổng quan

```text
A1                          plain private round (FedAvg LoRA)
K   [server, Hinton KD]     public BIRD, frozen teacher Coder-7B
A   [client, ExST]          on-policy, execution-verified targets; FedAvg LoRA
K   [server, Hinton KD]
A   [client, ExST]          -> deploy SLM adapter
```

Thông điệp chính: **teacher đưa tri thức vào qua server; round private học miền private bằng
target do chính model global sinh và được execution kiểm chứng, nên không xóa tri thức đó và không
kéo các client rời xa nhau.**

### 4.2 Server: Hinton KD (giữ nguyên từ v1)

Loss = 0.5 CE + 0.5 forward KL, T=2, trên 9,428 câu BIRD train, logit teacher lấy từ cache.
Một epoch cho mỗi stage K. Nguồn: Hinton et al. (2015). Phía server LLM → SLM tương tự phía SLM
của FedCoLLM (arXiv 2411.11707) và FedMKT (COLING 2025).

### 4.3 Client: ExST (mới)

Round r, client i nhận adapter global θ:

1. **Sample.** Với mỗi câu train (q, s\*) của client, sinh k SQL từ π_θ(· | q, schema),
   dùng temperature T. Dùng đúng prompt SQL-only như khi train và eval.
2. **Verify.** Chạy từng SQL trên DB local, giữ s nếu EX(s, s\*) = 1 (`spider_result_eq_v1`).
   Bỏ trùng theo SQL đã chuẩn hóa, bỏ bản trùng gold, giữ tối đa m biến thể mỗi câu.
3. **Train.** Một epoch local trên D_i ∪ {(q, s)}, CE `target_fp32`, cùng recipe LoRA như round A.
4. **Aggregate.** FedAvg LoRA, trọng số theo |D_i| gốc, để dữ liệu thêm vào không đổi trọng số giữa
   các client.

Siêu tham số khởi đầu (P2.28 đã đo ở k=8, T=0.7): k=8, T=0.7, top-p 1.0, m=4.

Gold vẫn được giữ trong tập train. Gold đảm bảo client luôn có tín hiệu đúng, kể cả ở những câu mà
model chưa sample được SQL đúng. Các biến thể on-policy làm phần lớn khối lượng train nằm gần
phân phối của model global.

### 4.4 Cơ chế: vì sao target on-policy giữ KD và giảm drift

- **RL's Razor** (ICLR 2026, arXiv 2509.04259): fine-tune on-policy quên ít hơn SFT, vì nó giữ
  KL giữa model mới và model gốc nhỏ.
- **SDFT** (ACL 2024, arXiv 2402.13669): viết lại target theo phân phối của chính model giúp giảm
  catastrophic forgetting khi fine-tune.

Áp vào FL:
- **H1 (giữ KD).** Từ cùng adapter K2, round A[ExST] giữ được nhiều hơn phần tri thức teacher so với
  A[plain]. Đo bằng Hinton − gold, BIRD, DK sau A3.
- **H2 (giảm drift).** Các client đều bắt đầu từ cùng θ và train trên target gần π_θ, nên các LoRA
  delta gần nhau hơn và có norm nhỏ hơn. FedAvg ít bị triệt tiêu hơn. Đo bằng cosine similarity và
  norm giữa các delta của client, cùng KL(π_θ ‖ π_client) trên một tập câu cố định.
- **H3 (heterogeneity).** Nếu H2 đúng, lợi ích của ExST lớn hơn khi non-IID mạnh hơn: α=0.1 so với
  α=0.5, và ở các client lệch nhiều.

Hai điểm cần nói rõ trong paper:
- Đây là các giả thuyết có nguồn. Hai paper trên đo trong bối cảnh centralized; việc chuyển sang FL
  là điều paper này kiểm chứng.
- Ngoài hiệu ứng giữ tri thức, ExST còn có lợi ích trực tiếp ở miền private (P2), đến từ các biến
  thể đúng và phần rescue.

### 4.5 Nguồn cho từng thành phần

| Thành phần | Nguồn |
|---|---|
| Sample → lọc theo đúng/sai → SFT lại | STaR (Zelikman et al., NeurIPS 2022); RFT (Yuan et al. 2023, arXiv 2308.01825); ReST-EM (Singh et al. 2023, arXiv 2312.06585) |
| Target on-policy làm giảm forgetting | RL's Razor (ICLR 2026, arXiv 2509.04259); SDFT (ACL 2024, arXiv 2402.13669) |
| Execution làm verifier/reward cho Text-to-SQL | SLM-SQL (arXiv 2507.22478, reward EX); Reasoning-SQL |
| Federated RL với verifiable reward | FedMOA (arXiv 2602.00453, math/code) |
| Non-IID client drift trong FL | FedNTD (Lee et al., NeurIPS 2022) và các tài liệu nó trích |
| pass@k làm thước đo headroom | Chen et al. (2021, arXiv 2107.03374) |
| Bỏ trùng, giới hạn số đường đúng mỗi câu | RFT (Yuan et al.: lợi ích đến từ các đường suy luận khác nhau) |

Lựa chọn kỹ thuật riêng của đề xuất, sẽ nêu rõ trong paper: trọng số FedAvg theo |D_i| gốc; m=4;
giữ gold trong tập train.

### 4.6 Quyền riêng tư

Không thay đổi so với v1. Sample, execution và gold đều ở lại client; chỉ LoRA delta rời client.
Client không nhận output của teacher; server không thấy dữ liệu client. ExST không thêm kênh trao đổi.

### 4.7 Biến thể mở rộng

- **ExST-GRPO.** Thay bước 3 bằng GRPO với reward R_EX + 0.1·R_format như SLM-SQL. Biến thể này học
  thêm từ mẫu sai, và theo RL's Razor còn on-policy hơn RFT. Chi phí cao hơn nhiều; chỉ làm khi
  ExST-RFT cho thấy hướng đúng nhưng mức tăng chưa đủ.
- **Execution-gated KD ở server.** Chỉ distill teacher trên các câu BIRD mà SQL greedy của teacher chạy
  đúng: 5,319/9,428 câu, đã có sẵn từ pool SeqKD. Khi đó execution là verifier chung cho cả hai phía,
  cho teacher (public) và cho student (private). **Chưa có nguồn trực tiếp** cho việc gate logit KD
  theo execution. Nguồn gần nhất là việc lọc target của SeqKD theo execution đã dùng trong dự án.
  Nếu làm thì phải ghi rõ đây là lựa chọn của chúng tôi.

## 5. Kỳ vọng

- **Spider:** +1 đến +3 so với A3 plain cùng parent. Headroom 13–18 điểm là trần đo trên câu train.
  Mức chuyển sang dev (schema chưa từng thấy) nhỏ hơn nhiều, như FL A2 → A3 đã cho thấy.
- **Giữ KD (H1):** sau A3[ExST], khoảng cách Hinton − gold gần với mức đo ở K2 (+3.0 Spider,
  +4.6 BIRD) hơn so với mức sau A3 plain (+1.4, +1.9).
- **Drift (H2):** cosine giữa các delta của client cao hơn, norm thấp hơn so với A[plain].
- Nếu H1 và H2 đúng, Spider và BIRD cùng tăng nhờ hai đường: học thêm ở miền private, và giữ được
  phần teacher đóng góp. Đó là lý do mức tăng tổng có thể vượt +1 đến +3.

## 6. Kế hoạch triển khai v2

Hướng v2 đã được chọn. Các bước dưới đây dùng để xây dựng và tinh chỉnh method, không phải để
quyết định có làm hay không. Không dùng ngưỡng p<.05 trên một seed làm cổng.

### 6.1 P2.29: round cuối, để dựng và chỉnh ExST

Mọi arm chạy một round A3 từ adapter đã publish, seed 0, eval đủ 5 bộ. **Lưu adapter của từng
client** (trước FedAvg) cho mọi arm.

| Arm | Parent | Round A3 | Vai trò |
|---|---|---|---|
| `h_plain` | Hinton v1 K2 | plain (không NTD) | Control; đồng thời là ablation NTD (so với Hinton v1 A3) |
| `h_exst` | Hinton v1 K2 | ExST | **Method v2** |
| `h_dup` | Hinton v1 K2 | plain, gold lặp lại cho bằng số bước của `h_exst` | Control compute |
| `g_plain` / `g_exst` | gold v1 K2 | plain / ExST | Đo H1: Hinton − gold sau A3 plain và sau A3[ExST] |
| `fl_exst` | FL A2 | ExST | ExST khi không có KD, so với FL A3 |
| `c_exst` | central Spider E2 | một epoch ExST trên central Spider | Trả lời "có đặc thù FL không": so với central E3 |

### 6.2 Các phép đo

| Đo | Cho | Cách tính |
|---|---|---|
| Δ Spider, 5 bộ, BIRD | P2, toàn bộ | `h_exst` − `h_plain`; `h_exst` − `h_dup` |
| Giữ KD | H1 | (Hinton − gold) sau ExST so với sau plain; BIRD và DK từ K2 → A3 |
| Drift | H2 | cosine và norm giữa các LoRA delta của client; KL(π_θ ‖ π_client) trên 500 câu cố định |
| Theo client | H3 | Δ Spider và drift theo kích thước và số cụm domain của từng client |
| Đặc thù FL | | (`fl_exst` − FL A3) so với (`c_exst` − central E3) |
| Chi phí | | thời gian sample, số biến thể giữ lại theo client, `distinct_correct` |

Kết quả P2.29 dùng để chọn cấu hình ExST (k, m, cách lọc biến thể). `h_exst` phải hơn `h_dup`; nếu
không, mức tăng chỉ do train nhiều bước hơn và cần sửa thiết kế (trọng số biến thể, hoặc chỉ giữ
biến thể cho câu greedy sai). Nếu lần đầu yếu, chỉnh cấu hình hoặc chuyển sang ExST-GRPO thay vì bỏ hướng.

### 6.3 Full chain v2

Chạy song song với 6.1 khi có GPU rảnh, không chờ P2.29: A1 > K[kd] > A[ExST] > K[kd] > A[ExST]
từ base, dùng A1 chung với P2.27. Thêm gold > ExST cùng chain để đo H1 trên toàn chain. Nếu P2.29
cho thấy cần đổi cấu hình, chạy lại chain.

### 6.4 Seed, heterogeneity và baseline cho paper

- Seed 1 và 2 cho v2, Hinton v1 (hoặc Hinton không NTD), gold, FL và FedNTD.
- H3: chạy v2 và Hinton plain ở α=0.5 với Coder-1.5B.
- Kiểm định trong paper: McNemar gộp qua 3 seed (hoặc mixed-effects logistic theo câu hỏi), cộng
  khoảng tin cậy bootstrap. Báo effect size cho mọi comparison, kể cả những cái không có ý nghĩa.
- Baseline bổ sung: central Spider+BIRD ở 1.5B, client public replay.

### 6.5 Chi phí

Một round A plain mất khoảng 1.6 h. ExST thêm phần sample (8,659 câu × 8 mẫu) và phần train trên
dữ liệu lớn hơn, tối đa (1 + m) lần. Thời gian sample sẽ ước lượng từ log P2.28. Nếu quá đắt thì
dùng k=4, hoặc chỉ sample các câu greedy sai cùng một tập con ngẫu nhiên các câu greedy đúng.
Các phép đo drift chạy offline trên adapter đã lưu, gần như không tốn GPU.

## 7. Đóng góp dự kiến của paper

| | Đóng góp | Trạng thái bằng chứng |
|---|---|---|
| C1 | Server teacher KD đưa tri thức public vào FL mà không làm hại miền private, tăng robustness trên các bộ Spider biến thể | Có ở seed 0, 1.5B, α=0.1: BIRD +19; DK, Syn, Realistic +3 đến +6; Spider không thua. Cần thêm seed |
| C2 | Chẩn đoán: round private SFT gold làm mòn phần đóng góp của teacher, bão hòa ở miền private, và retention kiểu regularizer (NTD) không chữa được | Có (P2.27, P2.28; NTD từ P2.21–P2.27) |
| C3 | ExST: round private on-policy được execution kiểm chứng; giữ KD, giảm drift và học thêm ở miền private | Headroom có (P2.28); H1, H2 và mức tăng chờ P2.29 |
| C4 | Phân tích: headroom pass@k theo client; tác dụng theo mức heterogeneity; teacher so với public gold theo từng stage | Một phần có; H3 cần α=0.5 |

**Novelty, nói thận trọng.**
- Đã có trước: server KD từ LLM vào SLM trong FL (FedCoLLM, FedMKT); self-training có verifier và RL
  với reward EX cho Text-to-SQL ở dạng centralized (SLM-SQL, Reasoning-SQL); federated RL với
  verifiable reward cho math/code (FedMOA); on-policy làm giảm forgetting ở dạng centralized
  (RL's Razor, SDFT).
- Chúng tôi **chưa tìm thấy** công trình nào (1) nhận ra rằng round private trong FL làm mòn tri
  thức do teacher ở server đưa vào, và (2) chữa việc đó bằng target on-policy được kiểm chứng ở client.
  Cần một lần search có hệ thống trước khi viết.
- Đóng góp chính là cơ chế này cùng phần đo đạc (giữ KD, drift, headroom). Phù hợp mục tiêu Q3,
  không phải đột phá.

## 8. Rủi ro và cách giảm

| Rủi ro | Cách giảm |
|---|---|
| H1 khó thấy vì ở 1.5B BIRD gần như không bị quên | Đo H1 bằng Hinton − gold (phần riêng của teacher) và DK, không chỉ bằng BIRD tuyệt đối; nếu cần, kiểm tra thêm ở 0.5B, nơi forgetting rõ |
| H2 yếu nếu FL gần như không thua central (drift nhỏ) | Chờ số `central`; nếu khoảng cách nhỏ thì H2 chỉ là phân tích phụ và H3 chuyển sang các client lệch nhiều |
| Mức tăng chỉ do train nhiều bước hơn | Arm `h_dup` |
| ExST tăng cả ở centralized nên không đặc thù FL | Arm `c_exst`. Nếu tăng như nhau thì claim chính chuyển sang H1/H2, vì đây là các hiệu ứng chỉ có trong FL + KD |
| SQL đúng "nhờ may" trên DB này (false positive của EX; Zhong et al., EMNLP 2020) | Bỏ biến thể khi kết quả của gold rỗng; báo tỉ lệ biến thể khớp EM với gold; kiểm tra tay 100 mẫu |
| Variant bị thổi phồng bởi alias hoặc `count(*)` so với `count(1)` | Báo `distinct_correct`; ghi rõ cách chuẩn hóa |
| Mức tăng nhỏ hơn noise ở 1 seed | Kiểm định gộp 3 seed; báo effect size và CI cho mọi comparison |
| Chi phí sample | k=4 hoặc sample có chọn lọc; đo trong P2.29 |

## 9. Việc cần làm

1. Publish P2.28 (`summary.json` và 3 file JSONL); ghi thời gian chạy vào `A5000_RUN_CONFIG.md`.
2. Viết P2.29: runner, trainer ExST ở client, lưu adapter từng client, script đo drift (offline),
   test, smoke VRAM. Chạy `h_plain` và `g_plain` trước vì không cần trainer mới.
3. Chạy `h_exst`, `g_exst`, `h_dup`, `fl_exst`, `c_exst`; chỉnh cấu hình ExST theo kết quả.
4. Full chain v2 khi có GPU; sau đó seed 1–2, α=0.5 và các baseline ở mục 6.4.
5. Ghi kết quả từng bước vào LAB_LOG; ghi `central` khi chạy xong.
