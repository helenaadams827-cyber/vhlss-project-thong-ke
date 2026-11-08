# Outline: Mức sống 2010–2014 — thu nhập, khả năng trang trải và điều kiện vật chất

Cập nhật 08/11/2026. [Plan chi tiết](plan_nghien_cuu_muc_song_2010_2014.md) · [Thước đo từ papers](thuoc_do_muc_song_tu_papers.md).

**Mạch bài:** nguồn lực → thu nhập có trang trải chi tiêu không → thành thị/nông thôn và Q1 → giáo dục, y tế → tài sản.

**Quy ước:** một quan sát là một hộ/năm. Hai năm coi là mẫu độc lập theo mô hình làm việc; không paired, không theo cùng hộ. Thu/chi đều cả năm; giữ `Quart` gốc; tiền thực theo giá 2010. Mỗi hộ có trọng số bằng nhau, chưa hiệu chỉnh thiết kế khảo sát quốc gia.

## I. Thu nhập và khả năng trang trải

### Câu 1. Thu nhập đầu người có cải thiện sau điều chỉnh giá không?

- **Biến:** `income / size`, với và không CPI; cùng hộ cho hai phiên bản.
- **Mẫu:** 9.399 hộ năm 2010 và 9.398 hộ năm 2014 có thu nhập/quy mô hợp lệ.
- **Giả thuyết:** $H_0:\mu_{y,2014}=\mu_{y,2010}$; $H_1$: khác nhau.
- **Test:** independent two-sample t-test, variances unknown and not assumed equal, hai phía — **Chap 7 §7.2.4**. CI và dấu chênh lệch quyết định cách diễn giải tăng/giảm. Median/CV dùng mô tả.

### Câu 2. Thu nhập có trang trải chi tiêu tốt hơn không?

Đặt $I=income$, $C=$ tổng 13 khoản chi ghi nhận, $n=size$:

| Chỉ tiêu | Công thức | Câu hỏi / phương pháp |
|---|---|---|
| Tiêu dùng thực đầu người | $c^R=(C/n)\times100/CPI$ | Giữ đối chiếu trung bình 2014–2010 bằng t hai mẫu phương sai riêng — Chap 7 §7.2.4 |
| Chênh lệch thu–chi thực đầu người | $D^R=((I-C)/n)\times100/CPI$ | Phần thu nhập còn lại sau chi ghi nhận có thay đổi? $H_0:\mu_{D,2014}=\mu_{D,2010}$; $H_1$: khác nhau. Cùng test t hai mẫu ở trên |
| Tỷ lệ hộ chi vượt thu nhập | $Z=1\{C>I\}$, $p=P(Z=1)$ | $H_0:p_{2014}=p_{2010}$; $H_1$: khác nhau. **Independent two-proportion Z-test**, pooled dưới H₀ — Chap 7 §7.4 |
| Tỷ lệ thu nhập còn lại | $M=(I-C)/I$ nếu $I>0$ | Mô tả độ dư/thiếu tương đối; chưa thêm kiểm định chỉ để tăng số phép test |

- **Phạm vi hai kiểm định thu–chi đã chốt:** toàn mẫu phạm vi cả nước và riêng Q1, Q2, Q3, Q4. Trong mỗi phạm vi, so hộ năm 2014 với hộ năm 2010; không so Q1 với Q4 bằng các test này.
- **Mẫu:** hộ đủ cả 13 khoản chi và thu nhập/quy mô hợp lệ. Tính $I-C$ trong từng hộ trước, rồi so hai mẫu năm. Giữ nhãn Quart gốc trước khi lọc thiếu.

| Phạm vi | Hộ hợp lệ 2010 | Hộ hợp lệ 2014 | Hai kiểm định chính |
|---|---|---|---|
| Toàn mẫu | 9.387 | 8.579 | Tỷ lệ $C>I$; mean $D^R$ |
| Q1 | 2.346 | 1.845 | Tỷ lệ $C>I$; mean $D^R$ |
| Q2 | 2.347 | 2.149 | Tỷ lệ $C>I$; mean $D^R$ |
| Q3 | 2.347 | 2.272 | Tỷ lệ $C>I$; mean $D^R$ |
| Q4 | 2.347 | 2.313 | Tỷ lệ $C>I$; mean $D^R$ |

Với mỗi phạm vi g: $H_0:p_{g,2014}=p_{g,2010}$ và $H_0:\mu_{D,g,2014}=\mu_{D,g,2010}$; hai H₁ tương ứng là khác nhau. Có **10 giả thuyết thu–chi chính** (5 phạm vi × 2 chỉ tiêu), mặc định hai phía. $M$ mô tả bổ sung trong cả năm phạm vi. Toàn mẫu bao gồm các Q nên các kết quả không độc lập; đưa mỗi giả thuyết vào danh sách Holm một lần.
- **Ý nghĩa:** mức dư trung bình và tỷ lệ thiếu hụt bổ sung nhau. Mean dương chưa có nghĩa mọi hộ đều trang trải đủ.
- **Giới hạn:** đây là chênh lệch theo khoản ghi nhận, chưa phải tiết kiệm thực tế hay khả năng trả nợ; thiếu tài sản thanh khoản/nợ. Thu nhập đủ chi cũng chưa tự chứng minh chất lượng sống tốt nếu nhu cầu chưa được đáp ứng.
- Giữ `fuel` thiếu; kiểm tra tổng 12 khoản bỏ nhiên liệu ở cả hai năm để đánh giá ảnh hưởng cấu phần/mất mẫu, không coi đó là sửa được tổng chi thiếu.

