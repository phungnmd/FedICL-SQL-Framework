# Đề xuất CoT + RL cho FedLS-SQL

Cập nhật: **2026-11-03**. Trạng thái: **đang chuẩn bị phương pháp, chưa triển khai federated CoT-DPO**.

Đây là bản đề xuất được cập nhật cho đến khi bắt đầu chạy federated. Các thực
nghiệm CoT/RL hiện tại nhằm chọn recipe cho setup BIRD public, Spider private;
kết quả centralized là bằng chứng chuẩn bị và mốc tham chiếu. Evidence chi tiết
ở [LAB_LOG](LAB_LOG.md), literature ở [COT_RL_RESEARCH](COT_RL_RESEARCH.md).
Lệnh chạy vẫn chỉ nằm trong [PIPELINE_NEXT](PIPELINE_NEXT.md).

## 1. Mục tiêu và setup

Server dùng teacher để dạy student reasoning trên public data. Student tiếp tục
học trên private data tại từng client bằng execution feedback; server aggregate
các adapter để tích lũy kiến thức qua nhiều round. Câu hỏi chính là CoT + RL có
cải thiện Spider EX trong federated learning so với các recipe SQL-only không.

| Thành phần | Thiết lập |
|---|---|
| Teacher | Qwen2.5-Coder-7B, frozen, 4-bit, chỉ chạy tại server trên BIRD |
| Public data | BIRD train có evidence, 9.428 câu trong pool gốc |
| Student | Qwen2.5-Coder-1.5B-Instruct, LoRA r16 |
| Private data | Spider train, split hiện có: 5 client, domain-cluster non-IID, alpha 0.1 |
| Aggregation | Sample-weighted, factor-wise FedAvg của LoRA như setup cũ |
| Triển khai | Chỉ student; không cần teacher hay gold khi inference |
| Compute | Hai RTX A5000 24 GB; các client có thể chạy lần lượt trên hai GPU |

Teacher không được đọc private Spider. Question, schema, gold SQL và rollout
private ở lại client; client gửi LoRA adapter. CoT được sinh khi trả lời,
SQL cuối là phần dùng để tính EX. Đóng góp teacher và CoT chưa được tách riêng
trong screen hiện tại; chỉ diễn giải theo comparator thực sự đã chạy.

## 2. Pipeline đích

```text
SERVER, PUBLIC BIRD
Teacher sinh CoT + SQL, không thấy gold của câu đang giải
    -> execution đối chiếu gold
    -> SFT student trên lời giải teacher đúng
    -> DPO + NLL student trên pair đúng/sai của teacher
    -> global student G0

FEDERATED SPIDER, LẶP THEO GLOBAL ROUND
Server gửi Gt cho các client
    -> mỗi client sinh K output cho toàn bộ local train đủ điều kiện
    -> execution tại client, chọn pair đúng/sai
    -> local DPO + NLL từ Gt
    -> gửi adapter, FedAvg thành Gt+1
    -> sinh lại trên cùng local pool bằng Gt+1 ở round tiếp theo
```

### 2.1. Public bootstrap bằng teacher

Phạm vi đích là toàn bộ BIRD train. Teacher nhận question, schema và evidence;
gold chỉ dùng ở bộ kiểm execution. Giữ nguyên CoT và SQL thật của teacher khi
SQL đúng, không ghép reasoning đó với gold SQL khác.

- **CoT SFT:** mỗi câu lấy một lời giải đúng đã kiểm. Câu chưa có lời giải đúng
  chưa tham gia CoT SFT.
- **Teacher-DPO:** mỗi câu có cả output đúng và sai lấy một pair. Student học
  trên toàn bộ pair thu được; teacher vẫn frozen. Đây là một chặng off-policy,
  không phải student tự khám phá nhiều vòng trên BIRD.
- Prompt đầu tiên giữ cách hiện tại, adaptation free-form từ OmniSQL. Số
  candidate teacher, cách chọn public pair và lịch public training sẽ được chốt
  từ coverage, chất lượng và chi phí đã đo. Chưa có lệnh sinh full BIRD.

Cách greedy rồi chỉ sample thêm câu sai của P2.60 chủ yếu thu positive cho SFT.
Để tạo teacher pairs rộng hơn, cần thêm stochastic output cho cả các câu greedy
đúng. Không mặc định dùng 32 candidate/câu như ExCoT trên hai A5000.

