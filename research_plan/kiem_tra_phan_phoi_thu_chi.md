# Kiểm tra phân phối thu–chi — 08/11/2026

Đã cập nhật normality test và điều kiện số đếm sau quy ước mới `fuel` trống = 0, cho toàn mẫu và Q1–Q4. Đây là diagnostics, chưa phải kiểm định thay đổi mức sống giữa hai năm. Chưa thêm Mann–Whitney, Kruskal–Wallis, bootstrap hay permutation test.

## 1. Mẫu và phương pháp

Đọc Excel gốc, chỉ 2010/2014; gán 3 ô fuel trống năm 2010 và 813 năm 2014 bằng 0 trong bản phân tích theo yêu cầu người dùng. Không điền khoản khác: còn 9/7 hộ thiếu `fhouse`. Mẫu hợp lệ là 9.390/9.391 hộ, đủ 13 khoản sau quy ước, thu nhập không âm và quy mô hộ dương; giữ Quart gốc. Tính D thực đầu người theo giá 2010 và M = (I−C)/I với thu nhập dương. Không xóa/sửa giá trị lớn hoặc sửa Excel gốc. Mỗi phạm vi/năm là một mẫu.

Fuel trống = 0 là quy ước phân tích, không phải số chi đã quan sát. [Sổ mẫu](financial_sample_audit.csv) báo số hộ có fuel ghi nhận để đối chiếu tỷ lệ mô tả; không dùng quy ước này để suy mọi khoản trống khác đều bằng 0.

Normality test: Jarque–Bera theo Chap 9, trang PDF 21; tính skewness/kurtosis từ moment mẫu với mẫu số n, so công thức với SciPy. Xét thêm mức ảnh hưởng của quan sát lớn qua tỷ lệ tổng bình phương độ lệch SS.

## 2. Chênh lệch thu–chi thực đầu người D

| Phạm vi | n 2010 / 2014 | Skewness 2010 / 2014 | SS của một quan sát lớn nhất, %: 2010 / 2014 | Normality test |
|---|---|---|---|---|
| All | 9390 / 9391 | 68.65 / 13.19 | 78.41 / 17.61 | Bác bỏ chuẩn ở cả hai năm |
| Q1 | 2346 / 2350 | -4.09 / -2.12 | 10.52 / 2.51 | Bác bỏ chuẩn ở cả hai năm |
| Q2 | 2347 / 2349 | -2.57 / -3.62 | 5.01 / 8.26 | Bác bỏ chuẩn ở cả hai năm |
| Q3 | 2349 / 2346 | -2.38 / -2.71 | 5.81 / 5.87 | Bác bỏ chuẩn ở cả hai năm |
| Q4 | 2348 / 2346 | 36.94 / 10.29 | 82.46 / 24.84 | Bác bỏ chuẩn ở cả hai năm |

Cả 10 mẫu D và 10 mẫu M đều có p JB xấp xỉ nhỏ hơn 10⁻¹⁶. Không báo p bằng 0: số 0 của phần mềm là giới hạn biểu diễn; CSV lưu log10(p) theo tham chiếu χ²₂. M cũng lệch mạnh và hiện chỉ dùng mô tả.

JB dùng tham chiếu tiệm cận, không phải phân phối hữu hạn mẫu chính xác. Sau quy ước fuel, mọi mẫu trong bảng có n >2.000; điều này vẫn không biến p tiệm cận thành chính xác. Độ lệch và ảnh hưởng đuôi là thông tin bổ sung.

Điểm đáng chú ý: một hộ chiếm 78,41% SS của D toàn mẫu 2010 và 82,46% trong Q4 năm đó. Đây là ảnh hưởng trong mẫu, chưa chứng minh bản ghi sai hoặc mô tả được đuôi tổng thể. Không tự xóa hộ đó.

## 3. Tỷ lệ hộ chi vượt thu nhập

Không dùng JB cho chỉ báo 0/1: nó có phân phối Bernoulli. Với Z hai tỷ lệ cần kiểm tra số có/không và kỳ vọng theo tỷ lệ gộp dưới H₀.

| Phạm vi | Số đếm quan sát nhỏ nhất | Số kỳ vọng theo tỷ lệ gộp nhỏ nhất | Ngưỡng ≥10 |
|---|---|---|---|
| All | 2809 | 2941.34 | Đạt |
| Q1 | 803 | 847.78 | Đạt |
| Q2 | 780 | 813.65 | Đạt |
| Q3 | 408 | 425.23 | Đạt |
| Q4 | 165 | 202.41 | Đạt |

Cả năm đối chiếu đạt điều kiện số đếm. Điều này hỗ trợ xấp xỉ chuẩn cho kiểm định hai tỷ lệ, chưa chứng minh giả định độc lập hay xử lý được thiên lệch do thiếu chi.

Hướng giả thuyết hiện tại là tỷ lệ giảm: $H_0:p_{14}\ge p_{10}$, $H_1:p_{14}<p_{10}$; Z hai tỷ lệ độc lập, pooled tại biên bằng nhau, một phía trái — Chap 7 §7.4. Chưa tính thống kê Z/p hoặc kết luận thay đổi.

## 4. Cách dùng trong bài

- Giữ normality test và χ² independence trong Chap 9 theo nội dung đã học. Chưa thêm test thứ hạng.
- Không chuẩn của giá trị hộ chưa tự động loại t-test mẫu lớn; nhưng cỡ mẫu lớn cũng chưa đủ bảo đảm xấp xỉ tốt khi một điểm chi phối. Đặc biệt không gọi t/CI của D toàn mẫu và Q4 là đã được xác nhận đáng tin chỉ qua n.
- Phạm vi đã rút gọn: bỏ test/CI mean D khỏi plan chính, giữ D/M mô tả. Tỷ lệ chi vượt thu làm đối chiếu tài chính chính vì đã đạt điều kiện số đếm. Chưa chạy test thay đổi hoặc kết luận tăng/giảm; các test mean khác vẫn cần diagnostics đúng mẫu.
- Mann–Whitney kiểm định phân phối/thứ hạng, không tự kiểm định chênh lệch mean. Không đổi tham số để tránh kết quả kiểm tra chuẩn.
- Audit này chỉ bao gồm D, M và số đếm chi vượt thu; chưa thay thế diagnostics cho 72 nhóm so sánh tài sản hoặc các câu khác.

## 5. Dữ liệu kiểm tra và tài liệu

[20 mẫu liên tục](distribution_diagnostics_financial.csv) · [Số đếm chỉ báo](financial_indicator_counts.csv) · [Điều kiện hai tỷ lệ](financial_proportion_conditions.csv).

[Code tái tạo](update_financial_diagnostics.py) · [Sổ mẫu và số ô fuel gán 0](financial_sample_audit.csv). Chạy `.venv/bin/python research_plan/update_financial_diagnostics.py` từ thư mục dự án để cập nhật bốn CSV; bảng Markdown này tóm tắt lần chạy đã đối chiếu.

Tham chiếu phương pháp: [Jarque–Bera](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.jarque_bera.html), [t hai mẫu](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html), [mục tiêu kiểm định Mann–Whitney](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html).
