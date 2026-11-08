# Kiểm tra phân phối thu–chi — 08/11/2026

Đã thực hiện normality test và kiểm tra điều kiện số đếm cho hai thước đo thu–chi trong toàn mẫu và Q1–Q4. Đây là diagnostics, chưa phải kiểm định thay đổi mức sống giữa hai năm. Chưa thêm Mann–Whitney, Kruskal–Wallis, bootstrap hay permutation test.

## 1. Mẫu và phương pháp

Excel gốc, chỉ 2010/2014; đủ 13 khoản chi hợp lệ, thu nhập không âm và quy mô hộ dương; giữ Quart gốc. Tính D thực đầu người theo giá 2010 và M = (I−C)/I với thu nhập dương. Không xóa hay sửa giá trị lớn. Mỗi phạm vi/năm là một mẫu.

Normality test: Jarque–Bera theo Chap 9, trang PDF 21; tính skewness/kurtosis từ moment mẫu với mẫu số n, so công thức với SciPy. Xét thêm mức ảnh hưởng của quan sát lớn qua tỷ lệ tổng bình phương độ lệch SS.

## 2. Chênh lệch thu–chi thực đầu người D

| Phạm vi | n 2010 / 2014 | Skewness 2010 / 2014 | SS của một quan sát lớn nhất, %: 2010 / 2014 | Normality test |
|---|---|---|---|---|
| All | 9387 / 8579 | 68.64 / 12.91 | 78.41 / 17.93 | Bác bỏ chuẩn ở cả hai năm |
| Q1 | 2346 / 1845 | -4.09 / -2.13 | 10.52 / 2.86 | Bác bỏ chuẩn ở cả hai năm |
| Q2 | 2347 / 2149 | -2.57 / -3.74 | 5.01 / 8.88 | Bác bỏ chuẩn ở cả hai năm |
| Q3 | 2347 / 2272 | -2.40 / -2.78 | 5.85 / 6.06 | Bác bỏ chuẩn ở cả hai năm |
| Q4 | 2347 / 2313 | 36.93 / 10.30 | 82.46 / 24.97 | Bác bỏ chuẩn ở cả hai năm |

Cả 10 mẫu D và 10 mẫu M đều có p JB xấp xỉ nhỏ hơn 10⁻¹⁶. Không báo p bằng 0: số 0 của phần mềm là giới hạn biểu diễn; CSV lưu log10(p) theo tham chiếu χ²₂. M cũng lệch mạnh và hiện chỉ dùng mô tả.

JB dùng tham chiếu tiệm cận, không phải phân phối hữu hạn mẫu chính xác. Riêng Q1 năm 2014 có n = 1.845, dưới mốc thận trọng >2.000 mà tài liệu SciPy nêu cho JB; không diễn giải p như một chứng nhận chính xác. Độ lệch và ảnh hưởng đuôi là thông tin bổ sung.

Điểm đáng chú ý: một hộ chiếm 78,41% SS của D toàn mẫu 2010 và 82,46% trong Q4 năm đó. Đây là ảnh hưởng trong mẫu, chưa chứng minh bản ghi sai hoặc mô tả được đuôi tổng thể. Không tự xóa hộ đó.

## 3. Tỷ lệ hộ chi vượt thu nhập

Không dùng JB cho chỉ báo 0/1: nó có phân phối Bernoulli. Với Z hai tỷ lệ cần kiểm tra số có/không và kỳ vọng theo tỷ lệ gộp dưới H₀.

| Phạm vi | Số đếm quan sát nhỏ nhất | Số kỳ vọng theo tỷ lệ gộp nhỏ nhất | Ngưỡng ≥10 |
|---|---|---|---|
| All | 2501 | 2661.66 | Đạt |
| Q1 | 637 | 633.93 | Đạt |
| Q2 | 731 | 754.73 | Đạt |
| Q3 | 400 | 414.16 | Đạt |
| Q4 | 162 | 199.53 | Đạt |

Cả năm đối chiếu đạt điều kiện số đếm. Điều này hỗ trợ xấp xỉ chuẩn cho kiểm định hai tỷ lệ, chưa chứng minh giả định độc lập hay xử lý được thiên lệch do thiếu chi.

## 4. Cách dùng trong bài

- Giữ normality test và χ² independence trong Chap 9 theo nội dung đã học. Chưa thêm test thứ hạng.
- Không chuẩn của giá trị hộ chưa tự động loại t-test mẫu lớn; nhưng cỡ mẫu lớn cũng chưa đủ bảo đảm xấp xỉ tốt khi một điểm chi phối. Đặc biệt không gọi t/CI của D toàn mẫu và Q4 là đã được xác nhận đáng tin chỉ qua n.
- Phạm vi đã rút gọn: bỏ test/CI mean D khỏi plan chính, giữ D/M mô tả. Tỷ lệ chi vượt thu làm đối chiếu tài chính chính vì đã đạt điều kiện số đếm. Chưa chạy test thay đổi hoặc kết luận tăng/giảm; các test mean khác vẫn cần diagnostics đúng mẫu.
- Mann–Whitney kiểm định phân phối/thứ hạng, không tự kiểm định chênh lệch mean. Không đổi tham số để tránh kết quả kiểm tra chuẩn.
- Audit này chỉ bao gồm D, M và số đếm chi vượt thu; chưa thay thế diagnostics cho 72 nhóm so sánh tài sản hoặc các câu khác.

## 5. Dữ liệu kiểm tra và tài liệu

[20 mẫu liên tục](distribution_diagnostics_financial.csv) · [Số đếm chỉ báo](financial_indicator_counts.csv) · [Điều kiện hai tỷ lệ](financial_proportion_conditions.csv).

Tham chiếu phương pháp: [Jarque–Bera](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.jarque_bera.html), [t hai mẫu](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html), [mục tiêu kiểm định Mann–Whitney](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).