**Full pool không đồng nghĩa full supervision:** phải báo riêng số câu nguồn,
số câu có lời giải đúng, số câu mixed và số pair giữ được. Câu toàn đúng hoặc
toàn sai không tạo pair DPO. Lặp nhiều epochs trên cùng teacher cache vẫn là
học lại dữ liệu off-policy cố định.

G0 phải có lineage chỉ train trên public BIRD, chẳng hạn `cot1` hoặc bản có
thêm public teacher-DPO. Các adapter `c1_rl*`, `sql2` và `sql_rl*` đã train
centralized trên private Spider chỉ là mốc tham chiếu, không làm parent của FL.

### 2.2. Local DPO rồi FedAvg

Ở round t, mọi client tham gia nhận cùng Gt. Mỗi client dùng Gt sinh mới trên
toàn bộ local pool đủ điều kiện, thay vì chia các câu thành những nhóm chỉ gặp
một lần. Gold không được đưa vào prompt sinh; execution và tạo pair diễn ra
tại client. Không có bước self-CoT SFT Spider (`cot2`) trong pipeline chính.

| Thành phần | Cấu hình đề xuất cho pilot FL, chưa phải cấu hình đã chạy |
|---|---|
| Rollout | K=8/câu, sinh CoT + SQL bằng global model đầu round |
| Pair | Một pair/câu mixed; giữ quy tắc nearest final SQL hiện có |
| Loss | DPO + NLL trên chosen; beta 0.1, NLL alpha 1 |
| Local training | Bắt đầu với một epoch trên tập pair, lr 1e-5 |
| Reference | Bản frozen của Gt, chung cho các client trong round; cập nhật ở round sau |
| FedAvg | Giữ weighting theo private-data size của setup cũ; báo thêm số pair/client |
| Round tiếp theo | Từ global adapter sau FedAvg, sinh lại trên cùng local pool |

Các output trong một lượt sampling dùng cùng model đầu round. Model chỉ cập
nhật khi train DPO; không sinh lại candidate giữa các optimizer step. NLL học
bắt chước chosen, không bắt chước rejected. Trường hợp gold không kiểm được,
output chưa kết thúc hoặc vượt context phải có số lượng và lý do loại rõ ràng.
Phạm vi xử lý gold trả kết quả rỗng cần được ghi trong recipe trước khi chạy.

Client không có pair private sẽ không tạo một local DPO update mới. Trước khi
launch phải chốt cách xử lý client đó trong aggregation. Public replay, nếu
thêm, không được làm tăng trọng số private của client.

Các giá trị K, số pair và local epoch là lựa chọn pilot. Một local epoch có
tiền lệ trong FedPref; reference cập nhật theo round lấy từ Iterative RPO.
Tổ hợp local execution pairs, rolling reference và FedAvg cho SQL là adaptation
của dự án. Nó chưa được xác nhận bằng kết quả FL của ta.

## 3. Các thực nghiệm hiện tại hỗ trợ quyết định gì?

| Thực nghiệm | Câu hỏi phục vụ đề xuất federated | Trạng thái và cách dùng |
|---|---|---|
| P2.60 `cot1`, `sql1` | Public BIRD tạo student khởi đầu ra sao? | Đã train; nguồn parent của `c1`, `s1`. CoT dùng 1.266 câu, SQL dùng 9.428 nên không phải đối chứng chỉ đổi format |
| P2.62 `c1`, `s1` | Bỏ self-CoT SFT Spider, DPO có cải thiện được student từ public bootstrap không? | Tiếp tục theo queue; là screen centralized cho local objective, chưa phải federated |
| P2.60 SQL route | Recipe có gold Spider SFT rồi DPO mạnh đến đâu? | Mốc mạnh; không đồng nhất với `s1` vốn không có chặng Spider SFT |
| P2.59 `tp`, `tc` và P2.61 E1 | Target, coverage, gold supervision và reasoning ảnh hưởng thế nào? | Evidence chẩn đoán; không kết luận độ dài là nguyên nhân đã được cô lập |
| Đếm teacher pairs BIRD | Cache hiện có có đủ contrast để thử teacher-DPO không? | Đã có chức năng đếm; chặng public DPO chưa implement |
| Full-local DPO + FedAvg | Gain của local objective có sống qua aggregation và các round không? | Là thí nghiệm federated cần triển khai sau giai đoạn chuẩn bị |

