# Email: đổi method, xin ý kiến Thầy

**Tiêu đề:** Xin ý kiến Thầy về method mới và tên bài

Chào Thầy,

Em xin báo cáo việc đổi method và xin Thầy vài ý kiến.

**Method mới.** Em bỏ bước KD từ LLM teacher. Method còn lại: 2 round
FedAvg SFT, sau đó là các round DPO. Mỗi round, client sample SQL từ model
global, chạy trên database của mình để gán nhãn đúng hay sai, rồi train
DPO + NLL trên các cặp đúng và sai đó.

**Lý do bỏ KD.** Gain nhỏ so với compute phải chạy. Ở setup cũ em đo
riêng từng bước trên Spider test (gộp 2 seed):

| Bước | Gain EX | Compute trên một card A5000 |
| --- | ---: | --- |
| Cả bước public (KD trên BIRD) | +1.40 | chạy teacher 7B trên 9,428 câu: khoảng 14 giờ (ước tính từ 5.5 giây mỗi câu); KD: 3.3 đến 3.6 giờ mỗi epoch |
| Riêng teacher, so với train gold SQL trên cùng data | +0.98 (p = 0.04) | như trên; train gold SQL không cần teacher: 2.7 giờ mỗi epoch |
| DPO ở client | **+3.19 đến +3.91** | khoảng 3 giờ mỗi round |

Em để KD làm hướng mở rộng sau.

**Kết quả.** Em so method với hai baseline, trên hai dataset và qua các
student model: FedAvg SFT là baseline federated ở cùng số round, centralized
SFT là mức tham chiếu khi gộp data của mọi client. EX, 5 client non-IID, 4
round.

BIRD dev (dataset chính):

| Model | Chưa train | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 29.47 | chờ chạy | 42.57 | **48.76** | +6.19 |

Spider test:

| Model | Chưa train | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 68.05 | 75.73 | 74.71 | **78.20** | +3.49 |
| Qwen2.5-Coder-0.5B | 54.40 | dự kiến | 64.09 | **66.19** | +2.10 |
| DeepSeek-Coder-1.3B | 55.85 | dự kiến | 69.82 (round 2) | **75.08** (round 3) | +5.26 |

- Method hơn FedAvg SFT trên cả hai dataset và cả ba model; với model
  1.5B trên Spider test, method hơn cả centralized SFT.
- DeepSeek chưa có FedAvg SFT round 3, nên gain tính so với round 2, là
  điểm xuất phát của round DPO.
- Trên BIRD, round tốt nhất của FedAvg SFT là 43.68. Method hơn ở cả ba
  mức độ khó, rõ nhất ở moderate (39.66 so với 29.96), và số SQL lỗi khi
  chạy giảm từ 268 xuống 128.

**Kế hoạch thực nghiệm của bài.** Setup chung: 5 client, mỗi database
nằm trọn ở một client, non-IID (Dirichlet alpha 0.1); student train bằng
LoRA; đo EX trên BIRD dev và Spider test; một seed, kiểm định McNemar trên
từng câu hỏi. BIRD là dataset chính, Spider dùng cho phần mở rộng.

Baseline (model 1.5B):

| Baseline | Là gì | BIRD | Spider |
| --- | --- | --- | --- |
| Chưa train | student gốc | xong | xong |
| Local SFT | mỗi client tự train trên data của mình | không chạy | dự kiến |
| Centralized SFT | SFT trên data gộp của mọi client | chờ chạy | xong |
| FedAvg SFT | SFT trên gold SQL, FedAvg | xong | xong |
| FedProx SFT | như trên, với FedProx | không chạy | dự kiến |
| FedDPO (OpenFedLLM) | DPO trong FedAvg: cặp tạo một lần, reference cố định, không có NLL | chờ chạy | chờ chạy |

Ablation (method bỏ từng phần):

| Phần bỏ đi | Hàng so sánh | BIRD | Spider |
| --- | --- | --- | --- |
| Sample lại mỗi round | các round sau dùng lại cặp và reference của round DPO đầu | xong | xong |
| NLL term | DPO thuần | chờ chạy | xong |
| Thành phần preference | chỉ NLL trên các sample đúng | round đầu xong, 4 round chờ chạy | round đầu xong, 4 round chờ chạy |
| 2 round SFT đầu | số round SFT trước DPO: k = 0, 1, 2, 3 | k = 2 xong; k = 0, 1 mới đến 2 round | k = 0, 2, 3 xong |
| Trọng số FedAvg | theo số cặp, theo số câu hỏi, đều nhau | xong | xong |

Thực nghiệm mở rộng và phân tích:

| Thực nghiệm | Nội dung | Dataset | Trạng thái |
| --- | --- | --- | --- |
| Student model khác | Qwen2.5-Coder-0.5B, DeepSeek-Coder-1.3B: FedAvg SFT, method, centralized SFT | Spider | 0.5B xong; DeepSeek chờ round 3 và 4; centralized SFT dự kiến |
| Mức non-IID | alpha 0.1 và IID, FedAvg SFT và method | Spider | alpha 0.1 xong; IID chờ chạy |
| Federated so với gộp client | các round DPO trên data gộp, không aggregation | Spider | chờ chạy |
| FedAvg SFT chạy thêm round | baseline có đuổi kịp method không | Spider | xong |
| Robustness | Spider-Syn, Spider-Realistic, Spider-DK | Spider | 1.5B xong; hai model kia chờ chạy |
| Test-suite accuracy | SQL đúng trên nhiều bản database, không chỉ một | Spider dev | 1.5B và 0.5B xong |
| Loại lỗi theo round | execution error và wrong result | cả hai | xong |
| Kết quả theo độ khó | BIRD: simple, moderate, challenging; Spider: easy đến extra | cả hai | xong |
| Client update | số cặp theo round và client, cosine giữa các client update | cả hai | xong |
| Chi phí | thời gian mỗi round ở client (sample, chạy SQL, train), dung lượng adapter gửi đi | cả hai | dự kiến, lấy từ log |

**Khoảng trống.** Federated Text-to-SQL mới có một bài (Zhang et al., ACL
2023: T5-base, chỉ SFT). CodeLutra (TMLR 2025) có vòng sample, execution
và DPO tương tự nhưng train tập trung; em tìm thấy bài này sau khi thiết
kế. Phần mới của em: nhãn execution do từng client tạo trên database
riêng, sample lại theo từng round FL, với model 1.5B.

Em xin Thầy ba việc:

1. Đặt giúp em tên bài (tên tạm: FedLS-SQL).
2. Xem kế hoạch baseline, ablation và thực nghiệm như trên đã đủ chưa ạ.
3. Khoảng trống như trên có đủ cho một bài không ạ.

Em cảm ơn Thầy.
