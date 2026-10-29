# FedLS-SQL: bảng 4.2 Overall NL-to-SQL Performance (30/10/2026)

Seed 0. EM và EX tính trên Spider test (2,147 câu); các cột bên phải là
Spider dev, BIRD dev và các biến thể robustness của Spider dev.

| Method                    |        EM |        EX | Trainable Params | Latency (s/câu) | Spider dev EX | BIRD dev EX | Realistic EX |    SYN EX |     DK EX |
| ------------------------- | --------: | --------: | ---------------: | --------------: | ------------: | ----------: | -----------: | --------: | --------: |
| Centralized SLM           |     61.53 |     71.08 |            18.5M |            0.30 |         71.37 |       25.75 |        61.61 |     56.00 |     58.50 |
| Centralized SLM\* (+BIRD) | **65.02** |     73.78 |            18.5M |            0.30 |         73.21 |       43.68 |        62.99 |     58.90 |     58.69 |
| FedAvg-SLM                |     60.22 |     71.50 |            18.5M |            0.30 |         67.60 |       25.68 |        59.65 |     53.68 |     53.27 |
| FedProx-SLM               | đang chạy | đang chạy |            18.5M |       đang chạy |     đang chạy |   đang chạy |    đang chạy | đang chạy | đang chạy |
| FedAvg-SLM\* (+BIRD)      |     63.58 |     72.61 |            18.5M |            0.30 |         71.57 |       41.26 |        62.01 |     55.13 |     53.83 |
| Federated LLM             |           |           |                  |                 |               |             |              |           |           |
| LLM zero-shot             |     46.48 | **77.22** |                0 |            0.83 |     **76.69** |   **47.07** |    **71.06** | **63.83** | **62.43** |
| LLM few-shot (5-shot)     | đang chạy | đang chạy |                0 |       đang chạy |     đang chạy |             |    đang chạy | đang chạy | đang chạy |
| **FedLS-SQL\***           |     64.00 |     73.17 |            18.5M |            0.30 |         74.08 |       44.78 |        63.58 |     58.70 |     57.20 |

Ghi chú:

- \* có dùng BIRD (public data ở server); các dòng khác chỉ dùng Spider.
  BIRD dev chỉ so được giữa các dòng có \*.
- Các dòng SLM cùng một model khi deploy nên latency như nhau; LLM chạy
  4-bit.
- EM của LLM thấp vì model chưa fine-tune trên Spider viết SQL khác style
  gold dù kết quả chạy giống nhau.