Lịch centralized hiện tại dùng tối đa 1.200 câu mới mỗi round, tối đa hai
pair/câu và hai epochs. Hai round retry quay lại các câu chưa giải được.
Đó là lựa chọn screen theo compute, không phải lịch full-local đích. Một
centralized RL round hiện tại không tương đương một global FL round.

Kết quả mới cập nhật vào LAB_LOG trước; bảng trên chỉ đổi khi kết quả làm thay
đổi recipe, parent hoặc thứ tự thử. Số mới chỉ được báo trong chat chưa được
coi là evidence đã publish.

## 4. BIRD trong giai đoạn private

Mốc đầu tiên là pipeline ở mục 2, không thêm replay. Nhánh tiếp theo là một
cache public BIRD gồm teacher CoT đúng, gửi một lần cho client để thêm một
phần NLL nhỏ trong local training. Teacher không chạy tại client; private
pair vẫn do student và execution tại client tạo ra.

Lượng replay và hệ số loss chưa chốt. CoT dài hơn SQL-only nên phải báo cả
target tokens và optimizer steps, không chỉ tỉ lệ số câu. BIRD CoT replay
cùng local DPO là adaptation cần thử, chưa có kết quả trực tiếp tại dự án.

Evidence cũ hướng dẫn vị trí của nhánh này:

- P2.48: một server step nâng BIRD dev 36,77 lên 45,18 nhưng hạ Spider dev
  71,57 xuống 65,57; private round sau phục hồi Spider và mất phần lớn gain
  BIRD. Các step BIRD riêng giữa round chưa phải mặc định cho pipeline mới.
- Client replay trước đây giữ BIRD tốt hơn. Trên Spider test, replay so với
  không replay chênh -0,33 và +0,47 ở hai seed: chưa có lợi ích private rõ ràng.

Đây là kết quả Hinton/replay cũ, không phải kết quả CoT-DPO. Chi tiết ở
[LAB_LOG, P2.48 và tổng hợp hai seed](LAB_LOG.md).

## 5. Cơ sở literature và các cách CoT