## II. Ai ghi nhận cải thiện?

### Câu 3. Thành thị–nông thôn: thu nhập, tiêu dùng và trang trải khác nhau thế nào?

- **Mẫu:** so riêng hộ 2010 với 2014 trong từng khu vực. Với thu nhập dùng hồ sơ thu nhập hợp lệ; với tiêu dùng/thu–chi dùng hồ sơ đủ chi.
- **Mức tiền:** thay đổi trung bình thu nhập, tiêu dùng, $D^R$ và CI — Chap 7 §7.2.4, hai mẫu độc lập, phương sai chưa biết/không giả sử bằng nhau.
- **Tỷ lệ thiếu hụt:** bảng $P(C>I)$ và CI theo khu vực/năm; ưu tiên mô tả phạm vi, chưa thêm mọi p-value.
- **Đối chiếu cuối kỳ:** tiêu dùng thành thị so với nông thôn năm 2014; $H_0:\mu_U=\mu_R$, $H_1:\mu_U\ne\mu_R$; cùng test t hai mẫu. Mẫu đủ chi: 2.692 hộ thành thị và 5.887 hộ nông thôn.
- Không suy ra hai mức tăng khác nhau hoặc khoảng cách thu hẹp từ các CI/p riêng. Tương tự, một Q có p nhỏ và Q khác không có chưa chứng minh thay đổi giữa hai Q khác nhau.

### Câu 4. Nhìn đủ Q1–Q4 rồi tập trung Q1: tiêu dùng tăng có đi cùng trang trải tốt hơn không?

- Giữ nhãn Q từng năm; thành viên Q1 có thể khác nhau. Bảng bốn Q là bước dẫn vào, không kiểm định thu nhập Q4 khác Q1 như phát hiện mới.
- **4a — Tiêu dùng Q1:** $H_0:\Delta\mu_c\le0$; $H_1:\Delta\mu_c>0$; independent t, unknown variances/not assumed equal, một phía — Chap 7 §7.2.4.
- **4b — Trang trải trong Q1–Q4:** đọc lại hai đối chiếu thu–chi của từng Q đã có ở câu 2, rồi tập trung diễn giải Q1. Bao gồm test tỷ lệ chi vượt thu và test mean $D^R$; không chạy hay tính Holm lần thứ hai cho cùng giả thuyết.
- **Mẫu đủ chi:** 2.346 hộ Q1 năm 2010 và 1.845 hộ Q1 năm 2014. Báo thêm $D^R$, $M$, CI và mức mất mẫu. Chưa gọi Q1 theo nhãn là nghèo theo chuẩn tuyệt đối.

## III. Giáo dục và y tế

### Câu 5. Nhiều hộ có chi giáo dục hơn hay nhóm có chi chi nhiều hơn?

- **5a:** chỉ báo `edu > 0`; mẫu 9.399 hộ năm 2010 và 9.398 hộ năm 2014; $H_0:p_{2014}=p_{2010}$, $H_1$: khác nhau. Z hai tỷ lệ độc lập, pooled dưới H₀ — Chap 7 §7.4.
- **5b:** chi giáo dục thực/người trong hộ có `edu > 0`; mẫu 5.963 và 5.637 hộ; $H_0:\mu^+_{e,2014}=\mu^+_{e,2010}$, $H_1$: khác nhau. t hai mẫu độc lập, phương sai chưa biết/không giả sử bằng nhau — Chap 7 §7.2.4.
- Chưa suy ra tiếp cận hay kết quả học tập vì thiếu số người đang học và kết quả giáo dục.

### Câu 6. Y tế: đang chọn lại thước đo tài chính phù hợp

