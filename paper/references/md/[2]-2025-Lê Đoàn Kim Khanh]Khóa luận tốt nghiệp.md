TRƯỜNG ĐẠI HỌC QUY NHƠN
KHOA CÔNG NGHỆ THÔNG TIN
TRƯỜNG ĐẠI HỌC QUY NHƠN
KHOA CÔNG NGHỆ THÔNG TIN

KHÓA LUẬN TỐT NGHIỆP
ĐỀ CƯƠNG
KHÓA LUẬN TỐT NGHIỆP
ỨNG DỤNG HỌC LIÊN KẾT CHO MỘT SỐ BÀI
XÂY DỰNG MÔ HÌNH DEEP LEARNING NHẬN DẠNG BIỂN BÁO GIAO
TOÁN XỬ LÝ NGÔN NGỮ TỰ NHIÊN
THÔNG

Sinh viên

Giảng viên hướng dẫn
Sinh viên
Mã sinh viên
Chuyên ngành
Chuyên ngành
Khóa học
Khóa học
Lớp

TS. Lê Quang Hùng
Lê Đoàn Kim Khanh
4451050862
Lê Thị Minh Tâm
Trí tuệ nhân tạo
Khoa học máy tính
K44
K41
CNTT K44E

Người hướng dẫn

TS. Lê Xuân Vinh

Quy Nhơn, tháng 10 năm 2024

TRƯỜNG ĐẠI HỌC QUY NHƠN
KHOA CÔNG NGHỆ THÔNG TIN
TRƯỜNG ĐẠI HỌC QUY NHƠN
KHOA CÔNG NGHỆ THÔNG TIN

KHÓA LUẬN TỐT NGHIỆP
ĐỀ CƯƠNG
KHÓA LUẬN TỐT NGHIỆP
ỨNG DỤNG HỌC LIÊN KẾT CHO MỘT SỐ BÀI
XÂY DỰNG MÔ HÌNH DEEP LEARNING NHẬN DẠNG BIỂN BÁO GIAO
TOÁN XỬ LÝ NGÔN NGỮ TỰ NHIÊN
THÔNG

Giảng viên hướng dẫn
Sinh viên
Sinh viên
Mã sinh viên
Chuyên ngành
Chuyên ngành
Khóa học
Khóa học
Lớp

TS. Lê Quang Hùng
Lê Đoàn Kim Khanh
Lê Thị Minh Tâm
4451050862
Trí tuệ nhân tạo
Khoa học máy tính
K44
K41
CNTT K44E

Người hướng dẫn

TS. Lê Xuân Vinh

Quy Nhơn, tháng 10 năm 2024

LỜI CẢM ƠN

Trước tiên, em xin gửi lời cảm ơn chân thành và sâu sắc đến quý thầy, cô khoa

Công nghệ thông tin trường Đại Học Quy Nhơn, những người đã tận tình giảng dạy,

truyền đạt kiến thức và tạo điều kiện thuận lợi cho em trong suốt quá trình học tập tại
trường.

Đặc biệt, em xin bày tỏ lòng biết ơn sâu sắc đến thầy Lê Quang Hùng – người đã

trực tiếp hướng dẫn, định hướng và hỗ trợ em trong suốt quá trình thực hiện khóa

luận tốt nghiệp. Nhờ sự tận tình chỉ bảo, những góp ý quý báu của thầy, em đã có thể

hoàn thành tốt đề tài nghiên cứu của mình.

Em cũng xin gửi lời cảm ơn đến các anh/chị, bạn bè và gia đình đã luôn đồng hành,
động viên, hỗ trợ em cả về tinh thần và kiến thức trong suốt quá trình học tập và hoàn

thành khóa luận.

Mặc dù đã cố gắng hết sức, nhưng khóa luận không tránh khỏi những thiếu sót.

Em rất mong nhận được sự thông cảm và góp ý từ quý thầy cô để em có thể hoàn

thiện hơn trong các nghiên cứu sau này.

Em xin chân thành cảm ơn!

Lê Đoàn Kim Khanh.

MỤC LỤC

Danh mục hình ảnh ................................................................................................................ 1

Danh mục chữ viết tắt ............................................................................................................ 2

Mở đầu ................................................................................................................................... 4

1.  Lý do chọn đề tài ....................................................................................................... 4

2.  Tổng quan .................................................................................................................. 4

3.  Mục tiêu ..................................................................................................................... 5

4.  Phạm vi nghiên cứu ................................................................................................... 5

5.  Bố cục của khóa luận ................................................................................................. 5

Chương 1: Giới thiệu ............................................................................................................. 6

1.1.

Sơ lược về xử lý ngôn ngữ tự nhiên ....................................................................... 6

1.2.  Các kỹ thuật trong xử lý ngôn ngữ tự nhiên .......................................................... 7

1.2.1.

1.2.2.

1.2.3.

Kỹ thuật tiền xử lý ......................................................................................... 7

Kỹ thuật biểu diễn văn bản .......................................................................... 10

Học máy và học sâu ..................................................................................... 14

1.2.4.  Mô hình ngôn ngữ lớn ................................................................................. 15

1.2.5.

Kỹ thuật chuyên biệt cho các tác vụ cụ thể .................................................. 16

1.3.  Một số ứng dụng xử lý ngôn ngữ tự nhiên .......................................................... 18

1.4.  Các tiêu chí đánh giá ............................................................................................ 19

1.5.

Sơ lược về học liên kết ........................................................................................ 20

1.5.1.

1.5.2.

1.5.3.

Khái niệm và mô hình toán học ................................................................... 20

Thách thức dữ liệu không đồng nhất ........................................................... 22

Các thuật toán tối ưu .................................................................................... 23

1.5.4.  Mô hình triển khai ........................................................................................ 25

1.5.5.

Các thách thức về bảo mật và riêng tư ......................................................... 28

1.6.

Tổng kết chương 1 ............................................................................................... 28

Chương 2: Học liên kết cho một số bài toán xử lý ngôn ngữ tự nhiên ................................ 30

2.1.  Định nghĩa bài toán .............................................................................................. 30

2.1.1.

2.1.2.

Bài toán 1. Sinh văn bản .............................................................................. 30

Bài toán 2. Phân loại văn bản ...................................................................... 31

2.2. Mô hình BART ......................................................................................................... 33

2.2.1. Giới thiệu ........................................................................................................... 33

2.2.2. Kiến trúc của BART .......................................................................................... 33

2.2.2.1.  Kiến trúc tổng quan seq2seq ...................................................................... 33

2.2.2.2. Bộ mã hóa hai chiều .................................................................................... 35

2.2.2.3.  Bộ giải mã tự hồi quy ................................................................................ 39

2.2.3. Ứng dụng của BART trong học liên kết ............................................................ 41

2.2.4. Ưu điểm của BART trong học liên kết .............................................................. 42

2.3. Thuật toán FedOPT ................................................................................................... 43

2.3.1. Giới thiệu về FedOPT ........................................................................................ 43

2.3.2. Kỹ thuật nén trong SCA trong FedOPT............................................................. 43

2.3.3.

2.3.4.

Tích hợp bảo mật trong FedOPT cho xử lý ngôn ngữ tự nhiên ................... 45

Kiến trúc triển khai FedOPT trong hệ thống học liên kết ............................ 45

2.4.  Quy trình ứng dụng học liên kết trong xử lý ngôn ngữ tự nhiên ......................... 47

2.5.

Tổng kết chương 2 ............................................................................................... 50

Chương 3: Thực nghiệm ...................................................................................................... 52

3.1. Dữ liệu ...................................................................................................................... 52

3.1.1. AgNews ............................................................................................................. 52

3.1.2.

3.1.3.

20News ........................................................................................................ 53

CNN/Dailymail ............................................................................................ 54

3.2.  Cài đặt thực nghiệm ............................................................................................. 56

3.3.  Đánh giá ............................................................................................................... 58

3.3.2.

3.3.3.

3.3.4.

Phân loại văn bản ......................................................................................... 58

Sinh văn bản ................................................................................................. 65

Thực nghiệm so sánh trên nhiều số lượng client khác nhau ........................ 66

Kết luận ................................................................................................................................ 69

1.  Tóm lược các kết quả đạt được ................................................................................ 69

2.  Hướng phát triển tương lai: ...................................................................................... 69

Tài liệu tham khảo ............................................................................................................... 71

Danh mục hình ảnh

Hình 1. Kiến trúc tổng quan của BART .............................................................................. 34
Hình 2. Các chiến lược làm nhiễu........................................................................................ 37
Hình 3. Quá trình mã hóa văn bản nhiễu hai chiều .............................................................. 38
Hình 4.Kiến trúc triển khai FedOPT trong hệ thống FL ...................................................... 46
Hình 5. Quy trình áp dụng FL trong NLP............................................................................ 47
Hình 6. Trực quan dữ liệu - AgNews .................................................................................. 52
Hình 7. Trực quan dữ liệu - 20News ................................................................................... 53
Hình 8. Trực quan dữ liệu - CNN/Dailymail ....................................................................... 55
Hình 9. Quy trình cài đặt thực nghiệm ................................................................................ 56
Hình 10. Biểu đồ phân tán dữ liệu 20News trên các client.................................................. 58
Hình 11. Biểu đồ phân bố dữ liệu AgNews trên các client.................................................. 59
Hình 12. Accurary trên tập dữ liệu 20News ........................................................................ 60
Hình 13. F1-score trên tập dữ liệu 20News ......................................................................... 61
Hình 14. Accurary trên tập dữ liệu AgNews ....................................................................... 62
Hình 15. F1-score trên tập dữ liệu 20News ......................................................................... 63
Hình 16. Kết quả thực nghiệm sinh văn bản ........................................................................ 65
Hình 17. Biểu đồ phân tán dữ liệu trên số lượng client khác nhau ...................................... 66
Hình 18. Kết quả thực nghiệm trên nhiều số lượng client khác nhau .................................. 67

1

Danh mục chữ viết tắt

Chữ viết tắt

Ý nghĩa

NLP

FL

NFD

NFC

BoW

CBOW

TF-IDF

Natural Language Processing (Xử lý ngôn ngữ tự nhiên)

Federated Learning (Học liên kết)

Normalization Form Decomposed (Dạng chuẩn hóa phân rã)

Normalization Form Composed (Dạng chuẩn hóa tổ hợp)

Bag-of-Words (Túi từ)

Continuous Bag-of-Words

Term Frequency - Inverse Document Frequency

Word2Vec

Word to Vector

GloVe

SVM

RNN

LSTM

GRU

CNN

LLMs

NER

Global Vectors for Word Representation

Support Vector Machine

Recurrent Neural Network

Long Short-Term Memory

Gated Recurrent Unit

Convolutional Neural Network

Large Language Models

Named Entity Recognition

POS Tagging

Part-of-Speech Tagging

FedFMC

Federated Feature Matching and Clustering

FedCD

FedAvg

Federated Clustering and Distillation

Federated Averaging

2

Chữ viết tắt

Ý nghĩa

FedProx

Federated Proximal

NLG

FFN

GeLU

ReLU

SCA

SGD

Natural Language Generation

Feed Forward Network

Gaussian Error Linear Unit

Rectified Linear Unit

Sparse Compression Algorithm

Stochastic Gradient Descent

3

Mở đầu

1.  Lý do chọn đề tài
Xử  lý  ngôn  ngữ  tự  nhiên  (Natural  Language  Processing  -  NLP)  là  một  trong
những lĩnh vực ứng dụng phổ biến và dễ thấy nhất của Trí tuệ nhân tạo trong những

năm gần đây. Một phần là do nó liên quan đến đặc điểm chung của con người: ngôn

ngữ. NLP phát triển các thuật toán và mô hình để phân tích, hiểu và tạo ngôn ngữ của

con người theo cách có thể được sử dụng cho nhiều ứng dụng khác nhau, chẳng hạn

như dịch ngôn ngữ, phân tích tình cảm và tạo văn bản.

Văn  bản  là  phương  tiện  giao  tiếp  tự  nhiên  của  con  người  và  dữ  liệu  văn  bản

thường truyền tải thông tin cá nhân. Do đó, nhiều ứng dụng NLP (ví dụ: dự đoán từ

tiếp theo, nhận dạng cảm xúc, phân tích tình cảm, phân loại văn bản, v.v.) đã chuyển

từ mô hình tập trung sang phi tập trung, nơi dữ liệu văn bản do người dùng tạo (như

hồ sơ lâm sàng, truy vấn web, v.v.) không cần phải gửi đến máy chủ trung tâm.

Học  liên  kết  (Federated  Learning  -  FL)  là  một  phương  pháp  học  máy  phi  tập

trung cho phép đào tạo các mô hình mà không cần chia sẻ dữ liệu cục bộ. Do đó, FL
bảo vệ quyền riêng tư tốt hơn so với học máy tập trung. Khóa luận này nghiên cứu

ứng dụng FL cho một số bài toán NLP, bao gồm: (i) sinh văn bản, và (ii) phân loại

văn bản.

2.  Tổng quan
FL đã trở thành một cách tiếp cận học máy mới để đào tạo một mô hình trên nhiều

thiết bị biên phi tập trung. Thuật ngữ FL lần đầu tiên được đề xuất vào năm 2016.

Trong bối cảnh thực tế, các tổ chức như các bệnh viện khác nhau sở hữu dữ liệu bí

mật, trong khi các bệnh viện này muốn đào tạo một mô hình phân loại bệnh để sử

dụng chung, việc yêu cầu họ tải dữ liệu của mình lên đám mây là điều rất khó. Ngay

cả trong cùng một bệnh viện, các khoa khác nhau thường lưu thông tin bệnh nhân cục
bộ. Một ví dụ khác là con người tạo ra rất nhiều dữ liệu văn bản bằng điện thoại thông
minh của họ, những dữ liệu này cung cấp nền tảng để huấn luyện các mô hình ngôn
ngữ lớn hiện nay. Tuy nhiên, điều này cho thấy hầu hết các mô hình ngôn ngữ đều
gặp phải các vấn đề về đạo đức, vì chúng có thể làm rò rỉ thông tin cá nhân của người

dùng  theo  cách  không  mong  muốn.  Trong  số  nhiều  nghiên  cứu  về  FL,  Google  và

Apple đi đầu trong việc sử dụng FL trong NLP thông qua các sản phẩm nổi tiếng như

Gboard (Google), Siri (Apple).

4

3.  Mục tiêu
Trong khóa luận này, chúng tôi đặt ra ba mục tiêu chính:

•  Thứ nhất, tìm hiểu cơ sở lý thuyết về NLP, FL.

•  Thứ hai, tìm hiểu cách áp dụng FL cho hai bài toán phân loại văn bản và

sinh văn bản.

•  Thứ ba, cài đặt thực nghiệm.

4.  Phạm vi nghiên cứu
Trong khoá luận này, chúng tôi tìm hiểu cách áp dụng FL cho hai bài toán phân
loại văn bản và sinh văn bản trong xử lý NLP và cài đặt thực nghiệm trên ba tập dữ

liệu là 20News, AgNews và CNN/Dailymail.

5.  Bố cục của khóa luận

Ngoài phần mở đầu và kết luận, khóa luận được tổ chức thành ba chương với bố

cục như sau:

•  Chương 1. GIỚI THIỆU. Giới thiệu tổng quan về NLP gồm có: sơ lược
về NLP, các kỹ thuật trong NLP, một số ứng dụng của NLP, các tiêu chí

đánh giá cho các bài toán NLP, sơ lược về FL.

•  Chương  2.  HỌC  LIÊN  KẾT  CHO  MỘT  SỐ  BÀI  TOÁN  XỬ  LÝ
NGÔN NGỮ TỰ NHIÊN.  Định nghĩa hai bài toán sinh văn bản và phân

loại văn bản, mô hình BART, thuật toán FedOPT, quy trình áp dụng FL
cho hai bài toán này với yêu cầu là sử dụng mô hình BART có tích hợp

thuật toán tối ưu FedOPT.

•  Chương 3. THỰC NGHIỆM. Cài đặt thực nghiệm những yêu cầu đã nêu

ở chương 2.

5

Chương 1: Giới thiệu

Trong chương này, chúng tôi sẽ giới thiệu tổng quan về NLP, bao gồm: NLP là

gì? Các kỹ thuật, ứng dụng của NLP, tiêu chí đánh giá cho các bài toán NLP, tổng
quan về FL.

1.1.

Sơ lược về xử lý ngôn ngữ tự nhiên

NLP đã trở thành một trong những lĩnh vực quan trọng nhất trong học máy và trí

tuệ nhân tạo hiện đại. Theo định nghĩa của các nhà nghiên cứu hàng đầu, NLP được

mô tả như một lĩnh vực trong học máy, nơi các mô hình ngôn ngữ hiện đại thường

được đào tạo với dữ liệu văn bản lớn [1]. Sự phát triển vượt bậc này chủ yếu dựa trên

khả năng xử lý và học hỏi từ những khối lượng dữ liệu văn bản khổng lồ, điều mà
trước đây là không thể tưởng tượng được.

Một trong những yếu tố then chốt quyết định thành công của các mô hình NLP

hiện đại chính là dữ liệu văn bản lớn. Đây là một tập hợp lớn các văn bản được thu

thập từ nhiều nguồn khác nhau để phục vụ cho việc huấn luyện các mô hình ngôn

ngữ. Tầm quan trọng của loại dữ liệu này không thể phủ nhận, bởi chúng cung cấp

nền tảng để mô hình “học” từ ngữ nghĩa, ngữ pháp, và ngữ cảnh của ngôn ngữ một

cách toàn diện. Đặc biệt, loại dữ liệu này có kích thước lớn và bao gồm các phong

cách ngôn ngữ khác nhau, từ ngôn ngữ trang trọng đến ngôn ngữ hàng ngày trên nhiều

loại ngôn ngữ, điều này giúp mô hình trở nên linh hoạt khi xử lý các dạng câu hỏi và

tình huống khác nhau.

Từ góc độ ứng dụng, NLP phát triển các phương pháp và công cụ cho việc phân

tích, hiểu, và tạo ngôn ngữ tự nhiên một cách có hệ thống. Lĩnh vực này đã mở rộng

để bao quát nhiều nhiệm vụ phức tạp, trong đó các nhiệm vụ phổ biến bao gồm phân
loại văn bản, gắn nhãn chuỗi, trả lời câu hỏi, và sinh văn bản [2]. Điều đáng chú ý là

NLP không chỉ đơn thuần là một lĩnh vực kỹ thuật, mà còn kết hợp các kiến thức từ
cả ngôn ngữ học và khoa học máy tính để xử lý các văn bản và lời nói của con người
một cách hiệu quả và chính xác.

Để hiểu rõ hơn về bản chất của các bài toán NLP, ta có thể xem xét định nghĩa

toán học tổng quát. Trong phạm vi này, đầu vào của một bài toán NLP thường là tập
hợp  văn  bản 𝑋 = {𝑥1, 𝑥2, … , 𝑥𝑛},  trong  đó  mỗi 𝑥𝑖  là  một  đoạn  văn  bản  hoặc  câu.
Tương ứng với đó, đầu ra 𝑌 sẽ phụ thuộc vào yêu cầu của bài toán cụ thể. Chẳng hạn,
đầu ra có thể là nhãn phân loại 𝑦𝑖 ∈ 𝐶 với 𝐶 là một tập hợp các nhãn đã được định

6

nghĩa từ trước nếu đây là bài toán phân loại văn bản hoặc phân tích cảm xúc. Trong
trường hợp khác, đầu ra có thể là chuỗi văn bản 𝑦 = [𝑦1, 𝑦2, … , 𝑦𝑚] nếu đây là bài
toán sinh văn bản, dịch máy, hoặc tóm tắt văn bản. Cuối cùng, đầu ra cũng có thể là
tập hợp các thực thể 𝐸 = {𝑒1, 𝑒2, … , 𝑒𝑘} trong trường hợp bài toán nhận diện thực thể
được đặt tên.

Sự đa dạng trong các dạng đầu ra này phản ánh tính phong phú và phức tạp của

lĩnh vực NLP, đồng thời cũng cho thấy tiềm năng ứng dụng rộng lớn của nó trong

nhiều lĩnh vực khác nhau của đời sống và công nghệ.

Các kỹ thuật trong xử lý ngôn ngữ tự nhiên

1.2.
NLP là một lĩnh vực đòi hỏi sự kết hợp tinh tế của nhiều kỹ thuật khác nhau để

có thể chuyển đổi ngôn ngữ tự nhiên phức tạp và đa dạng của con người thành dạng

thông tin mà máy tính có thể hiểu và xử lý một cách hiệu quả. Về bản chất, những kỹ

thuật này đóng vai trò như những cầu nối quan trọng, giúp thu hẹp khoảng cách giữa

cách con người giao tiếp tự nhiên và khả năng tính toán của máy móc [3].

Để đạt được mục tiêu này, các kỹ thuật trong NLP được phát triển theo một hệ

thống phân tầng, từ những bước xử lý cơ bản nhất cho đến những phương pháp tiên
tiến nhất hiện nay. Mỗi tầng kỹ thuật đều có những vai trò và chức năng riêng biệt,

nhưng đồng thời cũng bổ trợ lẫn nhau để tạo nên một quy trình xử lý hoàn chỉnh và

toàn diện. Điều đáng chú ý là sự phát triển của các kỹ thuật NLP không chỉ phản ánh

tiến bộ về mặt công nghệ mà còn thể hiện sự hiểu biết ngày càng sâu sắc về bản chất

của ngôn ngữ tự nhiên [3].

Trong bối cảnh này, việc tìm hiểu các kỹ thuật cốt lõi trở nên vô cùng quan trọng

để nắm bắt được toàn bộ quá trình NLP. Những kỹ thuật này có thể được phân loại

thành các nhóm chính, bắt đầu từ giai đoạn tiền xử lý dữ liệu thô, tiếp theo là các

phương pháp biểu diễn văn bản, rồi đến những thuật toán học máy và học sâu, cùng
với các mô hình ngôn ngữ lớn hiện đại, và cuối cùng là những kỹ thuật chuyên biệt

được thiết kế cho từng tác vụ cụ thể.

1.2.1.  Kỹ thuật tiền xử lý
Phân tách từ
Phân tách từ (Tokenization) là bước đầu tiên và cũng là nền tảng quan trọng nhất
trong quy trình tiền xử lý văn bản, bởi lẽ nó quyết định cách phân tách văn bản thành
các đơn vị có ý nghĩa để máy tính xử lý. Về mặt bản chất, phân tách từ là quá trình

7

chuyển đổi một chuỗi ký tự thô thành một tập hợp các token có thứ tự, trong đó mỗi

token đại diện cho một đơn vị ngữ nghĩa cơ bản.

Xét về mặt toán học, quá trình tách từ có thể được mô tả như một ánh xạ từ không

gian chuỗi ký tự sang không gian các dãy token. Cụ thể, cho một văn bản đầu vào
𝑆 = [𝑠1, 𝑠2, … , 𝑠𝑛] với 𝑠𝑖 là các ký tự, quá trình phân tách từ sẽ tạo ra một dãy token
𝑇 = [𝑡1, 𝑡2, … , 𝑡𝑚] thông qua hàm ánh xạ 𝑓: Σ∗ →   𝒯 ∗ trong đó Σ là bảng chữ cái ký
tự và 𝒯 là từ vựng token.

Trong thực tế, việc xác định ranh giới giữa các token không phải lúc nào cũng

đơn giản như việc phân tách theo khoảng trắng. Điều này đặc biệt rõ rệt khi xem xét

những thách thức mà kỹ thuật phân tách từ phải đối mặt. Chẳng hạn, với câu “Don't
split  this  sentence!”,  quá  trình  phân  tách  từ  đơn  giản  theo  khoảng  trắng  sẽ  tạo  ra

