# Outline: Mức sống thay đổi thế nào từ 2010 đến 2014?

Cập nhật 08/11/2026. Đây là bản đọc nhanh; công thức, estimator và điều kiện đầy đủ nằm trong [plan chi tiết](plan_nghien_cuu_muc_song_2010_2014.md).

**Mạch bài:** nguồn lực và tiêu dùng → phạm vi cải thiện → giáo dục và gánh nặng chăm sóc → điều kiện vật chất.

## Sample và loại test: quy ước cụ thể

**Một quan sát là một hộ trong một năm.** Ví dụ mẫu thu nhập 2010 là vector 9.399 giá trị `income / size` của 9.399 hộ, không phải một số mean của năm. Tính hai mean từ hai vector hộ rồi mới lập thống kê kiểm định. Dùng chỉ tiêu đầu người không biến mỗi thành viên thành một quan sát độc lập.

Hai năm được coi là mẫu độc lập theo mô hình đã thống nhất; không ghép hộ theo dòng. Mẫu của các câu khác nhau có thể trùng hộ; điều đó không biến từng phép so sánh năm thành paired test, và cũng không có nghĩa các kết quả khác câu độc lập với nhau.

| Câu | Tên test chính xác | Quan hệ giữa mẫu | Phương sai tổng thể | Phía kiểm định |
|---|---|---|---|---|
| 1, 2 | **Independent two-sample t-test, unknown variances, not assumed equal** — Chap 7 §7.2.4 | Hộ 2014 so với hộ 2010 | Chưa biết; dùng hai phương sai mẫu riêng, không gộp | Hai phía |
| 3a | Cùng công thức hai mẫu ở trên; ưu tiên estimate/CI | 2014 so với 2010, riêng từng khu vực và chỉ tiêu | Chưa biết, không giả sử bằng nhau | CI hai phía; không thêm p vào luận điểm chính |
| 3b | **Independent two-sample t-test, unknown variances, not assumed equal** — Chap 7 §7.2.4 | Thành thị so với nông thôn, cùng năm 2014 | Chưa biết, không giả sử bằng nhau | Hai phía |
| 4 | **Independent two-sample t-test, unknown variances, not assumed equal** — Chap 7 §7.2.4 | Q1 năm 2014 so với Q1 năm 2010 | Chưa biết, không giả sử bằng nhau | Một phía tăng |
| 5a | **Independent two-proportion Z-test**, pooled proportion dưới $H_0$ — Chap 7 §7.4 | Các chỉ báo `edu > 0` của hai năm | Không phải phân loại known/unknown variance của test mean; tham số là hai tỷ lệ chưa biết | Hai phía |
| 5b, 6 | **Independent two-sample t-test, unknown variances, not assumed equal** — Chap 7 §7.2.4 | Hai nhóm hộ theo năm, lọc đúng điều kiện từng câu | Chưa biết, không giả sử bằng nhau | Hai phía |
| 7 | **Pearson chi-square test of independence** trên bảng 4 × 2 — Chap 9 §9.2 | Một mẫu hộ của một năm cho từng tài sản, phân vào tám ô | Không có giả định cùng phương sai thu nhập | Bác bỏ ở đuôi phải của χ²; $H_1$ là có liên hệ |
| 8A | **Partial F-tests in a multifactor linear model with selected interactions** | Hộ của cả hai năm gộp trong từng Q; các hộ độc lập theo mô hình | Chưa biết nhưng giả sử phương sai sai số chung; ước lượng từ residual mean square | F đuôi phải cho các ràng buộc hệ số bằng 0 |
| 8B | **HC3 heteroskedasticity-robust Wald tests** cho đúng các ràng buộc của 8A | Cùng mẫu và mô hình 8A | Chưa biết, không áp đặt phương sai chung | Wald χ² đuôi phải; không phải F cổ điển |

Các test mean của bài **không phải one-sample**, không phải known-variance Z-test và không phải paired t-test. Phương pháp Chap 7 §7.2.4 thường có tên phần mềm là Welch two-sample t-test; không cần chứng minh hai phương sai khác nhau trước khi dùng.

