# Plan nghiên cứu mức sống: 2010 và 2014

Ngày cập nhật: 08/11/2026.

**Mục tiêu:** kiểm tra sự thay đổi của nguồn lực, tiêu dùng và một số khía cạnh đời sống được đo bằng dữ liệu hiện có. Chưa điền kết quả hay kết luận thực nghiệm.

**Mạch bài:** thu nhập thực → tiêu dùng thực → thành thị/nông thôn → Q1–Q4 và tập trung Q1 → giáo dục → gánh nặng chăm sóc người bệnh → tài sản có còn phân biệt thu nhập không.

Các câu giáo dục và gánh nặng chăm sóc người bệnh đã được đồng ý. Outline mới dành hai câu hỏi nghiên cứu rõ ràng cho Chap 9 và Chap 8: **câu 7 kiểm định độc lập sở hữu–Quart bằng χ²; câu 8 xét nhiều nhân tố tài sản và tương tác với năm bằng ANOVA/mô hình tuyến tính**. Với câu 8, dùng F cổ điển nếu điều kiện phù hợp; nếu không, dùng Wald–HC3 khi chính điều kiện xấp xỉ của phương án này phù hợp. Kiến thức ngoài lớp đã được cho phép và được đánh dấu riêng.

### Bốn phần của bài

| Phần | Nội dung | Câu hỏi |
|---|---|---|
| I. Mặt bằng nguồn lực và tiêu dùng | Thu nhập có tăng thực không, tiêu dùng có thay đổi không? | 1–2 |
| II. Phạm vi của cải thiện | Thành thị/nông thôn → Q1–Q4 → tập trung Q1 | 3–4 |
| III. Giáo dục và chăm sóc người bệnh | Phân biệt tỷ lệ có chi với mức chi; xem gánh nặng của Q1 | 5–6 |
| IV. Điều kiện vật chất | Sở hữu khác giữa các Q không → liên hệ riêng của các tài sản trong từng Q và từng năm | 7–8 |

### Đọc nhanh các câu hỏi

| Câu | Câu hỏi chính | Tham số / đối chiếu | Phương pháp |
|---|---|---|---|
| 1 | Thu nhập đầu người thay đổi thế nào sau điều chỉnh giá? | Trung bình 2014 − 2010; đối chiếu thêm danh nghĩa | t hai mẫu phương sai riêng, Chap 7 |
| 2 | Tiêu dùng thực đầu người có thay đổi? | Trung bình 2014 − 2010 trên hộ đủ chi | t hai mẫu phương sai riêng, Chap 7 |
| 3 | Thay đổi có xuất hiện ở hai khu vực; khoảng cách cuối kỳ ra sao? | Thay đổi trong từng khu vực; khoảng cách thành thị − nông thôn năm 2014 | Estimate/CI; kiểm định hai mẫu, Chap 7 |
| 4 | Q1 có tăng tiêu dùng thực? | Trung bình Q1 năm 2014 − Q1 năm 2010 | t hai mẫu một phía tăng, Chap 7 |
| 5 | Giáo dục: nhiều hộ có chi hơn hay nhóm có chi chi nhiều hơn? | Chênh lệch tỷ lệ có chi; chênh lệch trung bình có điều kiện | Z hai tỷ lệ và t hai trung bình, Chap 7 |
| 6 | Gánh nặng thuốc/chăm sóc người bệnh của Q1 có giảm? | Chênh lệch trung bình tỷ số chi/thu nhập | t hai mẫu phương sai riêng, Chap 7 |
| 7 | Tỷ lệ sở hữu từng tài sản có khác giữa Q1–Q4 trong từng năm? | Độc lập giữa sở hữu và Quart; tỷ lệ sở hữu từng Q | χ² độc lập, Chap 9 §9.2 |
| 8 | Sau khi xét các tài sản khác, tài sản nào còn phân biệt thu nhập trong từng Q; mối liên hệ có đổi qua thời gian? | Hệ số từng tài sản ở mỗi năm và tương tác với năm | ANOVA nhiều nhân tố, Chap 8; F nếu phù hợp, Wald–HC3 là mở rộng |

Các mục dưới viết đầy đủ biến, giả thuyết và điều kiện. “Có thay đổi” là câu hỏi kiểm định; chiều tăng/giảm và độ lớn mới quyết định cách diễn giải cải thiện.

## 1. Khóa cách hiểu dữ liệu và đối tượng suy luận

| Nội dung | Quy ước của bài |
|---|---|
| Thời gian | Chỉ năm 2010 và 2014; bỏ 2012 khỏi phân tích này. |
| Đơn vị quan sát | Một hộ trong một năm. Hai năm được coi là hai mẫu độc lập theo mô hình làm việc đã thống nhất. |
| Thu và chi | Đều là tổng cả năm, đơn vị gốc nghìn đồng. |
| Thu nhập đầu người | `income / size`; `size` gồm mọi thành viên, kể cả người chưa đi làm. Không gọi đây là thu nhập mỗi người lao động. |
| Cách lấy trung bình | Mỗi hộ có trọng số bằng nhau. Trung bình của các mức thu nhập đầu người của hộ chưa phải trung bình có trọng số theo số người hay ước lượng quốc gia theo thiết kế VHLSS. |
| Nhóm thu nhập | Giữ `Quart` gốc của từng năm, trước khi lọc thiếu. Q1 là nhóm thu nhập thấp nhất theo nhãn file, chưa phải nhóm nghèo theo chuẩn chính thức. |
| So sánh Q1 qua thời gian | So sánh nhóm Q1 của hai năm; thành viên có thể khác nhau. Các phép tính điều kiện theo nhãn nhóm đã cho, chưa tính riêng bất định do ước lượng điểm cắt nhóm. |
| Khoản chi khác | Theo xác nhận, `nfood` không bao gồm các khoản chi được ghi riêng. |
| `aid` | Chi của hộ để chăm sóc người bệnh. |
| Tài sản | Giá trị > 0: có sở hữu; = 0: không sở hữu; thiếu/âm: chưa xác định. |
| Điện, nước, rác | Là khoản chi; chưa suy ra khả năng tiếp cận dịch vụ. |
| Thiếu dữ liệu | Giữ là thiếu. Đặc biệt, không điền `fuel` trống thành 0. |

Nguồn tính toán là Excel gốc `dataset/VHLSS_2014.xls`. Những quy tắc làm sạch khác trong sản phẩm cũ trên GitHub không thay thế quy ước ở plan này.

### Quy đổi giá và định nghĩa biến chung

Đặt $P_t$ là CPI bình quân năm, lấy năm 2010 = 100; $P_{2010}=100$, $P_{2014}=143.69$.

Với khoản tiền danh nghĩa $X_{it}$ của hộ $i$ trong năm $t$:

$$
X^R_{it}=X_{it}\frac{100}{P_t}.
$$

Ký hiệu dùng trong toàn bài:

$$
y^N_{it}=\frac{income_{it}}{size_{it}},\qquad
y^R_{it}=\frac{income_{it}}{size_{it}}\frac{100}{P_t}.
$$

$$
C^{13}_{it}=rice+nrice+tobaco+nfood+edu+med+hins+aid+water+elec+garb+fuel+fhouse.
$$

$$
c^R_{it}=\frac{C^{13}_{it}}{size_{it}}\frac{100}{P_t}.
$$

Chỉ tính $C^{13}$ khi đủ cả 13 khoản hợp lệ. Đây là **tổng tiêu dùng ghi nhận theo 13 khoản**, chưa phải tổng tiêu dùng phúc lợi chính thức đầy đủ. Giá trị nhà và tài sản không cộng vào tổng này. CPI chung chỉ điều chỉnh giá theo thời gian; chưa hiệu chỉnh khác biệt giá giữa vùng hay giá riêng của giáo dục/y tế.

Khi trình bày có thể đổi nghìn đồng thành triệu đồng, nhất quán trong từng bảng.

## 2. Các công thức kiểm định dùng chung

### M — Hai trung bình độc lập, không giả sử phương sai bằng nhau

**Tài liệu:** Chap 7 §7.2.4, trang PDF 14; ví dụ phần mềm ở trang 17. Kết hợp Chap 3 về phân phối lấy mẫu và Lecture 5 về khoảng tin cậy.

Với hai nhóm độc lập A và B, tham số là $\Delta=\mu_A-\mu_B$.

Estimator:

$$
\widehat\Delta=\bar X_A-\bar X_B,\qquad
S_g^2=\frac{\sum_i(X_{ig}-\bar X_g)^2}{n_g-1}.
$$

$$
SE=\sqrt{\frac{S_A^2}{n_A}+\frac{S_B^2}{n_B}},\qquad
T=\frac{\widehat\Delta-\Delta_0}{SE}.
$$

$$
\nu=
\frac{(S_A^2/n_A+S_B^2/n_B)^2}
{(S_A^2/n_A)^2/(n_A-1)+(S_B^2/n_B)^2/(n_B-1)}.
$$

Dưới $H_0$ tại $\Delta_0=0$, dùng $T\approx t_\nu$. Khoảng tin cậy hai phía 95%:

$$
\widehat\Delta\pm t_{\nu,0.975}SE.
$$

Mẫu độc lập, phương sai hữu hạn và xấp xỉ phân phối lấy mẫu đủ tốt là các điều kiện cần xem xét. Với dữ liệu tiền lệch phải, không gọi đây là phân phối t chính xác. Không cần kiểm định phương sai bằng nhau trước khi chọn công thức này.

### P — Hai tỷ lệ độc lập

**Tài liệu:** Chap 7 §7.4, trang PDF 22; Chap 3 về phân phối tỷ lệ mẫu.

Với biến chỉ báo $Z\in\{0,1\}$, $Z\sim Bernoulli(p)$, estimator là $\hat p=x/n$.

Kiểm định $H_0:p_A=p_B$ dùng tỷ lệ gộp:

$$
\hat p=\frac{x_A+x_B}{n_A+n_B},\qquad
Z_{test}=\frac{\hat p_A-\hat p_B}
{\sqrt{\hat p(1-\hat p)(1/n_A+1/n_B)}}\approx N(0,1).
$$

CI cho $p_A-p_B$ dùng sai số chuẩn **không gộp**:

$$
(\hat p_A-\hat p_B)\pm z_{0.975}
\sqrt{\frac{\hat p_A(1-\hat p_A)}{n_A}+
\frac{\hat p_B(1-\hat p_B)}{n_B}}.
$$

Kiểm tra số có/không ở từng nhóm và các tần số kỳ vọng theo tỷ lệ gộp; lấy ngưỡng thận trọng ít nhất 10 cho mỗi số đếm để dùng xấp xỉ này. Chênh lệch tỷ lệ báo bằng **điểm phần trăm**.

### Quy tắc giả thuyết

- Các kiểm định mặc định hai phía, $\alpha=5\%$: $H_0:\Delta=0$ và $H_1:\Delta\ne0$.
- Câu Q1 tăng tiêu dùng giữ hướng một phía đã thống nhất trước đây.
- Với câu hỏi “cải thiện” nhưng dùng hai phía, chỉ diễn giải có bằng chứng tăng khi kết quả có hướng dương và CI phù hợp. Bác bỏ $H_0$ tự nó chưa xác định chiều.
- Các CI 95% là khoảng riêng lẻ, chưa có bảo đảm đồng thời 95%. Với loạt kiểm định khoa học của bài, báo cả p thô và p điều chỉnh Holm như mục 11; các kiểm định JB chỉ phục vụ diagnostics và được ghi riêng.

## 3. Câu 1 — Thu nhập đầu người có cải thiện sau khi điều chỉnh giá không?

**Câu hỏi cụ thể:** Trung bình thu nhập thực đầu người của các hộ năm 2014 có khác năm 2010 không, và chiều thay đổi có hỗ trợ nhận định cải thiện nguồn lực không?

**Biến:** `income`, `size`, `Year`, CPI; biến phân tích chính là $y^R$.

**Tham số và giả thuyết:**

$$
\Delta_y=E(y^R_{2014})-E(y^R_{2010}),\qquad
H_0:\Delta_y=0;\quad H_1:\Delta_y\ne0.
$$

**Estimator:** $\widehat\Delta_y=\bar y^R_{2014}-\bar y^R_{2010}$.

**Phương pháp:** M — Chap 7 §7.2.4. Lấy mọi hộ có thu nhập và quy mô hộ hợp lệ của từng năm; không lọc theo việc hộ có đủ khoản chi hay không.

**Đối chiếu có/không CPI:** tính cùng estimator, CI và kiểm định cho $y^N$. Hai phiên bản dùng cùng các hộ, trả lời hai tham số khác nhau: thay đổi danh nghĩa và thay đổi theo giá 2010. Không xem chúng là hai bằng chứng độc lập.

**Mô tả hỗ trợ:** mean, median, độ lệch chuẩn, CV. CV đo mức phân tán tương đối; không đưa một CV mỗi năm vào kiểm định t hai mẫu và không dùng kiểm định mean để kết luận CV thay đổi có ý nghĩa.

**Giới hạn:** thu nhập có đuôi phải mạnh; phải kiểm tra mức ảnh hưởng của các giá trị lớn trước khi tin vào CI/p xấp xỉ. Trung bình tăng chưa có nghĩa mọi hộ đều tăng.

## 4. Câu 2 — Tiêu dùng thực đầu người có thay đổi không?

