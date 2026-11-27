<!-- cold review | 2026-11-27 07:06 | codex-cli 0.170.0 | model: gpt-6.2-astra | effort: high | session 1 of 1
     prompt: owner question (verbatim)
     isolation: fresh /private/tmp dir with the PDF only, --ignore-user-config, memories off, --ephemeral; the owner's global ~/.codex/AGENTS.md (general preferences, no project content) may still load
     file: paper/manuscript/build/main.pdf sha256 b7863a6348c2
     paper git: 3c8fdd3 (dirty) -->

## Prompt

```text
Review bài 1 cách công tâm, đọc bài và cho đánh giá có đủ đăng CMC và JIIS không ( sau khi hoàn thiện, không phải bản draft/ chưa chạy) chủ yếu đánh giá novety rõ ràng

Files in your working directory: main.pdf
```

## Response

**CMC: có. JIIS: sát ngưỡng, mình nghiêng về major revision.** Mình đánh giá bản hoàn thiện theo thiết kế trong bài, với các con số đã báo cáo. **FedLS-SQL có đóng góp mới rõ về cách huấn luyện Text-to-SQL khi mỗi tổ chức giữ database riêng. Độ mới thuật toán thấp, còn giá trị thực nghiệm đủ để thành một bài báo.** Nếu chọn nơi nộp cho công trình này, mình chọn **CMC**.

### FedLS-SQL mới ở đâu?