### Mẫu của từng câu, trên dữ liệu hiện tại

| Câu | Mẫu 2010 | Mẫu 2014 | Giá trị của một quan sát |
|---|---|---|---|
| 1 | 9.399 hộ có thu nhập/quy mô hợp lệ | 9.398 hộ tương ứng | Thu nhập đầu người danh nghĩa hoặc thực |
| 2 | 9.387 hộ đủ cả 13 khoản chi và quy mô hợp lệ | 8.579 hộ tương ứng | Tiêu dùng thực đầu người |
| 3a | Riêng từng khu vực, lấy đúng mẫu của biến thu nhập hoặc tiêu dùng | Tương tự, riêng từng khu vực năm 2014 | Thu nhập hoặc tiêu dùng thực đầu người |
| 3b | Không dùng 2010 cho phép so sánh cuối kỳ | 2.692 hộ thành thị và 5.887 hộ nông thôn đủ chi | Tiêu dùng thực đầu người |
| 4 | 2.346 hộ `Quart = 1` đủ chi | 1.845 hộ `Quart = 1` đủ chi | Tiêu dùng thực đầu người |
| 5a | 9.399 hộ có `edu` hợp lệ, giữ cả chi 0 | 9.398 hộ tương ứng | 1 nếu `edu > 0`, 0 nếu `edu = 0` |
| 5b | 5.963 hộ có `edu > 0`, quy mô hợp lệ | 5.637 hộ tương ứng | Chi giáo dục thực đầu người |
| 6 | 2.350 hộ Q1 có `med`, `aid`, thu nhập hợp lệ và thu nhập dương | 2.352 hộ tương ứng | Tỷ số `(med + aid)/income` |
| 7 | Mọi hộ có `Quart` và giá trị tài sản đang xét hợp lệ | Làm thành mẫu/bảng riêng năm 2014 | Một cặp nhãn `(Quart, sở hữu có/không)` |
| 8A/8B | Hộ trong Q đang xét, đủ thu nhập/quy mô và các tài sản thật sự dùng | Gộp cùng Q năm 2014; có biến năm để phân biệt | Một thu nhập thực đầu người kèm năm và các chỉ báo tài sản |

Cỡ mẫu câu 7 khác theo tài sản; ví dụ TV dùng 9.218 hộ năm 2010 và 9.354 hộ năm 2014. Cỡ mẫu cuối của câu 8 chưa khóa vì cần chốt tập nhân tố đủ điều kiện; hai phiên bản A/B phải dùng cùng các hộ. Số hộ từng khu vực và từng tài sản được ghi đầy đủ trong plan chi tiết. Các số trên là kiểm tra mẫu hợp lệ, chưa phải kết quả giả thuyết.

### Câu 8 thuộc loại ANOVA nào?

- **Không phải one-way ANOVA. Cũng không phải một mô hình chỉ có hai factor.** Mỗi tài sản có/không là một factor riêng.
- Trong mỗi Q, nếu đủ chín tài sản thì có **10 factor hai mức**: năm + chín tài sản. Khi phải giảm tập tài sản còn $k_q$ biến, số factor là $k_q+1$.
- **Có tương tác chọn lọc:** năm × từng tài sản, để hỏi mối liên hệ thu nhập–sở hữu có thay đổi từ 2010 sang 2014 không. Không có tương tác giữa các tài sản với nhau hoặc các tương tác bậc cao khác.
- **Quart là điều kiện chia mẫu thành bốn mô hình**, không phải một factor bổ sung bên trong từng mô hình. Không dùng repeated-measures ANOVA.
- Chap 8 §8.3 dạy **two-factor ANOVA with interaction**. Câu 8 mở rộng ý tưởng này sang nhiều factor; phần mở rộng và cách xử lý thiết kế không cân bằng cần được giải thích riêng. Nếu chỉ xét năm và TV, đó mới là ví dụ hai factor có tương tác, nhưng chưa điều chỉnh cho các tài sản khác như mô hình chính.

## I. Nguồn lực và tiêu dùng có cải thiện không?

### Câu 1. Thu nhập đầu người năm 2014 có khác năm 2010 sau điều chỉnh giá không?

