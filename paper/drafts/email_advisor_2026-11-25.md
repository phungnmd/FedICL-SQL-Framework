# Email: báo cáo method và hướng của bài

**Tiêu đề:** Báo cáo Thầy về method và hướng của bài (25/11)

Chào Thầy,

Em xin báo cáo ngắn về method hiện tại, kết quả mới trên BIRD và hướng
tiếp theo của bài.

**1. Method**

Hai round FedAvg SFT trên gold SQL, sau đó là các round DPO. Trong mỗi
round DPO, client sample SQL từ model global của round đó, chạy trên
database của mình để gán nhãn đúng hay sai, rồi train DPO + NLL trên các
cặp đúng và sai; server lấy trung bình như FedAvg. Bản hiện tại không có
bước LLM public.

**2. Kết quả** (student Qwen2.5-Coder-1.5B, 5 client non-IID, EX, một seed)

| Tổng số round | BIRD dev: FedAvg SFT | BIRD dev: method | Spider test: FedAvg SFT | Spider test: method |
| ---: | ---: | ---: | ---: | ---: |
| 2 (SFT, chung) | 42.70 | | 74.10 | |
| 3 | 43.68 | 46.22 | 74.71 | 77.46 |
| 4 | 42.57 | **48.76** | 74.71 | **78.20** |

- Ở 4 round, method hơn FedAvg SFT 6.19 điểm trên BIRD dev (p < 0.001;
  hơn round tốt nhất của FedAvg SFT 5.08 điểm) và 3.49 điểm trên Spider
  test.
- Chạy thêm round không giúp FedAvg SFT: nó giảm ở round 4 trên BIRD và
  ở round 5 trên Spider (73.92).
- Với Qwen2.5-Coder-0.5B trên Spider test: 66.19 so với 64.09 (+2.10,
  p = 0.006).

**3. Từng phần đóng góp gì**

- Sample lại mỗi round, so với cặp tạo một lần và reference cố định như
  FedDPO của OpenFedLLM: +2.61 trên BIRD (p < 0.001); trên Spider test
  không khác.
- NLL term: bỏ đi thì một round DPO cho 73.59 trên Spider test, dưới điểm
  xuất phát 74.10; có NLL là 77.46.
- Thành phần preference: ở round DPO đầu nó cho khoảng một nửa gain, nửa
  còn lại đến từ NLL trên các sample đúng (so với chỉ NLL: +1.59 trên
  Spider test, p = 0.015; +1.83 trên BIRD, p = 0.057). Tác dụng rõ nhất là
  giảm execution error (BIRD: 247 xuống 91). Em đang chạy so sánh này ở 4
  round.
- Hai round SFT đầu: trên test-suite accuracy (Spider dev), chỉ dạng có
  SFT trước mới hơn FedAvg SFT (+2.42); bắt đầu thẳng từ base model thì
  không.

**4. Hướng tiếp theo**

- BIRD là dataset chính của bài: gain lớn hơn và các phần của method tách
  rõ ở đó. Spider dùng cho phần mở rộng: ba student model, split IID,
  Spider-Syn, Realistic, DK và test-suite accuracy.
- Các hàng còn chạy: so sánh với chỉ NLL ở 4 round, FedDPO theo
  OpenFedLLM và centralized SFT trên BIRD, split IID, DeepSeek-Coder-1.3B.
- Journal em đang cân nhắc: JIIS (Springer) và CMC.

Em xin ý kiến Thầy hai điểm:

1. Method và hướng lấy BIRD làm dataset chính như trên đã ổn chưa ạ?
2. Giữa JIIS và CMC, Thầy nghiêng về journal nào ạ?

Em cảm ơn Thầy.