**Câu hỏi cụ thể:** Trong các hộ đủ dữ liệu 13 khoản chi, trung bình tổng tiêu dùng ghi nhận thực đầu người năm 2014 có khác năm 2010 không?

**Biến:** 13 khoản của $C^{13}$, `size`, `Year`, CPI.

Gọi $V_t=1$ khi hộ đủ dữ liệu hợp lệ để tính $C^{13}$.

$$
\Delta_c^V=E(c^R_{2014}\mid V_{2014}=1)-E(c^R_{2010}\mid V_{2010}=1).
$$

$$
H_0:\Delta_c^V=0;\qquad H_1:\Delta_c^V\ne0.
$$

**Estimator:** chênh lệch hai trung bình $c^R$ trên hai mẫu đủ dữ liệu.

**Phương pháp:** M — Chap 7 §7.2.4. Hai năm nên dùng kiểm định hai mẫu độc lập; ANOVA không đem lại thêm câu trả lời ở đây.

**Kiểm tra thiếu dữ liệu bắt buộc:**

1. Báo tỷ lệ thiếu theo năm, khu vực và Quart, đặc biệt thiếu `fuel`.
2. Tính thêm $C^{12}$ bằng 12 khoản, bỏ `fuel` ở cả hai năm.
3. So sánh $C^{12}$ trên mẫu đủ 13 khoản và trên toàn bộ mẫu đủ 12 khoản để thấy ảnh hưởng của việc thay đổi mẫu.

$C^{12}$ là chỉ tiêu khác, chưa sửa được phần nhiên liệu thiếu. Kết quả complete cases chưa tự suy rộng sang mọi hộ khi cơ chế thiếu chưa rõ.

## 5. Câu 3 — Cải thiện có xuất hiện ở cả thành thị và nông thôn không?

Phân tích khu vực trước, rồi mới đi vào Quart.

### 3a. Thay đổi trong từng khu vực

**Biến:** `area` (1 thành thị, 2 nông thôn), `Year`, $y^R$, $c^R$.

Với từng khu vực $a$ và từng chỉ tiêu $X\in\{y^R,c^R\}$:

$$
\Delta_{a,X}=E(X_{2014}\mid area=a)-E(X_{2010}\mid area=a).
$$

Thêm điều kiện đủ chi khi $X=c^R$.

**Giả thuyết tương ứng:** $H_0:\Delta_{a,X}=0$; $H_1:\Delta_{a,X}\ne0$.

**Estimator:** $\bar X_{a,2014}-\bar X_{a,2010}$.

**Phương pháp:** M — Chap 7 §7.2.4; ưu tiên bảng estimate và CI 95% cho bốn thay đổi, thay vì thêm bốn p-value vào luận điểm chính. Mỗi mẫu khu vực/năm có diagnostics riêng.

### 3b. Khoảng cách cuối kỳ

**Câu hỏi cụ thể:** Năm 2014, trung bình tiêu dùng thực đầu người có khác giữa thành thị và nông thôn không?

$$
G_{2014}=E(c^R_{2014}\mid urban,V=1)-E(c^R_{2014}\mid rural,V=1).
$$

$$
H_0:G_{2014}=0;\qquad H_1:G_{2014}\ne0.
$$

**Phương pháp:** M — Chap 7 §7.2.4, với A = thành thị và B = nông thôn. Báo CI cho khoảng cách này; thu nhập theo khu vực được trình bày bên cạnh để làm bối cảnh.

**Phạm vi trả lời:** kiểm định này trả lời khác biệt năm 2014. Nó chưa kiểm định khoảng cách đã thu hẹp từ 2010; CI/p của từng khu vực cũng chưa kiểm định hai mức tăng khác nhau.

## 6. Câu 4 — Nhóm Q1 có cải thiện tiêu dùng thực không?

### Bước dẫn: nhìn đủ Q1–Q4

Trình bày trung bình thu nhập, tiêu dùng và CI cho thay đổi tiêu dùng của từng Quart. Giữ nhãn nhóm của từng năm. Không kiểm định “thu nhập Q4 khác Q1” như một phát hiện mới, vì thu nhập chính là tiêu chí tạo nhóm.

### Câu hỏi kiểm định chính

**Câu hỏi cụ thể:** Trung bình tiêu dùng thực đầu người của Q1 năm 2014 có cao hơn Q1 năm 2010 không, trên các hộ có đủ khoản chi?

**Biến:** `Quart = 1`, `Year`, $c^R$, chỉ báo đủ chi $V$.

$$
\Delta_{Q1}^V=
E(c^R_{2014}\mid Quart_{2014}=1,V_{2014}=1)
-E(c^R_{2010}\mid Quart_{2010}=1,V_{2010}=1).
$$

$$
H_0:\Delta_{Q1}^V\le0;\qquad H_1:\Delta_{Q1}^V>0.
$$

**Estimator:** chênh lệch hai trung bình Q1 đủ dữ liệu.

**Phương pháp:** M — Chap 7 §7.2.4, một phía tăng; tính thống kê và phân phối tại biên $\Delta=0$. Báo thêm CI hai phía 95% để thể hiện độ lớn và độ bất định; dùng p một phía để quyết định giả thuyết một phía.

**Kiểm tra riêng:** thiếu chi và `fuel` trong Q1, phân phối, quan sát ảnh hưởng; làm lại đối chiếu $C^{12}$ như câu 2.

**Phạm vi trả lời:** mức tiêu dùng của nhóm Q1 từng năm; chưa phải “các hộ nghèo nhất năm 2010 đã khá lên”, hoặc “Q1 cải thiện nhiều hơn Q4”.

## 7. Câu 5 — Thay đổi chi giáo dục đến từ tỷ lệ hộ có chi hay mức chi trong nhóm có chi?

Đây là một câu hỏi kinh tế gồm hai giả thuyết bổ sung nhau. Phân tích chính dùng toàn mẫu; bảng Q1–Q4 dùng để mô tả phạm vi, chưa tự thêm cùng loạt kiểm định cho mọi nhóm.

### 5a. Tỷ lệ hộ phát sinh chi giáo dục

**Biến:** `edu`, `Year`.

$$
D_{it}=\mathbf{1}(edu_{it}>0),\qquad p_t=P(edu_t>0).
$$

`edu = 0` giữ là 0; `edu` thiếu giữ là thiếu.

$$
H_0:p_{2014}=p_{2010};\qquad H_1:p_{2014}\ne p_{2010}.
$$

**Estimator:** $\hat p_t=\#\{edu>0\}/\#\{edu\text{ hợp lệ}\}$; chênh lệch $\hat p_{2014}-\hat p_{2010}$.

**Phương pháp:** P — Chap 7 §7.4. Chỉ báo là Bernoulli; thống kê kiểm định có phân phối chuẩn xấp xỉ khi điều kiện số đếm phù hợp. Không kiểm định chuẩn của biến nhị phân bằng JB.