- **Biến:** `income / size`, năm và CPI; làm hai phiên bản danh nghĩa và giá 2010 trên cùng các hộ.
- **Giả thuyết:** $H_0:\mu_{y,2014}-\mu_{y,2010}=0$; $H_1:\mu_{y,2014}-\mu_{y,2010}\ne0$.
- **Estimator:** chênh lệch trung bình thu nhập đầu người của hai mẫu.
- **Phương pháp:** kiểm định t hai mẫu độc lập, không giả sử phương sai bằng nhau, kèm CI — **Chap 7 §7.2.4**.
- **Trả lời được:** thay đổi trung bình nguồn lực; chiều dương và độ bất định phù hợp mới hỗ trợ nhận định tăng. Median và CV bổ sung mô tả, chưa suy ra mọi hộ cùng tăng.

### Câu 2. Tổng tiêu dùng ghi nhận thực đầu người có thay đổi không?

- **Biến:** tổng 13 khoản `rice, nrice, tobaco, nfood, edu, med, hins, aid, water, elec, garb, fuel, fhouse`, chia `size`, điều chỉnh CPI.
- **Giả thuyết:** $H_0:\mu_{c,2014}-\mu_{c,2010}=0$; $H_1:\mu_{c,2014}-\mu_{c,2010}\ne0$, trên hộ đủ chi.
- **Estimator:** chênh lệch hai trung bình tiêu dùng thực đầu người.
- **Phương pháp:** t hai mẫu phương sai riêng và CI — **Chap 7 §7.2.4**.
- **Kiểm tra bắt buộc:** giữ `fuel` trống là thiếu; báo mất mẫu. Đối chiếu tổng 12 khoản không gồm `fuel` ở cả hai năm để xem ảnh hưởng cấu phần và mẫu. Kết quả hộ đủ chi chưa tự đại diện mọi hộ.

## II. Cải thiện xuất hiện ở những nhóm nào?

### Câu 3. Thành thị và nông thôn có ghi nhận cải thiện; khoảng cách cuối kỳ ra sao?

- **Biến:** `area`, năm, thu nhập và tiêu dùng thực đầu người.
- **Trong từng khu vực:** ước lượng $\Delta_{a,X}=\mu_{a,X,2014}-\mu_{a,X,2010}$, với $X$ là thu nhập hoặc tiêu dùng; báo CI. Giả thuyết tương ứng là $H_0:\Delta_{a,X}=0$ và $H_1:\Delta_{a,X}\ne0$.
- **Đối chiếu cuối kỳ:** $H_0:\mu_{c,urban,2014}=\mu_{c,rural,2014}$; $H_1$: hai trung bình khác nhau.
- **Phương pháp:** chênh lệch trung bình và CI/kiểm định hai mẫu phương sai riêng — **Chap 7 §7.2.4**.
- **Trả lời được:** thay đổi trong mỗi khu vực và khoảng cách năm 2014; chưa kiểm định hai mức tăng khác nhau hoặc khoảng cách đã thu hẹp.

### Câu 4. Tiêu dùng thực của nhóm ít nguồn lực nhất có tăng không?

- **Dẫn vào:** mô tả thu nhập, tiêu dùng và thay đổi tiêu dùng của đủ Q1–Q4, rồi tập trung Q1.
- **Biến:** `Quart = 1`, năm, tiêu dùng thực đầu người trên hộ đủ chi.
- **Giả thuyết:** $H_0:\mu_{c,Q1,2014}-\mu_{c,Q1,2010}\le0$; $H_1:\mu_{c,Q1,2014}-\mu_{c,Q1,2010}>0$.
- **Estimator:** chênh lệch trung bình tiêu dùng thực của Q1 từng năm.
- **Phương pháp:** t hai mẫu độc lập phương sai riêng, một phía tăng — **Chap 7 §7.2.4**. Báo thêm CI hai phía 95% để thể hiện độ bất định.
- **Trả lời được:** nhóm Q1 từng năm có mức tiêu dùng cao hơn không; chưa theo dõi cùng hộ. Giữ nhãn Quart gốc, kiểm tra thiếu chi riêng trong Q1.