Phép thử đơn giản nhất là giả sử được gom toàn bộ dữ liệu về một nơi. Khi đó, phần lớn thuật toán đã có trong **CodeLutra**: lấy mẫu từ model hiện tại, chạy SQL để phân đúng/sai, ghép cặp, huấn luyện bằng DPO cộng NLL trên câu đúng, rồi lặp lại. CodeLutra còn đánh giá trên chính **BIRD và Spider**. Ở chiều ngược lại, Zhang et al. đã huấn luyện Text-to-SQL theo federated learning từ năm 2023, còn OpenFedLLM đã dùng DPO giữa các client. Vì vậy, phản biện “CodeLutra chạy ở từng client rồi FedAvg” có cơ sở kỹ thuật. Warm-up bằng SFT, giảm số cặp và chuẩn hóa NLL theo token là các lựa chọn thiết kế hợp lý, nhưng từng thay đổi đều có sức nặng hạn chế về novelty. [CodeLutra, TMLR 2025](https://openreview.net/pdf/596898e8f20e19d0c7790dd96398350c5a7da163.pdf) · [Zhang et al., ACL 2023](https://aclanthology.org/2023.acl-long.678/) · [OpenFedLLM](https://arxiv.org/abs/2402.06954)

**Phần mới còn lại có ý nghĩa thực tế.** Mỗi tổ chức chỉ có một câu SQL chuẩn cho mỗi câu hỏi, nhưng có thể dùng database của mình để chấm nhiều câu SQL do model chung sinh ra. Qua mỗi vòng, các tổ chức cùng cải thiện một model mà câu hỏi, SQL và kết quả truy vấn đều ở lại nơi giữ dữ liệu. Server vẫn chỉ nhận adapter và một số đếm. Trong các công trình mình đối chiếu, chưa thấy bài trước dùng đúng cơ chế này để huấn luyện federated Text-to-SQL. Mình đồng ý với claim hẹp ở mục 3.4 của tác giả. Điểm mình đánh giá khác là **giá trị xuất bản nằm nhiều hơn ở điều các thí nghiệm cho thấy về cơ chế đó, còn chữ “first” tự nó có ít sức nặng**. [Bản thảo, mục 2.4 và 3.4](/private/tmp/review.uXzBTl/main.pdf)

### Kết quả nào thực sự có sức nặng?

- **Mức tăng đủ lớn để có giá trị ứng dụng.** Sau cùng bốn vòng, execution accuracy tăng từ **42,57% lên 48,76% trên BIRD dev** và từ **74,71% lên 78,20% trên Spider test**. Cả hai chênh lệch đều có ý nghĩa sau hiệu chỉnh Holm, trên database mà các client chưa thấy. Trên BIRD, hai vòng preference tốn lần lượt 2,7 và 2,3 lần thời gian của một vòng SFT. Kết luận được dữ liệu hỗ trợ là mô hình chính xác hơn với cùng số vòng giao tiếp, có đánh đổi bằng compute tại client. [Bảng 3 và 7](/private/tmp/review.uXzBTl/main.pdf)
- **Ablation xác định được giới hạn của claim về DPO.** Làm mới đồng thời các cặp và reference model đem lại **2,61 điểm EX trên BIRD**, nhưng chỉ **0,18 điểm trên Spider**. Sau vòng preference đầu tiên, so với chỉ học các mẫu đúng đã được execution xác nhận, thêm DPO đem lại **1,83 điểm trên BIRD** và **1,59 điểm trên Spider**. Cả hai chênh lệch sau đều chưa đạt ý nghĩa sau hiệu chỉnh Holm. Do đó, mình tin kết luận *execution feedback tại client giúp ích*. Việc quy phần lớn mức tăng 6,19 điểm cho *preference optimization* sẽ vượt quá bằng chứng. [Bảng 8](/private/tmp/review.uXzBTl/main.pdf)
- **Phát hiện đáng đăng nhất là sự thay đổi loại lỗi.** Trên BIRD, số truy vấn lỗi thực thi giảm từ **268 xuống 128**. Trong 153 câu chỉ FedLS-SQL trả lời đúng, có **75** câu baseline gặp lỗi thực thi và **78** câu baseline chạy được nhưng trả lời sai. Tức là phương pháp thực sự sửa được cả hai dạng lỗi. Tuy nhiên, **107** truy vấn từng báo lỗi nay chạy được và trả về đáp án sai. Với người dùng giao diện hỏi đáp database, điều này quan trọng: xác suất nhận đáp án đúng tăng, đồng thời một phần lỗi từng nhìn thấy được trở thành kết quả sai khó nhận ra. Đây là nhận xét có giá trị riêng ngay cả với độc giả đã biết CodeLutra. [Mục 5.4 và 7.1](/private/tmp/review.uXzBTl/main.pdf)

### Vì sao mình chấm hai tạp chí khác nhau?

**CMC (*Computers, Materials & Continua*)**. Nếu phản biện bản hoàn thiện, mình **nghiêng về chấp nhận sau sửa**. Bài có một ràng buộc ứng dụng rõ, một cách tận dụng dữ liệu phù hợp với ràng buộc đó, mức tăng trên hai benchmark và phân tích được chi phí lẫn loại lỗi. Chừng đó đủ cho một bài AI ứng dụng có đóng góp thực nghiệm. CMC cũng đã đăng nghiên cứu đánh giá LLM sinh SQL trên database quan hệ, nên mức độ phù hợp về chủ đề có tiền lệ trực tiếp. [Phạm vi CMC](https://www.techscience.com/cmc/info/journal_overview) · [Nghiên cứu về SQL generation trên CMC](https://www.techscience.com/cmc/v88n2/67604)

**JIIS (*Journal of Intelligent Information Systems*)**. Đây thậm chí là nơi **khớp chủ đề hơn**. JIIS quan tâm trực tiếp đến giao diện truy vấn thông minh và đã đăng **GradeSQL**, dùng execution label để huấn luyện bộ chọn câu SQL. FedLS-SQL huấn luyện chính model sinh SQL trong điều kiện nhiều bên giữ database riêng, nên hai bài có đóng góp khác nhau. Điều khiến mình dừng ở **major revision** là câu hỏi về federation: **khi buộc phải tách database theo tổ chức, phương pháp giữ được bao nhiêu lợi ích của cùng một quy trình học từ execution nếu được phép gom dữ liệu?** Dòng *Clients pooled* trong thiết kế của bài là đối chứng đúng cho câu hỏi này trên Spider. Nếu bản hoàn thiện định lượng rõ khoảng cách đó và cho thấy nó thay đổi thế nào theo cách chia client, mình sẽ nghiêng về chấp nhận ở JIIS. Một khoảng cách nhỏ **hoặc** một mức suy giảm được giải thích tốt đều có giá trị. Chỉ riêng việc thắng FedAvg SFT chưa trả lời được câu hỏi này. [Phạm vi JIIS](https://link.springer.com/journal/10844/aims-and-scope) · [GradeSQL, JIIS](https://link.springer.com/article/10.1007/s10844-026-01071-6)

Mình sẽ giữ hướng nghiên cứu hiện tại. Với **CMC**, đóng góp ứng dụng và bằng chứng thực nghiệm đã tạo thành một câu chuyện đủ trọn vẹn. Với **JIIS**, kết quả có thể đổi phán quyết của mình là đối chứng *pooled* và ảnh hưởng của cách chia client, hơn là thêm một model hoặc thêm một benchmark.

*Git không cho khởi tạo repository vì thư mục `.git` bị giới hạn quyền ghi. Mình chỉ đọc bản thảo và không sửa file.*