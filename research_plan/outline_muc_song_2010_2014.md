# Outline: Mức sống 2010–2014 — thu nhập, khả năng trang trải và điều kiện vật chất

Cập nhật 08/11/2026. [Plan chi tiết](plan_nghien_cuu_muc_song_2010_2014.md) · [Thước đo từ papers](thuoc_do_muc_song_tu_papers.md).

**Mạch bài:** nguồn lực → khả năng trang trải toàn mẫu và Q1–Q4 → thành thị/nông thôn → chi giáo dục → tài sản.

**Phạm vi giữ lại:** sáu câu dưới đây; bỏ câu y tế và các hướng chưa chốt từ papers. Giữ hai phiên bản ANOVA đã thống nhất. Các kiểm định mean/ANOVA chỉ được diễn giải khi diagnostics của đúng mẫu hỗ trợ xấp xỉ; thiết kế câu hỏi rõ chưa đồng nghĩa mọi mẫu đã đạt điều kiện.

**Quy ước:** một quan sát là một hộ/năm. Hai năm coi là mẫu độc lập theo mô hình làm việc; không paired, không theo cùng hộ. Thu/chi đều cả năm; giữ `Quart` gốc; tiền thực theo giá 2010. Theo yêu cầu mới, ô `fuel` trống được gán 0 trong dữ liệu phân tích; các khoản khác thiếu vẫn giữ thiếu. Mỗi hộ có trọng số bằng nhau, chưa hiệu chỉnh thiết kế khảo sát quốc gia.

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
| Chênh lệch thu–chi thực đầu người | $D^R=((I-C)/n)\times100/CPI$ | Mô tả mean/median và độ phân tán; bỏ kiểm định mean D khỏi suy luận chính vì ảnh hưởng quan sát lớn đã phát hiện |
| Tỷ lệ hộ chi vượt thu nhập | $Z=1\{C>I\}$, $p=P(Z=1)$ | $H_0:p_{2014}\ge p_{2010}$; $H_1:p_{2014}<p_{2010}$. **Independent two-proportion Z-test, một phía trái**, pooled tại biên bằng nhau — Chap 7 §7.4 |
| Tỷ lệ thu nhập còn lại | $M=(I-C)/I$ nếu $I>0$ | Mô tả độ dư/thiếu tương đối; chưa thêm kiểm định chỉ để tăng số phép test |

- **Phạm vi kiểm định tỷ lệ chi vượt thu:** toàn mẫu phạm vi cả nước và riêng Q1, Q2, Q3, Q4. Trong mỗi phạm vi, so hộ năm 2014 với hộ năm 2010; không so Q1 với Q4 bằng các test này.
- **Mẫu:** hộ đủ cả 13 khoản chi sau khi gán `fuel` trống bằng 0, thu nhập/quy mô hợp lệ. Tính $I-C$ trong từng hộ trước, rồi so hai mẫu năm. Giữ nhãn Quart gốc trước khi lọc thiếu.

| Phạm vi | Hộ hợp lệ 2010 | Hộ hợp lệ 2014 | Kiểm định thu–chi chính |
|---|---|---|---|
| Toàn mẫu | 9.390 | 9.391 | Tỷ lệ $C>I$ |
| Q1 | 2.346 | 2.350 | Tỷ lệ $C>I$ |
| Q2 | 2.347 | 2.349 | Tỷ lệ $C>I$ |
| Q3 | 2.349 | 2.346 | Tỷ lệ $C>I$ |
| Q4 | 2.348 | 2.346 | Tỷ lệ $C>I$ |

Với mỗi phạm vi g: $H_0:p_{g,2014}\ge p_{g,2010}$; $H_1:p_{g,2014}<p_{g,2010}$. Có **5 giả thuyết tỷ lệ thu–chi chính**, một phía trái ở mức 5%; đối chiếu tiêu dùng toàn mẫu vẫn hai phía. $D^R$ và $M$ chỉ mô tả bổ sung trong cả năm phạm vi. Toàn mẫu bao gồm các Q nên các kết quả không độc lập; đưa mỗi giả thuyết vào danh sách Holm một lần.

Tỷ lệ tính bằng số hộ $C>I$ chia tổng số hộ hợp lệ, bao gồm cả hộ không vượt thu; không phải số tiền vượt trung bình trong nhóm thiếu hụt. Lấy chênh lệch 2014−2010: $Z_{test}<-1,645$ là miền bác bỏ chưa điều chỉnh ở mức 5%; danh sách kết luận chính dùng p Holm. Chọn hướng giảm theo câu hỏi trước khi chạy kiểm định, không đổi hướng theo p. Nếu giữ test hai phía và CI chênh lệch nằm hoàn toàn dưới 0 thì vẫn có bằng chứng tỷ lệ giảm.
- **Đọc sâu Q1 ngay trong bảng các Q:** dùng kết quả tỷ lệ đã có, thêm mức thu nhập/tiêu dùng thực, $D^R$ và $M$ để mô tả; không thêm câu hỏi hay kiểm định riêng cho Q1. Giữ nhãn Q từng năm nên thành viên có thể khác nhau; chưa gọi Q1 là nghèo theo chuẩn tuyệt đối. Báo rõ số hộ còn thiếu khoản chi khác.
- **Ý nghĩa:** mức dư trung bình và tỷ lệ thiếu hụt bổ sung nhau. Mean dương chưa có nghĩa mọi hộ đều trang trải đủ.
- **Giới hạn:** đây là chênh lệch theo khoản ghi nhận, chưa phải tiết kiệm thực tế hay khả năng trả nợ; thiếu tài sản thanh khoản/nợ. Thu nhập đủ chi cũng chưa tự chứng minh chất lượng sống tốt nếu nhu cầu chưa được đáp ứng.
- `fuel` trống = 0 là quy ước phân tích do người dùng chốt, không phải giá trị quan sát được. Báo số ô được gán và đối chiếu tỷ lệ trên nhóm có `fuel` ghi nhận để thấy ảnh hưởng quy ước; không gán 0 cho `fhouse` còn thiếu.