| Nguồn | Phần dùng cho phương pháp | Phần chưa khớp với ta |
|---|---|---|
| [ExCoT, Findings ACL 2025](https://aclanthology.org/2025.findings-acl.982.pdf), §3-4 | Teacher traces có execution check, SFT, off-policy DPO, sinh lại dữ liệu cho iterative DPO | Centralized, student 32B/70B; teacher đọc cả BIRD và Spider |
| [Iterative RPO, NeurIPS 2024](https://arxiv.org/html/2404.19733v3), §2 | DPO + NLL, model mới sinh lại trên cùng prompt pool, reference theo iteration | Toán và reasoning, chưa phải SQL hay FL |
| [OpenFedLLM, KDD 2024](https://arxiv.org/html/2402.06954), §3.3 | Local DPO và aggregate LoRA trong FL | Preference alignment, không có SQL execution hoặc teacher BIRD |
| [FedPref, bản preprint được nhận tại ELAMI/MICCAI 2026](https://arxiv.org/html/2608.16971), §3 | Local DPO một epoch/round, trao đổi LoRA rồi FedAvg cho structured output | Teacher tại client, pairs và SFT reference cố định; ta sinh private pairs bằng student mỗi round |

Trong các nguồn đã kiểm ngày 2026-11-03 chưa tìm thấy federated DPO cho
Text-to-SQL đúng setup này. Không dùng kết quả tìm kiếm đó để claim “first”.
Code ExCoT chọn một pair/câu theo edit distance toàn output; pairing theo
SQL của ta là adaptation, dù paper mô tả khoảng cách giữa SQL.

Prompt giữ nguyên trong phép thử federation đầu tiên. Các lựa chọn sau được
thử riêng để không trộn thay đổi format với tác động FedAvg:

| Cách CoT | Nguồn và tình trạng |
|---|---|
| Free-form step-by-step rồi SQL | [OmniSQL](https://arxiv.org/html/2503.02240), adaptation inference prompt đang dùng. OmniSQL synthesis có SQL tham chiếu; teacher của ta không thấy gold |
| Divide-and-conquer, pseudo-SQL, ghép và tối ưu query | ExCoT §3.2, Appendix A; teacher tự giải với few-shot. Ứng viên format tiếp theo |
| Clause-driven theo logic order | [VCoT-SQL](https://aclanthology.org/2026.emnlp-main.2686.pdf), §3.1, Appendix E; teacher 7B, few-shot và gold khi synthesis |
| Reasoning steps và retry/self-correction | [RetrySQL](https://arxiv.org/html/2507.02529), §3; tạo reasoning từ SQL tham chiếu, thêm retry là thay recipe training |
| Tự giải, câu sai sinh lại với gold hint | [STaR-SQL](https://aclanthology.org/2025.acl-long.1187/); là cách tổng hợp dữ liệu lặp, không phải một format cố định. Không thêm lại self-CoT SFT vào pipeline chính |
| Các dòng ngắn Tables/Joins/Filters/... | Format của dự án, không phải prompt nguyên bản từ một paper; chưa thay prompt chính |

## 6. Thứ tự chuẩn bị và đánh giá

1. Hoàn tất các screen đang chạy theo queue để chọn parent và đọc đường EX,
   coverage, mixed rate, độ dài, chi phí. Các screen phục vụ phương pháp FL,
   không bắt buộc tối ưu đến một centralized ceiling trước khi thử FL.
2. Đếm cache teacher pairs, thử thêm public teacher-DPO. Mở rộng public BIRD
   theo phép đo coverage/compute, tiến tới full pool của pipeline đích. Mốc
   cùng public CoT SFT nhưng không teacher-DPO tách tác dụng chặng này.
3. Chọn public bootstrap cho pilot full-local DPO + FedAvg, giữ prompt hiện
   tại. Có thể kiểm federation trước khi trả chi phí sinh full BIRD; phải ghi
   đúng public pool đã dùng. So CoT và SQL-only dưới cùng split và lịch private.
   Đo global EX sau aggregation; không suy từ local loss rằng global EX sẽ tăng.
4. Thử BIRD replay nếu cần giữ public reasoning qua FL. Đổi prompt CoT sau
   phép thử federation đầu, trên cùng recipe để đọc được tác dụng format.

Metric chính là Spider EX của global student. Chọn cấu hình trên dev; các arm
được chốt cho paper chạy Spider test và nhiều seed theo protocol của dự án.
So central và FL phải ghi đúng private passes, generation, pair exposure,
public training và compute. BIRD và robustness dùng theo phạm vi evaluation
hiện hành; kiểm retention BIRD cần được đưa thành mục đánh giá khi thử replay.

Mục tiêu trước mắt là recipe CoT + RL so với SQL-only. Khi viết bài, không
gọi mọi gain là teacher-specific nếu comparator còn đổi cả format, coverage
và training. Không thêm writer-control vào queue hiện tại chỉ từ tài liệu này.

Các điểm cần chốt trước launch federated: parent; candidate budget public;
local epochs; số global rounds dự kiến; aggregation khi client không có pair;
chính sách gold rỗng; phạm vi evaluation và compute đã đo. Mỗi GPU path mới
cần smoke theo cấu hình A5000 hiện có. Không có training federated nào được
khởi động bởi bản đề xuất này.

## 7. Cập nhật đến khi bắt đầu federated

Tài liệu này giữ pipeline đích, trạng thái từng phần và các quyết định còn mở.
Khi có kết quả mới, cập nhật đúng mục liên quan; số liệu và provenance vẫn ở
LAB_LOG/RESULT_REGISTRY. Khi bắt đầu triển khai FL, ghi recipe được chọn và
liên kết runbook/code tại đây, giữ lại các giới hạn của bằng chứng.

| Ngày | Cập nhật |
|---|---|
| 2026-11-03 | Lập đề xuất theo hướng public teacher CoT SFT và DPO, sau đó full-local student DPO và FedAvg lặp; giữ prompt hiện tại, replay/format là nhánh sau. Các screen hiện tại phục vụ hướng federated này |