## III. Nguồn lực cao hơn đi cùng thay đổi gì trong giáo dục và chăm sóc?

### Câu 5. Chi giáo dục thay đổi do nhiều hộ có chi hơn hay do nhóm có chi chi nhiều hơn?

- **Biến:** `edu`, `size`, năm, CPI.
- **5a — Tỷ lệ có chi:** $p_t=P(edu_t>0)$; $H_0:p_{2014}=p_{2010}$; $H_1:p_{2014}\ne p_{2010}$. Estimator là tỷ lệ hộ có chi. Dùng **Z hai tỷ lệ — Chap 7 §7.4**.
- **5b — Mức chi trong nhóm có chi:** $e^R=(edu/size)\times100/CPI$; $H_0:E(e^R_{2014}\mid edu>0)=E(e^R_{2010}\mid edu>0)$; $H_1$: khác nhau. Dùng chênh lệch hai trung bình có điều kiện và **t hai mẫu phương sai riêng — Chap 7 §7.2.4**.
- **Liên kết:** trung bình chi chung = tỷ lệ có chi × trung bình của nhóm có chi, trên hồ sơ hợp lệ chung.
- **Trả lời được:** thay đổi chi giáo dục ghi nhận; chưa đo tiếp cận/chất lượng vì thiếu số người đang học và kết quả học tập.

### Câu 6. Gánh nặng thuốc và chăm sóc người bệnh của Q1 có giảm không?

- **Biến:** $B=(med+aid)/income$ của từng hộ Q1; yêu cầu thu nhập dương, giữ cả tử số bằng 0. `hins` trình bày riêng.
- **Giả thuyết:** $H_0:\mu_{B,Q1,2014}-\mu_{B,Q1,2010}=0$; $H_1:\mu_{B,Q1,2014}-\mu_{B,Q1,2010}\ne0$.
- **Estimator:** chênh lệch trung bình các tỷ số hộ; không lấy tỷ số hai tổng tiền của nhóm.
- **Phương pháp:** t hai mẫu phương sai riêng — **Chap 7 §7.2.4**; kiểm tra kỹ tỷ số lớn. CPI chung triệt tiêu trong tỷ số cùng năm.
- **Trả lời được:** phần thu nhập dành cho hai khoản chi có thay đổi không. Chiều âm và CI thích hợp mới hỗ trợ giảm gánh nặng; chưa chứng minh sức khỏe tốt hơn.

## IV. Điều kiện vật chất còn phân biệt mức sống thế nào?

### Câu 7. Sở hữu từng tài sản có liên quan đến nhóm Q1–Q4 không? — Chap 9

- **Biến:** `Quart` và sở hữu có/không của từng biến `oto, moto, bicycle, bed, tab, tele, tv, emachine, hmachine`; làm riêng 2010 và 2014.
- **Giả thuyết:** với mỗi tài sản/năm, $H_0:p_{Q1}=p_{Q2}=p_{Q3}=p_{Q4}$, tương đương sở hữu độc lập với Quart; $H_1$: có ít nhất hai tỷ lệ khác nhau.
- **Estimator:** tỷ lệ sở hữu trong mỗi Q.
- **Phương pháp:** **χ² độc lập trên bảng 4 × 2 — Chap 9 §9.2**; df = 3. Có 18 bảng dự kiến; kiểm tra tần số kỳ vọng, không yêu cầu thu nhập chuẩn hay cùng phương sai.
- **Trả lời được:** tài sản nào có tỷ lệ sở hữu khác giữa các Q trong từng năm. Một năm có ý nghĩa, năm kia không chưa chứng minh mối liên hệ đã thay đổi.

### Câu 8. Khi xét các tài sản cùng lúc, tài sản nào còn phân biệt thu nhập trong từng Q? — Chap 8