## II. Ai ghi nhận cải thiện?

### Câu 3. Thành thị–nông thôn: thu nhập, tiêu dùng và trang trải khác nhau thế nào?

- **Mẫu:** so riêng hộ 2010 với 2014 trong từng khu vực. Với thu nhập dùng hồ sơ thu nhập hợp lệ; với tiêu dùng/thu–chi dùng hồ sơ đủ chi.
- **Mức tiền:** thay đổi trung bình thu nhập, tiêu dùng và CI — Chap 7 §7.2.4, hai mẫu độc lập, phương sai chưa biết/không giả sử bằng nhau; chỉ báo CI khi diagnostics phù hợp. $D^R$ giữ mô tả, không thêm CI/test mean D.
- **Tỷ lệ thiếu hụt:** bảng $P(C>I)$ và CI theo khu vực/năm; ưu tiên mô tả phạm vi, chưa thêm mọi p-value.
- **Đối chiếu cuối kỳ:** tiêu dùng thành thị so với nông thôn năm 2014; $H_0:\mu_U=\mu_R$, $H_1:\mu_U\ne\mu_R$; cùng test t hai mẫu. Mẫu đủ chi sau quy ước fuel: 2.781 hộ thành thị và 6.610 hộ nông thôn.
- Không suy ra hai mức tăng khác nhau hoặc khoảng cách thu hẹp từ các CI/p riêng. Tương tự, một Q có p nhỏ và Q khác không có chưa chứng minh thay đổi giữa hai Q khác nhau.

## III. Chi giáo dục

### Câu 4. Nhiều hộ có chi giáo dục hơn hay nhóm có chi chi nhiều hơn?

- **4a:** chỉ báo `edu > 0`; mẫu 9.399 hộ năm 2010 và 9.398 hộ năm 2014; $H_0:p_{2014}=p_{2010}$, $H_1$: khác nhau. Z hai tỷ lệ độc lập, pooled dưới H₀ — Chap 7 §7.4.
- **4b:** chi giáo dục thực/người trong hộ có `edu > 0`; mẫu 5.963 và 5.637 hộ; $H_0:\mu^+_{e,2014}=\mu^+_{e,2010}$, $H_1$: khác nhau. t hai mẫu độc lập, phương sai chưa biết/không giả sử bằng nhau — Chap 7 §7.2.4.
- Chưa suy ra tiếp cận hay kết quả học tập vì thiếu số người đang học và kết quả giáo dục.

## IV. Tài sản: từng yếu tố riêng

### Câu 5. Tỷ lệ sở hữu từng tài sản có khác giữa Q1–Q4 không? — Chap 9

- Dùng 9 tài sản `oto, moto, bicycle, bed, tab, tele, tv, emachine, hmachine`; **bỏ house** theo quyết định mới.
- Riêng từng tài sản/năm, mẫu gồm hộ có Quart và tài sản hợp lệ; chỉ báo >0 là có, =0 là không, thiếu/âm chưa biết.
- $H_0:p_{Q1}=p_{Q2}=p_{Q3}=p_{Q4}$; $H_1$: có ít nhất hai tỷ lệ khác nhau.
- **Pearson χ² independence test**, bảng 4 × 2, df = 3 — **Chap 9 §9.2**. Có 18 bảng dự kiến. Cả 18 bảng hiện đạt ngưỡng tần số kỳ vọng ≥5; chưa tính χ²/p.

### Câu 6. Với từng tài sản, thu nhập thực của hộ có và không có tài sản có khác nhau không? — Chap 8

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
- **Đã kiểm tra D và M:** normality test bác bỏ chuẩn trong cả năm phạm vi của hai năm; D toàn mẫu/Q4 năm 2010 có một quan sát chi phối mạnh. Vì vậy bỏ test/CI mean D khỏi plan chính, giữ mô tả. Năm đối chiếu tỷ lệ chi vượt thu đều đạt điều kiện số đếm. [Xem diagnostics](kiem_tra_phan_phoi_thu_chi.md). Các mean khác vẫn phải kiểm tra đúng mẫu trước khi dùng t/ANOVA; không tự đổi sang test thứ hạng.
- Mức ý nghĩa 5%; riêng tỷ lệ chi vượt thu dùng một phía trái, các test thay đổi mean và tỷ lệ chi giáo dục giữ hai phía. ANOVA và χ² dùng miền bác bỏ phía phải cho giả thuyết có khác biệt. Bản B là kết quả chính cho danh sách tài sản khi nới giả định phương sai; A trình bày theo giả định để đối chiếu. Điều chỉnh Holm cho danh sách p chính; CI 95% thường là CI riêng lẻ.
- Bỏ khỏi bài các câu chưa chốt: y tế, chuẩn nghèo FGT chưa có ngưỡng, equivalence scale và chỉ số tài sản PCA. Các khoản thuốc/chăm sóc/bảo hiểm vẫn nằm trong tổng chi 13 khoản; bỏ câu y tế không thay định nghĩa tổng chi. Không dùng mô hình nhiều nhân tố, HC3/Wald hay tương tác. Đã chạy normality test/kiểm tra số đếm; chưa chạy các test thay đổi 2010–2014 hoặc điền kết luận mức sống.