- `med` là tiền thuốc; `aid` là chi chăm sóc người bệnh; `hins` là tiền bảo hiểm, giữ riêng.
- Chi y tế hoặc `(med + aid)/income` cao chưa tự cho biết mức sống xấu đi. Phần thuốc/chăm sóc đã được tính trong tổng $C$ ở câu 2.
- Hướng nghiên cứu là **khả năng đáp ứng nhu cầu sau chi chữa bệnh / bảo vệ tài chính**, không mặc định ít chi hơn là tốt hơn.
- Chưa chốt kiểm định thay thế cho câu này. Xem [papers và giới hạn đo lường](thuoc_do_muc_song_tu_papers.md#5-y-tế-đo-bảo-vệ-tài-chính-không-đồng-nhất-chi-cao-với-mức-sống-thấp). Không tự áp ngưỡng chi y tế thảm họa khi chưa có OOP đầy đủ và chuẩn nhu cầu cơ bản.

## IV. Tài sản: từng yếu tố riêng

### Câu 7. Tỷ lệ sở hữu từng tài sản có khác giữa Q1–Q4 không? — Chap 9

- Dùng 9 tài sản `oto, moto, bicycle, bed, tab, tele, tv, emachine, hmachine`; **bỏ house** theo quyết định mới.
- Riêng từng tài sản/năm, mẫu gồm hộ có Quart và tài sản hợp lệ; chỉ báo >0 là có, =0 là không, thiếu/âm chưa biết.
- $H_0:p_{Q1}=p_{Q2}=p_{Q3}=p_{Q4}$; $H_1$: có ít nhất hai tỷ lệ khác nhau.
- **Pearson χ² independence test**, bảng 4 × 2, df = 3 — **Chap 9 §9.2**. Có 18 bảng dự kiến. Cả 18 bảng hiện đạt ngưỡng tần số kỳ vọng ≥5; chưa tính χ²/p.

### Câu 8. Với từng tài sản, thu nhập thực của hộ có và không có tài sản có khác nhau không? — Chap 8

- **One-way ANOVA**, mỗi lần chỉ một factor: sở hữu tài sản đang xét, hai mức có/không. **Không interaction; không multifactor.** Q và năm chỉ chia phạm vi phân tích, không đưa vào làm factor trong cùng test.
- **Mẫu cụ thể:** trong Q và năm cố định, lấy hai nhóm hộ có/không tài sản, có thu nhập/quy mô và tài sản đó hợp lệ. Không yêu cầu đủ cả chín tài sản hay đủ khoản chi.
- **Kết quả:** thu nhập thực đầu người, không dùng mã Q như một biến kết quả liên tục.
- **Giả thuyết:** $H_0:\mu_{owner,j,q,t}=\mu_{nonowner,j,q,t}$; $H_1$: khác nhau.
- **A — Giả sử phương sai bằng nhau:** standard one-way ANOVA F-test, phương sai chung chưa biết — Chap 8 §8.1. Với hai nhóm, $F=T_{pooled}^2$; t gộp phương sai ở Chap 7 §7.2.3.
- **B — Không giả sử phương sai bằng nhau:** Welch one-way ANOVA. Với đúng hai nhóm, $F_W=T_{unequal}^2$ và bậc tự do mẫu số theo Chap 7 §7.2.4. Công thức hai mẫu đã có trong lớp; cách trình bày thành Welch ANOVA là mở rộng.
- **Đầu ra:** 9 bảng tổng hợp, mỗi bảng cho một tài sản; bên trong tách 2010/2014 và Q1–Q4, đặt kết quả A/B cạnh nhau. Đây là tối đa 72 đối chiếu có/không, mỗi đối chiếu hai phiên bản, không phải chỉ 9 kiểm định. Mỗi đối chiếu A/B dùng đúng cùng hộ.
- Không điều chỉnh đồng thời các tài sản khác. Không kết luận tài sản gây giàu/nghèo; không kết luận mối liên hệ đã thay đổi qua năm từ hai p-value riêng. Nhóm quá ít hộ có thể chỉ đủ mô tả.

## Kiểm tra và phạm vi

- Mean dùng trung bình mẫu; tỷ lệ dùng trung bình chỉ báo Bernoulli — Lecture 4/Chap 4. Không lấy hai mean năm làm hai quan sát.
- Chap 2–3: phân phối dữ liệu, CLT và ảnh hưởng đuôi. **Chap 9 chỉ dùng normality test và χ² independence theo phần đã học; chưa thêm Mann–Whitney/Kruskal–Wallis hay các test phi tham số khác.** Không chuẩn chưa tự cấm suy luận mean xấp xỉ, nhưng mẫu lớn chưa tự bảo đảm CI/p tốt.
- **Đã kiểm tra D và M:** normality test bác bỏ chuẩn trong cả năm phạm vi của hai năm; D toàn mẫu/Q4 năm 2010 có một quan sát chi phối mạnh. Năm đối chiếu tỷ lệ chi vượt thu đều đạt điều kiện số đếm. [Xem diagnostics](kiem_tra_phan_phoi_thu_chi.md). t/CI của mean vẫn cần đọc như xấp xỉ có giới hạn, chưa được xác nhận đáng tin chỉ bằng n; chưa tự đổi sang test thứ hạng.
- Kiểm định mặc định hai phía 5%, riêng 4a một phía tăng. Bản B là kết quả chính cho danh sách tài sản khi nới giả định phương sai; A trình bày theo giả định để đối chiếu. Điều chỉnh Holm cho danh sách p chính; CI 95% thường là CI riêng lẻ.
- Các thước đo mới từ papers còn là đề xuất, chưa tự đưa hết vào bài. Không còn mô hình nhiều nhân tố, HC3/Wald hay tương tác trong plan này. Đã chạy normality test/kiểm tra số đếm; chưa chạy các test thay đổi 2010–2014 hoặc điền kết luận mức sống.