[“Don't”, “split”, “this”, “sentence!”], nhưng một phương pháp tinh tế hơn có thể tách

thành [“Do”, “n't”, “split”, “this”, “sentence”, “!”] để bảo toàn tính ngữ pháp của từng

thành phần.

Hơn nữa, sự phức tạp của kỹ thuật phân tách từ còn tăng lên đáng kể khi xử lý

các ngôn ngữ không có dấu phân cách rõ ràng như tiếng Trung, tiếng Nhật, hoặc thậm

chí tiếng Việt với các từ ghép. Trong những trường hợp này, thuật toán phân tách từ

cần phải dựa vào các quy tắc ngữ pháp phức tạp hoặc các mô hình thống kê để xác

định ranh giới từ một cách chính xác.

Tầm quan trọng của tách từ không chỉ dừng lại ở việc phân tách văn bản mà còn
ảnh hưởng trực tiếp đến hiệu suất của toàn bộ hệ thống NLP. Một chiến lược phân

tách từ không phù hợp có thể dẫn đến việc mất mát thông tin quan trọng hoặc tạo ra

những biểu diễn không nhất quán, từ đó làm giảm độ chính xác của các mô hình học

máy trong những bước xử lý tiếp theo. Do đó, việc lựa chọn phương pháp phân tách

từ phù hợp với đặc thù của từng tác vụ và ngôn ngữ cụ thể trở thành một quyết định

chiến lược quan trọng trong thiết kế hệ thống NLP.

Chuẩn hóa
Sau khi quá trình phân tách từ hoàn tất, chuẩn hóa (normalization) xuất hiện như
một bước tiếp theo không thể thiếu trong chuỗi tiền xử lý, đóng vai trò chuẩn hóa và
thống nhất các token đã được tạo ra để đảm bảo tính nhất quán trong việc biểu diễn
thông tin. Về bản chất, chuẩn hóa là quá trình biến đổi các token thô thành dạng chuẩn
hóa thông qua một tập hợp các quy tắc và phép biến đổi được định nghĩa trước, nhằm

giảm thiểu sự biến thiên không cần thiết trong dữ liệu văn bản.

Từ góc độ toán học, quá trình chuẩn hóa có thể được mô tả như một hàm ánh xạ

8

𝑔: 𝒯 → 𝒯 ′, trong đó 𝒯 là tập hợp các token gốc và 𝒯′ là tập hợp các token đã được
chuẩn hóa. Đặc biệt, hàm này thường không phải là đơn ánh (injective), có nghĩa là
nhiều token khác nhau có thể được ánh xạ về cùng một token chuẩn, tức là:

∃ 𝑡1, 𝑡2   ∈  𝒯: 𝑡1 ≠ 𝑡2 nhưng 𝑔(𝑡1) = 𝑔(𝑡2).
Một trong những kỹ thuật chuẩn hóa phổ biến nhất là chuyển đổi chữ hoa thành

chữ thường. Chẳng hạn, các token “Apple”, “APPLE”, và “apple” đều được chuẩn

hóa thành “apple”, điều này giúp giảm kích thước từ vựng và tránh tình trạng các từ

giống nhau về mặt ngữ nghĩa lại được coi là khác biệt. Tuy nhiên, việc áp dụng kỹ

thuật này cần được cân nhắc cẩn thận, bởi trong một số trường hợp, chữ hoa mang ý
nghĩa đặc biệt như trong tên riêng (thành phố “Paris” khác với “paris” trong tiếng

Pháp có nghĩa là “cá cược”).

Bên cạnh đó, việc loại bỏ các dấu câu cũng là một thành phần quan trọng của quá

trình chuẩn hóa. Tuy nhiên, điều này đòi hỏi sự tinh tế trong việc quyết định loại bỏ

dấu câu nào, bởi một số dấu câu mang thông tin ngữ nghĩa quan trọng. Ví dụ, trong

câu hỏi “What time is it?”, dấu hỏi chấm “?” không chỉ là một ký tự mà còn chỉ ra

tính chất của câu, do đó việc loại bỏ nó có thể làm mất thông tin quan trọng về ngữ

cảnh.

Chuẩn hóa còn bao gồm cả việc xử lý các ký tự đặc biệt và ký tự Unicode. Trong

môi trường đa ngôn ngữ, cùng một ký tự có thể được biểu diễn bằng nhiều mã hóa

unicode khác nhau. Chẳng hạn, ký tự “é” có thể được biểu diễn như một ký tự đơn

(U+00E9) hoặc như tổ hợp của ký tự “e” (U+0065) và dấu sắc (U+0301). Quá trình

chuẩn hóa Unicode, đặc biệt là các dạng Normalization Form Decomposed (NFD) và

Normalization Form Composed (NFC), giúp thống nhất cách biểu diễn này.

Chuẩn hóa không chỉ giảm thiểu kích thước từ vựng mà còn cải thiện hiệu suất

của các mô hình học máy bằng cách tạo ra những biểu diễn nhất quán hơn. Khi các

từ có cùng ý nghĩa được chuẩn hóa về cùng một dạng, mô hình có thể học được các
mẫu tổng quát hóa tốt hơn, từ đó nâng cao độ chính xác trong các tác vụ NLP tiếp

theo. Điều này đặc biệt quan trọng trong bối cảnh dữ liệu văn bản thường chứa nhiều
biến thể và sự không nhất quán về mặt hình thức.

Loại bỏ stop words
Tiếp nối quá trình chuẩn hóa, việc loại bỏ stop words đóng vai trò là bước tinh
chỉnh cuối cùng trong giai đoạn tiền xử lý, nhằm loại trừ những từ có tần suất xuất
hiện cao nhưng ít mang thông tin ngữ nghĩa quan trọng cho tác vụ xử lý cụ thể. Về
mặt lý thuyết thông tin, stop words có thể được hiểu là những từ có entropy thông tin

9

thấp, nghĩa là chúng không cung cấp nhiều thông tin phân biệt để phân loại hoặc phân

tích văn bản.

Quá  trình  loại  bỏ  stop  words  có  thể  được  mô  tả  như  một  phép  lọc  (filtering

operation) trên tập hợp token đã được chuẩn hóa. Cụ thể, cho tập hợp stop words 𝑆 =
{𝑠1, 𝑠2, … , 𝑠𝑛} và chuỗi token đầu vào 𝑇 = [𝑡1, 𝑡2, … , 𝑡𝑛], quá trình lọc sẽ tạo ra chuỗi
token mới 𝑇′ = [𝑡1

′ ] với 𝑚 ≤ 𝑛, trong đó 𝑇′ =   {𝑡𝑖 ∈ 𝑇: 𝑡𝑖 ∉ 𝑆}.

′ , … , 𝑡𝑚

′ , 𝑡2

Trong tiếng Việt, stop words thường bao gồm các từ như “là”, “của”, “và”, “có”,

“được”, “đã”, “sẽ”, “tôi”, “bạn”, “chúng ta”. Ví dụ, với câu “Tôi đã đọc cuốn sách

này và nó rất hay”, sau khi loại bỏ stop words, ta sẽ thu được “đọc cuốn sách rất hay”.

Điều này cho thấy rõ ràng việc loại bỏ stop words giúp làm nổi bật những từ khóa
mang ý nghĩa chính của câu văn.

Tuy nhiên, việc xác định stop words không phải lúc nào cũng đơn giản và cần

được xem xét trong bối cảnh cụ thể của từng ứng dụng. Trong tiếng Việt, sự phức tạp

của còn tăng lên do đặc thù ngôn ngữ học. Chẳng hạn, từ “không” có thể vừa là stop

word trong ngữ cảnh nhấn mạnh “không phải vậy” nhưng lại mang ý nghĩa quan trọng

trong phân tích tình cảm: “không tốt” vs “tốt”. Tương tự, các từ chỉ định lượng như

“nhiều”, “ít”, “rất” có thể được coi là stop words trong một số tác vụ nhưng lại cực

kỳ quan trọng trong phân tích cường độ cảm xúc.

Một cách tiếp cận tiên tiến hơn là sử dụng các phương pháp thống kê như TF-

IDF để xác định stop words một cách động thay vì dựa vào danh sách cố định. Trong
phương pháp này, những từ có điểm số thống kê thấp được coi là stop words.

Việc áp dụng kỹ thuật loại bỏ stop words cần được cân nhắc cẩn thận tùy theo tác

vụ cụ thể. Trong các tác vụ như phân loại chủ đề hoặc tìm kiếm thông tin, việc loại

bỏ stop words thường mang lại hiệu quả tích cực bằng cách giảm nhiễu và tập trung

vào những từ khóa quan trọng. Ngược lại, trong các tác vụ như phân tích ngữ pháp

hay dịch máy, stop words lại đóng vai trò quan trọng trong việc duy trì cấu trúc và ý

nghĩa của câu văn.

1.2.2.  Kỹ thuật biểu diễn văn bản
Túi từ
Sau khi hoàn tất quá trình tiền xử lý, việc chuyển đổi văn bản từ dạng ký tự sang
dạng số học để máy tính có thể xử lý trở thành thách thức trung tâm của bước biểu

diễn văn bản. Trong bối cảnh này, túi từ (Bag-of-Words - BoW) xuất hiện như một

trong những phương pháp cơ bản và quan trọng nhất, đóng vai trò tiên phong trong

10

lĩnh vực biểu diễn văn bản số. Về bản chất, túi từ là một mô hình đơn giản hóa ngôn

ngữ tự nhiên bằng cách coi mỗi văn bản như một “túi chứa từ”, trong đó thứ tự xuất

hiện của các từ được bỏ qua và chỉ tập trung vào tần suất xuất hiện của chúng.

Mô  hình  Bag-of-Words  biểu  diễn  một  văn  bản 𝑑  dưới  dạng  vector 𝑣𝑑  trong
không gian 𝑣𝑑 ∈ ℝ|𝑉|, trong đó 𝑉 là từ vựng của toàn bộ tập dữ liệu văn bản. Cụ thể
hơn,  với  từ  vựng 𝑉 = {𝑤1, 𝑤2, … , 𝑤|𝑉|},  vector  biểu  diễn  của  văn  bản 𝑑 được định
nghĩa như 𝑣𝑑 = [𝑐1, 𝑐2, … , 𝑐|𝑉|], trong đó 𝑐𝑖 đại diện cho số lần xuất hiện của từ 𝑤𝑖
trong văn bản 𝑑. Ta có thể viết 𝑐𝑖 = 𝑐𝑜𝑢𝑛𝑡(𝑤𝑖, 𝑑)

Để minh họa cụ thể, xét hai câu:

•  Câu 1: “Tôi thích đọc sách”.

•  Câu 2: “Sách hỗ trợ tôi học tập”.

Từ  vựng  của  tập  ngữ  liệu  này  là 𝑉 = {𝑡ô𝑖, 𝑡ℎí𝑐ℎ , đọ𝑐, 𝑠á𝑐ℎ, ℎỗ, 𝑡𝑟ợ, ℎọ𝑐,

𝑡ậ𝑝} với |𝑉| = 8. Khi đó, biểu diễn BoW của hai câu sẽ là:

•  𝑣(𝐶â𝑢 1) = [1, 1, 1, 1, 0, 0, 0, 0].

•  𝑣(𝐶â𝑢 2) = [1, 0, 0, 1, 1, 1, 1, 1].
Điều đáng chú ý là mặc dù hai câu này có cùng từ “tôi” và “sách”, nhưng thông

qua biểu diễn vector, ta có thể dễ dàng nhận ra sự khác biệt trong nội dung thông qua

các thành phần khác nhau của vector.

Một trong những ưu điểm nổi bật của túi từ là tính đơn giản và hiệu quả tính toán.
Việc tạo ra biểu diễn túi từ có độ phức tạp thời gian 𝑂(𝑛)với 𝑛 là tổng số từ trong văn
bản, điều này làm cho nó trở thành lựa chọn phù hợp cho các ứng dụng yêu cầu xử lý

khối lượng lớn dữ liệu văn bản. Hơn nữa, biểu diễn vector này có thể được sử dụng

trực tiếp với nhiều thuật toán học máy truyền thống như Support Vector Machine,

Naive Bayes, hay các phương pháp phân cụm.

Tuy nhiên, túi từ cũng tồn tại những hạn chế đáng kể. Trước hết, việc bỏ qua thứ

tự từ dẫn đến mất mát thông tin ngữ pháp và ngữ cảnh quan trọng. Chẳng hạn, hai
câu “Tôi không thích sách này” và “Tôi thích sách này không” sẽ có cùng biểu diễn
mặc dù ý nghĩa hoàn toàn khác nhau. Điều này đặc biệt phức tạp trong tiếng Việt vì
thứ tự từ đóng vai trò quan trọng trong việc xác định ý nghĩa câu.

Thêm vào đó, túi từ gặp khó khăn với vấn đề thưa thớt. Trong thực tế, kích thước

từ vựng |𝑉| có thể rất lớn (hàng chục nghìn từ), trong khi mỗi văn bản chỉ chứa một

phần nhỏ các từ này, dẫn đến việc vector biểu diễn có nhiều thành phần bằng 0. Mật
độ của vector BoW thường rất thấp, được tính như sau:

11

𝑠ố 𝑡ℎà𝑛ℎ 𝑝ℎầ𝑛 𝑘ℎá𝑐 0
|𝑉|
Để khắc phục một phần những hạn chế này, các biến thể của BoW đã được phát

(1.1)

𝜌 =

triển. N-gram BoW mở rộng mô hình cơ bản bằng cách xem xét không chỉ từ đơn lẻ

mà cả chuỗi 𝑛 từ liên tiếp. Ví dụ, với bigram 𝑛 = 2, câu “Tôi thích đọc sách” sẽ tạo

ra các bigram: “Tôi thích”, “thích đọc”, “đọc sách”. Điều này giúp giữ lại phần nào

thông tin về thứ tự từ, dù phải đánh đổi bằng việc làm tăng đáng kể kích thước không

gian đặc trưng.

Mặc dù có những hạn chế, túi từ vẫn giữ vai trò quan trọng trong nhiều ứng dụng

NLP, đặc biệt là trong các tác vụ phân loại văn bản, phân tích tình cảm cơ bản, và
trích xuất thông tin. Sự đơn giản và khả năng diễn giải của nó làm cho túi trở thành

cột mốc quan trọng để so sánh hiệu suất của các mô hình phức tạp hơn, đồng thời

cũng là bước đệm cần thiết để hiểu các phương pháp biểu diễn văn bản tiên tiến hơn.

TF-IDF

Mặc dù túi từ đã cung cấp một nền tảng vững chắc cho việc biểu diễn văn bản,

nhưng việc chỉ dựa vào tần suất xuất hiện đơn thuần của các từ vẫn còn những hạn

chế đáng kể. TF-IDF (Term Frequency - Inverse Document Frequency) ra đời như
một cải tiến quan trọng, không chỉ xem xét tần suất của từ trong một văn bản cụ thể

mà còn tính đến tầm quan trọng tương đối của từ đó trong toàn bộ tập ngữ liệu. Về

bản chất, TF-IDF dựa trên giả định rằng những từ xuất hiện thường xuyên trong một

văn bản nhưng hiếm khi xuất hiện trong các văn bản khác sẽ mang nhiều thông tin

đặc trưng hơn.

TF-IDF của một từ 𝑡 trong văn bản 𝑑 thuộc tập ngữ liệu 𝐷 được định nghĩa như

tích của hai thành phần: TF và IDF. Công thức tổng quát có thể được biểu diễn như

sau:

𝑇𝐹 − 𝐼𝐷𝐹(𝑡, 𝑑, 𝐷) = 𝑇𝐹(𝑡, 𝑑) ×  𝐼𝐷𝐹(𝑡, 𝐷)

(1.2)

Trong đó, TF và IDF thường được tính theo công thức chuẩn hóa:

𝑇𝐹(𝑡, 𝑑) =

𝐼𝐷𝐹(𝑡, 𝐷) = log

𝑓𝑡,𝑑

∑

𝑡′∈𝑑

𝑓𝑡′,𝑑
|𝐷|
|{𝑑 ∈ 𝐷: 𝑡 ∈ 𝑑|

(1.3)

(1.4)

trong đó |𝐷| là tổng số văn bản trong tập ngữ liệu và |{𝑑 ∈ 𝐷: 𝑡 ∈ 𝑑}| là số văn

bản chứa từ 𝑡.

Để làm rõ cơ chế hoạt động của TF-IDF, xem xét một tập ngữ liệu gồm ba văn

12

bản:

•  Văn bản 1: “Tôi thích đọc sách văn học”.

•  Văn bản 2: “Sách giáo khoa rất hữu ích”.

•  Văn bản 3: “Thư viện có nhiều sách hay”.
Xét từ “sách” xuất hiện trong cả ba văn bản với tần suất bằng nhau là một lần

trong mỗi văn bản. Khi đó:

•  𝑇𝐹(𝑠á𝑐ℎ, 𝑑1) =

1

5

= 0.2

•  𝐼𝐷𝐹(𝑠á𝑐ℎ, 𝐷) = log

3

3

= 0

•  𝑇𝐹 − 𝐼𝐷𝐹(𝑠á𝑐ℎ,  𝑑1, 𝐷) = 0.2 × 0 = 0
Ngược lại, từ “văn học” chỉ xuất hiện trong văn bản 1:

•  𝑇𝐹(𝑣ă𝑛 ℎọ𝑐, 𝑑1) =

1

5

= 0.2

•  𝐼𝐷𝐹(𝑣ă𝑛 ℎọ𝑐, 𝐷) = log

= log 3 ≈ 1.099

3

1
•  𝑇𝐹 − 𝐼𝐷𝐹(𝑣ă𝑛 ℎọ𝑐, 𝑑1, 𝐷) = 0.2 × 1.099 ≈ 0.22
Kết quả này minh họa rõ ràng nguyên lý cốt lõi của TF-IDF: những từ xuất hiện

phổ biến trong nhiều văn bản như từ “sách” sẽ có trọng số thấp, trong khi những từ

đặc trưng cho một văn bản cụ thể như từ “văn học” sẽ được gán trọng số cao hơn.

Ưu điểm vượt trội của TF-IDF so với BoW đơn thuần nằm ở khả năng phân biệt

tầm quan trọng của các từ. Trong khi BoW coi tất cả các từ có cùng tần suất là như

nhau, TF-IDF có thể nhận biết và làm nổi bật những từ khóa quan trọng, đặc biệt hữu

ích trong các tác vụ như trích xuất thông tin và phân loại tài liệu. Điều này đặc biệt

có ý nghĩa trong tiếng Việt, nơi mà nhiều từ chức năng như “là”, “của”, “và” xuất
hiện với tần suất cao nhưng ít mang thông tin phân biệt.

Tuy nhiên, TF-IDF cũng không tránh khỏi một số hạn chế của riêng mình. Trước

hết, phương pháp này vẫn kế thừa vấn đề cơ bản của BoW là bỏ qua thông tin về thứ

tự từ và ngữ cảnh. Hơn nữa, IDF có xu hướng gán trọng số cao cho những từ hiếm,
điều này có thể dẫn đến việc những từ có lỗi chính tả hoặc từ chuyên ngành được
đánh giá quá cao. Trong tiếng Việt, việc xử lý các từ láy, từ ghép, và biến thể vùng
miền cũng tạo ra những thách thức riêng cho việc tính toán IDF chính xác.

Mặt khác, TF-IDF còn gặp khó khăn trong việc xử lý các từ đồng nghĩa và các
mối quan hệ ngữ nghĩa phức tạp. Chẳng hạn, “ô tô” và “xe hơi” sẽ được coi là hai từ
hoàn toàn khác biệt mặc dù chúng có ý nghĩa tương đương. Điều này hạn chế khả

năng của TF-IDF trong việc nắm bắt được sự tương đồng ngữ nghĩa giữa các văn bản.
Mặc dù có những hạn chế, TF-IDF vẫn được coi là một cột mốc quan trọng trong

13

lịch sử phát triển của các phương pháp biểu diễn văn bản. Sự kết hợp tinh tế giữa TF

và IDF đã tạo nền tảng cho nhiều phương pháp biểu diễn văn bản tiên tiến hơn, đồng

thời vẫn được sử dụng rộng rãi trong các hệ thống NLP hiện đại.

Word Embeddings: Word2Vec và GloVe
Bên  cạnh  các  phương  pháp  biểu  diễn  truyền  thống  như  BoW  và  TF-IDF,  các
phương pháp Words Embeddings đã mang lại một bước đột phá quan trọng bằng cách

chuyển từ biểu diễn thưa thớt (sparse representation) sang biểu diễn dày đặc (dense
representation). Khác với BoW và TF-IDF chỉ quan tâm đến tần suất xuất hiện, Word

Embeddings tập trung vào việc học các vector có chiều thấp nhưng chứa đựng thông

tin ngữ nghĩa phong phú, dựa trên giả thuyết phân bố rằng các từ có ngữ cảnh tương

tự sẽ có nghĩa tương tự.

Word2Vec  cung  cấp  hai  kiến  trúc  chính  là  Skip-gram  và  CBOW  (Continuous

Bag of Words). Skip-gram hoạt động theo nguyên tắc dự đoán các từ ngữ cảnh từ một

từ trung tâm, trong khi CBOW thực hiện ngược lại bằng cách dự đoán từ trung tâm

từ các từ ngữ cảnh xung quanh. Để minh họa, với câu: “Hôm nay trời đẹp nên tôi đi

chơi”, Skip-gram sẽ học cách dự đoán các từ “đẹp”, “tôi” từ từ trung tâm “nên”, trong

khi CBOW sẽ thực hiện quá trình ngược lại.

Bên cạnh đó, GloVe đưa ra cách tiếp cận khác biệt bằng cách kết hợp ưu điểm
của phương pháp thống kê toàn cục và thông tin ngữ cảnh cục bộ. GloVe được xây
dựng dựa trên ma trận đồng xuất hiện toàn cục và giả định rằng tỷ lệ đồng xuất hiện

giữa các từ có thể mã hóa hiệu quả thông tin ngữ nghĩa. Chẳng hạn, từ “xe” có thể

đồng xuất hiện với “ô tô”, “máy”, “đạp” với tần suất khác nhau, và GloVe sẽ học

được mối quan hệ này thông qua thống kê trên toàn bộ tập ngữ liệu.

Tuy nhiên, cả hai phương pháp đều có những hạn chế chung như không thể xử lý

các từ ngoài từ vựng và không tính đến sự đa nghĩa của từ trong các ngữ cảnh khác

nhau. Dù vậy, Word Embeddings đã trở thành nền tảng quan trọng cho nhiều ứng

dụng NLP hiện đại, từ phân loại văn bản đến dịch máy, đóng vai trò như lớp biểu
diễn đầu vào cho các mô hình học sâu phức tạp hơn.

1.2.3.  Học máy và học sâu
Sau khi văn bản được tiền xử lý và biểu diễn dưới dạng vector, các thuật toán học
máy (Machine Learning) và học sâu (Deep Learning) đóng vai trò then chốt trong
việc thực hiện các tác  vụ  NLP cụ thể. Sự phát triển  từ các phương pháp  học máy
truyền thống đến học sâu đã tạo nên cuộc cách mạng trong lĩnh vực NLP, mang lại

14

những cải tiến đáng kể về hiệu suất và khả năng xử lý ngôn ngữ phức tạp.

Các thuật toán học máy truyền thống như SVM, Naive Bayes và Cây quyết định

từng là nền tảng chính cho nhiều ứng dụng  NLP. SVM thể hiện hiệu quả đặc biệt

trong phân loại văn bản nhờ khả năng xử lý dữ liệu có số chiều lớn và tìm ra ranh
giới tối ưu giữa các lớp. Chẳng hạn, trong bài toán phân loại tin tức, SVM có thể phân
biệt chính xác giữa các chủ đề như thể thao, kinh tế, và giải trí dựa trên đặc trưng TF-

IDF. Tương tự, Naive Bayes thường được ứng dụng trong phân tích cảm xúc nhờ tính
đơn giản và hiệu quả với dữ liệu văn bản, đặc biệt phù hợp khi có ít dữ liệu huấn

luyện.

Tuy nhiên, học sâu đã mở ra những khả năng hoàn toàn mới cho NLP thông qua

khả năng học biểu diễn tự động và xử lý các mẫu phức tạp. RNN và các biến thể như
LSTM và GRU được thiết kế đặc biệt để xử lý dữ liệu chuỗi, phù hợp với bản chất

tuần tự của ngôn ngữ.

Bên cạnh đó, CNN cũng tìm thấy vị trí trong NLP, đặc biệt hiệu quả trong phân

loại văn bản và trích xuất đặc trưng cục bộ. CNN có thể nắm bắt các mẫu n-gram

quan trọng trong văn bản, tương tự như cách chúng nhận diện các đặc trưng trong

hình ảnh.

Cơ chế chú ý (attention) đã đánh dấu bước ngoặt quan trọng tiếp theo, cho phép

mô hình tập trung vào những phần thông tin quan trọng nhất trong chuỗi đầu vào.

Điều này đặc biệt hữu ích trong các tác vụ như dịch máy, nơi mô hình cần biết từ nào

trong câu nguồn tương ứng với từ đang được tạo ra. Ví dụ, khi dịch “Tôi yêu Việt

Nam” sang tiếng Anh, cơ chế  chú ý giúp mô hình hiểu rằng  “yêu”  tương ứng với

“love” và “Việt Nam” tương ứng với “Vietnam”.

Sự kết hợp giữa học máy truyền thống và học sâu trong NLP không chỉ mang lại

hiệu suất cao hơn mà còn mở ra khả năng xử lý các tác vụ ngôn ngữ phức tạp hơn.

Trong khi các phương pháp truyền thống vẫn có giá trị trong những bài toán đơn giản

và khi có hạn chế về dữ liệu hoặc tài nguyên tính toán, học sâu đã trở thành lựa chọn
chủ đạo cho hầu hết các ứng dụng NLP hiện đại nhờ khả năng học và xử lý ngôn ngữ
tự nhiên ở mức độ tinh vi hơn.

1.2.4.  Mô hình ngôn ngữ lớn
Sự phát triển của mô hình ngôn ngữ lớn (Large Language Models - LLMs) đã tạo
ra bước ngoặt lớn trong NLP, chuyển từ các mô hình chỉ giải quyết một tác vụ riêng
lẻ sang các hệ thống có khả năng đa nhiệm với hiệu suất cao. Các mô hình này được

15

xây dựng trên kiến trúc Transformer và được huấn luyện trên lượng dữ liệu văn bản

khổng lồ.

BERT là một trong những mô hình tiên phong, sử dụng cách đọc hai chiều để

hiểu ngữ cảnh từ cả trước và sau một từ cần xử lý. Khi gặp câu “Anh ấy đi [MASK]
siêu thị mua đồ”, BERT có thể dự đoán từ “đến” bằng cách xem xét toàn bộ ngữ cảnh
xung quanh, không chỉ dựa vào những từ phía trước. Điều này giúp BERT hiểu văn

bản chính xác hơn các mô hình trước đó.

Trong khi đó, dòng GPT (từ GPT-1 đến GPT-4) chứng minh rằng việc tăng quy

mô mô hình có thể mang lại những khả năng đáng kinh ngạc. GPT không chỉ tạo ra

văn bản tự nhiên mà còn có thể thực hiện nhiều tác vụ khác nhau như dịch thuật, tóm

tắt, và thậm chí lập trình mà không cần huấn luyện thêm cho từng tác vụ cụ thể.

T5 đưa ra cách tiếp cận đơn giản bằng cách xem mọi tác vụ NLP như một bài

toán chuyển đổi từ văn bản này sang văn bản khác. Ví dụ, để dịch từ tiếng Việt sang

tiếng Anh, T5 nhận đầu vào “translate Vietnamese to English: Tôi yêu học máy” và

tạo ra “I love machine learning”.

Điểm đặc biệt quan trọng của các LLMs là khả năng tạo ra biểu diễn theo ngữ

cảnh (contextual embeddings), nghĩa là cùng một từ sẽ có biểu diễn khác nhau tùy

theo ngữ cảnh. Từ “bank” trong “ngân hàng thương mại” mang ý nghĩa khác hoàn

toàn với “bank” trong “bờ sông”, giải quyết được vấn đề từ đa nghĩa mà các phương

pháp trước không thể xử lý.

Nhờ những đặc điểm này, các mô hình ngôn ngữ lớn đã trở thành nền tảng cho

nhiều ứng dụng NLP hiện đại, cho phép sử dụng một mô hình duy nhất cho nhiều tác

vụ khác nhau thay vì phải xây dựng mô hình riêng cho từng bài toán cụ thể.

1.2.5.  Kỹ thuật chuyên biệt cho các tác vụ cụ thể
Nhận dạng thực thể được đặt tên (Named Entity Recognition)

Nhận dạng thực thể được đặt tên – NER - là tác vụ phân loại chuỗi nhằm xác định
và phân loại các thực thể có tên trong văn bản thành các danh mục định trước như tên
người, địa điểm, tổ chức, và thời gian.

Bài toán nhận dạng thực thể được đặt tên được mô hình hóa như việc tìm chuỗi
nhãn  tối  ưu 𝑌∗ = 𝑎𝑟𝑔𝑚𝑎𝑥 𝑃(𝑌|𝑋) cho  chuỗi  token  đầu  vào 𝑋 = {𝑥1, 𝑥2, … , 𝑥𝑛},
trong đó mỗi nhãn 𝑦𝑖 thuộc sơ đồ BIO - sơ đồ này phân biệt token bắt đầu thực thể
(B), token nằm trong thực thể (I), và token không thuộc thực thể nào (O). Để minh
họa, xét câu: “Trường Đại học Quy Nhơn được thành lập năm 1997” sẽ được gán

16

nhãn như sau: Trường (B-ORG) Đại (I-ORG) học (I-ORG) Quy (I-ORG) Nhơn (I-

ORG) được (O) thành (O) lập (O) năm (O) 1997 (B-TIME). Sau khi gán nhãn, hệ

thống sẽ trích xuất các thực thể đã được nhận dạng - trong trường hợp này là “Trường

Đại học Quy Nhơn” (tổ chức) và “1997” (thời gian) - để phục vụ cho các tác vụ xử
lý tiếp theo như xây dựng đồ thị tri thức, tìm kiếm thông tin có cấu trúc, hoặc phân
tích mối quan hệ giữa các thực thể.

Trong tiếng Việt, nhận dạng thực thể được đặt tên gặp nhiều thách thức đặc thù
do đặc điểm đa nghĩa và ngữ cảnh phong phú của ngôn ngữ. Mặc dù vậy, kỹ thuật

này vẫn giữ vai trò then chốt trong nhiều ứng dụng ở bước xử lý tiếp theo, như trích

xuất thông tin, hệ thống hỏi đáp và phân tích cảm xúc.

Gán nhãn từ loại
Gán nhãn từ loại (POS Tagging) là tác vụ phân loại chuỗi nhằm xác định từ loại

ngữ pháp của mỗi từ trong câu như danh từ (N), động từ (V), tính từ (A), và các từ

loại khác. Đây là một trong những bước tiền xử lý cơ bản nhất, cung cấp thông tin

ngữ pháp quan trọng cho các tác vụ xử lý ngôn ngữ cao cấp hơn.

Gán nhãn từ loại có thể được biểu diễn như việc tìm một chuỗi nhãn từ loại tối
ưu 𝑃∗ = 𝑎𝑟𝑔𝑚𝑎𝑥 𝑃(𝑃|𝑊) cho chuỗi từ đầu vào 𝑊 = {𝑤1, 𝑤2, … , 𝑤𝑛}, trong đó mỗi
𝑝𝑖 thuộc tập nhãn từ loại định trước. Xét câu: “Sinh viên học chăm chỉ” sẽ được gán
nhãn như sau: Sinh (N) viên (N) học (V) chăm (A) chỉ (A). Sau khi gán nhãn, thông

tin từ loại này được sử dụng để phân tích cú pháp, xác định vai trò ngữ pháp của các

thành phần trong câu, và hỗ trợ cho các tác vụ như phân tích ngữ nghĩa và dịch máy.

Đối với tiếng Việt, gán nhãn từ loại gặp phải thách thức đặc biệt do hiện tượng

đa nghĩa từ loại phổ biến - một từ có thể thuộc nhiều từ loại khác nhau tùy theo ngữ

cảnh. Ví dụ, từ “học” có thể là động từ trong “học bài” hoặc danh từ trong “môn học”.

Tuy nhiên, gán nhãn từ loại vẫn là nền tảng thiết yếu cho hầu hết các ứng dụng NLP,

từ phân tích cú pháp, trích xuất thông tin đến dịch máy và tóm tắt văn bản.

Phân tích cú pháp phụ thuộc

Trong khi các kỹ thuật như nhận dạng thực thể được đặt tên và gán nhãn từ loại
tập trung vào việc gán nhãn cho từng token riêng lẻ thì phân tích cú pháp phụ thuộc
(dependency parsing) đi sâu hơn vào việc khám phá mối quan hệ cú pháp giữa các từ
trong câu. Bản chất của phương pháp này là xây dựng một cây có hướng trong đó
mỗi từ được kết nối với từ chi phối nó, tạo thành mạng lưới các mối quan hệ ngữ
pháp.

Khác với biểu diễn tuyến tính của gán nhãn từ loại, phân tích cú pháp phụ thuộc

17

tạo ra cấu trúc phân cấp phản ánh cách các từ tương tác với nhau. Ví dụ, trong câu

“Con mèo nhỏ ngủ trên ghế”, từ “ngủ” đóng vai trò trung tâm (root), chi phối “mèo”

(chủ  ngữ)  và  “trên”  (trạng  ngữ),  trong  khi  “Con”  và  “nhỏ”  lần  lượt  bổ  nghĩa  cho

“mèo”, còn “ghế” là đối tượng của giới từ “trên”. Cấu trúc này có thể biểu diễn về

mặt toán học như đồ thị 𝐺 = (𝑉, 𝐸) với 𝑉 là tập các từ và 𝐸 là tập các cung phụ thuộc.

Tính phức tạp của phân tích cú pháp phụ thuộc nằm ở việc một câu có thể có
nhiều cách phân tích hợp lệ, đặc biệt trong tiếng Việt với hiện tượng mơ hồ cú pháp

thường gặp. Chính vì vậy, các thuật toán parsing hiện đại như phân tích cú pháp dựa
trên chuyển trạng thái (transition-based parsing) và phân tích cú pháp dựa trên đồ thị
(graph-based parsing) đều nhằm tìm ra cây phụ thuộc có điểm số cao nhất thông qua

việc học từ dữ liệu có gán nhãn. Kết quả thu được không chỉ hữu ích cho việc hiểu

cấu trúc câu mà còn là đầu vào quan trọng cho các tác vụ phức tạp hơn như trích xuất

quan hệ và tóm tắt văn bản.

1.3.

Một số ứng dụng xử lý ngôn ngữ tự nhiên

NLP đã được ứng dụng rộng rãi trong nhiều lĩnh vực, thể hiện khả năng giải quyết

các bài toán thực tế phức tạp.

Tóm tắt văn bản là một ứng dụng quan trọng, chuyển đổi văn bản dài thành bản

tóm tắt ngắn gọn và đầy đủ ý nghĩa, giúp người đọc nhanh chóng nắm bắt nội dung

chính. Quá trình này sử dụng các thuật toán trích lọc và tóm tắt ngôn ngữ một cách

có hệ thống.

Bên cạnh đó, các ứng dụng tìm kiếm và phân loại tài liệu đóng vai trò quan trọng

trong tổ chức thông tin. Hệ thống này phân loại tài liệu theo tiêu chí cụ thể, phục vụ

nghiên cứu và quản lý, như phân loại các báo cáo quân sự hoặc tài liệu tiếp thị [3].

Ở mức cao hơn, các hệ thống phân loại và trích xuất thông tin có khả năng sắp

xếp tài liệu theo danh mục và trích xuất thông tin có cấu trúc từ dữ liệu văn bản [4].
Ví dụ điển hình là phân loại chủ đề báo (chính trị, thể thao, giải trí) hoặc phân tích
cảm xúc trong đánh giá phim (tích cực, tiêu cực, trung lập).

Trong tương tác người-máy, hệ thống phản hồi và gợi ý thông minh phân tích lựa
chọn người dùng để đưa ra gợi ý từ ngữ hoặc câu trả lời tự động phù hợp với sở thích
cá nhân.

Dịch máy (Machine Translation) đã chứng minh vai trò then chốt trong giao tiếp

đa ngôn ngữ. Các mô hình như Dịch máy dựa trên ngữ đoạn và Dịch máy bằng mạng

18

nơ-ron có khả năng dịch văn bản với độ chính xác cao [4], hỗ trợ giao tiếp quốc tế

trong kinh doanh và du lịch.

Cuối cùng, nhận diện giọng nói (Speech Recognition) mở rộng khả năng xử lý từ

văn bản sang âm thanh. Các thuật toán như Mô hình âm thanh và phân loại kết nối
theo thời gian thực hiện chuyển lời nói thành văn bản [4], tạo điều kiện phát triển các
hệ thống tự động hóa thông minh.

Các tiêu chí đánh giá

1.4.
Việc đánh giá hiệu quả của các mô hình trong xử lý ngôn ngữ tự nhiên đòi hỏi

những tiêu chí phù hợp với từng loại bài toán cụ thể.

Tiêu chí đánh giá cho bài toán phân loại văn bản
Độ chính xác (Accuracy):

Độ chính xác là tiêu chí cơ bản nhất để đánh giá hiệu suất của mô hình phân loại,

thể hiện tỷ lệ các dự đoán đúng trên tổng số mẫu trong tập kiểm tra. Độ đo này được

tính toán thông qua công thức:

𝐴𝑐𝑐𝑢𝑟𝑎𝑟𝑦 =

𝑇𝑃 + 𝑇𝑁
𝑇𝑃 + 𝑇𝑁 + 𝐹𝑃 + 𝐹𝑁

(1.1. )

Trong đó, TP (True Positive) là số mẫu được phân loại đúng thuộc lớp dương

tính, TN (True Negative) là số mẫu được phân loại đúng thuộc lớp âm tính, FP (False
Positive) là số mẫu bị phân loại sai thành lớp dương tính, và FN (False Negative) là

số mẫu bị phân loại sai thành lớp âm tính.

Điểm F1 (F1-Score):

Bên cạnh độ chính xác, điểm F1 cung cấp góc nhìn cân bằng hơn về hiệu suất mô

hình bằng cách kết hợp hai yếu tố quan trọng là precision và recall. Điểm F1 được

định nghĩa như sau:

Với:

𝐹1 − 𝑆𝑐𝑜𝑟𝑒 = 2 ×

𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛×𝑅𝑒𝑐𝑎𝑙𝑙

𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛+𝑅𝑒𝑐𝑎𝑙𝑙

𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛 =

𝑇𝑃
𝑇𝑃 + 𝐹𝑃

𝑅𝑒𝑐𝑎𝑙𝑙 =

𝑇𝑃
𝑇𝑃 + 𝐹𝑁

(1.2)

(1.3)

Điểm F1 đặc biệt hữu ích khi tập dữ liệu có sự mất cân bằng giữa các lớp, giúp
đánh giá toàn diện khả năng của mô hình trong việc nhận diện chính xác cả các mẫu
dương tính và tránh các dự đoán sai lầm.

Tiêu chí đánh giá cho bài toán sinh văn bản
Đối với bài toán sinh văn bản, việc đánh giá trở nên phức tạp hơn do bản chất

19

chủ quan của ngôn ngữ tự nhiên. Để giải quyết thách thức này, tiêu chí phổ biến để

đánh giá cho bài toán này là ROUGE, được thiết kế đặc biệt cho các tác vụ sinh văn

bản.

ROUGE-1:
ROUGE-1 đo lường sự trùng khớp của các từ đơn giữa văn bản được sinh ra và

văn bản tham chiếu. Điểm số này được tính theo công thức đơn giản:

𝑅𝑂𝑈𝐺𝐸 − 1 =

𝑆ố 𝑡ừ 𝑡𝑟ù𝑛𝑔 𝑘ℎớ𝑝
𝑇ổ𝑛𝑔 𝑠ố 𝑡ừ 𝑡𝑟𝑜𝑛𝑔 𝑣ă𝑛 𝑏ả𝑛 𝑡ℎ𝑎𝑚 𝑐ℎ𝑖ế𝑢

(1.4)

Ví dụ, nếu văn bản tham chiếu có 10 từ và có 6 từ trùng với văn bản được sinh

ra, thì ROUGE-1 = 6/10 = 0.6.

ROUGE-2:

Để đánh giá mức độ liên kết ngữ nghĩa tốt hơn, ROUGE-2 xem xét sự trùng khớp

của các cặp từ liên tiếp (bigram). Công thức tính toán tương tự nhưng áp dụng cho

cặp từ:

𝑅𝑂𝑈𝐺𝐸 − 2 =

𝑆ố 𝑐ặ𝑝 𝑡ừ 𝑙𝑖ê𝑛 𝑡𝑖ế𝑝 𝑡𝑟ù𝑛𝑔 𝑘ℎớ𝑝
𝑇ổ𝑛𝑔 𝑠ố 𝑐ặ𝑝 𝑡ừ 𝑡𝑟𝑜𝑛𝑔 𝑣ă𝑛 𝑏ả𝑛 𝑡ℎ𝑎𝑚 𝑐ℎ𝑖ế𝑢

(1.5)

ROUGE-2 cung cấp thông tin về khả năng duy trì cấu trúc ngữ pháp và sự mạch

lạc của văn bản được sinh ra so với văn bản gốc.

ROUGE-L:

Cuối cùng, ROUGE-L sử dụng khái niệm dãy con chung dài nhất để đánh giá sự

tương đồng về cấu trúc câu. Điểm ROUGE-L được tính dựa trên độ dài của chuỗi từ

dài nhất xuất hiện theo thứ tự trong cả hai văn bản:

𝑅𝑂𝑈𝐺𝐸 − 𝐿 =

2 × 𝐿𝐶𝑆
𝐿𝑠𝑖𝑛ℎ + 𝐿𝑡ℎ𝑎𝑚 𝑐ℎ𝑖ế𝑢

(1.6)

Trong đó, 𝐿𝐶𝑆 là độ dài của dãy con chung dài nhất, 𝐿𝑠𝑖𝑛ℎ là độ dài văn bản được
sinh ra, 𝐿𝑡ℎ𝑎𝑚 𝑐ℎ𝑖ế𝑢 là độ dài văn bản tham chiếu. Công thức này tương tự như điểm
F1 nhưng áp dụng cho chuỗi con chung dài nhất.

Những tiêu chí đánh giá này cung cấp cái nhìn đa chiều về hiệu suất của các mô
hình học liên kết, từ khả năng phân loại chính xác đến chất lượng văn bản được sinh
ra, tạo nền tảng vững chắc cho việc so sánh và cải thiện các phương pháp được đề
xuất trong nghiên cứu.

1.5.

Sơ lược về học liên kết

1.5.1.  Khái niệm và mô hình toán học

20

FL đại diện cho một mô hình học máy phi tập trung, trong đó việc huấn luyện mô

hình được thực hiện trên nhiều thiết bị khác nhau mà không cần chia sẻ dữ liệu thô

giữa các bên tham gia. Khái niệm này được đưa ra lần đầu tiên bởi Google vào năm

2016 như một giải pháp cho bài toán bảo vệ quyền riêng tư dữ liệu trong khi vẫn có
thể khai thác sức mạnh tính toán phân tán [1]. Cách tiếp cận này đặc biệt quan trọng
trong các lĩnh vực yêu cầu tính bảo mật cao như y tế, tài chính và NLP, nơi dữ liệu

thường chứa thông tin nhạy cảm của người dùng [5].

Kiến  trúc  cơ bản  của  hệ  thống  FL  được  xây  dựng  theo  mô  hình  client-server,

trong đó máy chủ trung tâm đóng vai trò là bộ điều phối chính để quản lý quá trình

huấn luyện toàn cục [6]. Các thiết bị cục bộ, được gọi là clients, thực hiện việc huấn

luyện mô hình trên dữ liệu riêng của mình và chỉ chia sẻ các tham số mô hình đã được
cập nhật với máy chủ trung tâm. Ví dụ điển hình của kiến trúc này có thể thấy trong

ứng dụng Gboard của Google, nơi hàng triệu thiết bị di động cùng nhau huấn luyện

mô hình dự đoán văn bản mà không cần gửi dữ liệu gõ phím cá nhân lên máy chủ.

Để mô tả chính xác bài toán tối ưu hóa trong FL, chúng ta cần xem xét mô hình

toán học tổng quát. Giả sử có 𝑁 thiết bị tham gia quá trình huấn luyện, mục tiêu chính
của FL là tìm ra bộ tham số tối ưu 𝑤∗ cho mô hình toàn cục bằng cách giải bài toán
tối ưu sau:

𝑁
{ℒ(𝑤) =   ∑ 𝒫𝑘ℒ𝑘(𝑤)

min
w

}

(1.7)

𝑘=1
trong đó ℒ𝑘 là hàm mất mát cục bộ, 𝒫𝑘 là trọng số của thiết bị thứ 𝑘 (thường được
xác định bởi tỷ lệ dữ liệu mà thiết bị 𝑘 đóng góp so với tổng dữ liệu), và ℒ𝑘(𝑤) là
hàm mất mát cục bộ của thiết bị 𝑘.

Đi sâu vào chi tiết, hàm mục tiêu cục bộ ℒ𝑘(𝑤) cho thiết bị thứ 𝑘 được định nghĩa

như sau:

ℒ𝑘(𝑤) =

1
𝑛𝑘

 ∑ 𝚤(𝑤; 𝑥𝑘,𝑗)

𝑛𝑘

𝑗=1

(1.8)

Trong công thức này, 𝑤 biểu thị các tham số của mô hình đang được huấn luyện,
𝑛𝑘 là số lượng mẫu dữ liệu có sẵn trên thiết bị 𝑘, và 𝚤(𝑤; 𝑥𝑘,𝑗) là hàm mất mát được
tính tại tham số mô hình 𝑤 và mẫu dữ liệu 𝑥𝑘,𝑗 từ thiết bị 𝑘.

Quá trình huấn luyện trong FL diễn ra theo các vòng lặp (rounds) có cấu trúc. Tại
mỗi vòng lặp 𝑡, máy chủ trung tâm sẽ gửi mô hình toàn cục hiện tại 𝑤𝑡 đến các thiết
bị được lựa chọn tham gia. Mỗi thiết bị 𝑘 sau đó thực hiện 𝐸 epochs huấn luyện cục
bộ trên dữ liệu của mình để thu được mô hình cập nhật 𝑤𝑘𝑡+1. Tiếp theo, các thiết bị

21

gửi lại các tham số đã cập nhật cho máy chủ, và máy chủ sẽ tổng hợp các cập nhật

này để tạo ra mô hình toàn cục mới cho vòng lặp tiếp theo.

1.5.2.

Thách thức dữ liệu không đồng nhất

Một trong những thách thức chính trong FL là tính chất không đồng nhất của dữ

liệu phân tán. Khác với học máy truyền thống, dữ liệu trong FL không tuân theo phân

phối độc lập và đồng nhất (IID), mà thường có đặc tính không đồng nhất (non-IID).
Điều này có nghĩa là dữ liệu từ các thiết bị có thể khác nhau rõ rệt, dẫn đến sự phân

tán trong mô hình và ảnh hưởng đến hiệu suất cũng như khả năng hội tụ của mô hình

toàn cục [1].

Về mặt toán học, nếu ta có 𝑘 thiết bị với dữ liệu cục bộ 𝐷𝑘 trong trường hợp lý
tưởng ta mong muốn 𝑃𝑘(𝑋, 𝑌) = 𝑃(𝑋, 𝑌) cho mọi thiết bị 𝑘. Tuy nhiên, thực tế cho
thấy 𝑃𝑘(𝑋, 𝑌) ≠ 𝑃𝑗(𝑋, 𝑌) với 𝑘 = 𝑗, tạo ra sự khác biệt trong gradient cục bộ và làm
cho quá trình tối ưu hóa trở nên không ổn định.

Các dạng phân phối không đồng nhất:

Sự không đồng nhất của dữ liệu thể hiện qua ba dạng chính. Đầu tiên là sự khác

biệt về đặc trưng, khi các thiết bị có phân phối đặc trưng khác nhau. Chẳng hạn, trong

ứng dụng nhận dạng ảnh trên điện thoại, người dùng ở các vùng địa lý khác nhau sẽ

có dữ liệu ảnh với điều kiện ánh sáng và môi trường khác biệt.

Thứ hai là sự khác biệt về nhãn, khi phân phối nhãn không đồng đều giữa các

thiết bị. Ví dụ điển hình là trong hệ thống gợi ý âm nhạc, người dùng trẻ có xu hướng

nghe nhạc pop nhiều hơn, trong khi người dùng lớn tuổi lại thích nhạc cổ điển, tạo ra

sự mất cân bằng nhãn giữa các thiết bị.

Cuối cùng là sự khác biệt về mối quan hệ đặc trưng-nhãn, khi cùng một đầu vào

có thể có nhãn khác nhau tùy theo ngữ cảnh. Từ “bank” có thể được hiểu là “ngân
hàng” trên thiết bị của nhân viên tài chính nhưng lại là “bờ sông” trên thiết bị của
chuyên gia môi trường.

Các phương pháp xử lý:

Để giải quyết thách thức này, có thể áp dụng nhiều phương pháp khác nhau. Tăng
cường dữ liệu là cách tiếp cận đầu tiên, sử dụng tập dữ liệu chung làm điểm tham

22

chiếu. Ví dụ, có thể dùng tập ngữ liệu Wikipedia để tạo embedding từ vựng chung

trước khi áp dụng vào dữ liệu cụ thể của từng thiết bị.

Lập lịch tham gia thông minh là phương pháp thứ hai, điều chỉnh tần suất tham
gia của các thiết bị dựa trên đặc điểm dữ liệu. Các kỹ thuật như FedFMC và FedCD

giúp cân bằng sự đóng góp bằng cách nhóm các thiết bị có dữ liệu tương tự hoặc điều

chỉnh trọng số tổng hợp phù hợp.

Phương pháp tổ hợp (ensemble) kết hợp nhiều mô hình học máy thay vì xây dựng

một mô hình toàn cục duy nhất. Các mô hình con được huấn luyện riêng biệt trên các
nhóm thiết bị khác nhau, sau đó được kết hợp bằng các kỹ thuật như bỏ phiếu đa số

(voting) hoặc trung bình hóa (averaging). Cách tiếp cận này giúp mô hình xử lý hiệu

quả hơn sự đa dạng và không đồng nhất của dữ liệu.

Cuối cùng, huấn luyện cá nhân hóa tạo ra mô hình tối ưu cho từng thiết bị hoặc

nhóm thiết bị. Các kỹ thuật như Meta-Learning cho phép mô hình thích ứng nhanh

với dữ liệu mới, trong khi Multi-task Learning giúp học đồng thời nhiều nhiệm vụ

liên quan. Ví dụ, ứng dụng gợi ý từ trên bàn phím có thể học cách gõ phím chung

nhưng vẫn cá nhân hóa theo phong cách viết của từng người dùng.

Như vậy, thách thức dữ liệu không đồng nhất đòi hỏi các giải pháp linh hoạt và
tổng hợp, cần cân nhắc cả tính chính xác lẫn khả năng triển khai thực tế trong điều

kiện tài nguyên hạn chế.

1.5.3.  Các thuật toán tối ưu

Sự thành công của FL phụ thuộc rất lớn vào việc lựa chọn và thiết kế các thuật

toán tối ưu hóa phù hợp. Các thuật toán này không chỉ cần đảm bảo hiệu quả tính toán

mà còn phải xử lý được những thách thức đặc thù của môi trường phân tán, bao gồm
tính không đồng nhất của dữ liệu và hạn chế về băng thông. Việc lựa chọn thuật toán
phù hợp phụ thuộc vào đặc thù của hệ thống và dữ liệu, góp phần tăng cường tính
linh hoạt và độ chính xác của mô hình toàn cục [1].

Thuật toán FedAvg
Thuật toán FedAvg được xem là nền tảng và phổ biến nhất trong FL, đặt ra khuôn
khổ cơ bản cho hầu hết các phương pháp sau này. Quá trình hoạt động của FedAvg
hoạt động theo ba bước chính.

23

Trong bước đầu tiên, mỗi thiết bị tham gia sẽ thực hiện huấn luyện mô hình cục

bộ trên dữ liệu riêng của mình qua nhiều epoch. Quá trình này thường sử dụng các

thuật toán tối ưu hóa cổ điển như Stochastic Gradient Descent (SGD), trong đó thiết

bị 𝑘 cập nhật tham số mô hình theo công thức:

(𝑡+1) = 𝜃𝑘
𝜃𝑘

(𝑡) − 𝜂∇𝐹𝑘(𝜃𝑘

(𝑡))

(1.9)

trong đó 𝜂 là learning rate và 𝐹𝑘 là hàm loss cục bộ trên thiết bị 𝑘.
Tiếp theo, các thiết bị gửi các tham số mô hình đã được cập nhật đến máy chủ

trung tâm. Điều quan trọng là chỉ cần truyền tải các tham số mô hình (weights và

biases) thay vì toàn tập dữ liệu thô, giúp giảm đáng kể chi phí băng thông và bảo vệ

quyền riêng tư dữ liệu.

Cuối cùng, máy chủ tổng hợp các cập nhật từ tất cả thiết bị tham gia bằng cách

tính trung bình có trọng số:

𝐾
𝜃(𝑡+1) = ∑

𝑘=1

𝑛𝑘
𝑛

(𝑡+1)

𝜃𝑘

(1.10)

trong  đó 𝑛𝑘 là  số  lượng  mẫu  dữ  liệu  trên  thiết  bị 𝑘 và 𝑛 =   ∑

𝐾
𝑘=1

𝑛𝑘

 là  tổng  số

mẫu, mô hình toàn cục mới này sau đó được gửi lại cho các thiết bị để tiếp tục các

vòng huấn luyện tiếp theo.

Ưu điểm nổi bật của FedAvg là tính đơn giản và hiệu quả trong việc giảm thiểu

chi phí truyền tải. Ví dụ, trong một hệ thống nhận dạng giọng nói với 1000 thiết bị,

thay vì phải truyền hàng terabyte dữ liệu âm thanh, chỉ cần truyền vài megabyte tham

số mô hình, giảm băng thông cần thiết xuống hàng nghìn lần.

Thuật toán FedProx

Mặc dù FedAvg hiệu quả trong nhiều trường hợp, nó gặp khó khăn khi xử lý dữ

liệu non-IID nghiêm trọng. FedProx được phát triển như một cải tiến của FedAvg để

giải quyết vấn đề này thông qua việc thêm một ràng buộc proximal vào hàm mất mát
[1].

Điểm  khác  biệt  cốt  lõi  của  FedProx  nằm  ở việc  bổ  sung  một  thành  phần  điều

chuẩn vào hàm mục tiêu cục bộ:

min
𝜃

𝐹𝑘(𝜃) +

2
|𝜃 − 𝜃(𝑡)|

𝜇
2

(1.11)

trong đó 𝜇 > 0 là tham số điều chuẩn (regularization) và 𝜃(𝑡) là tham số mô hình
toàn cục hiện tại. Thành phần proximal này đóng vai trò như một “lực hút” giữ cho
các tham số mô hình cục bộ không quá xa so với mô hình toàn cục, từ đó giảm thiểu

24

sự phân tán giữa các mô hình cục bộ.

Cơ chế này đặc biệt hữu ích trong các tình huống như phân loại email spam, nơi

người dùng doanh nghiệp có thể nhận nhiều email kỹ thuật trong khi người dùng cá

nhân chủ yếu nhận email cá nhân. FedProx giúp đảm bảo rằng mô hình của mỗi nhóm
người dùng vẫn học được kiến thức chung về spam mà không bị ảnh hưởng quá mức
bởi đặc thù riêng của dữ liệu cục bộ.

Kỹ thuật lựa chọn thiết bị
Trong thực tế, việc yêu cầu tất cả thiết bị tham gia đồng thời trong mỗi vòng huấn

luyện thường không khả thi do các hạn chế về tài nguyên và kết nối mạng. Do đó, kỹ

thuật lựa chọn thiết bị trở thành một thành phần thiết yếu của hệ thống FL.

Chiến lược lựa chọn thông minh cho phép máy chủ chỉ làm việc với một tập con

các thiết bị trong mỗi vòng, thường là 𝐶 × 𝐾 thiết bị với 0 < 𝐶 ≤ 1 là tỷ lệ lựa chọn.

Việc lựa chọn có thể dựa trên nhiều tiêu chí khác nhau như chất lượng kết nối mạng,

mức độ pin còn lại, hoặc thậm chí là chất lượng dữ liệu.

Ví dụ, trong một ứng dụng bàn phím với hàng triệu điện thoại tham gia, hệ thống

có thể ưu tiên lựa chọn những thiết bị có kết nối WiFi ổn định và đang trong thời gian

sạc pin, tránh những thiết bị đang sử dụng mạng di động hoặc có pin thấp. Điều này

không chỉ tăng tốc độ huấn luyện mà còn cải thiện trải nghiệm người dùng.

Hơn nữa, kỹ thuật này còn có thể được kết hợp với các chiến lược lấy mẫu thông

minh (sampling) để đảm bảo tính đại diện của dữ liệu. Thay vì lựa chọn ngẫu nhiên,

hệ thống có thể ưu tiên các thiết bị có phân phối dữ liệu đa dạng hoặc những thiết bị

chưa tham gia gần đây, giúp cân bằng sự đóng góp và tránh overfitting vào một nhóm

thiết bị cụ thể.

1.5.4.  Mô hình triển khai

Việc triển khai FL trong thực tế đòi hỏi sự lựa chọn mô hình kiến trúc phù hợp

với đặc thù của từng ứng dụng cụ thể. Các mô hình triển khai khác nhau được phát
triển để đáp ứng những yêu cầu đa dạng về cấu trúc hệ thống, khả năng tính toán của

thiết bị, và mức độ tin cậy mạng. Việc hiểu rõ những ưu nhược điểm của từng mô
hình sẽ giúp đưa ra quyết định triển khai tối ưu cho các bài toán thực tế.

Mô hình tập trung (Centralized FL)
Mô hình tập trung là một kiến trúc cổ điển và phổ biến nhất trong lĩnh vực FL.
Trong mô hình này, một máy chủ trung tâm đóng vai trò điều phối duy nhất, chịu
trách nhiệm quản lý toàn bộ quá trình huấn luyện. Cụ thể, máy chủ sẽ gửi mô hình

25

ban đầu đến các thiết bị tham gia, sau đó thu thập các bản cập nhật từ chúng, tổng

hợp lại và phân phối mô hình đã được cập nhật trở lại cho các thiết bị.

Ưu điểm chính của mô hình tập trung là dễ triển khai và dễ kiểm soát. Nhờ khả

năng giám sát chặt chẽ và đồng bộ hóa tốt, mô hình này đặc biệt phù hợp với các ứng
dụng yêu cầu mức độ kiểm soát cao. Một ví dụ điển hình là hệ thống gợi ý từ trên bàn
phím điện thoại (như Gboard của Google), nơi hàng triệu thiết bị đóng góp vào việc

cải thiện mô hình ngôn ngữ, nhưng vẫn cần sự điều phối tập trung để đảm bảo chất
lượng và độ nhất quán.

Tuy nhiên, mô hình này cũng tồn tại những điểm yếu đáng kể. Khi số lượng thiết

bị tham gia quá lớn, máy chủ trung tâm có thể trở thành nút thắt, gây quá tải và làm

giảm hiệu quả hệ thống. Ngoài ra, việc phụ thuộc hoàn toàn vào một máy chủ duy
nhất khiến toàn bộ hệ thống dễ bị gián đoạn nếu máy chủ gặp sự cố.

Mô hình phân tán (Decentralized FL)

Để khắc phục những hạn chế của mô hình tập trung, mô hình phân tán đã được

phát triển với triết lý hoàn toàn khác biệt. Trong kiến trúc này, các thiết bị giao tiếp

trực tiếp với nhau thông qua mạng ngang hàng (peer-to-peer), loại bỏ hoàn toàn sự

phụ thuộc của máy chủ trung tâm. Quá trình tổng hợp mô hình được thực hiện thông

qua các thuật toán đồng thuận phân tán, trong đó mỗi thiết bị duy trì một bản sao của

mô hình toàn cục và cập nhật dựa trên thông tin từ các thiết bị lân cận.

Trong mô hình này, thiết bị 𝑖 cập nhật mô hình của mình dựa trên:

(𝑡+1) = 𝜃𝑖
𝜃𝑖

(𝑡) + 𝛼 ∑ 𝑤𝑖𝑗(𝜃𝑗

(𝑡) − 𝜃𝑖

(𝑡)

(1.12)

𝑗∈𝑁𝑖
trong đó 𝑁𝑖 là tập hợp các thiết bị lân cận của thiết bị 𝑖, 𝑤𝑖𝑗 là trọng số giao tiếp,

và 𝛼 là learning rate.

Lợi thế quan trọng nhất của mô hình phân tán là khả năng chống chịu cao với các

sự cố hệ thống. Việc loại bỏ điểm thất bại đơn giúp hệ thống có thể tiếp tục hoạt động

ngay cả khi một số thiết bị ngừng hoạt động. Mô hình này đặc biệt hiệu quả trong các
môi trường như mạng cảm biến không dây hoặc các hệ thống IoT, nơi khả năng kết
nối với máy chủ trung tâm có thể bị hạn chế. Ví dụ, trong một hệ thống giám sát môi
trường với hàng nghìn cảm biến phân tán trên một khu vực rộng lớn, các cảm biến có
thể chia sẻ thông tin và cập nhật mô hình dự đoán thời tiết mà không cần kết nối với
trung tâm điều khiển.

Dù vậy, mô hình phân tán cũng đối mặt với những thách thức riêng. Khả năng
hội tụ của mô hình phụ thuộc rất nhiều vào cấu trúc mạng và chất lượng kết nối giữa

26

các thiết bị. Trong môi trường mạng không ổn định hoặc có độ trễ cao, hiệu suất huấn

luyện có thể bị ảnh hưởng nghiêm trọng. Việc thiết kế một giao thức truyền thông

hiệu quả để đảm bảo sự đồng bộ giữa các thiết bị cũng là một thách thức kỹ thuật

đáng kể.

Mô hình không đồng nhất (Heterogeneous FL)
Nhận thấy thực tế rằng các thiết bị trong hệ thống thường có khả năng xử lý và

tài nguyên phần cứng rất khác nhau, mô hình không đồng nhất (heterogeneous) đã
được phát triển nhằm tận dụng tối đa sự đa dạng đó. Khác với hai mô hình trước vốn

giả định rằng tất cả thiết bị đều có năng lực tương đương, mô hình này cho phép mỗi

thiết bị huấn luyện một mô hình cục bộ với kiến trúc và mức độ phức tạp phù hợp với

khả năng tính toán riêng của nó [1].

Trong mô hình này, các thiết bị mạnh có thể huấn luyện mô hình phức tạp với

nhiều tham số, trong khi các thiết bị yếu hơn chỉ cần xử lý các mô hình đơn giản. Sau

đó,  quá  trình  tổng  hợp  mô  hình  sử  dụng  các  kỹ  thuật  như  chưng  cất  tri  thức

(knowledge distillation) hoặc chia sẻ tham số (parameter sharing) để xây dựng một

mô hình toàn cục hiệu quả từ các mô hình cục bộ không đồng nhất này.

Ưu điểm nổi bật của mô hình không đồng nhất là khả năng tận dụng tối đa tài

nguyên tính toán của từng thiết bị. Điều này đặc biệt quan trọng trong các hệ thống

IoT, nơi thiết bị có thể bao gồm từ điện thoại thông minh hiện đại đến các cảm biến

đơn giản với bộ nhớ và khả năng xử lý hạn chế. Ví dụ, trong một hệ thống thành phố

thông minh, các camera giám sát được trang bị bộ xử lý đồ họa mạnh có thể huấn

luyện mô hình học sâu để nhận dạng đối tượng, trong khi các cảm biến nhiệt độ đơn

giản chỉ cần dùng mô hình hồi quy tuyến tính để dự đoán xu hướng thời tiết.

Tuy nhiên, việc tổng hợp các mô hình không đồng nhất đòi hỏi các kỹ thuật tiên

tiến và tiêu tốn tài nguyên tính toán đáng kể, đặc biệt ở phía máy chủ. Bài toán cân

bằng giữa hiệu năng và độ chính xác khi kết hợp các mô hình với kiến trúc khác nhau

hiện vẫn là một thách thức lớn trong nghiên cứu. Thêm vào đó, các thiết bị có năng
lực hạn chế vẫn có thể gặp khó khăn trong việc xử lý dữ liệu lớn hoặc tham gia vào
quá trình cập nhật mô hình một cách liên tục.

Việc lựa chọn mô hình phù hợp để triển khai cần được cân nhắc kỹ lưỡng dựa
trên nhiều yếu tố như quy mô hệ thống, đặc điểm của dữ liệu, năng lực tính toán của
thiết bị, và yêu cầu về độ tin cậy. Sự phát triển liên tục của các mô hình mới cho thấy
tính linh hoạt và tiềm năng ứng dụng rộng rãi của FL trong nhiều lĩnh vực khác nhau.

27

1.5.5.  Các thách thức về bảo mật và riêng tư

Mặc dù FL được thiết kế nhằm bảo vệ quyền riêng tư bằng cách không yêu cầu

chia sẻ dữ liệu thô, phương pháp này vẫn phải đối mặt với nhiều thách thức nghiêm
trọng về bảo mật và riêng tư do bản chất phân tán của hệ thống [6].

Thách thức đầu tiên là khả năng suy luận thông tin từ các tham số mô hình được

chia sẻ. Các nghiên cứu gần đây đã chỉ ra rằng kẻ tấn công có thể khôi phục thông tin

nhạy cảm từ các cập nhật gradient mà không cần truy cập trực tiếp vào dữ liệu gốc.
Ví dụ, trong bài toán phân loại văn bản, kẻ tấn công có thể suy luận ra một email cụ

thể có trong tập huấn luyện hay không thông qua việc phân tích các gradient được

gửi từ thiết bị client.

Bên cạnh đó, các cuộc tấn công đầu độc mô hình đặt ra mối đe dọa đáng kể khác.

Do máy chủ trung tâm không thể kiểm soát trực tiếp chất lượng dữ liệu tại các thiết
bị cục bộ, các thiết bị độc hại có thể cố tình gửi các cập nhật sai lệch để làm suy giảm

hiệu suất mô hình toàn cục. Trong ứng dụng NLP, điều này có thể dẫn đến việc mô

hình dịch máy cho ra kết quả sai lệch hoặc hệ thống chatbot tạo ra các phản hồi không

phù hợp.

Thêm vào đó, vấn đề tấn công từ máy chủ trung tâm cũng cần được xem xét. Mặc
dù các thiết bị client tin tưởng rằng máy chủ sẽ bảo vệ quyền riêng tư của họ, máy

chủ độc hại vẫn có thể thu thập và phân tích các cập nhật mô hình để trích xuất thông

tin cá nhân. Điều này đặc biệt quan trọng trong các ứng dụng NLP xử lý dữ liệu nhạy

cảm như tin nhắn cá nhân hay tài liệu y tế.

Cuối cùng, thách thức về đồng bộ hóa và tính toàn vẹn dữ liệu trong môi trường

phân tán cũng ảnh hưởng đến tính bảo mật. Việc đảm bảo tất cả các thiết bị đều cập

nhật mô hình một cách đồng bộ và chính xác là một bài toán phức tạp, đặc biệt khi

phải đối phó với các thiết bị không ổn định hoặc kết nối mạng không đáng tin cậy.

Những thách thức này đòi hỏi sự phát triển của các kỹ thuật bảo mật tiên tiến như bảo
mật vi sai (differential privacy) và tổng hợp bảo mật (secure aggregation) để đảm
bảo tính an toàn cho hệ thống FL.

1.6.

Tổng kết chương 1

Chương một cung cấp một cái nhìn tổng quan về NLP và FL. Hai lĩnh vực có mối
quan hệ chặt chẽ trong việc ứng dụng các kỹ thuật máy học vào các tác vụ ngôn ngữ

phức tạp, trong khi vẫn bảo vệ quyền riêng tư của người dùng.

28

Đầu tiên, chương giới thiệu khái niệm, các nhiệm vụ và các tiêu chí đánh giá quan

trọng trong NLP, từ phân loại văn bản đến nhận diện thực thể, cùng với các kỹ thuật

nền tảng như phân tích cú pháp, gắn thẻ từ loại, mô hình hóa ngôn ngữ và biểu diễn

từ, giúp máy tính có thể phân tích, hiểu và sinh ngôn ngữ tự nhiên của con người một
cách hiệu quả.

Tiếp theo, chương giới thiệu khái niệm về FL và tầm quan trọng của nó trong các

lĩnh vực yêu cầu bảo mật dữ liệu cao như y tế và NLP. Bài toán tối ưu trong FL, cùng
với các thuật toán và kỹ thuật để giải quyết dữ liệu không đồng nhất giữa các thiết bị.

Các giải pháp như tăng cường dữ liệu, lập lịch tham gia thiết bị, tổ hợp mô hình, và

huấn luyện cá nhân hóa được trình bày nhằm cải thiện hiệu suất và tính hội tụ của mô

hình FL trong môi trường phi tập trung.

Chương  này  cũng  đã  thảo  luận  các  mô  hình  triển  khai  FL  khác  nhau  như  tập

trung, phi tập trung và không đồng nhất, mỗi khung có ưu điểm và hạn chế riêng,

nhằm đáp ứng nhu cầu đa dạng về cấu trúc hệ thống và khả năng tính toán của các

thiết bị tham gia. Cuối cùng, chương nêu bật các kỹ thuật bảo mật và bảo vệ quyền

riêng tư trong FL, bao gồm bảo mật vi sai, mã hóa đồng hình và môi trường thực thi

đáng tin cậy, giúp đảm bảo rằng dữ liệu người dùng được giữ kín và an toàn trong

quá trình huấn luyện mô hình.

29

Chương 2: Học liên kết cho một số bài toán xử lý
ngôn ngữ tự nhiên

Trong chương này, chúng tôi sẽ trình bày định nghĩa của hai bài toán sinh văn

bản và phân loại văn bản trong NLP, kiến trúc của mô hình BART, thuật toán tối ưu

FedOPT và cách áp dụng FL vào hai bài toán này với ràng buộc là có sử dụng mô

hình BART và FedOPT.

2.1.

Định nghĩa bài toán

2.1.1.

Bài toán 1. Sinh văn bản

Sinh văn bản (NLG), hay tạo sinh ngôn ngữ tự nhiên là một nhiệm vụ quan trọng

trong lĩnh vực NLP. Mục tiêu của sinh văn bản là tạo ra văn bản dễ hiểu bằng ngôn

ngữ con người từ các nguồn dữ liệu đa dạng như dữ liệu văn bản, số liệu, hình ảnh,
hoặc cơ sở tri thức có cấu trúc. Trong đó, sinh văn bản từ văn bản đầu vào là ứng

dụng phổ biến nhất [7].

Cơ chế hoạt động và ứng dụng:

Quá trình sinh văn bản bao gồm ba bước chính: nhận đầu vào dưới dạng văn bản

(chuỗi từ, từ khóa), xử lý thành biểu diễn ngữ nghĩa, và tạo ra văn bản đầu ra mong

muốn. Các ứng dụng tiêu biểu bao gồm dịch máy, tóm tắt văn bản, hệ thống trả lời

câu hỏi (QA), và chatbot hỗ trợ đối thoại với con người.

Với sự phát triển của học sâu, các mô hình sinh văn bản dựa trên mạng nơ-ron

sâu  đã  đạt  hiệu  suất  ấn  tượng.  Sinh  văn  bản  được  định  nghĩa  như  một  bài  toán

sequence-to-sequence (Seq2Seq), hoạt động theo sơ đồ mã hóa – giải mã (encoder-

decoder). Bộ mã hóa ánh xạ chuỗi đầu vào thành vector có kích thước cố định, bộ

giải mã ánh xạ vector này thành chuỗi đích. Các kiến trúc phổ biến gồm mã hóa –
giải mã bao gồm: RNN, CNN, và Transformer [7].

Mô hình toán học:

Bài toán sinh văn bản là một bài toán chuỗi sang chuỗi với mục tiêu tạo ra chuỗi
đầu ra 𝑌 = (𝑦1, 𝑦2, … , 𝑦𝑚) dựa trên ngữ cảnh các từ đã xuất hiện trước đó và chuỗi
đầu vào 𝑋 = (𝑥1, 𝑥2, … , 𝑥𝑛). Đây là bài toán mô hình hóa ngôn ngữ, trong đó mỗi từ
được sinh ra dựa trên đầu vào và ngữ cảnh từ các từ đã sinh trước đó.

Về mặt toán học, bài toán được mô hình hóa như một phân phối xác suất có điều

kiện, trong đó 𝑋 là chuỗi đầu vào (có thể là câu, đoạn văn, hoặc rỗng), 𝑌 là chuỗi đầu

30

ra cần sinh, và mục tiêu là dự đoán xác suất của 𝑌 dựa trên 𝑋 sao cho xác suất này

đạt giá trị lớn nhất [11].

2.1.2.

Bài toán 2. Phân loại văn bản

Phân loại văn bản đóng vai trò là một nhiệm vụ cơ bản và quan trọng trong lĩnh

vực NLP hiện đại. Với sự phát triển mạnh mẽ của công nghệ NLP trong những năm
gần đây, phân loại văn bản đã đạt được nhiều thành tựu đáng kể, góp phần quan trọng

vào việc giải quyết các bài toán thực tế [8].

Bản chất và tầm quan trọng của phân loại văn bản:
Về cơ bản, các phương pháp phân loại văn bản đều hướng tới một mục tiêu chung

là gán một nhãn được xác định trước cho một văn bản đầu vào nhất định. Tầm quan

trọng của phương pháp này càng trở nên rõ ràng khi xem xét bối cảnh hiện tại, nơi

khối lượng tài liệu kỹ thuật số đang gia tăng với tốc độ chóng mặt. Phân loại văn bản

không chỉ là phương pháp quan trọng để quản lý và xử lý hiệu quả khối lượng dữ liệu

khổng lồ này, mà còn đóng vai trò thiết yếu trong nhiều ứng dụng thực tế như trích

xuất thông tin, tìm kiếm tài liệu, phân tích cảm xúc, và gợi ý nội dung [9] [10].

Hơn nữa, phạm vi ứng dụng của phân loại văn bản không chỉ giới hạn ở các ứng

dụng  truyền  thống.  Ngày  nay,  phương  pháp  này  còn  được  sử  dụng  rộng  rãi  trong

nhiều bài toán phức tạp hơn, chẳng hạn như trả lời câu hỏi tự động, tóm tắt văn bản,

và gán nhãn chủ đề đa chiều. Ví dụ, trong hệ thống trả lời câu hỏi, phân loại văn bản

có thể được sử dụng để xác định loại câu hỏi (what, when, where, how) nhằm định

hướng chiến lược tìm kiếm câu trả lời phù hợp.

Định nghĩa toán học và cấu trúc bài toán:

Bài toán phân loại văn bản được định nghĩa một cách chính xác thông qua việc

xác định mục tiêu gán một hoặc nhiều nhãn thuộc tập các nhãn được xác định trước

cho một văn bản đầu vào dựa trên nội dung của nó.

Với mục tiêu gán một hoặc nhiều nhãn thuộc tập các nhãn được xác định trước

cho một văn bản đầu vào dựa trên nội dung của nó.

Cụ thể về cấu trúc đầu vào, ta có một tập các bản ghi được biểu diễn bởi một tập
hợp các văn bản 𝐷 = {𝑥1, 𝑥2, … , 𝑥𝑛}. Trong đó, mỗi bản ghi 𝑥𝑖 hoặc còn gọi là mẫu
(instance) được biểu diễn dưới dạng một vector đặc trưng (features) đại diện cho các
thuộc tính hoặc thông tin quan trọng của bản ghi đó. Mỗi bản ghi 𝑥𝑖 được gán một
nhãn 𝑦𝑖 thuộc một tập các nhãn rời rạc 𝐶 = {1, … , 𝑘}, trong đó 𝑘 là số lượng các nhãn
khác nhau.

31

Quá trình huấn luyện nhằm mục tiêu xây dựng một mô hình phân loại 𝑓 dựa trên

tập dữ liệu huấn luyện đã có nhãn để có thể dự đoán chính xác nhãn cho một mẫu thử

nghiệm chưa biết nhãn 𝑦 ∈ 𝐶. Sao cho 𝑓 ∶ 𝑥 → 𝐶.

Để minh họa, xét ví dụ về phân loại email spam: đầu vào là các email được biểu
diễn bằng vector đặc trưng (tần suất từ khóa, độ dài email, số lượng liên kết), và đầu

ra là nhãn “spam” hoặc “không spam”. Mô hình học từ dữ liệu huấn luyện gồm hàng

nghìn email đã được gán nhãn để có thể phân loại chính xác email mới.

Phân loại theo cách tiếp cận dự đoán:

Dựa trên cách thức đưa ra dự đoán, phân loại văn bản có thể được chia thành hai

loại chính, mỗi loại có những đặc điểm và ứng dụng riêng biệt.

Phân loại cứng (Hard Classification) là phương pháp truyền thống trong đó mỗi
bản ghi sẽ được gán  một nhãn cụ thể và duy nhất.  Phương pháp  này phù  hợp với

những bài toán có ranh giới rõ ràng giữa các lớp, chẳng hạn như phân loại thể loại tin

tức (thể thao, chính trị, kinh tế) hoặc phân loại mức độ cảm xúc (tích cực, tiêu cực,

trung tính).

Ngược lại, phân loại mềm (Soft Classification) áp dụng cách tiếp cận xác suất

bằng cách gán xác suất cho mỗi nhãn có thể, từ đó nhãn có xác suất cao nhất sẽ được

chọn  làm  kết  quả  cuối  cùng.  Phương  pháp  này  đặc  biệt  hữu  ích  trong  những  tình

huống mà ranh giới giữa các lớp không rõ ràng hoặc khi cần đánh giá độ tin cậy của

dự đoán. Ví dụ, trong phân tích cảm xúc, một bình luận có thể có 70% khả năng tích

cực và 30% khả năng trung tính, giúp người dùng hiểu được mức độ không chắc chắn

trong dự đoán.

Thách thức và triển vọng phát triển:

Với tốc độ gia tăng nhanh chóng của dữ liệu văn bản trong thời đại số, việc phát

triển các hệ thống phân loại chính xác và đáng tin cậy đã trở thành một nhu cầu cấp

thiết [10] [11]. Điều này đòi hỏi không chỉ sự cải tiến về mặt thuật toán mà còn cả
khả năng xử lý khối lượng dữ liệu lớn và đa dạng về ngôn ngữ, định dạng, và ngữ

cảnh.

Những thách thức này đồng thời cũng mở ra nhiều cơ hội nghiên cứu và ứng dụng
mới, từ việc phát triển các mô hình học sâu tiên tiến đến việc tích hợp trí tuệ nhân tạo
vào các hệ thống phân loại văn bản tự động. Sự phát triển này hứa hẹn sẽ tiếp tục góp
phần quan trọng vào việc giải quyết các thách thức trong xử lý và quản lý thông tin
trong kỷ nguyên dữ liệu lớn.

32

2.2. Mô hình BART

2.2.1. Giới thiệu

BART được phát triển bởi Facebook AI vào năm 2019, đại diện cho một bước

tiến quan trọng trong lĩnh vực NLP. Khác với các mô hình trước đó chỉ tập trung vào
một  khía  cạnh  duy  nhất,  BART  được  thiết  kế  để  kết  hợp  hài  hòa  hai  kiến  trúc
transformer quan trọng: khả năng mã hóa hai chiều như BERT và tính năng sinh văn

bản tự hồi quy như GPT.

Điểm đột phá của BART nằm ở việc sử dụng kiến trúc mã hóa – giải mã với cơ

chế huấn luyện tự mã  hóa khử nhiễu  (denoising autoencoder) độc  đáo. Trong quá

trình này, dữ liệu đầu vào được cố ý làm nhiễu thông qua các kỹ thuật như che từ,

xóa từ, hoặc hoán vị từ, sau đó mô hình phải học cách tái tạo lại văn bản gốc. Cơ chế
này không chỉ giúp BART học được biểu diễn ngữ nghĩa sâu sắc mà còn tạo ra khả

năng thích ứng linh hoạt với nhiều loại nhiệm vụ khác nhau.

Sự xuất hiện của BART đã giải quyết một thách thức lâu nay trong cộng đồng

nghiên cứu: làm thế nào để tạo ra một mô hình có thể xử lý đồng thời cả việc hiểu

ngôn ngữ và sinh văn bản. Trong khi BERT nổi bật trong việc hiểu ngữ nghĩa nhưng

không thể sinh văn bản, và GPT mạnh trong sinh văn bản nhưng bị hạn chế bởi tính

đơn hướng, BART đã thành công trong việc thu hẹp khoảng cách bằng cách kết hợp

ưu điểm của cả hai. Kết quả là một mô hình đa năng có thể thực hiện hiệu quả các tác

vụ từ tóm tắt văn bản, dịch máy đến trả lời câu hỏi và đối thoại tự động.

2.2.2. Kiến trúc của BART

2.2.2.1.  Kiến trúc tổng quan seq2seq
BART được thiết kế với kiến trúc seq2seq độc đáo, tạo ra sự kết hợp tối ưu giữa

khả năng hiểu ngữ nghĩa sâu và khả năng sinh văn bản linh hoạt. Kiến trúc này thể
hiện sự đột phá trong việc xử lý đa nhiệm trong lĩnh vực NLP bằng cách tích hợp ưu

điểm của cả BERT và GPT trong một mô hình thống nhất.

33

Hình 1. Kiến trúc tổng quan của BART

Bộ mã hóa hai chiều (Bidirectional Encoder):

Thành phần đầu tiên của BART là bộ mã hóa hai chiều, đóng vai trò như một bộ

xử lý ngữ nghĩa toàn diện. Bộ mã hóa hai chiều này sẽ tiếp nhận chuỗi văn bản đầu
vào là  𝑋 = (𝑥1, 𝑥2, … , 𝑥𝑛) và xử lý theo hướng hai chiều, cho phép mỗi token có thể
nhìn thấy và tương tác với tất cả các token khác trong chuỗi. Ví dụ, khi xử lý câu

“Hôm nay trời đẹp nên tôi đi dạo”, bộ mã hó có thể hiểu được mối quan hệ giữa “trời

đẹp” và “đi dạo” một cách đồng thời, không phụ thuộc vào thứ tự xử lý.

Cấu trúc bộ mã hóa bao gồm nhiều lớp Transformer (Encoder 1, 2, ..., N) được

khởi tạo ngẫu nhiên. Mỗi lớp sử dụng cơ chế multi-head attention để nắm bắt các mối

quan hệ phức tạp giữa các từ trong ngữ cảnh. Đặc biệt, bộ mã hóa tích hợp tích hợp

mã hóa vị trí (positional encoding) để bảo toàn thông tin vị trí của các token, đảm bảo
mô hình có thể phân biệt được “Tôi yêu em” và “Em yêu tôi” mặc dù sử dụng cùng
một tập từ vựng.

Trong quá trình huấn luyện, bộ mã hóa được thiết kế để hoạt động như một mạng
tự mã hóa khử nhiễu, nghĩa là nó học cách tạo ra biểu diễn ngữ nghĩa sâu từ văn bản
đã bị làm nhiễu. Khả năng này giúp mô hình trở nên mạnh mẽ hơn trong việc xử lý
văn bản có lỗi hoặc không hoàn chỉnh.

Bộ giải mã tự hồi quy (Autoregressive Decoder):

34

Ngược lại với bộ mã hóa, bộ giải mã tự hồi quy hoạt động theo cơ chế sinh tuần
tự, tạo ra chuỗi đầu ra 𝑌 = (𝑦1, 𝑦2, … , 𝑦𝑛) theo hướng từ trái sang phải. Bộ giải mã
này kế thừa ưu điểm của các mô hình ngôn ngữ tự hồi quy như GPT, trong đó mỗi

token được sinh ra dựa trên tất cả các token đã được tạo ra trước đó.

Cấu trúc bộ giải mã cũng bao gồm nhiều lớp Transformer (Decoder 1, 2, ..., N),

tuy  nhiên  điểm  khác  biệt  quan  trọng  là  cơ  chế  cross-attention.  Thông  qua  cross-
attention, bộ giải mã không chỉ dựa vào các token đã sinh ra trước đó mà còn kết hợp

thông tin từ bộ mã hóa để đưa ra dự đoán chính xác hơn. Ví dụ, khi dịch câu “The
weather is nice today” sang tiếng Việt, bộ giải mã sẽ sinh ra “Hôm nay” đầu tiên, sau
đó sử dụng cả thông tin từ “Hôm nay” và biểu diễn từ bộ mã hóa để sinh ra “thời tiết”.

Cuối cùng, đầu ra của bộ giải mã được xử lý qua các lớp Linear và Softmax để

tính toán phân phối xác suất trên toàn bộ từ vựng, từ đó lựa chọn token phù hợp nhất

cho vị trí tiếp theo.

Cơ chế kết nối và tương tác:

Sức mạnh thực sự của BART nằm ở cách bộ mã hóa và bộ giải mã tương tác với

nhau thông qua cơ chế attention được thiết kế tinh vi. Kết nối này cho phép mô hình

vừa có khả năng hiểu sâu ngữ nghĩa của văn bản đầu vào nhờ bộ mã hóa hai chiều

vừa có thể sinh ra văn bản chất lượng cao nhờ bộ giải mã tự hồi quy.

Kiến trúc tổng hợp này làm cho BART trở thành một mô hình đa năng, có thể xử

lý đồng thời nhiều loại nhiệm vụ khác nhau trong NLP. Từ tóm tắt văn bản, dịch máy

cho đến sinh văn bản sáng tạo, BART đều thể hiện hiệu suất ấn tượng nhờ vào sự kết

hợp hài hòa giữa khả năng hiểu và khả năng sinh của hai thành phần chính.

2.2.2.2. Bộ mã hóa hai chiều
Bộ mã hóa hai chiều  đóng vai trò then chốt trong kiến trúc BART, đảm nhận

nhiệm vụ mã hóa chuỗi đầu vào thành các biểu diễn ngữ nghĩa phong phú thông qua
khả năng xử lý hai chiều độc đáo. Khác biệt với các mô hình đơn hướng như GPT chỉ
có thể nhìn về phía trước, bỗ mã hóa của BART kế thừa và phát triển từ kiến trúc

BERT, cho phép xem xét đồng thời cả thông tin từ trái sang phải và từ phải sang trái
trong toàn bộ chuỗi đầu vào.

Khả  năng  xử  lý  hai  chiều  này  mang  lại  lợi thế  vượt trội  cho  BART  trong  các
nhiệm vụ đòi hỏi hiểu ngữ cảnh sâu sắc. Kết quả thực nghiệm cho thấy Bộ mã hóa
hai chiều giúp BART đạt điểm F1 90.8 trên tập dữ liệu SQuAD 1.1 với kỹ thuật Text
Infilling [1], chứng minh hiệu suất xuất sắc trong các tác vụ như tóm tắt văn bản,

35

phân tích ngữ nghĩa, và trả lời câu hỏi. Hơn nữa, khi kết hợp với bộ mã hóa, bộ giải

mã này còn hỗ trợ hiệu quả cho các nhiệm vụ sinh văn bản, biến BART thành một

mô hình đa năng trong lĩnh vực NLP.

Tuy nhiên, sức mạnh này cũng đi kèm với những thách thức nhất định. Việc xử
lý hai chiều đòi hỏi tài nguyên tính toán lớn hơn đáng kể so với các mô hình đơn
hướng, đặc biệt khi xử lý các chuỗi dài. Đồng thời, hiệu quả của bộ mã hóa phụ thuộc

chặt chẽ vào chất lượng và độ đa dạng của dữ liệu huấn luyện, cũng như sự lựa chọn
kỹ thuật làm nhiễu phù hợp [1].

Cơ chế hoạt động của bộ mã hóa hai chiều:

Về mặt kiến trúc, Bộ mã hóa hai chiều được xây dựng từ một tập hợp các lớp

Transformer,  với  6  lớp  trong  phiên  bản  BART-base  và  12  lớp  trong  BART-large,
tương ứng với kích thước ẩn là 768 và 1024 [1]. Mỗi lớp Transformer được cấu trúc

từ ba thành phần cốt lõi hoạt động một cách đồng bộ và bổ trợ lẫn nhau.

Thành phần đầu tiên và quan trọng nhất là Multi-Head Self-Attention, cho phép

bộ mã hóa tập trung vào các mối quan hệ giữa tất cả các từ trong chuỗi đầu vào mà

không bị giới hạn bởi khoảng cách vật lý giữa chúng. Khác với self-attention đơn

hướng chỉ có thể nhìn về phía trước, cơ chế này trong BART phân tích toàn bộ chuỗi

cùng lúc, tạo ra các vector biểu diễn có khả năng nắm bắt ngữ cảnh toàn diện. Ví dụ,

trong câu “Chiếc xe đỏ đang đậu bên ngoài nhà tôi rất đẹp”, cơ chế này có thể nhận

ra rằng “đẹp” đang mô tả “chiếc xe đỏ” chứ không phải “nhà tôi”.

Tiếp theo, Feed-Forward Neural Network (FFN) đảm nhận vai trò xử lý phi tuyến

tính. Sau khi attention được áp dụng, mỗi token trong chuỗi được xử lý qua mạng nơ-

ron truyền thẳng để tăng cường khả năng biểu diễn. Một điểm cải tiến đáng chú ý là
FFN trong BART sử dụng hàm kích hoạt GeLU thay vì ReLU như trong BERT, nhằm

cải thiện hiệu suất học [1]. Thay đổi này giúp bộ mã hóa học được các đặc trưng phức

tạp hơn từ dữ liệu đầu vào.

Cuối cùng, Layer Normalization và Residual Connections đóng vai trò ổn định
quá trình huấn luyện. Để tránh vấn đề gradient biến mất và đảm bảo tính ổn định, mỗi
lớp Transformer sử dụng chuẩn hóa lớp và kết nối dư, cho phép thông tin từ các lớp
trước được truyền trực tiếp lên các lớp sau [1]. Cơ chế này đặc biệt quan trọng khi xử
lý các mô hình sâu với nhiều lớp.

Để bảo toàn thông tin về vị trí của các từ trong chuỗi, bộ mã hóa tích hợp mã hóa
vị trí vào vector đầu vào. Những vector có thể học được này biểu diễn vị trí tương đối
của mỗi token, giúp mô hình phân biệt được sự khác nhau giữa “Tôi yêu em” và “Em

36

yêu tôi” mặc dù sử dụng cùng tập từ vựng. Các tham số của bộ mã hóa được khởi tạo

ngẫu nhiên và được tối ưu hóa trong quá trình huấn luyện.

Quá trình xử lý đầu vào với các chiến lược làm nhiễu:

Một đặc điểm độc đáo của BART nằm ở cách thức xử lý dữ liệu đầu vào. Thay
vì sử dụng văn bản sạch, bộ mã hóa được huấn luyện với văn bản đã được làm nhiễu
theo các chiến lược đặc trưng [1]. Phương pháp này không chỉ giúp mô hình trở nên

mạnh mẽ hơn mà còn cải thiện khả năng tổng quát hóa.

Hình 2. Các chiến lược làm nhiễu

Che từ (Token  Masking) là chiến lược đầu tiên, trong đó một tỷ lệ  từ (thường

khoảng  15%)  được  thay  thế  ngẫu  nhiên  bằng  token  đặc  biệt  [MASK].  Ví  dụ,  câu

“Hôm nay trời đẹp nên tôi đi dạo” có thể trở thành “Hôm nay [MASK] đẹp nên tôi đi

dạo”. Kỹ thuật này buộc mô hình phải dự đoán từ bị che dựa trên ngữ cảnh xung

quanh.

Xóa từ (Token  Deletion) đi xa hơn bằng cách xóa hoàn  toàn một số từ, tạo ra

thách thức lớn hơn cho mô hình. Câu “Hôm nay trời đẹp nên tôi đi dạo” có thể thành

“Hôm nay đẹp tôi đi dạo”. Kỹ thuật này không chỉ yêu cầu mô hình xác định nội dung

bị thiếu mà còn phải xác định chính xác vị trí cần bổ sung.

Điền văn bản (Text Infilling) mang tính thách thức cao nhất khi thay thế cả một

đoạn văn bản bằng một token [MASK] duy nhất. Độ dài đoạn bị thay thế được lấy
mẫu từ phân phối Poisson, tạo ra tính ngẫu nhiên cao. Ví dụ, “Hôm nay trời đẹp nên
tôi quyết định đi dạo công viên” có thể thành “Hôm nay [MASK] công viên”. Kỹ
thuật này buộc mô hình không chỉ dự đoán nội dung mà còn phải xác định số lượng
token cần thiết, từ đó cải thiện khả năng hiểu ngữ cảnh dài.

Hoán đổi câu (Sentence Permutation) hoạt động ở mức độ cao hơn bằng cách
hoán đổi thứ tự các câu trong một đoạn văn. Chiến lược này giúp mô hình học cách
sắp xếp lại thông tin một cách logic và hiểu được mối quan hệ giữa các ý tưởng trong
văn bản.

37

Token [MASK] trong các chiến lược này đóng vai trò như một ký hiệu đặc biệt

được thêm vào từ vựng của mô hình. Khi một từ hoặc đoạn văn được thay thế bằng

[MASK], mô hình phải dựa vào ngữ cảnh xung quanh để dự đoán nội dung gốc. Quá

trình này buộc mô hình học cách hiểu sâu về ngữ nghĩa và cấu trúc của câu, từ đó
tăng cường khả năng hiểu ngữ cảnh hai chiều và sinh văn bản mạch lạc.

Hình 3. Quá trình mã hóa văn bản nhiễu hai chiều

Quá trình xử lý diễn ra theo trình tự có hệ thống. Bộ mã hóa nhận chuỗi đầu vào

chứa [MASK] và tạo ra biểu diễn ngữ nghĩa cho toàn bộ chuỗi, bao gồm cả vị trí của

[MASK]. Nhờ khả năng hoạt động hai chiều, Bộ mã hó có thể tận dụng thông tin từ

cả bên trái và bên phải để hiểu ngữ cảnh một cách toàn diện. Biểu diễn này sau đó

được truyền sang bộ giải mã, nơi BART sử dụng thông tin từ bộ mã hóa để sinh ra

chuỗi đầu ra hoàn chỉnh, thay thế [MASK] bằng nội dung phù hợp.

Quá trình huấn luyện được tối ưu hóa thông qua việc so sánh đầu ra của bộ giải

mã với văn bản gốc, sử dụng hàm mất mát cross-entropy [1]. Cách tiếp cận này đảm

bảo mô hình không chỉ học được cách dự đoán từ bị thiếu mà còn hiểu được cấu trúc

và ngữ nghĩa tổng thể của văn bản.

Vai trò trung tâm trong hệ thống BART:
Bộ mã hóa hai chiều thực sự đóng vai trò như bộ não của BART, cung cấp nền

tảng ngữ nghĩa vững chắc cho bộ giải mã hoạt động hiệu quả. Khả năng xử lý hai

chiều cho phép bộ mã hóa nắm bắt các mối quan hệ phức tạp trong văn bản, từ sự phụ
thuộc giữa các từ cách xa nhau đến những ý nghĩa ẩn trong ngữ cảnh.

Để minh họa sức mạnh này, xét câu “Tôi không đi học vì trời mưa”. Bộ mã hóa
có thể hiểu rằng “trời mưa” là lý do trực tiếp cho hành động “không đi học” bằng
cách xem xét cả hai phần của câu cùng lúc [1]. Khả năng này đặc biệt quan trọng
trong các tác vụ phức tạp như tóm tắt văn bản, nơi mô hình cần hiểu mối quan hệ giữa
các ý tưởng để tạo ra bản tóm tắt chính xác và mạch lạc.

Thông qua việc tạo ra các biểu diễn ngữ nghĩa dưới dạng vector, bộ mã hóa hai
chiều không chỉ đơn thuần mã hóa thông tin mà còn trích xuất và tổ chức các đặc

38

trưng ngữ nghĩa quan trọng. Những vector này sau đó trở thành đầu vào có giá trị cho

bộ giải mã, cho phép tái tạo văn bản gốc hoặc sinh văn bản mới tùy thuộc vào yêu

cầu cụ thể của bài toán [1].

2.2.2.3.  Bộ giải mã tự hồi quy
Bộ giải mã tự hồi quy đóng vai trò là thành phần thứ hai trong kiến trúc seq2seq

của BART, đảm nhận trọng trách sinh ra chuỗi văn bản đầu ra dựa trên các biểu diễn
ngữ nghĩa được cung cấp từ bộ mã hóa hai chiều. Khác với bộ mã hóa xử lý toàn bộ

chuỗi cùng lúc, bộ giải mã của BART hoạt động theo cơ chế tuần tự, dự đoán từng

token trong chuỗi đầu ra một cách có trật tự từ trái sang phải. Quá trình này diễn ra

bằng cách sử dụng thông tin từ các token đã được sinh ra trước đó, tạo nên đặc tính

tự hồi quy đặc trưng của thành phần này.

Sự linh hoạt trong sinh văn bản của bộ giải mã giúp BART đạt được hiệu suất

cao trên nhiều nhiệm vụ đa dạng, từ dịch máy, tóm tắt văn bản cho đến sinh văn bản

sáng tạo. Khả năng này xuất phát từ thiết kế tinh vi cho phép bộ giải mã không chỉ

dựa vào các token đã sinh mà còn tận dụng thông tin ngữ nghĩa phong phú từ bộ mã

hóa thông qua cơ chế cross-attention.

Cơ chế hoạt động:

Về mặt kiến trúc, bộ giải mã tự hồi quy của BART được xây dựng từ nhiều lớp

Transformer, tương ứng với 6 lớp trong phiên bản BART-base và 12 lớp trong BART-

large, với kích thước ẩn lần lượt là 768 và 1024 [1]. Điểm khác biệt quan trọng so với

bộ mã hóa nằm ở việc bộ giải mã được trang bị hai cơ chế chú ý hoàn toàn khác nhau,

mỗi cơ chế phục vụ một mục đích riêng biệt trong quá trình sinh văn bản.

Cơ chế đầu tiên là Self-Attention với Masking, một phiên bản được điều chỉnh

của  self-attention  truyền  thống.  Trong  kiến  trúc  Transformer  thông  thường,  self-

attention cho phép mỗi token trong chuỗi chú ý đến tất cả các token khác, bao gồm
cả những token xuất hiện trước và sau nó. Tuy nhiên, trong bộ giải mã của BART,
self-attention được áp dụng mask để chỉ cho phép mỗi token chú ý đến các token xuất
hiện trước nó trong chuỗi đầu ra theo hướng từ trái sang phải.

Việc masking này được thực hiện bằng cách áp dụng một ma trận mask trong
phép  tính  attention,  đảm  bảo  rằng  token  hiện  tại  không  thể  “nhìn  thấy”  các  token
tương lai. Ví dụ, khi sinh câu “Hôm nay trời đẹp”, token “trời” chỉ có thể chú ý đến
“Hôm” và “nay”, không thể biết trước rằng từ tiếp theo sẽ là “đẹp”. Tính chất từ trái

sang phải này chính là cốt lõi của cơ chế tự hồi quy, đảm bảo rằng đầu ra được sinh

39

từng bước một cách tự nhiên, mỗi token mới dựa trên kiến thức từ các token đã sinh

trước đó.

Cơ chế thứ hai, Cross-Attention, đóng vai trò then chốt trong việc kết nối bộ giải

mã với bộ mã hóa. Trong kiến trúc transformer seq2seq, cross-attention cho phép bộ
giả mã tham chiếu đến thông tin từ bộ mã hóa, tạo ra sự liên kết chặt chẽ giữa quá
trình hiểu và sinh văn bản. Cụ thể trong BART, mỗi lớp của bộ giải mã không chỉ

thực hiện self-attention mà còn thực hiện cross-attention lên lớp ẩn cuối cùng của bộ
mã hóa hai chiều.

Điều này có ý nghĩa sâu sắc trong việc cải thiện chất lượng sinh văn bản. Bộ giả

mã không chỉ dựa vào các token đã sinh trước đó mà còn có khả năng truy cập vào

thông tin ngữ nghĩa phong phú từ bộ mã hóa, từ đó cải thiện đáng kể tính mạch lạc
và chính xác của văn bản được sinh ra.

Trong cơ chế cross-attention, các token trong chuỗi đầu ra đang được sinh bởi bộ

giải mã sẽ “chú ý” đến tất cả các token trong chuỗi đầu vào đã được mã hóa. Quá

trình này được thực hiện bằng cách sử dụng các vector query từ bộ giải mã để tương

tác với các vector key và value từ bộ mã hóa, tạo ra một đầu ra kết hợp thông tin từ

cả hai nguồn. Ví dụ, khi dịch câu “The weather is beautiful today” sang tiếng Việt,

bộ giải mã sinh ra “Hôm nay” không chỉ dựa vào token bắt đầu mà còn chú ý đến

toàn bộ ngữ cảnh của câu tiếng Anh.

Lợi thế  đặc  biệt  của  BART  nằm  ở việc  bộ  mã  hóa  hoạt  động  theo  cơ chế  hai

chiều, khiến lớp ẩn cuối cùng của nó chứa thông tin ngữ nghĩa toàn diện về chuỗi đầu

vào, bao gồm cả ngữ cảnh trước và sau của mỗi token. Bộ giải mã tận dụng điều này

để sinh ra các token đầu ra chính xác và phù hợp hơn, tạo nên sự khác biệt rõ rệt so
với các mô hình chỉ sử dụng bộ mã hóa đơn hướng.

Quá trình sinh văn bản khởi đầu từ một token đặc biệt, thường là token bắt đầu

câu. Sau mỗi bước dự đoán, đầu ra của bộ giải mã được xử lý qua lớp Linear và hàm

Softmax để tính toán phân phối xác suất cho token tiếp theo trong toàn bộ từ vựng.
Token có xác suất cao nhất sẽ được chọn (hoặc được lấy mẫu theo phân phối) để trở
thành token tiếp theo trong chuỗi đầu ra.

Vai trò chiến lược trong kiến trúc BART:
Bộ giải mã tự hồi quy đóng vai trò như bộ phận sinh đầu ra của BART, có khả
năng chuyển đổi các biểu diễn ngữ nghĩa trừu tượng từ bộ mã hóa thành chuỗi văn
bản có ý nghĩa và mạch lạc. Sự kết hợp hài hòa giữa bộ mã hóa hai chiều và bộ giải

40

mã tự hồi quy tạo nên một hệ thống hoàn chỉnh, cho phép BART xử lý đồng thời cả

hai khía cạnh quan trọng của NLP: hiểu và sinh văn bản.

So với các mô hình cùng thời kỳ, bộ giải mã của BART thể hiện những ưu thế

nổi bật. Khác với BERT – mô hình chỉ tập trung vào việc hiểu văn bản mà không có
khả năng sinh tự hồi quy, bộ giải mã tự hồi quy của BART mang lại lợi thế rõ rệt
trong các bài toán sinh ngôn ngữ. Mô hình có thể tạo ra các câu hoàn chỉnh, đoạn văn

mạch lạc, thậm chí cả văn bản dài một cách tự nhiên và logic. Chính khả năng thích
ứng linh hoạt này đã biến BART trở thành một công cụ đa năng trong lĩnh vực xử lý

ngôn ngữ tự nhiên (NLP).

2.2.3. Ứng dụng của BART trong học liên kết

Trong môi trường FL, BART thể hiện tiềm năng vượt trội cho các tác vụ NLP có
yêu cầu cao về bảo mật và riêng tư dữ liệu. Khác với các ứng dụng truyền thống tập

trung, FL đòi hỏi các mô hình phải hoạt động hiệu quả trên dữ liệu phân tán mà không

cần tập trung hóa thông tin nhạy cảm.

Một trong những ứng dụng nổi bật nhất là phân loại văn bản riêng tư, đặc biệt

trong lĩnh vực y tế và tài chính. Ví dụ, các bệnh viện có thể sử dụng BART để phân

loại hồ sơ bệnh án theo mức độ nghiêm trọng mà không cần chia sẻ dữ liệu bệnh nhân

với các cơ sở khác. Bộ mã hóa hai chiều của BART giúp hiểu ngữ cảnh phức tạp

trong văn bản y khoa, trong khi bộ giải mã có thể sinh ra các nhãn phân loại chính

xác dựa trên đặc trưng ngữ nghĩa đã được mã hóa.

Tóm tắt tài liệu nhạy cảm là một ứng dụng khác có giá trị cao trong FL. Các tổ

chức pháp lý hoặc công ty có thể sử dụng BART để tạo bản tóm tắt từ các hợp đồng,

báo cáo nội bộ mà không cần gửi toàn bộ tài liệu đến máy chủ trung tâm. Khả năng
xử lý chuỗi dài của BART kết hợp với cơ chế tự mã hóa khử nhiễu giúp mô hình tạo

ra bản tóm tắt chất lượng cao ngay cả khi được huấn luyện trên dữ liệu phân tán có

độ nhiễu khác nhau giữa các client.

Tuy nhiên, việc áp dụng BART trong môi trường phân tán cũng đặt ra những
thách  thức  đáng  kể.  Tính  không  đồng  nhất  của  dữ  liệu  giữa  các  client  có  thể  ảnh
hưởng đến chất lượng học của mô hình. Ví dụ, trong tác vụ dịch máy phân tán, một
client có thể chuyên về văn bản kỹ thuật trong khi client khác xử lý văn bản văn học,
dẫn đến sự mất cân bằng trong quá trình học. Hơn nữa, kích thước lớn của BART
(với 140 triệu tham số trong phiên bản base) tạo ra chi phí truyền thông đáng kể khi
cần đồng bộ hóa gradient giữa các client và server trong mỗi vòng huấn luyện.

41

2.2.4. Ưu điểm của BART trong học liên kết

Mặc dù tồn tại những thách thức, BART sở hữu nhiều đặc tính khiến nó trở thành

lựa chọn lý tưởng cho FL trong các tác vụ NLP. Những ưu điểm này không chỉ giải

quyết các vấn đề cốt lõi của FL mà còn mở ra khả năng ứng dụng rộng rãi trong thực
tế.

Khả năng fine-tuning hiệu quả với ít dữ liệu là một trong những điểm mạnh quan

trọng nhất của BART trong môi trường FL. Do được pre-train trên tập dữ liệu lớn với

cơ chế tự mã hóa khử nhiễu, BART đã học được các biểu diễn ngữ nghĩa phong phú,

cho phép mô hình thích ứng nhanh chóng với các tác vụ cụ thể chỉ với vài epoch fine-

tuning. Điều này đặc biệt có ý nghĩa trong FL, nơi mỗi client thường có lượng dữ liệu

hạn chế.

Kiến trúc seq2seq linh hoạt của BART mang lại lợi thế đáng kể khi triển khai

trên nhiều client với các tác vụ khác nhau. Khác với các mô hình chuyên biệt chỉ phù

hợp cho một loại nhiệm vụ, BART có thể được điều chỉnh để xử lý đồng thời cả tác

vụ hiểu ngôn ngữ thông qua bộ mã hóa và sinh văn bản thông qua bộ giải mã. Điều

này cho phép một mô hình BART duy nhất phục vụ nhiều clients với các nhu cầu

khác nhau, từ phân loại văn bản đến tóm tắt nội dung, giảm thiểu chi phí duy trì và

cập nhật mô hình.

Hơn nữa, khả năng học rất tốt của BART phù hợp với bản chất không đồng nhất

của FL. Khi các client có  miền dữ liệu khác nhau, các biểu diễn ngữ nghĩa chung

được học bởi bộ mã hóa có thể được chia sẻ và tái sử dụng hiệu quả. Ví dụ, kiến thức

về cấu trúc ngôn ngữ học được từ client xử lý văn bản tin tức có thể hỗ trợ client khác

trong việc xử lý văn bản y khoa, mặc dù nội dung khác biệt.

Tính modular của kiến trúc mã hóa – giải mã tạo ra cơ hội tối ưu hóa linh hoạt

trong FL. Tùy thuộc vào yêu cầu cụ thể của từng client, có thể chỉ fine-tune bộ mã

hóa cho các tác vụ phân loại văn bản, chỉ fine-tune bộ giải mã cho các tác vụ sinh văn
bản, hoặc fine-tune toàn bộ mô hình. Điều này không chỉ giảm chi phí tính toán mà
còn cho phép cá nhân hóa tốt hơn cho từng client trong khi vẫn duy trì khả năng tổng
quát hóa của mô hình toàn cầu.

Những ưu điểm này của BART tạo nên nền  tảng vững chắc cho việc áp dụng
trong FL, đồng thời cũng đặt ra yêu cầu về các thuật toán tối ưu hóa chuyên biệt. Việc
tận dụng tối đa tiềm năng của BART trong môi trường phân tán đòi hỏi các phương
pháp tối ưu hóa có thể xử lý hiệu quả tính không đồng nhất của dữ liệu và mô hình
lớn. Chính vì lý do này, thuật toán FedOPT được phát triển như một giải pháp chuyên

42

biệt để tối ưu hóa các mô hình transformer như BART trong FL, mà chúng ta sẽ tìm

hiểu chi tiết trong mục tiếp theo.

2.3. Thuật toán FedOPT

2.3.1. Giới thiệu về FedOPT

FL đã chứng minh được tiềm năng to lớn trong việc bảo vệ quyền riêng tư dữ liệu

người dùng bằng cách cho phép các thiết bị cá nhân huấn luyện mô hình mà không

cần chia sẻ dữ liệu gốc với máy chủ trung tâm. Tuy nhiên, khi áp dụng vào lĩnh vực
NLP, FL phải đối mặt với những thách thức đặc thù liên quan đến bản chất của dữ

liệu văn bản và độ phức tạp của các mô hình ngôn ngữ hiện đại [12].

Đặc biệt, các mô hình transformer như BART thường có kích thước tham số rất

lớn, dẫn đến hai vấn đề chính trong môi trường FL. Vấn đề đầu tiên là hiệu quả giao

tiếp, khi các client phải truyền tải các cập nhật mô hình có kích thước lớn đến máy

chủ trung tâm, gây ra chi phí giao tiếp cao và làm giảm hiệu quả tổng thể của quá

trình huấn luyện. Điều này đặc biệt nghiêm trọng đối với các mô hình NLP có thể

chứa hàng triệu hoặc thậm chí hàng tỷ tham số [2].

Vấn  đề  thứ  hai  liên  quan  đến  bảo  mật  thông  tin. Mặc  dù  dữ  liệu  văn  bản  gốc
không được chia sẻ trực tiếp, các gradient của mô hình vẫn có thể tiết lộ thông tin

nhạy cảm về nội dung văn bản. Trong bối cảnh NLP, điều này đặc biệt quan trọng vì

dữ liệu văn bản thường chứa thông tin cá nhân, ý kiến chính trị, hoặc các thông tin

nhạy cảm khác mà người dùng không muốn tiết lộ [2].

Để giải quyết những thách thức này, thuật toán FedOPT đã được phát triển như

một giải pháp tối ưu hóa toàn diện cho môi trường FL. FedOPT không chỉ tập trung

vào việc nâng cao hiệu quả giao tiếp thông qua thuật toán SCA (Sparse Compression

Algorithm), mà còn tích hợp các biện pháp bảo mật tiên tiến như mã hóa đồng cấu

cộng tính và bảo mật riêng tư vi sai.

2.3.2. Kỹ thuật nén trong SCA trong FedOPT

Trong FL, giảm thiểu chi phí giao tiếp là yếu tố quan trọng để tối ưu hóa quá trình
huấn luyện, đặc biệt khi phải truyền tải các mô hình có kích thước lớn. Một trong
những kỹ thuật quan trọng để giải quyết vấn đề này trong FedOpt là SCA.

SCA được thiết kế nhằm giảm thiểu số lượng bit cần truyền tải trong quá trình
huấn luyện mô hình, đồng thời đảm bảo độ chính xác của mô hình học. Để đạt được

43

điều này, SCA áp dụng kỹ thuật nén temporal sparsity. Kỹ thuật này giúp giảm độ trễ

giao tiếp trong mỗi vòng huấn luyện bằng cách cho phép mỗi client thực hiện nhiều

vòng lặp của thuật toán SGD (Stochastic Gradient Descent) để tính toán các cập nhật

mô hình có nhiều thông tin hơn [13].

Mã giả:
Thuật toán SCA:

Đầu vào: vector gradient ∆𝑣, tỷ lệ độ thưa 𝑞
Đầu ra: vector gradient sau khi nén ∆𝑣∗

Khởi tạo

1
2  𝑛𝑢𝑚+ ← 𝑡𝑜𝑝𝑞%(∆𝑣); 𝑛𝑢𝑚− ← 𝑡𝑜𝑝𝑞%(−∆𝑣)
3  𝛹+ ← 𝑚𝑒𝑎𝑛 (𝑛𝑢𝑚+); 𝛹− ← 𝑚𝑒𝑎𝑛(𝑛𝑢𝑚−)
4  𝑖𝑓 𝛹+ >   𝛹−
5
     𝑡ℎ𝑒𝑛
6  𝑟𝑒𝑡𝑢𝑟𝑛 (∆𝑣∗ ←   𝛹+(𝑣 ≥ min(𝑛𝑢𝑚+)))
7

     𝑒𝑙𝑠𝑒 𝑟𝑒𝑡𝑢𝑟𝑛 (∆𝑣  ←   𝛹−(𝑣 ≤ min (−𝑛𝑢𝑚−)))

8  𝑒𝑛𝑑

Cụ thể, SCA hoạt động như sau: Mỗi client sẽ tính toán các gradient sau 𝑛 vòng

lặp của SGD trên các tham số của mô hình trong dữ liệu cục bộ. Sau đó, thuật toán

SCA sẽ nén các gradient bằng cách loại bỏ các phần tử có giá trị nhỏ nhất và lớn nhất

trong các cập nhật gradient, giữ lại những giá trị quan trọng nhất. Công thức mô tả

quá trình này như sau:

∆𝑣 = 𝑆𝐺𝐷𝑛(𝑣, 𝐺𝑞) − 𝑣

(2.1)

Trong đó:
•  𝑆𝐺𝐷𝑛(𝑣, 𝐺𝑞) là bộ các cập nhật gradient sau 𝑛 vòng lặp của SGD trên tham

số mô hình 𝑣 với tập dữ liệu con 𝐺𝑞 của client 𝑞.

Một cách cụ thể hơn, SCA sử dụng kỹ thuật tính toán tỷ lệ giữa các gradient trong
tập dữ liệu để xác định các giá trị nhỏ và lớn, rồi thay thế chúng bằng các giá trị trung
bình. Cụ thể, nếu giá trị trung bình của các gradient âm lớn hơn giá trị trung bình của
các gradient dương, các giá trị dương sẽ được thay thế bằng giá trị trung bình dương
và các giá trị âm sẽ bị loại bỏ. Các bước cụ thể trong SCA được mô tả qua các công
thức sau:

•  Tìm các gradient lớn nhất và nhỏ nhất trong một phần của vector gradient:
𝑛𝑢𝑚+ ← 𝑡𝑜𝑝𝑞%(∆𝑣), 𝑛𝑢𝑚− ← 𝑡𝑜𝑝𝑞%(−∆𝑣)

(2.2)

44

•  Tính giá trị trung bình của các gradient dương và âm:

𝛹+   ← 𝑚𝑒𝑎𝑛(𝑛𝑢𝑚+), 𝛹− ← 𝑚𝑒𝑎𝑛(𝑛𝑢𝑚−)

(2.3)

•  So sánh giá trị trung bình của các gradient dương và âm và thay thế các giá trị

nhỏ hoặc lớn hơn bằng các giá trị trung bình tương ứng:
𝛹+   𝑖𝑓 𝛹+ ≥   𝛹−
𝛹−   𝑖𝑓 𝛹− >   𝛹+

∆𝑣∗ ← {

(2.4)

Phương pháp này giúp giảm kích thước của các gradient cần truyền tải mà không

ảnh hưởng nhiều đến độ chính xác của mô hình.

Kỹ thuật này không chỉ giúp giảm thiểu chi phí giao tiếp mà còn làm giảm độ trễ
trong quá trình huấn luyện, từ đó cải thiện hiệu quả tổng thể của mô hình trong các

ứng dụng FL. Các thử nghiệm cho thấy rằng việc sử dụng SCA có thể giảm đáng kể

lượng dữ liệu cần truyền tải, giúp tăng cường khả năng xử lý của hệ thống và giảm

chi phí tài nguyên trong môi trường huấn luyện phân tán [13].

SCA là một phần quan trọng trong FedOPT, giúp thuật toán này không chỉ cải

thiện hiệu quả giao tiếp mà còn tối ưu hóa việc bảo vệ quyền riêng tư và bảo mật

trong FL.

Tích hợp bảo mật trong FedOPT cho xử lý ngôn ngữ tự nhiên

2.3.3.
Bên cạnh việc tối ưu hóa giao tiếp, FedOPT còn đặc biệt chú trọng đến vấn đề

bảo mật trong bối cảnh NLP. Điều này đặc biệt quan trọng vì dữ liệu văn bản thường

chứa thông tin cá nhân nhạy cảm mà có thể bị suy luận từ các gradient của mô hình.

FedOPT  tích  hợp  mã  hóa  đồng  cấu  cộng  tính  (additively  homomorphic

encryption) để bảo vệ các gradient trong suốt quá trình truyền tải và tổng hợp. Phương
pháp này cho phép máy chủ trung tâm thực hiện các phép toán trên dữ liệu đã được

mã hóa mà không cần giải mã, đảm bảo rằng thông tin gradient của từng client được

bảo vệ ngay cả khỏi máy chủ trung tâm.

Đồng  thời, FedOPT  áp  dụng  kỹ  thuật  bảo  mật  riêng  tư  vi  sai  bằng  cách  thêm
nhiễu có kiểm soát vào các gradient trước khi truyền tải. Trong bối cảnh NLP, điều
này đặc biệt quan trọng vì giúp ngăn chặn các cuộc tấn công suy luận có thể khôi
phục lại nội dung văn bản gốc từ thông tin gradient.

2.3.4.  Kiến trúc triển khai FedOPT trong hệ thống học liên kết

45

Hình 4.Kiến trúc triển khai FedOPT trong hệ thống FL

Việc  triển  khai  FedOPT  trong  hệ  thống  FL  tuân  theo  một kiến  trúc  phân  tầng

được thiết kế để tối ưu hóa cả hiệu quả và bảo mật. Quá trình này bắt đầu từ việc huấn

luyện mô hình cục bộ tại các client, nơi mỗi thiết bị sử dụng dữ liệu văn bản cá nhân

để tinh chỉnh mô hình BART trên các tác vụ cụ thể như sinh văn bản hoặc phân loại

văn bản.

Các cập nhật mô hình sau đó được xử lý thông qua chuỗi máy chủ trung  gian

(Server Chain) nhằm phân tán tải và tăng cường bảo mật. Tại máy chủ FL chính, bộ

xử lý FedOPT và trình quản lý tài nguyên (resource manager) thực hiện tổng hợp các
cập nhật từ nhiều client. Quá trình này đặc biệt quan trọng đối với các mô hình NLP

vì cần đảm bảo rằng mô hình toàn cục có thể xử lý đa dạng các kiểu dữ liệu văn bản
từ các client khác nhau.

Sau khi tổng hợp và tối ưu hóa, mô hình toàn cục được phân phối trở lại các client
để tiếp tục quá trình huấn luyện lặp. Hệ thống cũng được hỗ trợ bởi các thành phần
quản lý tài nguyên thông minh, bao gồm trình giám sát tài nguyên (resource monitor)
để theo dõi việc sử dụng tài nguyên và trình quản lý dự đoán tài nguyên (Resource

46

Prediction Manager) để dự đoán nhu cầu tài nguyên dựa trên đặc điểm của dữ liệu

NLP.

2.4.

Quy trình ứng dụng học liên kết trong xử lý ngôn ngữ tự nhiên

Sau khi đã phân tích các thuật toán tối ưu hóa như FedOPT, việc hiểu rõ quy trình
tổng thể của FL trong NLP trở nên quan trọng để có thể áp dụng hiệu quả vào thực
tế. Như đã trình bày trong các chương trước, FL là một phương pháp học máy phi tập

trung cho phép huấn luyện mô hình dựa trên dữ liệu nằm tại các máy khách mà không
cần chia sẻ dữ liệu trực tiếp đến máy chủ trung tâm. Trong lĩnh vực NLP, phương

pháp này đặc biệt có ý nghĩa quan trọng do tính chất nhạy cảm của dữ liệu văn bản,

bao gồm hội thoại cá nhân, nhật ký y tế, email riêng tư hay các nội dung được nhập

từ bàn phím điện thoại thông minh.

Hình 5. Quy trình áp dụng FL trong NLP

Khởi tạo và thiết lập mô hình toàn cục
Quy trình ứng dụng FL trong NLP bắt đầu với việc thiết lập mô hình toàn cục tại
máy chủ trung tâm. Giai đoạn này đóng vai trò nền tảng cho toàn bộ quá trình huấn
luyện phân tán, trong đó máy chủ trung tâm khởi tạo một mô hình với các tham số
ngẫu nhiên hoặc được huấn luyện sơ bộ trên dữ liệu chung có sẵn công khai. Đối với
các bài toán NLP, việc lựa chọn kiến trúc mô hình phù hợp là yếu tố quyết định đến
hiệu quả của toàn bộ hệ thống.

47

Các mô hình transformer như BERT, DistilBERT, hoặc BART thường được ưu

tiên lựa chọn do tính hiệu quả cao trong nhiều nhiệm vụ NLP khác nhau [2]. Ví dụ,

trong bài toán phân loại văn bản, mô hình BERT có thể được khởi tạo với các tham

số đã được huấn luyện trước trên tập dữ liệu lớn như Wikipedia, sau đó được tinh
chỉnh cho các tác vụ cụ thể như phân loại cảm xúc hoặc phân loại chủ đề. Tương tự,
đối với bài toán sinh văn bản, mô hình BART với kiến trúc mã hóa – giải mã được

khởi tạo để thực hiện các tác vụ như tóm tắt văn bản, dịch máy, hoặc sinh câu hỏi tự
động.

Huấn luyện phân tán tại các client

Sau khi mô hình toàn cục được phân phối đến các client, giai đoạn huấn luyện

cục bộ được thực hiện độc lập tại mỗi thiết bị. Trong giai đoạn này, mỗi client sử
dụng tập dữ liệu cục bộ của riêng mình để tinh chỉnh mô hình thông qua thuật toán

giảm độ dốc ngẫu nhiên cục bộ. Quá trình này đặc biệt quan trọng vì nó cho phép mô

hình học được các đặc trưng đa dạng từ dữ liệu của từng client mà vẫn đảm bảo tính

bảo mật.

Để minh họa cụ thể, xét một kịch bản thực tế trong bài toán phân loại văn bản về

phân tích cảm xúc. Giả sử có một hệ thống gồm nhiều tổ chức khác nhau như ngân

hàng, công ty viễn thông và cửa hàng bán lẻ, mỗi tổ chức sở hữu dữ liệu phản hồi

khách hàng riêng biệt. Thay vì chia sẻ dữ liệu nhạy cảm này, mỗi tổ chức có thể huấn

luyện mô hình BERT trên dữ liệu cục bộ của mình để học các mẫu cảm xúc đặc trưng

của ngành nghề tương ứng. Ngân hàng có thể học về cảm xúc liên quan đến dịch vụ

tài chính, trong khi công ty viễn thông tập trung vào phản hồi về chất lượng mạng và

dịch vụ khách hàng.

Tương tự, trong bài toán sinh văn bản, các client có thể sở hữu các loại dữ liệu

văn bản khác nhau. Ví dụ, các tổ chức báo chí có thể có dữ liệu tin tức, các trường

đại học có dữ liệu nghiên cứu học thuật, và các công ty có dữ liệu báo cáo kinh doanh.

Mỗi client huấn luyện mô hình BART trên loại dữ liệu đặc thù của mình, giúp mô
hình học được các phong cách viết và đặc điểm ngôn ngữ đa dạng mà không cần chia
sẻ nội dung cụ thể.

Tổng hợp và tối ưu hóa mô hình
Giai đoạn tiếp theo trong quy trình là tổng hợp các cập nhật mô hình từ các client
tại máy chủ trung tâm. Đây là bước quan trọng nhất trong toàn bộ quá trình, nơi các
cập nhật tham số từ các client được kết hợp để tạo ra một mô hình toàn cục cải thiện.

48

Máy chủ trung tâm thực hiện quá trình này thông qua các thuật toán tối ưu hóa đặc

trưng của FL như FedAvg, FedProx hoặc FedOPT.

Trong số các thuật toán này, FedOPT được đánh giá cao đặc biệt trong bối cảnh

NLP nhờ khả năng xử lý hiệu quả dữ liệu không đồng nhất và giảm chi phí truyền
thông thông qua kỹ thuật SCA. Điều này đặc biệt quan trọng đối với các mô hình
NLP có kích thước lớn như BART, nơi việc truyền tải toàn bộ tham số có thể gây ra

chi phí băng thông đáng kể.

Quá trình tổng hợp trọng số toàn cục 𝑊𝐺 từ các client thường được tính theo công

thức cơ bản của FedAvg:

𝑊𝐺 =

1
𝑁

𝑁
∑ 𝑊𝑘
𝑘=1

(2.5)

trong đó 𝑊𝑘  là các trọng số từ client thứ 𝑘, và 𝑁 là tổng số client tham gia.
Tuy nhiên, trong thực tế, công thức này thường được điều chỉnh để phản ánh tầm
quan trọng khác nhau của các client dựa trên kích thước dữ liệu hoặc chất lượng cập

nhật. Đối với các bài toán NLP phức tạp, việc tổng hợp cần xem xét đến tính đa dạng

của dữ liệu văn bản và đặc thù của từng client.

Cập nhật và phân phối mô hình toàn cục

Sau khi hoàn tất quá trình tổng hợp, mô hình toàn cục được cập nhật và phân phối

trở lại các client để tiếp tục vòng huấn luyện tiếp theo. Giai đoạn này đảm bảo rằng

kiến thức học được từ toàn bộ hệ thống được chia sẻ một cách hiệu quả, giúp mỗi

client hưởng lợi từ việc học của những client khác mà không cần tiếp cận trực tiếp dữ

liệu của họ.

Quá trình lặp này tiếp tục cho đến khi đạt được điều kiện dừng, có thể là độ chính

xác mong muốn, số vòng lặp tối đa, hoặc mức độ hội tụ của mô hình. Trong bối cảnh

NLP, việc xác định điều kiện dừng thường phụ thuộc vào tác vụ cụ thể và yêu cầu về

chất lượng mô hình.

Đánh giá và kiểm soát chất lượng
Trong suốt quá trình FL, việc đánh giá hiệu suất mô hình được thực hiện định kỳ
để đảm bảo chất lượng và điều chỉnh các tham số huấn luyện khi cần thiết. Đối với
bài toán phân loại văn bản, các chỉ số đánh giá như accuracy, precision, recall và F1-
score được sử dụng để đánh giá trên tập dữ liệu kiểm tra. Trong khi đó, bài toán sinh
văn  bản  thường  được  đánh  giá  thông  qua  các  chỉ  số  như  BLEU,  ROUGE  hoặc
BERTScore để đo lường chất lượng của văn bản được sinh ra.

49

Một khía cạnh quan trọng trong đánh giá là việc kiểm soát hiện tượng overfitting

cục bộ, khi một client có dữ liệu không đại diện có thể ảnh hưởng tiêu cực đến mô

hình  toàn  cục.  Để  giải  quyết  vấn  đề  này,  các  kỹ  thuật  như  regularization  và  early

stopping thường được áp dụng trong quá trình huấn luyện cục bộ.

Tính hiệu quả và ứng dụng thực tiễn
Tổng thể, quy trình ứng dụng FL trong NLP cho phép khai thác sức mạnh của

các mô hình NLP hiện đại trên dữ liệu phân tán, đồng thời giải quyết hiệu quả các
thách thức về bảo mật và riêng tư dữ liệu. Điều này đặc biệt có ý nghĩa trong bối cảnh

hiện tại khi các quy định về bảo vệ dữ liệu cá nhân ngày càng nghiêm ngặt, và nhu

cầu phát triển các hệ thống AI đáng tin cậy ngày càng tăng cao.

Thông qua việc kết hợp các kỹ thuật tối ưu hóa như FedOPT với quy trình huấn
luyện phân tán, các tổ chức có thể xây dựng những mô hình NLP mạnh mẽ và chính

xác mà không cần phải hy sinh tính bảo mật và riêng tư của dữ liệu. Điều này mở ra

nhiều cơ hội ứng dụng mới trong các lĩnh vực nhạy cảm như y tế, tài chính, và giáo

dục, nơi mà việc chia  sẻ dữ liệu trực tiếp thường không khả thi hoặc không được

phép.

2.5.

Tổng kết chương 2

Chương đã trình bày về việc ứng dụng FL vào một số bài toán NLP cụ thể. Hai

bài toán quan trọng được lựa chọn làm minh họa là sinh văn bản và phân loại văn

bản. Đây là những bài toán phổ biến trong lĩnh vực NLP, thường yêu cầu một lượng

lớn dữ liệu huấn luyện, đồng thời đặt ra các thách thức về bảo mật và quyền riêng tư

dữ liệu.

Để giải quyết các bài toán này, mô hình BART là một kiến trúc Transformer nổi
bật. Nhờ kiến trúc này, BART có khả năng học hiệu quả các đặc trưng ngôn ngữ, đặc

biệt phù hợp cho các nhiệm vụ sinh văn bản và phân loại văn bản trong môi trường

FL.

Tiếp theo, thuật toán FedOPT là một thuật toán FL được thiết kế nhằm cải thiện
hiệu quả huấn luyện trong môi trường phân tán. FedOPT giải quyết hai vấn đề cốt lõi
trong FL là hiệu quả giao tiếp và bảo mật dữ liệu. Trong đó, kỹ thuật SCA được áp
dụng nhằm nén gradient, giảm đáng kể lượng dữ liệu cần truyền tải trong quá trình
huấn luyện.

Cuối cùng là quy trình ứng dụng FL trong NLP, từ giai đoạn khởi tạo mô hình,
huấn luyện cục bộ, tổng hợp mô hình trung tâm, đến việc phân phối lại mô hình toàn
cục cho các client. Quy trình này không chỉ đảm bảo hiệu quả trong việc xây dựng

50

các mô hình NLP phân tán mà còn giúp bảo vệ quyền riêng tư người dùng, tạo nền

tảng vững chắc cho các ứng dụng NLP trong thực tiễn.

51

Chương 3: Thực nghiệm

Trong  chương  này,  chúng  tôi  sẽ  cài  đặt  thực  nghiệm  các  nội  dung  đã  nêu  ở

chương 2, bao gồm: trực quan các tập dữ liệu sử dụng trong thực nghiệm nhằm tìm
ra các tham số tối ưu, cài đặt thực nghiệm cho bài toán phân loại văn bản trên tập dữ

liệu AgNews và 20News; bài toán sinh văn bản trên tập dữ liệu CNN/Dailymail. Cài

đặt thực nghiệm với Bart-base và thuật toán FedOPT. Đánh giá kết quả, so sánh học

máy phi tập trung và học máy tập trung, so sánh kết quả với các số lượng client khác

nhau.

3.1. Dữ liệu

3.1.1. AgNews

AG News là một tập dữ liệu phân loại văn bản gồm bốn danh mục: World, Sports,

Business và Sci/Tech, với tổng cộng 31.900 mẫu.

Hình 6. Trực quan dữ liệu - AgNews

Biểu đồ phân phối nhãn cho thấy số lượng mẫu giữa các danh mục và giữa hai

tập Train–Test được phân chia đồng đều, mỗi lớp có 7.500 mẫu huấn luyện và 475

52

mẫu kiểm tra. Tỷ lệ train:test đạt khoảng 94:6, giúp đảm bảo mô hình không bị thiên

lệch.

Biểu đồ phân phối độ dài văn bản theo từng danh mục chỉ ra rằng phần lớn các

văn bản nằm trong khoảng 15–20 từ. Danh mục World có xu hướng dài hơn một chút,
trong khi Sci/Tech có độ dài tập trung cao nhất. Điều này được thể hiện rõ hơn qua
biểu đồ boxplot, cho thấy các danh mục có trung vị tương đương, dao động quanh

mức 17–18 từ, với độ biến thiên thấp.

Bảng thống kê tổng quan xác nhận độ dài trung bình văn bản là 17.5 từ, độ lệch

chuẩn 3.3, với độ dài dao động từ 11 đến 21 từ. Những đặc điểm này phản ánh sự

chuẩn hóa tốt của dữ liệu, thuận lợi cho việc huấn luyện mô hình và áp dụng trong

môi trường học phân tán như FL.

3.1.2.

20News

Tập dữ liệu 20 Newsgroups là một trong những tập dữ liệu văn bản phổ biến nhất

trong lĩnh vực NLP, đặc biệt hữu ích cho các nghiên cứu phân loại văn bản trong môi

trường phi tập trung như FL. Với gần 19.000 văn bản được chia đều cho 20 chủ đề,

dữ liệu phản ánh tính đa dạng và không đồng nhất của các nguồn thông tin thực tế.

Hình 7. Trực quan dữ liệu - 20News

53

Biểu đồ phân phối 10 danh mục phổ biến nhất cho thấy sự phân bổ tương đối

đồng đều giữa hai tập train và test. Các chủ đề như Hardware, Hockey, Religion và

Motorcycles có số lượng văn bản cao, dao động từ khoảng 390 đến hơn 1.100 mẫu,

phản ánh mức độ quan tâm phổ biến trong cộng đồng người dùng Usenet. Đáng chú
ý, tỷ lệ train:test được duy trì ổn định, đảm  bảo tính cân bằng cho quá trình huấn
luyện và đánh giá mô hình.

Xét về độ dài văn bản, biểu đồ histogram cho thấy phân phối rõ rệt theo dạng lệch
phải. Phần lớn văn bản tập trung trong khoảng 0–500 từ, và chỉ một số ít vượt quá

2.000 từ, với giá trị cực đại lên đến hơn 11.000 từ. Mật độ phân phối cao nhất nằm ở

khoảng 100–300 từ, cho thấy phần lớn văn bản có độ dài vừa phải, phù hợp với các

mô hình học máy hiện đại. Phân tích theo chủ đề cũng cho thấy các danh mục như
Hardware và Hockey thường có các văn bản ngắn, trong khi một số văn bản thuộc

các danh mục khác lại có độ dài đáng kể.

Biểu đồ boxplot cung cấp cái nhìn trực quan về sự phân tán độ dài văn bản trong

các chủ đề tiêu biểu. Hardware có xu hướng có độ dài trung vị thấp, phản ánh các văn

bản ngắn gọn và tập trung. Ngược lại, các chủ đề như Religion và Motorcycles có

phân phối độ dài rộng hơn, với nhiều outliers cho thấy sự đa dạng nội dung. Điều này

làm nổi bật đặc điểm không đồng nhất của dữ liệu – một yếu tố quan trọng cần xem

xét khi áp dụng trong môi trường FL.

Cuối cùng, bảng thống kê tổng quan xác nhận tổng cộng 18.846 văn bản, với độ

dài trung bình khoảng 186 từ và độ lệch chuẩn khá lớn (524), minh chứng cho sự biến

thiên mạnh về kích thước văn bản giữa các danh mục. Sự không đồng đều này là một

thách thức đồng thời cũng là điều kiện lý tưởng để đánh giá độ linh hoạt và khả năng
tổng quát hóa của các mô hình học phân tán.

3.1.3.  CNN/Dailymail

Bộ dữ liệu CNN/DailyMail bao gồm 311,971 mẫu được chia thành tập huấn luyện

(287,113  mẫu), validation (13,368  mẫu)  và  test  (11,490  mẫu).  Phân  chia  này  tuân
theo tỷ lệ chuẩn với tập huấn luyện chiếm khoảng 92% tổng dữ liệu.

54

Hình 8. Trực quan dữ liệu - CNN/Dailymail

Phân tích cho thấy bài viết gốc có độ dài trung bình 691.9 từ (độ lệch chuẩn 51.6

từ), trong khi tóm tắt chỉ có 51.6 từ trung bình, tạo ra tỷ lệ nén 14.8:1. Phân phối độ

dài bài viết tương đối đồng nhất với phần lớn mẫu tập trung quanh giá trị trung bình,

trong khi tóm tắt có phân phối lệch phải với đa số mẫu có độ dài ngắn.

Biểu đồ phân tán thể hiện mối tương quan tích cực giữa độ dài bài viết và tóm

tắt, với mật độ cao nhất tập trung ở vùng 600-700 từ cho bài viết và 40-60 từ cho tóm

tắt. Điều này phản ánh đặc tính ổn định của tỷ lệ nén trong dữ liệu tin tức.

Sự đồng nhất trong phân phối dữ liệu và tỷ lệ nén ổn định tạo điều kiện thuận lợi
cho việc áp dụng FL. Đặc tính cân bằng của bộ dữ liệu giúp đảm bảo hiệu quả phân
phối học tập giữa các client và duy trì chất lượng mô hình toàn cục trong quá trình
FL.

55

3.2.

Cài đặt thực nghiệm

Hình 9. Quy trình cài đặt thực nghiệm

Thực nghiệm được thiết kế để so sánh hiệu quả giữa hai phương pháp huấn luyện:

phương  pháp  tập  trung  truyền  thống  và  phương  pháp  học  liên  kết  (Federated

Learning). Nghiên cứu sử dụng mô hình BART-base làm nền tảng cho cả hai bài toán

phân loại văn bản và sinh văn bản tóm tắt, nhằm đánh giá khả năng ứng dụng của học

liên kết trong các tác vụ xử lý ngôn ngữ tự nhiên khác nhau.

Kiến trúc thực nghiệm bao gồm một máy chủ trung tâm kết nối với nhiều client

khác nhau, mô phỏng môi trường phân tán thực tế. Trong phương pháp học liên kết,

mỗi client thực hiện huấn luyện cục bộ trên dữ liệu riêng của mình, sau đó gửi các

tham số mô hình về máy chủ để tổng hợp. Ngược lại, phương pháp tập trung thực

hiện huấn luyện toàn bộ dữ liệu tại một vị trí duy nhất.

Để đảm bảo sự so sánh công bằng giữa hai phương pháp, số epoch của huấn luyện

tập trung được điều chỉnh để tương đương với tổng số epoch thực hiện trong học liên
kết. Công thức tính số epoch cho huấn luyện tập trung như sau:

𝐶𝑒𝑛𝑡𝑟𝑎𝑙𝑖𝑧𝑒𝑑 𝑒𝑝𝑜𝑐ℎ𝑠

= [

(𝑛𝑢𝑚𝑐𝑙𝑖𝑒𝑛𝑡 ∗ 𝑔𝑙𝑜𝑏𝑎𝑙 𝑟𝑜𝑢𝑛𝑑 ∗ 𝑙𝑜𝑐𝑎𝑙 𝑒𝑝𝑜𝑐ℎ ∗ 𝑎𝑣𝑔 𝑐𝑙𝑖𝑒𝑛𝑡 𝑏𝑎𝑡𝑐ℎ)
𝑐𝑒𝑛𝑡𝑟𝑎𝑙𝑖𝑧𝑒𝑑 𝑏𝑎𝑡𝑐ℎ

]

Với:
•  𝑛𝑢𝑚𝑐𝑙𝑖𝑒𝑛𝑡: số lượng clients
•  𝑔𝑙𝑜𝑏𝑎𝑙 𝑟𝑜𝑢𝑛𝑑: số vòng huấn luyện của FL.

56

•  𝑙𝑜𝑐𝑎𝑙 𝑒𝑝𝑜𝑐ℎ: số vòng huấn luyện local trên mỗi client

•  𝑎𝑣𝑔 𝑐𝑙𝑖𝑒𝑛𝑡 𝑏𝑎𝑡𝑐ℎ: số batch trung bình trên mỗi client

•  𝑐𝑒𝑛𝑡𝑟𝑎𝑙𝑖𝑧𝑒𝑑 𝑏𝑎𝑡𝑐ℎ: số batch trong huấn luyện tập trung

Công thức này đảm bảo rằng cả hai phương pháp đều nhận được lượng cập nhật

tham số tương đương nhau, tạo nền tảng cho việc so sánh khách quan về hiệu suất.

Cấu hình tham số thực nghiệm:

Thực nghiệm được thực hiện với các tham số cụ thể nhằm mô phỏng môi trường

thực tế của học liên kết. Số lượng client được thiết lập là 4, đại diện cho một mạng

lưới nhỏ nhưng đủ để thể hiện tính phân tán của dữ liệu. Mô hình BART-base được
lựa chọn do khả năng xử lý hiệu quả cả hai tác vụ phân loại và sinh văn bản.

Quá trình huấn luyện được cấu hình với 15 vòng huấn luyện toàn cục, mỗi client

thực hiện 4  epoch  huấn luyện cục bộ  trong  mỗi vòng. Đặc  biệt, tham số Dirichlet

Alpha được đặt ở mức 0.3 để mô phỏng sự phân tán không đồng nhất của dữ liệu giữa
các client. Giá trị alpha thấp này phản ánh tình huống thực tế trong học liên kết, nơi

mỗi client thường sở hữu dữ liệu có đặc điểm riêng biệt và không được phân phối

đồng đều như trong môi trường lý tưởng.

So sánh theo số lượng client khác nhau:

Để  đánh  giá  tác  động  của  quy  mô  mạng  lưới  đến  hiệu  suất  học  liên  kết,  thực

nghiệm được mở rộng với các cấu hình số lượng client khác nhau.

Với mỗi cấu hình số lượng client, các tham số khác được giữ cố định để đảm bảo

tính nhất quán trong so sánh. Cụ thể, số vòng huấn luyện toàn cục vẫn là 15, số epoch

cục bộ là 4, và hệ số Dirichlet Alpha duy trì ở mức 0.3. Việc giữ nguyên các tham số

này cho phép tách biệt và đo lường chính xác ảnh hưởng của số lượng client đến chất

lượng mô hình.

Khi số lượng client tăng lên, dữ liệu được phân chia thành nhiều phần nhỏ hơn,

dẫn đến tình trạng mỗi client sở hữu ít dữ liệu huấn luyện hơn. Điều này tạo ra thách
thức về khả năng học của từng client cục bộ, đồng thời cũng gia tăng độ đa dạng trong
quá trình tổng hợp mô hình toàn cục. Mặt khác, số lượng client nhiều hơn có thể mang
lại lợi ích về tính tổng quát của mô hình nhờ sự đóng góp từ nhiều nguồn dữ liệu khác
biệt.

Thông qua việc so sánh hiệu suất trên các quy mô mạng lưới khác nhau, nghiên
cứu sẽ xác định được ngưỡng tối ưu về số lượng client cho từng loại bài toán, từ đó
đưa ra khuyến nghị về cấu hình hệ thống học liên kết phù hợp với các ứng dụng thực

tế.

57

Thiết kế thực nghiệm này cho phép đánh giá toàn diện khả năng của học liên kết

trong việc xử lý dữ liệu phân tán không đồng nhất, đồng thời cung cấp cơ sở so sánh

công bằng với phương pháp huấn luyện tập trung truyền thống và hiểu biết sâu sắc

về tác động của quy mô mạng lưới đến hiệu suất hệ thống.

3.3.

Đánh giá

3.3.2.
Phân loại văn bản
Phân tích mức độ phân tán dữ liệu:

Hình 10. Biểu đồ phân tán dữ liệu 20News trên các client

Ma trận thể hiện phân phối các lớp dữ liệu trên 4 client cho thấy tính không đồng

nhất (non-IID) rõ rệt trong bộ dữ liệu 20Newsgroups. Từ 20 nhóm tin tức ban đầu,

mỗi client chỉ chứa một tập con giới hạn các lớp với tỷ lệ phân phối không cân bằng.

Client  0  tập  trung  chủ  yếu  vào  các  chủ  đề  máy  tính  và  thương  mại  với
comp.graphics  (0.16),  misc.forsale  (0.18),  và  rec.crypt  (0.19)  chiếm  tỷ  trọng  cao.
Client  1  có  sự  phân  bố  đa  dạng  hơn  với  comp.os.ms  (0.22)  chiếm  ưu  thế  cùng
talk.politics.guns (0.14). Client 2 thể hiện sự tập trung vào khoa học và kỹ thuật với
sci.med (0.17) và alt.religion (0.13), trong khi Client 3 có phân phối cân bằng giữa
comp.windows.x (0.21) và rec.sport.hockey (0.21).

Sự phân phối không đồng nhất này tạo ra những thách thức đặc trưng cho môi
trường FL thực tế. Mỗi client đại diện cho một miền dữ liệu riêng biệt với đặc tính

58

chủ đề khác nhau: Client 0 tập trung vào công nghệ và thương mại, Client 1 nghiêng

về chính trị, Client 2 hướng khoa học, và Client 3 kết hợp công nghệ với thể thao.

Đặc biệt, việc một số lớp chỉ xuất hiện trên client cụ thể (như comp.op.ms chủ

yếu ở Client 1 với 0.22 hoặc rec.sport.hockey tập trung ở Client 3 với 0.21 nhưng
không xuất hiện trong các clients khác) tạo ra hiện tượng không đồng nhất. Sự chênh
lệch này có thể dẫn đến vấn đề lệch hướng, nơi mô hình local của mỗi client có xu

hướng tối ưu hóa riêng cho phân phối dữ liệu của mình, gây khó khăn cho việc học
global model hiệu quả.

Hình 11. Biểu đồ phân bố dữ liệu AgNews trên các client

Ma trận cho thấy bộ dữ liệu AG News được phân chia trên 4 client với mức độ

không đồng nhất cao. Bộ dữ liệu gồm 4 lớp chính được phân phối không cân bằng

giữa các client, tạo ra môi trường non-IID điển hình.

Client 0 tập trung chủ yếu vào tin tức thể thao với 19,261 mẫu (0.7603), chiếm
tỷ trọng áp đảo, trong khi chỉ có 5,986 mẫu tin tức thế giới (0.2363). Client 1 có phân
phối ngược lại với 13,892 mẫu tin tức thế giới (0.5476) và 11,229 mẫu tin kinh doanh
(0.4426), hoàn toàn không có dữ liệu thể thao. Client 2 thể hiện sự cân bằng tương
đối giữa các lớp với 26,257 mẫu khoa học công nghệ (0.6195), 7,703 mẫu thể thao
(0.1818) và 7,005 mẫu tin tức thế giới (0.1653).

Đặc biệt, Client 3 tập trung gần như hoàn toàn vào lĩnh vực kinh doanh với 14,381
mẫu  (0.9641),  chỉ  có  số  lượng nhỏ  các  lớp khác.  Sự  phân  chia  này  phản  ánh  tình

59

huống thực tế khi các tổ chức báo chí khác nhau có xu hướng chuyên biệt hóa theo

từng lĩnh vực cụ thể.

Phân phối dữ liệu cho thấy mức độ bất cân xứng nghiêm trọng giữa các client,

đặc biệt ở Client 1 hoàn toàn thiếu dữ liệu thể thao và Client 3 gần như độc quyền về
tin kinh doanh. Điều này tạo ra thách thức statistical heterogeneity mạnh mẽ, trong
đó mỗi client có distribution riêng biệt và không chồng lấp.

Sự chênh lệch về kích thước dữ liệu giữa các client cũng đáng chú ý, từ Client 0
với khoảng 26,000 mẫu đến Client 2 với hơn 42,000 mẫu. Điều này không chỉ gây ra

vấn đề về tính đại diện trong quá trình tổng hợp mà còn có thể dẫn đến hiện tượng

overfitting trên các client có ít dữ liệu.

Ý nghĩa cho FL:
Từ những ví dụ trên, có thể thấy rằng phân phối dữ liệu này đòi hỏi việc áp dụng

các kỹ thuật FL tiên tiến để xử lý tính không đồng nhất. Thuật toán FedOPT hoặc các

thuật toán tói ưu sẽ cần thiết để đảm bảo hội tụ ổn định và hiệu suất tốt trên toàn bộ

hệ thống.

Hơn nữa, việc đánh giá hiệu suất mô hình cần xem xét cả hiệu năng của mô hình

toàn cục và cục bộ để đảm bảo công bằng giữa các client. Sự phân phối không cân

bằng này cũng yêu cầu thiết kế chiến lược tổng hợp phù hợp để tránh thiên vị đối với

các client có dữ liệu nhiều hơn.

Kết quả thực nghiệm phân loại văn bản:

Hình 12. Accurary trên tập dữ liệu 20News

60

Hình 13. F1-score trên tập dữ liệu 20News

Dựa trên hai biểu đồ so sánh hiệu suất với chất lượng rõ nét hơn, có thể rút ra

những nhận định chính xác và sâu sắc hơn về hiệu quả của FL trong bài toán phân

loại văn bản trên tập dữ liệu 20News.

Xét về độ chính xác (Accuracy), một điểm đáng chú ý là FL thể hiện tốc độ hội

tụ nhanh chóng và ấn tượng ngay từ những vòng đầu tiên. Cụ thể, FL khởi đầu từ

mức 0.05 và tăng trưởng mạnh mẽ, đạt khoảng 0.46 tại vòng thứ nhất, sau đó tiếp tục

tăng  lên  0.62  tại  vòng  thứ  hai.  Ngược lại,  phương pháp  học  máy  tập  trung  truyền

thống cho thấy sự khởi đầu chậm chạp hơn đáng kể, duy trì ở mức thấp trong hai

vòng đầu tiên trước khi bùng nổ với tốc độ tăng trưởng mạnh mẽ từ vòng thứ ba trở

đi. Điều thú vị là sau vòng thứ năm, cả hai phương pháp đều hội tụ về cùng một mức

hiệu suất, đạt khoảng 0.7 và duy trì ổn định.

Đối với chỉ số F1-Score, xu hướng tương tự được thể hiện một cách rõ ràng hơn.
FL khởi đầu từ mức thấp khoảng 0.17 nhưng nhanh chóng tăng lên 0.39 tại vòng đầu

tiên và đạt 0.61 tại vòng thứ hai. Trong khi đó, học máy tập trung trải qua một giai
đoạn bất thường với sự tăng nhẹ đến 0.29 tại vòng đầu tiên, sau đó giảm xuống 0.14
tại vòng thứ hai trước khi phục hồi mạnh mẽ. Hiện tượng dao động này của học máy
tập trung truyền thống có thể được giải thích bởi tính chất của thuật toán tối ưu hóa
hoặc chiến lược khởi tạo tham số.

61

Từ góc độ phân tích sâu hơn, ưu thế rõ rệt của FL trong giai đoạn đầu có thể được

lý giải thông qua đặc tính của thuật toán FL. Việc tổng hợp gradient từ nhiều client

khác nhau có thể tạo ra hiệu ứng regularization tự nhiên, giúp mô hình tránh được

overfitting  ban đầu  và  đạt được hiệu  suất tốt  hơn trong những vòng đầu tiên.  Mặt
khác, sự chậm trễ của học máy tập trung truyền thống có thể phản ánh thời gian cần
thiết để mô hình thích nghi với toàn bộ phân bố dữ liệu phức tạp.

Hơn nữa, sự hội tụ cuối cùng của cả hai phương pháp về cùng một mức hiệu suất
cao (khoảng 0.7 cho cả Accuracy và F1-Score) là một kết quả có ý nghĩa quan trọng.

Điều này không chỉ chứng minh tính hiệu quả của FL mà còn cho thấy khả năng duy

trì chất lượng mô hình mà không cần tập trung hóa dữ liệu. Đặc biệt, trong một số

giai đoạn cuối, FL thậm chí còn thể hiện hiệu suất cao hơn một cách nhỏ so với học
máy tập trung, gợi ý về tiềm năng vượt trội của phương pháp này trong điều kiện cụ

thể.

Kết quả này có những hàm ý thực tiễn quan trọng đối với ứng dụng  FL trong

NLP. Tốc độ hội tụ nhanh của FL không chỉ giúp tiết kiệm thời gian huấn luyện mà

còn giảm thiểu chi phí truyền thông giữa các client và server. Đồng thời, khả năng

đạt được hiệu suất tương đương hoặc thậm chí vượt trội so với phương pháp tập trung

hóa mở ra những triển vọng to lớn cho việc ứng dụng FL trong các bài toán thực tế,

đặc biệt trong bối cảnh bảo mật dữ liệu và quyền riêng tư ngày càng được chú trọng.

Hình 14. Accurary trên tập dữ liệu AgNews

62

Hình 15. F1-score trên tập dữ liệu 20News

Dựa trên kết quả thực nghiệm trên tập dữ liệu AG News, có thể quan sát thấy

những đặc điểm hiệu suất khác biệt đáng kể so với tập dữ liệu 20News, phản ánh sự

phức tạp và đa dạng trong ứng dụng FL cho các tác vụ NLP khác nhau.

Xét về độ chính xác, cả hai phương pháp đều thể hiện sự hội tụ nhanh chóng và

đồng bộ trong giai đoạn đầu. Cụ thể, từ điểm khởi đầu khoảng 0.22, cả  FL và học

máy tập trung truyền thống đều tăng trưởng mạnh mẽ và đạt mức cao khoảng 0.9 chỉ

sau vòng đầu tiên. Điều đáng chú ý là không giống như trên tập dữ liệu 20News, ở

đây không tồn tại sự chênh lệch đáng kể về tốc độ hội tụ giữa hai phương pháp. Thay

vào đó, cả hai đều duy trì hiệu suất ổn định và tương đương nhau trong suốt quá trình

huấn luyện.

Tuy nhiên, một khía cạnh thú vị được thể hiện trong giai đoạn sau vòng thứ 3 là

sự  xuất  hiện  của  xu  hướng khác  biệt  nhẹ.  Phương pháp  học  máy  tập  trung  truyền
thống cho thấy dấu hiệu suy giảm hiệu suất từ đỉnh cao khoảng 0.95 xuống mức 0.93-

0.92 trong các vòng cuối, trong khi FL duy trì được sự ổn định tốt hơn với mức độ
chính xác dao động quanh 0.91-0.92. Hiện tượng này có thể được giải thích thông
qua góc độ overfitting, nơi mà phương pháp tập trung hóa có thể gặp phải vấn đề
thích nghi quá mức với dữ liệu huấn luyện.

Đối với chỉ số F1-Score, xu hướng tương tự được thể hiện một cách rõ ràng hơn.
Sự hội tụ nhanh chóng của cả hai phương pháp trong giai đoạn đầu cho thấy tính chất

63

phù hợp của AG News với các thuật toán học máy. Đặc biệt, việc đạt được F1-Score

cao khoảng 0.9 ngay từ vòng đầu tiên phản ánh độ phức tạp tương đối thấp hơn của

tập dữ liệu này so với 20News. Tương tự như với độ chính xác, học máy tập trung

truyền thống thể hiện sự suy giảm nhẹ trong giai đoạn sau, trong khi FL duy trì được
sự ổn định tốt hơn.

Từ góc độ so sánh với kết quả trên 20News, sự khác biệt rõ rệt trong mô hình

hiệu suất cho thấy tầm quan trọng của đặc tính dữ liệu đối với hiệu quả của FL. AG
News, với tính chất phân loại tin tức đơn giản hơn và ít phân mảnh chủ đề hơn, tạo

điều kiện thuận lợi cho cả hai phương pháp đạt được hiệu suất cao ngay từ đầu. Điều

này trái ngược với 20News, nơi sự phức tạp và đa dạng chủ đề đòi hỏi thời gian hội

tụ dài hơn.

Hơn nữa, sự ổn định vượt trội của FL trong giai đoạn cuối có ý nghĩa quan trọng

đối với ứng dụng thực tế. Khả năng tránh được overfitting thông qua cơ chế tổng hợp

gradient từ nhiều client khác nhau không chỉ giúp duy trì hiệu suất mà còn tăng cường

tính robust của mô hình. Điều này đặc biệt có giá trị trong bối cảnh triển khai thực tế,

nơi mà tính ổn định lâu dài của mô hình thường quan trọng hơn việc đạt được hiệu

suất đỉnh cao tức thời.

Kết quả này cũng nhấn mạnh tiềm năng của FL trong việc xử lý các tác vụ phân

loại văn bản có độ phức tạp trung bình. Việc FL không chỉ đạt được hiệu suất tương

đương mà còn thể hiện tính ổn định tốt hơn so với phương pháp tập trung hóa mở ra

những triển vọng tích cực cho việc ứng dụng rộng rãi trong các hệ thống thực tế, đặc

biệt khi xem xét đến các yêu cầu về bảo mật dữ liệu và tính phân tán của môi trường

ứng dụng hiện đại.

64

3.3.3.

Sinh văn bản

Hình 16. Kết quả thực nghiệm sinh văn bản

Biểu đồ phân bố mẫu thể hiện sự không cân bằng rõ rệt với Client 3 chiếm ưu thế

(130,000 mẫu), Client 1 có 95,000 mẫu, Client 0 có 45,000 mẫu và Client 4 chỉ có

10,000 mẫu. Sự phân bố non-IID này tạo ra thách thức cốt lõi trong FL. Sự không

cân bằng dữ liệu khiến Client 3 chi phối quá trình cập nhật tham số toàn cục, trong

khi Client 4 đóng góp hạn chế. Điều này tạo thách thức về không công bằng trong

FL. Sự khác biệt về độ dài bài báo cũng tạo yêu cầu mâu thuẫn cho mô hình toàn cục

khi xử lý các loại văn bản khác nhau.  Đồng thời, độ dài trung bình bài báo dao động

từ 620 từ (Client 0) đến 740 từ (Client 4), phản ánh sự đa dạng về nguồn dữ liệu và
tạo ra những gradient có đặc tính khác biệt.

Training loss giảm dần từ 0.52 xuống 0.30 qua 5 vòng, với một điểm bất thường
tại vòng 3 (tăng lên 0.38). Hiện tượng dao động này phản ánh tính chất stochastic của
FL khi tổng hợp gradient từ các client khác nhau.

Phân tích hiệu suất mô hình qua các vòng giao tiếp:
ROUGE-1 thể hiện sự ổn định, giảm nhẹ từ 0.382 xuống 0.362 (5.2%), cho thấy

khả năng duy trì độ bao phủ từ vựng. Ngược lại, ROUGE-L cải thiện tích cực từ 0.235

lên 0.249 (6%), phản ánh khả năng tạo ra tóm tắt có cấu trúc tốt hơn. ROUGE-2 duy

65

trì ổn định (0.152-0.158), chứng tỏ mô hình bảo tồn khả năng nắm bắt mối quan hệ

ngữ nghĩa. BLEU giảm nhẹ từ 0.072 xuống 0.067 nhưng vẫn ở mức ổn định.

So sánh với học tập trung truyền thống:

Các nghiên cứu trước về BART với học tập trung truyền thống đạt ROUGE-1
khoảng 0.44-0.45 trên CNN/DailyMail. Kết quả FL (0.362-0.382) thấp hơn 15-18%
nhưng vẫn chấp nhận được khi xét đến lợi ích bảo mật. Đáng chú ý, FL đạt ổn định

chỉ sau 6 vòng so với rất nhiều vòng của học tập trung, phản ánh hiệu quả của thuật
toán FedOpt.

Thử nghiệm chứng minh tính khả thi của  FL cho tóm tắt văn bản mặc dù còn

khoảng cách so với học tập trung. Việc đạt ROUGE-1 trên 0.36 với dữ liệu không

đồng nhất là thành tựu đáng kể, mở ra khả năng ứng dụng thực tế nơi các tổ chức có
thể cộng tác cải thiện chất lượng tóm tắt mà không chia sẻ dữ liệu độc quyền.

3.3.4.

Thực nghiệm so sánh trên nhiều số lượng client khác nhau

Hình 17. Biểu đồ phân tán dữ liệu trên số lượng client khác nhau

Hai biểu đồ phản ánh sự phân tán dữ liệu trong mô hình FL khi triển khai trên
các nhóm client khác nhau, từ 2 đến 10 client. Biểu đồ đầu tiên thể hiện phân bố khối
lượng dữ liệu theo từng client cho thấy sự không đồng đều đáng kể trong việc phân
phối dữ liệu ban đầu. Biểu đồ thứ hai tập trung vào ba chỉ số chuẩn hóa đo lường mức
độ cân bằng: tỷ lệ Max/Min, hệ số Gini và hệ số biến thiên. Các giá trị này dao động
trong khoảng 0.0 đến 1.0, phản ánh xu hướng thay đổi rõ rệt khi số lượng client tăng.
Khi số client tăng từ 6 lên 10, hệ số Gini và hệ số biến thiên có xu hướng giảm
dần, điều này gợi ý rằng dữ liệu trở nên cân bằng hơn do sự đa dạng hóa nguồn phân
phối. Tuy nhiên, tỷ lệ Max/Min lại không giảm đồng nhất, cho thấy vẫn tồn tại sự

66

chênh lệch đáng kể giữa client có dữ liệu lớn nhất và nhỏ nhất. Việc chuẩn hóa các

chỉ số giúp so sánh trực quan hơn, nhưng cũng nhấn mạnh thách thức trong việc đảm

bảo công bằng khi mở rộng quy mô hệ thống.

Những phát hiện này có ý nghĩa quan trọng đối với đề tài áp dụng FL vào NLP.
Sự mất cân bằng dữ liệu giữa các client có thể dẫn đến thiên lệch mô hình, đặc biệt
khi một số client chi phối quá trình huấn luyện. Do đó, nghiên cứu cần xem xét các

cơ chế điều chỉnh trọng số hoặc kỹ thuật lấy mẫu lại để tối ưu hóa hiệu suất tổng thể.
Kết quả phân tích cũng khẳng định tầm quan trọng của việc đánh giá độ phân tán dữ

liệu trước khi triển khai FL, nhằm đảm bảo tính khả thi và công bằng trong các ứng

dụng thực tế.

Hình 18. Kết quả thực nghiệm trên nhiều số lượng client khác nhau

Kết quả được trình bày trong hình cho thấy sự biến động của ba chỉ số ROUGE
(ROUGE-1, ROUGE-2 và ROUGE-L) khi thay đổi số lượng client từ 2 đến 10. Đây
là các chỉ số phổ biến trong đánh giá chất lượng tóm tắt hoặc sinh văn bản, phản ánh
mức độ trùng khớp giữa văn bản sinh ra và văn bản tham chiếu.

Có thể thấy rằng:

•  Chỉ số ROUGE-1 (đường màu xanh lam) duy trì ở mức giảm khá ổn định
trong khoảng từ 2 đến 7 client, dao động nhẹ quanh mức 0.30. Tuy nhiên,

từ mốc 8 client trở đi, chỉ số này tăng rõ rệt và đạt đỉnh ở 9 client (~0.34)

trước khi giảm nhẹ ở 10 client. Điều này gợi ý rằng việc tăng số lượng

67

client có thể góp phần cải thiện chất lượng mô hình đến một mức độ nhất

định, do tăng cường đa dạng dữ liệu.

•  Chỉ số ROUGE-2 (đường màu đỏ) có giá trị thấp hơn so với ROUGE-1,
nhưng cũng thể hiện xu hướng tương tự. Từ 2 đến 7 client, ROUGE-2 gần

như không thay đổi nhiều (~0.11), nhưng bắt đầu cải thiện rõ từ 8 client

trở đi, đạt đỉnh ở mức ~0.134 tại 9 client. Mặc dù mức độ cải thiện không
mạnh như ROUGE-1, xu hướng tích cực vẫn được ghi nhận.

•  Chỉ  số  ROUGE-L  (đường  màu  xanh  lá)  thể  hiện  mức  độ  tương  tự
ROUGE-1, cho thấy cải thiện rõ ràng từ 7 đến 8 client. Đáng chú ý, giá trị

ROUGE-L tăng mạnh tại mốc 8 client và giữ mức ổn định cao hơn trước
đó, phản ánh sự cải thiện về mặt ngữ nghĩa và cấu trúc trong các văn bản

sinh ra.

Nhìn chung, kết quả thực nghiệm cho thấy việc gia tăng số lượng client trong FL

có thể giúp cải thiện chất lượng mô hình, đặc biệt là khi vượt qua ngưỡng 7 client. Sự

cải thiện này có thể bắt nguồn từ việc mô hình học được từ nhiều nguồn dữ liệu phong
phú hơn, giúp tăng tính tổng quát. Tuy nhiên, tại mốc 10 client, một số chỉ số bắt đầu

giảm nhẹ, cho thấy có thể tồn tại hiện tượng nhiễu do dữ liệu quá phân tán và không

đồng đều hoàn toàn, điều này là phù hợp với những thông tin trên biểu đồ phân tán

dữ liệu.

Những quan sát này nhấn mạnh tầm quan trọng của việc lựa chọn số lượng client

phù hợp khi triển khai FL. Không chỉ cần cân nhắc về mặt kỹ thuật (như hiệu suất và

tài nguyên), mà còn cần đảm bảo rằng sự phân phối dữ liệu giữa các client đủ cân

bằng để tránh mô hình bị thiên lệch.

Trong các ứng dụng NLP như tóm tắt văn bản, dịch máy hay sinh văn bản, chất

lượng đầu ra phụ thuộc mạnh vào sự đa dạng và tính đại diện của dữ liệu huấn luyện.

Vì vậy, các chiến lược điều phối như cân bằng dữ liệu, gán trọng số thích hợp cho
các client hoặc chọn lọc client theo độ tin cậy có thể là những hướng tiếp cận tiềm
năng để nâng cao hiệu quả mô hình FL trong tương lai.

68

Kết luận

Trong phần này, chúng tôi tóm lược lại các kết quả chính của khoá luận. Ngoài

ra, chúng tôi trình bày về hướng phát triển tiếp theo trong tương lai.

1.

Tóm lược các kết quả đạt được

Trong khóa luận này, chúng tôi tập trung nghiên cứu lý thuyết và ứng dụng của

FL trong hai bài toán thuộc lĩnh vực NLP: sinh văn bản và phân loại văn bản, đồng

thời tiến hành các thực nghiệm minh họa. Nội dung và kết quả nghiên cứu được trình

bày chi tiết trong các Chương 1 đến 3. Các kết quả chính có thể được tóm tắt như sau:

•  Thứ nhất, chúng tôi đã khảo sát tổng quan về các bài toán, kỹ thuật và ứng
dụng trong NLP, đồng thời tìm hiểu FL từ khái niệm cơ bản đến các thách

thức trong thực tế, đặc biệt là vấn đề dữ liệu không đồng nhất. Chúng tôi
cũng trình bày các thuật toán tối ưu phổ biến như FedAvg, FedProx, các

chiến lược lựa chọn thiết bị tham gia huấn luyện, cũng như ba mô hình

triển khai: tập trung, phân tán và không đồng nhất.

•  Thứ hai, chúng tôi đi sâu vào cách tích hợp FL vào các bài toán NLP. Cụ
thể, chúng tôi phân tích kiến trúc BART với hai thành phần chính là bộ

mã  hóa  hai  chiều  (bidirectional  encoder)  và  bộ  giải  mã  tự  hồi  quy

(autoregressive  decoder),  tìm  hiểu  kỹ  thuật  nén  SCA  trong  thuật  toán

FedOPT, đồng thời trình bày kiến trúc hệ thống FL và quy trình áp dụng

vào các bài toán xử lý ngôn ngữ.

•  Thứ ba, chúng tôi đã triển khai thực nghiệm trên hai bài toán: sinh văn bản
(tóm tắt văn bản) và phân loại văn bản. Kết quả được so sánh giữa mô hình

học tập trung truyền thống và mô hình FL phân tán, cũng như giữa các

kịch bản với số lượng client khác nhau. Kết quả cho thấy, mặc dù FL có

hiệu suất đánh giá thấp hơn đôi chút so với học tập trung, nhưng bù lại
mang lại lợi ích rõ rệt về bảo mật dữ liệu. Ngoài ra, kết quả thực nghiệm

so sánh giữa các số lượng client khác nhau cũng làm nổi bật thách thức do
dữ liệu không đồng nhất, đồng thời nhấn mạnh vai trò quan trọng của các
thuật toán tối ưu như FedOPT trong việc cải thiện hiệu quả mô hình.

2.

Hướng phát triển tương lai:

Trong tương lai, khóa luận có thể được mở rộng và phát triển theo các hướng sau:

69

•  Thứ nhất, tiếp tục đào sâu nghiên cứu các giải pháp nhằm xử lý hiệu quả
vấn  đề  dữ  liệu  phi  đồng  nhất,  chẳng  hạn  như  học  tập  cá  nhân  hóa
(personalized  federated  learning)  và  học  chuyển  giao  trong  môi  trường

liên kết (federated transfer learning). Những hướng tiếp cận này hứa hẹn

sẽ nâng cao hiệu suất mô hình cũng như khả năng thích ứng với đặc điểm

riêng biệt của từng client.

•  Thứ hai, mở rộng phạm vi nghiên cứu sang các tác vụ khác trong lĩnh vực
NLP  như  dịch  máy  (machine  translation),  nhận  dạng  thực  thể  có  tên

(named  entity  recognition  -  NER),  và  phân  tích  cảm  xúc  (sentiment

analysis). Việc áp dụng FL vào các bài toán này sẽ góp phần đánh giá toàn
diện hơn về tiềm năng và giới hạn của FL trong NLP.

•  Thứ ba, tích hợp thêm các cơ chế bảo vệ quyền riêng tư tiên tiến như vi sai
riêng tư hoặc mã hóa đồng hình để nâng cao mức độ bảo mật, đặc biệt trong

các ứng dụng thực tế yêu cầu xử lý dữ liệu nhạy cảm.

•  Thứ tư, phát triển giao diện trực quan để mô phỏng quá trình FL trên nhiều
client, qua đó hỗ trợ người học dễ dàng quan sát, đánh giá và điều chỉnh

các tham số mô hình trong quá trình huấn luyện phân tán.

Những định hướng trên không chỉ giúp hoàn thiện hơn mô hình FL trong lĩnh vực

NLP, mà còn mở ra tiềm năng ứng dụng rộng rãi trong các lĩnh vực khác có dữ liệu

phân tán và nhạy cảm, như y tế, tài chính và giáo dục.

70

Tài liệu tham khảo

[1]   Liu, M., Ho, S., Wang, M., Gao, L., Jin, Y., & Zhang, H. (2021). Federated learning

meets natural language processing: A survey. arXiv preprint arXiv:2107.12603.

[2]   Lin, B. Y., He, C., Zeng, Z., Wang, H., Huang, Y., Dupuy, C., ... & Avestimehr, S.

(2021).  Fednlp:  Benchmarking  federated  learning  methods  for  natural  language
processing tasks. arXiv preprint arXiv:2104.08815.

[3]   Jain,  A.,  Goyal,  A.,  Singh,  V.,  Tripathi,  A.,  &  Kandasamy,  S.  (2020).  Text
categorization techniques and current trends. International Journal of Engineering and
Advanced Technology (IJEAT), 9.

[4]   Church,  K.  W.,  &  Rau,  L.  F.  (1995).  Commercial  applications  of  natural  language

processing. Communications of the ACM, 38(11), 71-79.

[5]   Liu, B., Lv, N., Guo, Y., & Li, Y. (2024). Recent advances on federated learning: A

systematic survey. Neurocomputing, 128019.

[6]    Khan, Y., Sánchez, D., & Domingo-Ferrer, J. (2024). Federated learning-based natural
language  processing:  a  systematic  literature  review.  Artificial  Intelligence  Review,

57(12), 1-39.

[7]    Yu, W., Zhu, C., Li, Z., Hu, Z., Wang, Q., Ji, H., & Jiang, M. (2022). A survey of

knowledge-enhanced text generation. ACM Computing Surveys, 54(11s), 1-38.

[8]   Yao,  L.,  Mao,  C.,  &  Luo,  Y.  (2019,  July).  Graph  convolutional  networks  for  text

classification. In Proceedings of the AAAI conference on artificial intelligence (Vol.
33, No. 01, pp. 7370-7377).

[9]    Ikonomakis,  M.,  Kotsiantis,  S.,  &  Tampakas,  V.  (2005).  Text  classification  using
machine learning techniques. WSEAS transactions on computers, 4(8), 966-974.

[10]   Gasparetto, A., Marcuzzo, M., Zangari, A., & Albarelli, A. (2022). A survey on text

classification algorithms: From text to predictions. Information, 13(2), 83.

[11]  A. a. T. I. MuhammadAsad, FedOpt: Towards Communication Efficiency and Privacy

Preservation in Federated Learning, MDPI, 21 April 2020.

[12]   Iqbal, T., & Qureshi, S. (2022). The survey: Text generation models in deep learning.
Journal  of  King  Saud  University-Computer  and  Information  Sciences,  34(6),  2515-

2528.

[13]   Aggarwal, C. C. Data Mining (PDFDrive. com).

71