### 5b. Mức chi trong nhóm có chi

**Biến:** `edu`, `size`, `Year`, CPI; chỉ lấy hộ có `edu > 0` và quy mô hộ hợp lệ.

$$
e^R_{it}=\frac{edu_{it}}{size_{it}}\frac{100}{P_t},\qquad
\mu^+_{e,t}=E(e^R_t\mid edu_t>0).
$$

$$
H_0:\mu^+_{e,2014}=\mu^+_{e,2010};\qquad
H_1:\mu^+_{e,2014}\ne\mu^+_{e,2010}.
$$

**Estimator:** chênh lệch trung bình $e^R$ của hai nhóm có chi.

**Phương pháp:** M — Chap 7 §7.2.4; diagnostics trên chính nhóm có chi, không mượn phân phối toàn mẫu.

### Vì sao hai giả thuyết cùng trả lời một câu hỏi?

Trên tập hồ sơ hợp lệ chung, với chi giáo dục không âm:

$$
E(e^R_t)=P(edu_t>0)\,E(e^R_t\mid edu_t>0).
$$

Vì vậy, trung bình chung có thể đổi do tỷ lệ có chi, mức chi của nhóm có chi, hoặc cả hai. Dùng cùng tập hồ sơ có `edu` và `size` hợp lệ khi minh họa đẳng thức này. Hai kết quả bổ sung nhau, chưa phải hai bằng chứng độc lập.

**Phạm vi trả lời:** hành vi và nguồn lực chi giáo dục ghi nhận. Thiếu số người đang học, độ tuổi và kết quả học tập; chưa suy ra tiếp cận, chất lượng hay chi cho mỗi người học. CPI chung chưa phải chỉ số giá giáo dục riêng.

## 8. Câu 6 — Gánh nặng tiền thuốc và chăm sóc người bệnh của Q1 có giảm không?

**Câu hỏi cụ thể:** Tỷ lệ thu nhập dùng cho tiền thuốc và chăm sóc người bệnh, tính bình quân trên các hộ Q1, năm 2014 có khác năm 2010 không? Nếu khác, chiều thay đổi có hỗ trợ nhận định giảm gánh nặng không?

**Biến:** `med`, `aid`, `income`, `Quart`, `Year`.

$$
B_{it}=\frac{med_{it}+aid_{it}}{income_{it}},\qquad income_{it}>0.
$$

Giữ các hộ có tử số bằng 0. Loại khỏi phép tính những hồ sơ thiếu một thành phần cần dùng hoặc có giá trị không hợp lệ; báo số loại và lý do. Không yêu cầu đủ 13 khoản tiêu dùng.

$$
\Delta_B=E(B_{2014}\mid Quart_{2014}=1)-E(B_{2010}\mid Quart_{2010}=1).
$$

Các kỳ vọng trên hiểu là điều kiện trên hồ sơ đủ dữ liệu hợp lệ để tính $B$.

$$
H_0:\Delta_B=0;\qquad H_1:\Delta_B\ne0.
$$

**Estimator:** $\widehat\Delta_B=\bar B_{Q1,2014}-\bar B_{Q1,2010}$. Đây là **trung bình tỷ số của từng hộ**, khác với tỷ số giữa tổng chi và tổng thu nhập của cả nhóm.

**Phương pháp:** M — Chap 7 §7.2.4. Giữ hai phía để kiểm tra cả khả năng tăng và giảm; hướng âm cùng CI thích hợp mới hỗ trợ nhận định giảm. Kiểm tra kỹ thu nhập nhỏ và các tỷ số lớn vì chúng có thể chi phối trung bình.

**CPI:** không cần điều chỉnh riêng tỷ số $B$ khi tử và mẫu cùng kỳ, cùng đơn vị; cùng một hệ số CPI sẽ triệt tiêu.

**Mô tả hỗ trợ:** số tiền thuốc/chăm sóc thực đầu người, mức thu nhập và tỷ lệ hộ có khoản chi này. Chúng giúp đọc tỷ số, không xác định nguyên nhân thay đổi.

**Phạm vi trả lời:** gánh nặng của hai khoản chi ghi nhận. `hins` trình bày riêng. Không gọi đây là chỉ tiêu chi y tế thảm họa chuẩn quốc tế; chi thấp có thể do ít bệnh hoặc không chi trả được, chưa khẳng định sức khỏe tốt hơn.

## 9. Câu 7 — Tỷ lệ sở hữu tài sản có còn khác giữa Q1–Q4 không? — Chap 9

**Vai trò:** xác định tài sản nào phân biệt các nhóm thu nhập về tỷ lệ sở hữu. Đây là một câu hỏi nghiên cứu chính, dùng trực tiếp Chap 9; không chỉ dùng chương này để kiểm tra chuẩn.

**Câu hỏi cụ thể:** Trong riêng năm 2010, rồi riêng năm 2014, tỷ lệ sở hữu mỗi tài sản có khác giữa Q1–Q4 không?

**Biến:** `Year`, `Quart` và chỉ báo có/không của từng tài sản trong danh sách `oto`, `moto`, `bicycle`, `bed`, `tab`, `tele`, `tv`, `emachine`, `hmachine`. Giá trị dương là có, 0 là không, thiếu/âm là chưa biết. Mỗi bảng dùng những hộ có Quart và tài sản đó hợp lệ, không yêu cầu đủ tất cả tài sản hay khoản chi.

Với tài sản $j$, năm $t$, đặt:

$$
p_{j,q,t}=P(A_j=1\mid Quart=q,Year=t).
$$

**Giả thuyết cho mỗi tài sản/năm:**

$$
H_{0,j,t}:p_{j,1,t}=p_{j,2,t}=p_{j,3,t}=p_{j,4,t};
\qquad H_{1,j,t}:\text{có ít nhất hai tỷ lệ khác nhau}.
$$

Tương đương $H_0$: sở hữu tài sản $j$ và Quart độc lập trong năm đó. Đây chưa phải giả thuyết sở hữu tài sản làm thay đổi thu nhập.

**Estimator:** $\hat p_{j,q,t}=x_{j,q,t}/n_{j,q,t}$; báo tỷ lệ của cả bốn Q và độ lớn chênh lệch, bên cạnh kiểm định chung.

**Phương pháp:** kiểm định độc lập Pearson $\chi^2$, Chap 9 §9.2, trang PDF 11–13. Lập bảng $4\times2$ cho từng tài sản/năm; chín tài sản × hai năm = 18 bảng dự kiến.

$$
E_{qa}=\frac{R_qC_a}{N},\qquad
\chi^2=\sum_{q=1}^4\sum_{a=0}^1\frac{(O_{qa}-E_{qa})^2}{E_{qa}}
\approx\chi^2_{(4-1)(2-1)}=\chi^2_3.
$$

