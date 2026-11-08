# Outline: Mức sống thay đổi thế nào từ 2010 đến 2014?

Cập nhật 08/11/2026. Đây là bản đọc nhanh; công thức, estimator và điều kiện đầy đủ nằm trong [plan chi tiết](plan_nghien_cuu_muc_song_2010_2014.md).

**Mạch bài:** nguồn lực và tiêu dùng → phạm vi cải thiện → giáo dục và gánh nặng chăm sóc → điều kiện vật chất.

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
