# Thước đo mức sống từ papers: dùng được gì với file hiện có?

Ngày nghiên cứu: 08/11/2026. Đây là danh sách để chọn thước đo, chưa tự đưa tất cả vào kiểm định. [Outline hiện tại](outline_muc_song_2010_2014.md) · [Plan phương pháp](plan_nghien_cuu_muc_song_2010_2014.md).

Ký hiệu $I=income$, $C=$ tổng 13 khoản ghi nhận, $n=size$. Thu/chi cả năm, cùng đơn vị; tiền thực quy về giá 2010. Mỗi dòng là hộ, chưa có trọng số khảo sát quốc gia.

## 1. Khả năng thu nhập trang trải chi tiêu

**Paper:** Condino, Domma & Madeo (2026), [On Households’ Difficulties in Covering Expected Expenses](https://link.springer.com/article/10.1007/s11205-026-03883-z), *Social Indicators Research*.

- Đại lượng nghiên cứu là $P(C>I)$. Paper ước lượng phân phối chung bằng copula; bài của mình có thể dùng tỷ lệ mẫu trực tiếp, không cần tái tạo mô hình đó.
- **Tạo biến:** $Z_i=1\{C_i>I_i\}$; $\hat p_t=\sum Z_i/N_t$.
- **Câu hỏi:** năm 2014 có ít hộ chi vượt thu nhập hơn năm 2010 không? Làm tương tự riêng Q1 nếu cần.
- **Test lớp:** hai tỷ lệ độc lập, pooled dưới H₀ — Chap 7 §7.4; kiểm tra điều kiện số đếm.
- **Giới hạn:** chỉ đo bất cân đối dòng thu/chi ghi nhận; chưa phân biệt tiêu tài sản tích lũy với khó khăn thực sự, không ước lượng rủi ro cá nhân tương lai của mô hình gốc.

**Mức phù hợp:** cao; bổ sung trực tiếp cho mean thu nhập/tiêu dùng hiện có.

## 2. Chênh lệch thu–chi và phần thu nhập còn lại

**Paper:** De Stefani, Laws & Sollaci (2022), [Household Vulnerability to Income Shocks… Cambodia, Nepal and Vietnam](https://www.imf.org/-/media/files/publications/wp/2022/english/wpiea2022064-print-pdf.pdf), IMF WP/22/64, phần Việt Nam và Appendix B.1.

Paper dùng financial margin sau chi tiêu và trả nợ, chuẩn hóa theo thu nhập; có lưu ý về thiếu tài sản thanh khoản. Với file mình, chỉ xây dựng **phiên bản giới hạn**:

$$
D_i^R=\frac{I_i-C_i}{n_i}\frac{100}{CPI_t},\qquad
M_i=\frac{I_i-C_i}{I_i}\quad(I_i>0).
$$

- **Câu hỏi:** hộ còn lại bao nhiêu nguồn lực sau chi ghi nhận; mức này thay đổi ra sao ở toàn mẫu/Q1?
- **Test:** mean $D^R$ giữa hai mẫu độc lập, phương sai chưa biết và không giả sử bằng nhau — Chap 7 §7.2.4. $M$ dùng mô tả độ dư/thiếu tương đối.
- Đây chưa phải FMR đầy đủ của paper, tiết kiệm thực tế hoặc khả năng chống chịu cú sốc; không có nợ/tài sản thanh khoản.

**Mức phù hợp:** cao; đọc cùng tỷ lệ thiếu hụt ở mục 1, không dùng mean dương thay cho kết luận mọi hộ đủ chi.

## 3. Độ thiếu hụt so với một chuẩn sức mua cố định

**Paper:** Foster, Greer & Thorbecke (1984), [A Class of Decomposable Poverty Measures](https://selc.wordpress.ncsu.edu/files/2013/03/A-Class-of-Decomposable-Poverty-Measures.pdf), *Econometrica*.

Với $y_i^R$ là thu nhập thực đầu người và $z>0$ là ngưỡng cùng mặt bằng giá:

$$
P_0=\frac1N\sum_i1\{y_i^R<z\},\qquad
P_1=\frac1N\sum_i\max\left(\frac{z-y_i^R}{z},0\right).
$$

$P_0$ phản ánh tỷ lệ dưới chuẩn; $P_1$ thêm độ sâu thiếu hụt. Chỉ số bình quân trên **toàn mẫu**, hộ trên chuẩn đóng góp 0.

- **Câu hỏi:** phần đáy có tiến gần hơn đến cùng chuẩn sống, kể cả khi chưa vượt chuẩn không?
- **Biến:** `income`, `size`, CPI; có thể thay bằng tiêu dùng nếu chọn được chuẩn phù hợp aggregate chi của bài.
- **Test khi z được cố định phù hợp:** P₀ dùng Z hai tỷ lệ; P₁ là mean của biến gap, có thể dùng hai mẫu phương sai riêng sau kiểm tra điều kiện — Chap 7.
- **Chưa đủ để dùng ngay:** phải chốt z và đối tượng nghèo phù hợp. Q1 mỗi năm luôn gần một phần tư, không thay thế một chuẩn tuyệt đối cố định. Nếu lấy z từ phân vị mẫu thì phát sinh bất định điểm cắt; không tự coi nó là ngưỡng biết trước để dùng CI/p đơn giản.
- Kết quả không trọng số là chỉ số của các hộ trong mô hình mẫu, chưa phải tỷ lệ nghèo quốc gia theo người.

**Mức phù hợp:** có giá trị cho câu hỏi phần đáy, nhưng còn thiếu quyết định về chuẩn z.

## 4. Điều chỉnh nhu cầu theo quy mô hộ: equivalised income/consumption

**Paper:** Buhmann, Rainwater, Schmaus & Smeeding (1988), [Equivalence Scales, Well-Being, Inequality and Poverty](https://www.lisdatacenter.org/wps/liswps/17.pdf), về độ nhạy khi thay cách điều chỉnh quy mô hộ. Một lựa chọn phổ biến là square-root scale, được giải thích trong [khung thống kê thu nhập–tiêu dùng–tài sản OECD](https://www.oecd.org/content/dam/oecd/en/publications/reports/2013/06/oecd-framework-for-statistics-on-the-distribution-of-household-income-consumption-and-wealth_g1g2c4b5/9789264194830-en.pdf).

$$
y_{eq}^R=\frac{I}{\sqrt n}\frac{100}{CPI_t},\qquad
c_{eq}^R=\frac{C}{\sqrt n}\frac{100}{CPI_t}.
$$

- Ý tưởng: sống chung có chi phí dùng chung; nhu cầu không nhất thiết tăng đúng tỷ lệ số người.
- Chỉ cần `size`, không cần tuổi từng thành viên. Đây là giả định điều chỉnh, chưa phải nhu cầu thực được đo từ dữ liệu.
- **Câu hỏi:** nhận định cải thiện có thay đổi khi dùng thước đo này thay cách chia đầu người không?
- **Test:** hai mean độc lập, unknown variances/not assumed equal — Chap 7 §7.2.4, cho tham số mới.
- Giữ như kiểm tra độ nhạy; không tự thay chỉ tiêu đầu người hay gọi thu nhập file là disposable income theo đúng định nghĩa OECD.

**Mức phù hợp:** tính được ngay; là lựa chọn bổ sung để bàn, chưa chốt vào bài.

## 5. Y tế: đo bảo vệ tài chính, không đồng nhất chi cao với mức sống thấp

**Papers:**

- Wagstaff & van Doorslaer (2003), [Catastrophe and impoverishment… Vietnam 1993–1998](https://pubmed.ncbi.nlm.nih.gov/14601155/): phân biệt cách đo theo tỷ lệ chi y tế với cách đo nguồn lực sau chi y tế và nghèo hóa.
- Xu et al. (2003), [Household catastrophic health expenditure: a multicountry analysis](https://pubmed.ncbi.nlm.nih.gov/12867110/): gắn chi y tế với khả năng chi trả sau nhu cầu sinh hoạt. Ngưỡng trong nghiên cứu là lựa chọn của nghiên cứu, không tự trở thành ngưỡng hợp lệ cho file mình.

[WHO về financial protection](https://www.who.int/health-topics/financial-protection) nhấn mạnh khả năng tiếp cận chăm sóc và đáp ứng nhu cầu khác mà không chịu khó khăn tài chính.

**Đối chiếu file:** `med` chỉ là tiền thuốc, `aid` là chăm sóc người bệnh; chưa đủ mọi OOP và hoàn trả. `hins` là khoản bảo hiểm, không phải bằng chứng có/không được bảo hiểm. Không có nhu cầu điều trị chưa đáp ứng, sức khỏe, nợ hay chuẩn chi cơ bản.

Vì vậy chưa tự áp chỉ số catastrophic spending/medical impoverishment chuẩn, hoặc coi giảm `(med + aid)/income` là sống tốt hơn. Có thể mô tả chi thực và khả năng trang trải tổng chi trong nhóm có các khoản này, nhưng chưa chứng minh chính y tế gây thiếu hụt. Đây là hướng cần chọn lại, không ép một kiểm định cho đủ chủ đề.

Lưu ý đại số: nếu $H=med+aid$ và chi khác là $C-H$, thì $(I-H)-(C-H)=I-C$. “Thu nhập sau y tế trừ chi khác” không tạo thêm thông tin so với chênh lệch thu–chi chung.

**Mức phù hợp:** mạnh về định hướng câu hỏi; dữ liệu chưa đủ tái tạo các thước đo chuẩn của papers.

## 6. Gộp tài sản thành proxy nguồn lực dài hạn

**Paper:** Filmer & Pritchett (2001), [Estimating wealth effects without expenditure data—or tears](https://read.dukeupress.edu/demography/article-abstract/38/1/115/170414/Estimating-wealth-effects-without-expenditure-data), *Demography*.

Paper dùng chỉ báo tài sản và PCA để tạo trọng số cho proxy wealth. Chín biến sở hữu đã xác nhận của mình có thể làm đầu vào, bỏ `house` theo yêu cầu.

- **Câu hỏi:** các hộ ít nguồn lực tiền tệ có đồng thời thiếu điều kiện vật chất không?
- **Phần ngoài lớp:** PCA và cách xây trọng số. Nếu so hai năm phải dùng cùng quy tắc/trọng số/chuẩn hóa, không chạy hai index tùy ý rồi coi mức điểm tuyệt đối so sánh được.
- PCA cần được kiểm tra ý nghĩa của các tải số; không tự bảo đảm điểm cao luôn là sống tốt hơn. Chưa là tổng tài sản ròng hay chỉ số mức sống toàn diện.
- Có thể chỉ đếm số nhóm sở hữu để mô tả cho đơn giản, nhưng đó là chỉ tiêu tự định nghĩa với trọng số bằng nhau, **không phải phương pháp PCA của paper**.

**Mức phù hợp:** khả thi nhưng chưa ưu tiên; hiện đã chốt one-way ANOVA từng tài sản, chưa thêm PCA vào plan.

## 7. Giữ nền tảng tiêu dùng thực, nhưng không đồng nhất chi cao với sống tốt

**Paper:** Meyer & Sullivan (2003), [Measuring the Well-Being of the Poor Using Income and Consumption](https://www.nber.org/papers/w9760), đối chiếu ưu/nhược điểm của thu nhập và tiêu dùng trong đo phúc lợi vật chất. [Deaton & Zaidi (2002)](https://documents1.worldbank.org/curated/en/206561468781153320/pdf/Guidelines-for-constructing-consumption-aggregates-for-welfare-analysis.pdf) giải thích xây aggregate và điều chỉnh giá/quy mô hộ.

Giữ thu nhập/tiêu dùng thực đầu người làm nền tảng; C13 chỉ là proxy của file, chưa có dịch vụ nhà ở và đồ bền đầy đủ. Đọc cùng khả năng trang trải, phân bố/Q1 và điều kiện vật chất; không dùng một khoản chi tăng để kết luận chất lượng hay mọi nhu cầu được đáp ứng.

## Lựa chọn đề xuất cho bài

| Vai trò | Thước đo | Trạng thái |
|---|---|---|
| Nền tảng | Thu nhập và tiêu dùng thực đầu người | Đã có trong plan |
| Trục bổ sung chính | $D^R$, $M$ và tỷ lệ $C>I$ | Đã đưa vào phần thu–chi, chờ triển khai sau khi chốt câu hỏi |
| Tập trung phần đáy | Các chỉ tiêu trên trong Q1; FGT nếu có z phù hợp | Q1 đã có; FGT còn cần chốt z |
| Kiểm tra độ nhạy | Equivalence scale căn bậc hai | Đề xuất, chưa tự áp dụng |
| Điều kiện vật chất | Tỷ lệ sở hữu và one-way ANOVA riêng từng tài sản | Đã chốt; chưa thêm PCA |
| Y tế | Bảo vệ tài chính/khả năng đáp ứng nhu cầu | Đang chọn lại thước đo vì giới hạn dữ liệu |

Không gọi các chỉ số cùng xuất phát từ I và C là những bằng chứng độc lập. Các nghiên cứu trên cung cấp mục tiêu đo lường; công thức kiểm định vẫn phải khớp đúng tham số, mẫu và điều kiện của bài.