**Điều kiện:** quan sát hộ độc lập theo mô hình làm việc, mỗi hộ thuộc đúng một ô, và tần số kỳ vọng đủ lớn. Kiểm tra mọi $E_{qa}\ge5$; điều kiện này áp dụng cho **số kỳ vọng**, không bắt buộc mọi số quan sát đều ít nhất 5. Không cần phân phối thu nhập chuẩn hay phương sai thu nhập bằng nhau.

**Đã kiểm tra khả năng áp dụng:** trên dữ liệu hiện tại, cả 18 bảng đều có tần số kỳ vọng nhỏ nhất trên 5 (nhỏ nhất khoảng 20,16). Đây là kiểm tra thiết kế, chưa phải kết quả kiểm định mối liên hệ. Vì vậy, ô tô hiếm bên trong Q1 có thể gây khó cho mô hình câu 8 nhưng chưa ngăn kiểm định sở hữu ô tô giữa bốn Q ở câu này.

**Báo kết quả sau này:** bảng tỷ lệ Q1–Q4 cho hai năm, $\chi^2$, df, p thô và p Holm. Chỉ bác bỏ kiểm định chung chưa chỉ ra tất cả cặp Q đều khác nhau; không tự chạy thêm mọi cặp.

**Phạm vi trả lời:** mối liên hệ giữa nhóm thu nhập và sở hữu trong từng năm. Một năm có ý nghĩa, năm kia không chưa chứng minh mối liên hệ đã yếu đi. Câu 8 kiểm tra trực tiếp thay đổi của mối liên hệ với thu nhập trong mô hình nhiều nhân tố; đó là tham số khác, không phải kiểm định sự thay đổi của chính mối liên hệ $\chi^2$. Tỷ lệ sở hữu cao/thấp được đọc từ bảng tỷ lệ, không suy ra từ p-value.

## 10. Câu 8 — Những tài sản nào còn phân biệt thu nhập, trong từng Q và từng năm?

**Câu hỏi cụ thể:** Trong cùng nhóm thu nhập, sở hữu mỗi loại tài sản có liên hệ riêng với thu nhập đầu người không, sau khi xét đồng thời các tài sản còn lại? Mối liên hệ đó có thay đổi giữa 2010 và 2014 không?

Đây là câu hỏi về **mối liên hệ có điều chỉnh trong mô hình**, khác với chênh lệch trung bình thô của hai nhóm sở hữu. Không gọi hệ số là tác động nhân quả.

### 8a. Biến dùng và phạm vi

| Nhóm | Biến |
|---|---|
| Kết quả | Thu nhập thực đầu người $y^R$ |
| Nhân tố thời gian | $T=0$ cho 2010, $T=1$ cho 2014 |
| Chín nhân tố tài sản có/không | `oto`, `moto`, `bicycle`, `bed`, `tab`, `tele`, `tv`, `emachine`, `hmachine` |
| Phân tích riêng | Bốn mô hình tương ứng Q1, Q2, Q3, Q4 |

Với mỗi tài sản $j$, đặt $A_j=1$ khi giá trị dương, $A_j=0$ khi bằng 0. Thiếu/âm giữ là chưa biết. `hmachine` và `emachine` là nhóm thiết bị gộp, không phải một thiết bị cụ thể. `house` là giá trị nhà ước tính, chưa có xác nhận mã hóa có/không tương tự chín biến trên; không đưa nó vào làm biến sở hữu.

Các tài sản **không cần độc lập với nhau**. Mô hình phải xem xét mức trùng lặp, đa cộng tuyến và biến thiên còn lại của từng nhân tố. Chỉ tiêu nhân tố là có/không, không phải giá trị tài sản bằng tiền.

Các bảng tỷ lệ sở hữu theo Quart và năm đi trước mô hình để thấy mức phổ biến. Chúng mô tả trên hồ sơ hợp lệ của từng tài sản. Mẫu mô hình đồng thời cần đủ các biến thực sự đưa vào mô hình; phải báo tỷ lệ mất mẫu theo năm/Q và sự khác biệt với mẫu mô tả.

### 8b. Mô hình nhiều nhân tố và tương tác với năm

Trong mỗi Quart $q$, mô hình dự kiến là:

$$
y^R_i=\beta_{0q}+\beta_{Tq}T_i
+\sum_{j\in S_q}\beta_{jq}A_{ij}
+\sum_{j\in S_q}\gamma_{jq}(T_iA_{ij})+\varepsilon_i.
$$

$S_q$ là tập nhân tố đủ điều kiện ước lượng và suy luận trong Quart đó, xác định bằng diagnostics thiết kế trước khi xét p-value. Tất cả chín tài sản đều được kiểm tra điều kiện, không tự hứa có p-value đáng tin cậy cho mọi tài sản ở mọi Q.

**Đọc từng phần của mô hình:**

- $\beta_{jq}$: chênh lệch thu nhập gắn với tài sản $j$ trong năm 2010, sau khi điều chỉnh tuyến tính cho các tài sản còn lại.
- $\beta_{jq}+\gamma_{jq}$: chênh lệch tương ứng trong năm 2014.
- $\gamma_{jq}$: mức thay đổi của mối liên hệ đã điều chỉnh giữa hai năm.
- $\beta_{Tq}$ cho phép mặt bằng thu nhập khác giữa hai năm; nó không tự là mức tăng trung bình chung của cả Quart.

Ví dụ với TV trong Q1: so sánh thu nhập gắn với việc có TV trong các hộ Q1, có tính đến xe máy, điện thoại và những tài sản khác đủ điều kiện. Sau đó kiểm tra trực tiếp mối liên hệ của TV có thay đổi qua thời gian không.

Cấu trúc dùng các nhân tố tài sản cộng gộp và các tương tác **năm × từng tài sản**. Chưa đưa tương tác giữa mọi cặp tài sản hay toàn bộ tổ hợp: chín biến nhị phân đã có tới $2^9=512$ tổ hợp mỗi năm/Q, nhiều tổ hợp có thể ít hoặc không có hộ. Đây là hạn chế cấu trúc của mô hình; hệ số không mô tả mọi cách kết hợp tài sản có thể có.