- **Biến kết quả:** thu nhập thực đầu người. **Nhân tố:** các chỉ báo sở hữu tài sản và năm. Phân tích riêng từng Q.
- **Mô hình:** các nhân tố tài sản cộng gộp, năm và tương tác năm × từng tài sản. Xét điều kiện của đủ chín tài sản; tài sản quá hiếm có thể chỉ đủ mô tả trong một số Q.
- **Giả thuyết cho tài sản $j$:** năm 2010 $H_0:\beta_j=0$; năm 2014 $H_0:\beta_j+\gamma_j=0$; thay đổi qua thời gian $H_0:\gamma_j=0$. Mỗi giả thuyết đối là khác 0. Có thêm kiểm định chung cho cả nhóm hệ số.
- **Estimator:** hệ số mô hình và các tổ hợp hệ số tương ứng; chúng là mối liên hệ có điều chỉnh cho những tài sản khác thực sự có trong mô hình.
- **Phương pháp:** **ANOVA nhiều nhân tố và tương tác — Chap 8**, trình bày qua mô hình tuyến tính cho thiết kế không cân bằng, với hai phiên bản song song: **A giả sử phương sai bằng nhau, dùng F cổ điển; B không giả sử phương sai bằng nhau, dùng Wald–HC3** (ngoài lớp, đã được cho phép). Cùng mẫu, tập tài sản, mô hình và giả thuyết; lập bảng SS–df–MS và đối chiếu SE, CI, p của hai bản. F chỉ có diễn giải cổ điển khi các điều kiện sai số phù hợp; HC3 vẫn cần đủ hỗ trợ dữ liệu và điều kiện xấp xỉ.
- **Trả lời được:** liên hệ của mỗi tài sản với thu nhập sau điều chỉnh, và liên hệ đó có đổi qua thời gian không. Chưa suy ra quan hệ nhân quả hoặc “không có ý nghĩa = không còn phản ánh mức sống”.

### Đối chiếu hai phiên bản ANOVA

| Nội dung | A — Giả sử phương sai bằng nhau | B — Không giả sử phương sai bằng nhau |
|---|---|---|
| Hệ số, mẫu, mô hình, SS | Giống bản B | Giống bản A |
| Độ bất định | SE và CI theo covariance cổ điển | SE và CI theo HC3 |
| Kiểm định | F từng phần | Wald χ² xấp xỉ |
| Vai trò | Đối chiếu theo giả định cổ điển | Suy luận chính của câu 8 khi cho phép phương sai khác nhau |

Hai phiên bản là kiểm tra độ nhạy của cùng phân tích. Báo cả hai, không chọn theo p nhỏ hơn. p Holm cho danh sách kiểm định chính dùng kết quả bản B của câu 8; bản A báo p theo giả định để đối chiếu. Chi tiết công thức và cách diễn giải nằm ở mục 11 của plan đầy đủ.

## Kiểm tra và nguyên tắc chung

- **Chap 2–3:** mô tả phân phối và cơ sở phân phối lấy mẫu; không mặc định mẫu lớn đủ khắc phục mọi đuôi mạnh.
- **Lecture 4/Chap 4:** xác định parameter → estimator → estimate cho từng câu.
- **Lecture 5 và Chap 6:** CI, giả thuyết, mức ý nghĩa; không bác bỏ chưa chứng minh bằng nhau.
- **Chap 9 bổ sung:** Jarque–Bera trên biến liên tục/phần dư để chẩn đoán; không dùng JB cho biến sở hữu nhị phân.
- Kiểm tra phân phối và ảnh hưởng ở đúng các mẫu dùng suy luận; phương sai mẫu không cần bằng nhau từng con số để giả định phương sai tổng thể chung có thể phù hợp.
- Mặc định kiểm định hai phía 5%, riêng câu 4 giữ một phía đã thống nhất. Báo p thô và p Holm cho danh sách kiểm định khoa học; CI 95% thông thường là CI riêng lẻ.
- Hai năm là mẫu độc lập theo mô hình làm việc; mọi khoản thu/chi là cả năm. Thiếu trọng số và thông tin thiết kế: chưa coi CI/p là đã hiệu chỉnh đầy đủ khảo sát quốc gia.
- Chưa chạy kiểm định hay điền kết luận. Mục tiêu là khớp **câu hỏi → tham số → giả thuyết → phương pháp → phạm vi kết luận**.
