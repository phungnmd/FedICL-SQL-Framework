# FedLS-SQL: bảng 4.2 Overall NL-to-SQL Performance (30/10/2026)

Seed 0. EM và EX tính trên Spider test (2,147 câu); các cột bên phải là
Spider dev, BIRD dev và các biến thể robustness của Spider dev.

| Method                                                     |        EM |        EX | Trainable Params | Latency (s/câu) | Spider dev EX | BIRD dev EX | Realistic EX |    SYN EX |     DK EX |
| ---------------------------------------------------------- | --------: | --------: | ---------------: | --------------: | ------------: | ----------: | -----------: | --------: | --------: |
| Centralized SLM (Spider)                                   |     61.53 |     71.08 |            18.5M |            0.30 |         71.37 |       25.75 |        61.61 |     56.00 |     58.50 |
| Centralized SLM\* (Spider + BIRD gộp, không privacy)       | **65.02** |     73.78 |            18.5M |            0.30 |         73.21 |       43.68 |        62.99 |     58.90 |     58.69 |
| FedAvg-SLM (Spider, 5 client)                              |     60.22 |     71.50 |            18.5M |            0.30 |         67.60 |       25.68 |        59.65 |     53.68 |     53.27 |
| FedProx-SLM (Spider, 5 client)                             | đang chạy | đang chạy |            18.5M |       đang chạy |     đang chạy |   đang chạy |    đang chạy | đang chạy | đang chạy |
| FedAvg-SLM\* + public BIRD (Spider, 5 client; không teacher) |     63.58 |     72.61 |            18.5M |            0.30 |         71.57 |       41.26 |        62.01 |     55.13 |     53.83 |
| Federated LLM (7B, Spider, 5 client)                       |           |           |                  |                 |               |             |              |           |           |
| LLM zero-shot (7B)                                         |     46.48 | **77.22** |                0 |            0.83 |     **76.69** |   **47.07** |    **71.06** | **63.83** | **62.43** |
| LLM few-shot (7B, 5 ví dụ từ Spider train)                 | đang chạy | đang chạy |                0 |       đang chạy |     đang chạy |             |    đang chạy | đang chạy | đang chạy |
| **FedLS-SQL\*** (Spider, 5 client; BIRD và teacher ở server) |     64.00 |     73.17 |            18.5M |            0.30 |         74.08 |       44.78 |        63.58 |     58.70 |     57.20 |

Ghi chú:

- SLM là Qwen2.5-Coder-1.5B + LoRA r16 (18.5M tham số train, 1.2% model);
  LLM là Qwen2.5-Coder-7B.
- \* dùng thêm BIRD (public data ở server). Các baseline FL không có \*
  chỉ dùng Spider của client, như cách FedCoLLM và FedDF so với FedAvg.
  BIRD dev chỉ so được giữa các dòng có \*.
- Mọi dòng SLM khi deploy là cùng một model, nên latency như nhau. Latency
  đo trên RTX A5000, batch 16, gồm cả thời gian chấm SQL; LLM chạy 4-bit.
- EM của LLM thấp vì EM so cấu trúc SQL với gold, mà model chưa fine-tune
  trên Spider viết SQL khác style dù kết quả chạy giống nhau.