**Estimator:** vector hệ số OLS $\hat\theta_q=(X_q'X_q)^{-1}X_q'y_q$ khi ma trận thiết kế có hạng đầy đủ. Đây là phần mở rộng ngoài lớp. Các hệ số là tham số của mô hình tuyến tính/best linear projection trên mẫu mục tiêu; chỉ diễn giải thành chênh lệch kỳ vọng có điều kiện không đổi khi cấu trúc kỳ vọng tuyến tính đã nêu phù hợp.

### 8c. Giả thuyết cho từng tài sản

Với từng $j$ trong từng Quart $q$:

| Câu hỏi | $H_0$ | $H_1$ |
|---|---|---|
| Năm 2010 còn phân biệt thu nhập không? | $\beta_{jq}=0$ | $\beta_{jq}\ne0$ |
| Năm 2014 còn phân biệt thu nhập không? | $\beta_{jq}+\gamma_{jq}=0$ | $\beta_{jq}+\gamma_{jq}\ne0$ |
| Mối liên hệ đã thay đổi chưa? | $\gamma_{jq}=0$ | $\gamma_{jq}\ne0$ |

**Estimator tương ứng:** $\hat\beta_{jq}$, $\hat\beta_{jq}+\hat\gamma_{jq}$, $\hat\gamma_{jq}$. Với tổng hai hệ số, SE phải tính cả hiệp phương sai giữa hai estimator, không cộng riêng hai SE.

Cả ba giả thuyết là ràng buộc tuyến tính trong ANOVA nhiều nhân tố. Dùng F từng phần nếu mô hình sai số chuẩn, độc lập và phương sai chung phù hợp; nếu không, dùng Wald–HC3 khi điều kiện xấp xỉ của phương án đó phù hợp (mục 11). Báo hệ số, CI, p thô và p điều chỉnh.

**Diễn giải đúng mục tiêu:** một năm có ý nghĩa, năm kia không, chưa kiểm định sự thay đổi; hàng thứ ba mới trả lời việc đó. Không bác bỏ hệ số bằng 0 cũng chưa chứng minh tài sản hết khả năng phân biệt về mặt kinh tế. Muốn khẳng định chênh lệch đủ nhỏ cần chốt ngưỡng nhỏ có ý nghĩa và thiết kế kiểm định tương đương riêng; đó chưa là kết luận được hứa trong plan.

### 8d. Giả thuyết cho cả nhóm tài sản

Trong từng Quart, đặt $k_q=|S_q|$:

1. **Năm 2010:** $H_0:\beta_{jq}=0$ với mọi $j\in S_q$; $H_1$: có ít nhất một hệ số khác 0.
2. **Năm 2014:** $H_0:\beta_{jq}+\gamma_{jq}=0$ với mọi $j$; $H_1$: có ít nhất một tổng khác 0.
3. **Thay đổi giữa hai năm:** $H_0:\gamma_{jq}=0$ với mọi $j\in S_q$; $H_1$: có ít nhất một hệ số tương tác khác 0.

Mỗi kiểm định chung xét $k_q$ ràng buộc độc lập: dùng F từng phần theo mô hình cổ điển hoặc Wald–HC3 theo điều kiện ở mục 11. Với Wald, cần ma trận hiệp phương sai của các ràng buộc khả nghịch. Bác bỏ kiểm định chung cho biết có ít nhất một mối liên hệ phù hợp giả thuyết đối; các kiểm định riêng mới chỉ ra tài sản nào có bằng chứng.

### 8e. Điểm thiết kế đã kiểm tra, chưa phải kết quả giả thuyết

Đã kiểm tra số hộ sở hữu trên hồ sơ đủ chín biến, chưa ước lượng hệ số hay tính p:

- Ở Q1 năm 2010 chỉ có **một hộ sở hữu ô tô**. Đưa riêng hiệu ứng ô tô theo năm vào mô hình sẽ tạo một điểm leverage bằng 1; HC3 với mẫu đó không áp dụng được theo công thức thông thường.
- Ô tô cũng rất ít ở Q2–Q3 năm 2010; nhóm không có `hmachine` rất ít ở Q4 năm 2014. Các trường hợp này cần đánh giá độ ổn định riêng, không lấy tổng số hộ lớn của Quart làm bảo đảm.
- Vì vậy, bảng cuối phải có trạng thái cho từng tài sản/Q: đủ điều kiện suy luận, suy luận còn yếu, hoặc chỉ mô tả. Nếu cần thu hẹp $S_q$, nêu biến bị loại và lý do thiết kế, không chọn theo dấu hệ số hoặc p-value.
- Việc tất cả chín cột có thể có hạng đầy đủ chưa đủ chứng minh các kiểm định đáng tin cậy. Sau khi chốt tập nhân tố phải kiểm tra lại hạng, leverage, hỗ trợ dữ liệu và phần dư.

Trường hợp phải giảm nhân tố, kết luận chỉ điều chỉnh cho tập $S_q$ thực sự đã dùng; không viết là đã kiểm soát đủ chín tài sản. Phần sở hữu hiếm vẫn có số đếm/tỷ lệ mô tả và ghi rõ vì sao chưa thể kết luận suy luận.

## 11. ANOVA nhiều nhân tố và cách đưa ra kết luận khi phương sai khác nhau

### Phần nối với kiến thức lớp

- Chap 8 §8.1: so sánh trung bình, phân rã biến thiên, SS/df/MS.
- Chap 8 §8.2–8.3: nhiều nhân tố và tương tác. Mô hình câu 8 mở rộng số nhân tố và giữ các tương tác phục vụ đúng câu hỏi thời gian.
- Giả thuyết F cổ điển cần mô hình sai số phù hợp, gồm phương sai chung; dữ liệu hộ quan sát chưa cho phép diễn giải nhân tố thành nguyên nhân.

### Nhánh 1 — Kiểm định F theo mô hình ANOVA cổ điển

Với cùng các hộ quan sát, gọi U là mô hình đầy đủ và R là mô hình bị ràng buộc bởi $H_0$. Nếu $H_0$ đặt $r$ ràng buộc độc lập và $p_U=rank(X_U)$:

$$
F=\frac{(SS_{E,R}-SS_{E,U})/r}{SS_{E,U}/(N-p_U)}.
$$

Dưới $H_0$, nếu sai số độc lập, chuẩn và cùng phương sai, $F\sim F_{r,N-p_U}$. Đây là nguyên lý SS–df–MS của Chap 8, trình bày qua mô hình tuyến tính để xử lý nhiều nhân tố và cỡ ô không cân bằng. Không chép công thức SS cân bằng trong slide sang dữ liệu nhiều nhân tố này.

Mô hình R và U phải dùng đúng cùng một mẫu. Ví dụ kiểm định hệ số năm 2014 bằng 0 là ràng buộc $\beta_j+\gamma_j=0$, không đơn giản xóa một cột tùy ý. Kiểm tra phần dư, sự khác biệt mức phân tán và ảnh hưởng của điểm lớn; một p kiểm tra chuẩn/phương sai không tự chứng minh mọi giả định.

### Nhánh 2 — Phần mở rộng đã được cho phép: HC3 và Wald

**HC3** là cách ước lượng ma trận hiệp phương sai của các hệ số khi phương sai sai số có thể khác nhau giữa các hộ. Nó thay cách tính độ bất định, không tự thay estimator OLS hoặc sửa sai lệch do mô hình, chọn mẫu và bỏ sót biến.

Với $\hat e_i$ là phần dư và $h_{ii}$ là leverage:

$$
\widehat V_{HC3}=(X'X)^{-1}X'
\operatorname{diag}\left(\frac{\hat e_i^2}{(1-h_{ii})^2}\right)
X(X'X)^{-1}.
$$

Công thức và vai trò của HC3 được đối chiếu với [tài liệu phương pháp của statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.HC3_se.html).

**Wald** kiểm tra một hoặc nhiều ràng buộc hệ số cùng lúc. Viết $H_0:R\theta=r_0$, với $r$ ràng buộc độc lập:

$$
W=(R\hat\theta-r_0)'
[R\widehat V_{HC3}R']^{-1}
(R\hat\theta-r_0)
\approx\chi^2_r\quad\text{dưới }H_0.
$$

Trong nhánh phương sai khác nhau này, chọn tham chiếu $\chi^2$ xấp xỉ, không dùng phân phối F cổ điển. Trong triển khai cần truyền rõ covariance HC3 và `use_f=False`; kiểm tra hạng và tính khả nghịch của các ràng buộc. Cách đặt giả thuyết chung và lựa chọn phân phối được đối chiếu với [tài liệu Wald test](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.wald_test.html).

**Điều kiện:** quan sát độc lập theo mô hình làm việc, số nhân tố hữu hạn so với cỡ mẫu, các điều kiện moment cho xấp xỉ hiệp phương sai (chẳng hạn moment bậc bốn hữu hạn), ma trận thiết kế được xác định và có đủ hỗ trợ/biến thiên; không có một số ít điểm chi phối xấp xỉ. HC3 không yêu cầu cùng phương sai hay sai số có phân phối chuẩn chính xác, nhưng suy luận vẫn là xấp xỉ mẫu lớn. Nó không khắc phục phụ thuộc cụm trong thiết kế khảo sát khi chưa có thông tin cụm, hoặc một nhóm sở hữu chỉ có một hộ.

### Bảng ANOVA sẽ trình bày thế nào?

Hai bảng phục vụ hai việc riêng:

1. **Bảng phân rã mô hình OLS:** $SS_T=SS_{model}+SS_E$, với df mô hình $rank(X)-1$, df sai số $N-rank(X)$, df tổng $N-1$; tính MS để nối với Chap 8. Đây là phân rã đại số khi có intercept.
2. **Bảng kiểm định nhân tố và tương tác:** tên tài sản/nhóm hệ số, giả thuyết cụ thể, số ràng buộc, thống kê F và bậc tự do nếu dùng nhánh cổ điển; hoặc Wald $W$ và phân phối $\chi^2$ xấp xỉ nếu dùng nhánh HC3. Báo p thô/p điều chỉnh và các ước lượng liên quan.

Các nhân tố tài sản có tương quan và cỡ ô không cân bằng, nên phần SS của từng nhân tố có thể phụ thuộc cách phân rã; không cộng các partial SS như các phần đóng góp độc lập. Kiểm định dùng các ràng buộc tường minh ở câu 8, tránh việc lựa chọn Type I/II/III làm thay đổi ngầm câu hỏi.

Không gắn nhãn Wald $W$ là F cổ điển, và không trình bày SS suy ngược từ bảng robust như một phân rã SS cộng được theo slide.

### Nhiều tài sản: kiểm soát việc kiểm định nhiều lần

Xét nhiều tài sản làm tăng khả năng có p nhỏ ngẫu nhiên. Dùng điều chỉnh **Holm** cho danh sách p của các giả thuyết khoa học được báo như kết luận kiểm định trong toàn plan; báo cả p thô và p điều chỉnh. Đây là kiến thức ngoài lớp, được giải thích và đối chiếu với [tài liệu điều chỉnh p](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html).

Danh sách được khóa theo thiết kế trước khi xét p: các kiểm định chính về thu nhập, tiêu dùng, khu vực cuối kỳ, Q1, hai thành phần giáo dục, gánh nặng chăm sóc; cùng các kiểm định độc lập tài sản–Quart ở câu 7 và các kiểm định tài sản riêng/chung đủ điều kiện ở câu 8. Nếu dùng cả kiểm định thu nhập danh nghĩa để kết luận, đưa nó vào danh sách. Các bảng chỉ mô tả/CI và kiểm định JB chẩn đoán được ghi rõ, không âm thầm biến thành thêm kết luận kiểm định.

Với $m$ giả thuyết có p hợp lệ, xếp $p_{(1)}\le\cdots\le p_{(m)}$; so sánh tuần tự với $\alpha/(m-i+1)$ và dừng bác bỏ khi gặp phép không đạt. Báo p điều chỉnh theo bước này. Kiểm soát sai lầm cả họ vẫn phụ thuộc việc các p đầu vào đủ hợp lệ; Holm không sửa được HC3 không đáng tin ở nhóm quá hiếm. CI 95% thường vẫn là CI riêng lẻ, chưa tự được điều chỉnh đồng thời theo Holm.

**Hướng kết luận được phép:** tài sản nào có liên hệ với thu nhập trong mô hình; liên hệ đó đã thay đổi hay chưa; độ lớn và độ bất định đến đâu. “Chưa đủ bằng chứng” là một kết quả có thể xảy ra, không bị đổi thành khẳng định bằng cách chọn phương pháp khác.

## 12. Distribution check, estimator và inference được kiểm tra thế nào?

### Trước hết xác định tham số, rồi mới chọn estimator

- Hỏi trung bình: dùng $\bar X$; so sánh hai trung bình dùng $\bar X_A-\bar X_B$.
- Hỏi tỷ lệ: dùng $\hat p$, tức trung bình của biến chỉ báo Bernoulli.
- Hỏi trung bình gánh nặng: tính tỷ số từng hộ trước, rồi lấy trung bình.
- Lecture 4/Chap 4: phân biệt **parameter**, **estimator** và **estimate**. Dưới mô hình iid có kỳ vọng hữu hạn, $\bar X$ không chệch cho $\mu$; điều đó chưa bảo đảm CI/p hữu hạn mẫu chính xác hay khắc phục thiếu dữ liệu.

### Kiểm tra dữ liệu liên tục trong đúng từng mẫu được suy luận

1. Số quan sát hợp lệ, số 0 và số thiếu; quy tắc giữ/loại giá trị.
2. Histogram, boxplot hoặc Q–Q plot; mean, median, phương sai, skewness và kurtosis — Chap 2.
3. Jarque–Bera theo Chap 9 §9.4, trang PDF 21:

$$
H_0:X\text{ có phân phối chuẩn};\qquad
JB=n\left(\frac{g_1^2}{6}+\frac{g_2^2}{24}\right)\approx\chi^2_2.
$$

Trong đó $m_r=n^{-1}\sum_i(x_i-\bar x)^r$, $g_1=m_3/m_2^{3/2}$ và $g_2=m_4/m_2^2-3$.

4. Kiểm tra các quan sát lớn chiếm bao nhiêu tổng bình phương độ lệch; đặc biệt ở thu nhập, nhóm chi giáo dục dương và tỷ số y tế/thu nhập.
5. Đánh giá có cơ sở dùng phân phối lấy mẫu xấp xỉ hay chưa — Chap 3. Cỡ mẫu lớn hỗ trợ CLT nhưng mốc $n>30$ chưa là bảo đảm tự động với đuôi quá mạnh. Nếu vài quan sát chi phối, CI/p được đánh dấu chưa đủ tin cậy; không âm thầm xóa hộ hay đổi tham số.

JB kiểm tra phân phối của **giá trị hộ**, không kiểm tra trực tiếp phân phối của **trung bình mẫu**. Bác bỏ chuẩn chưa tự động cấm suy luận mean xấp xỉ; không bác bỏ cũng chưa chứng minh dữ liệu chuẩn. JB không quyết định thay mean bằng median.

### Với dữ liệu phân loại

- Hai tỷ lệ: kiểm tra số đếm cho xấp xỉ chuẩn, không yêu cầu biến 0/1 có phân phối chuẩn.
- Bảng chéo: kiểm tra tần số kỳ vọng cho xấp xỉ $\chi^2$.
- Tính độc lập đến từ thiết kế/mô hình dữ liệu, không thể được chứng minh chỉ bằng histogram hay JB.

## 13. Bảng đối chiếu kiến thức lớp

| Kiến thức | Dùng vào đâu | Tài liệu |
|---|---|---|
| Mean, variance, median, CV, mô tả phân phối | Thu nhập, tiêu dùng, các nhóm, diagnostics | Chap 2 |
| Phân phối lấy mẫu, CLT | Cơ sở xấp xỉ của mean và tỷ lệ | Chap 3, đặc biệt trang PDF 14 và 20 |
| Parameter / estimator / estimate; tính chất estimator | Định nghĩa mục tiêu và estimator của từng câu | Lecture 4 / Chap 4 |
| CI và độ bất định | Chênh lệch mean, tỷ lệ và khoảng cách | Lecture 5; công thức hai mẫu ở Chap 7 |
| $H_0$, $H_1$, $\alpha$, bác bỏ/không bác bỏ | Mọi câu kiểm định | Chap 6 |
| Hai trung bình độc lập, phương sai riêng | Câu 1–4, 5b, 6 | Chap 7 §7.2.4, trang PDF 14 |
| Hai tỷ lệ | Câu 5a | Chap 7 §7.4, trang PDF 22 |
| ANOVA, nhiều nhân tố và tương tác; SS, df, MS, F khi điều kiện phù hợp | Mô hình tài sản ở câu 8 | Chap 8 §8.1–8.3; suy rộng số nhân tố ngoài slide |
| Độc lập hai biến phân loại | Câu 7: sở hữu từng tài sản và Quart, riêng mỗi năm | Chap 9 §9.2, trang PDF 11–13 |
| Kiểm tra chuẩn JB | Chẩn đoán các biến liên tục và phần dư mô hình | Chap 9 §9.4, trang PDF 21 |
| OLS nhiều nhân tố, HC3, Wald | Câu 8: hệ số từng năm, thay đổi và kiểm định chung | Ngoài lớp; đã được cho phép, công thức ở mục 10–11 |
| Holm | Điều chỉnh p cho danh sách kiểm định khoa học của bài | Ngoài lớp; mục 11 |

Các số trang trên là thứ tự trang PDF. Lecture 4 và Lecture 5 có thể có số trang in trên slide khác thứ tự PDF.

## 14. Cách triển khai notebook sau khi chốt plan

Mỗi câu dùng cùng trình tự:

1. Markdown: câu hỏi → vai trò trong bài → biến → tham số → giả thuyết.
2. Code: tạo biến, xác định mẫu và báo số quan sát/thiếu.
3. Code và note: diagnostics, điều kiện dùng phân phối kiểm định.
4. Code: tính estimator, phương sai, SE, thống kê, df, CI; đối chiếu phép tính với thư viện. Với câu 7, kiểm tra bảng quan sát/kỳ vọng và thống kê χ². Với câu 8, kiểm tra thêm residuals, leverage, hạng ma trận, F hoặc covariance HC3/Wald theo nhánh áp dụng, các contrast và p Holm.
5. Markdown: diễn giải độ lớn, độ bất định, quyết định kiểm định và giới hạn đúng với câu hỏi.

Tên biến thể hiện rõ nội dung và đơn vị, ví dụ `real_income_per_person`, `positive_education_spending`, `medicine_care_income_ratio`, `owns_tv`, `year_2014`, `year_2014_x_owns_tv`. Giữ biến gốc bên cạnh biến dẫn xuất. Không dùng việc ô thiếu trở thành 0 để tăng cỡ mẫu.

### Những điều plan này chưa khẳng định

- Chưa có kết luận mức sống tăng hay giảm.
- Câu 7 đã kiểm tra tần số kỳ vọng nhưng chưa tính thống kê χ²/p hay kết luận về tài sản.
- Câu 8 dùng ANOVA qua mô hình tuyến tính: F nếu mô hình sai số phù hợp; Wald–HC3 nếu cần xử lý phương sai khác nhau và có đủ hỗ trợ dữ liệu. Chưa fit mô hình hay đưa kết luận hệ số.
- Đã thấy vấn đề tài sản hiếm; tập nhân tố đủ điều kiện trong từng Q phải được khóa bằng diagnostics trước khi xem p.
- HC3 và điều chỉnh Holm chưa bảo đảm xấp xỉ tốt khi dữ liệu có điểm chi phối; mỗi trường hợp vẫn cần kiểm tra.
- Thiếu trọng số, PSU/tầng và mã theo dõi hộ: CI/p là suy luận theo mô hình làm việc, chưa là suy luận đầy đủ theo thiết kế khảo sát quốc gia.
- Nhiều chỉ tiêu dùng chung thu nhập, tiêu dùng hoặc cùng các hộ; tổng hợp dựa trên ý nghĩa của từng chỉ tiêu, không đếm số p-value nhỏ như các bằng chứng độc lập.

**Tiêu chí duyệt plan:** mỗi giả thuyết phải khớp đúng câu hỏi; mỗi estimator phải khớp đúng tham số; mỗi phân phối kiểm định phải có điều kiện áp dụng được giải thích. Các mục cần chốt được giữ rõ trạng thái, không chuyển thành kết luận chắc chắn bằng cách chạy thêm kiểm định.
