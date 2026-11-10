# Thu nhập 2010–2014

Cập nhật **10/11/2026**. Bản đang dùng: [notebook bỏ top 0,1% mỗi năm](thu_nhap_4_cau_bo_top_0_1_phan_tram.ipynb).

**Kết quả chính:** sau lọc, thu nhập thực bình quân tăng **16,73%**; mean của cả bốn Q đều tăng theo các kiểm định xấp xỉ. Phương sai mẫu tăng **3,86%** và gap tuyệt đối Q4−Q1 tăng trong mẫu; chưa có bằng chứng gap giảm. Phần phương sai chưa có kiểm định F hợp lệ.

## Dữ liệu và cách tính

- Chỉ dùng **2010 và 2014** từ [Excel gốc](../dataset/VHLSS_2014.xls). Một dòng là một hộ/năm; hai năm được coi là hai mẫu độc lập, không paired.
- `income` là tổng thu nhập cả hộ trong cả năm, đơn vị nghìn đồng. `size` gồm mọi thành viên, kể cả người chưa lao động.
- Mỗi hộ có trọng số bằng nhau. Mean là trung bình của thu nhập đầu người từng hộ, không phải tổng thu nhập chia tổng số người.
- Dùng CPI bình quân năm, cùng gốc **2010 = 100**: 2010 = **100**; 2014 = **143,69**, đọc từ [CSV CPI](cpi_2010_2014.csv).
- **Đã tra cứu lại Cục Thống kê ngày 10/11/2026:** chỉ số cùng gốc vẫn đúng. Mức tăng năm 2010 là 9,19% so với 2009 và năm 2014 là 4,09% so với 2013; không lấy hai tỷ lệ này chia nhau. [Nguồn, bảng đối chiếu và phép nối chỉ số](CPI_nguon_va_cach_quy_doi.md).

$$
Y=\frac{income}{size}\times\frac{100}{CPI}\times\frac{1}{1000}.
$$

Đơn vị kết quả: **triệu đồng/người/năm, theo giá 2010**. Phương sai có đơn vị bình phương của mức tiền này.

### Lọc top 0,1%

Xếp hộ theo thu nhập đầu người trong **từng năm**, bỏ $k=\lceil0,001n\rceil=10$ hộ cao nhất. Không sửa giá trị trong Excel và không chia lại `Quart` sau lọc. Cả 20 hộ bị loại đều thuộc Q4 gốc.

| Mẫu | 2010 | 2014 |
|---|---:|---:|
| Trước lọc | 9.399 | 9.398 |
| Bị loại | 10 | 10 |
| Sau lọc | **9.389** | **9.388** |
| Q4 sau lọc | 2.340 | 2.339 |

Q1–Q3 không mất hộ. Q4 sau lọc là phần còn lại của Q4 ban đầu, không phải nhóm mới chiếm đúng 25%. Nhãn Q của từng năm không theo cùng hộ qua thời gian.

## Bốn câu hỏi, giả thuyết và kết luận

Mức ý nghĩa **5% cho từng phép kiểm định**. Theo cách trình bày trong slide Chap 7, **H₀ viết dấu “=”**; hướng tăng/giảm nằm ở H₁ và quyết định phía kiểm định. Các mean trong phần này là mean của phần hộ được giữ.

### 1. Thu nhập bình quân đầu người có tăng không?

Đặt $\Delta=\mu_{2014}-\mu_{2010}$; **H₀: $\Delta=0$; H₁: $\Delta>0$**. Estimator là chênh lệch hai mean sau lọc.

Dùng **t-test hai mẫu độc lập, phương sai tổng thể chưa biết và không giả sử bằng nhau, một phía phải — Chap 7 §7.2.4**, tính từ mẫu còn lại sau lọc.

**Kết luận:** mean tăng từ **17,598 lên 20,543**, tương đương **+2,944 triệu (+16,73%)**. Theo xấp xỉ, p ≈ **5,62×10⁻³⁴**, bác bỏ H₀. CI hai phía 95% của mức tăng: **[2,468; 3,421] triệu**.

### 2. Thu nhập bình quân trong từng Q1–Q4 có tăng không?

Với mỗi q, đặt $\Delta_q=\mu_{q,2014}-\mu_{q,2010}$; **H₀: $\Delta_q=0$; H₁: $\Delta_q>0$**.

**Cả Q1–Q4:** cùng t-test hai mẫu độc lập, phương sai tổng thể chưa biết và không giả sử bằng nhau, một phía phải — **Chap 7 §7.2.4**. Dùng số hộ và phương sai của từng Q sau lọc; không lấy hai mean năm làm hai quan sát.

| Nhóm | Mean 2010 | Mean 2014 | Thay đổi | p một phía |
|---|---:|---:|---:|---:|
| Q1 | 5,257 | 6,292 | **+19,69%** | 3,04×10⁻⁸¹ |
| Q2 | 10,382 | 13,024 | **+25,45%** | <10⁻³⁰⁰ |
| Q3 | 17,093 | 20,758 | **+21,44%** | <10⁻³⁰⁰ |
| Q4 sau lọc | 37,744 | 42,210 | **+11,83%** | 8,93×10⁻¹⁴ |

**Kết luận:** cả bốn test riêng lẻ bác bỏ H₀ theo xấp xỉ đang dùng. Không suy mức tăng giữa các Q khác nhau bằng cách so các p riêng. Giá trị p cực nhỏ được ghi bằng cận, không gọi là p bằng 0.

### 3. Độ phân hóa thu nhập — phương sai — có giảm không?

**H₀: $\sigma^2_{2014}=\sigma^2_{2010}$; H₁: $\sigma^2_{2014}<\sigma^2_{2010}$**. Tính phương sai mẫu bằng các hộ còn lại, mẫu số n−1.

F-test hai phương sai, một phía trái — **Chap 7 §7.3** — cần mô hình chuẩn phù hợp. Sau lọc, dữ liệu vẫn bác bỏ chuẩn, nên **không tính p theo F hoặc đưa ra quyết định H₀ bằng test này**. Đây không phải ANOVA.

**Kết luận mô tả:** phương sai mẫu tăng từ **271,865 lên 282,347**, tức **+3,86%**. Chưa khẳng định phương sai tổng thể tăng hay giảm bằng một kiểm định hợp lệ trong bài hiện tại. Phương sai đo phân tán tuyệt đối, không đồng nhất với Gini hay bất bình đẳng tương đối.

### 4. Gap thu nhập Q1–Q4 có giảm không?

Gap chính là **chênh lệch tiền giữa hai mean**: $G_t=\mu_{Q4,t}-\mu_{Q1,t}$. Đặt $\Delta_G=G_{2014}-G_{2010}$; **H₀: $\Delta_G=0$; H₁: $\Delta_G<0$**.

Dùng **tương phản bốn mean, xấp xỉ chuẩn, một phía trái**. SE cộng bốn thành phần $S^2/n$ của các nhóm sau lọc. Đây là vận dụng CLT và tính phương sai tổng từ **Chap 3**; không phải t-test với hai gap làm hai quan sát.

**Kết luận:** gap trong mẫu tăng từ **32,487 lên 35,918**, tức **+3,431 triệu đồng/người/năm**. Test phía giảm có Z ≈ **5,652**, p ≈ **0,99999999**: không bác bỏ H₀, **chưa có bằng chứng gap tuyệt đối giảm**. Không dùng p này để thay cho kiểm định phía tăng. Tỷ số Q4/Q1 chỉ được báo mô tả, là một thước đo khác.

## Kiểm tra phân phối và công thức trong lớp

**Chap 9 trang 21:** kiểm tra Jarque–Bera ở đúng 10 mẫu (toàn mẫu và bốn Q, mỗi năm). Các mẫu sau lọc vẫn bác bỏ chuẩn. Một điểm lớn nhất đóng góp khoảng **1,87% SS toàn mẫu 2010**, giảm từ khoảng 68% trước lọc; ảnh hưởng đuôi đã giảm nhưng không biến dữ liệu thành chuẩn.

**Lecture 4 / Chap 3:** phân biệt tham số, estimator, giá trị ước lượng và SE. CLT cho mean không tự bảo đảm phân phối F của tỷ số phương sai. **Chap 6:** không bác bỏ chưa có nghĩa chứng minh bằng nhau.

**Công thức dùng sau lọc:** với n hộ còn lại, tính $\bar Y$, $S^2$ (mẫu số n−1) và:

$$
SE(\bar Y)=\frac{S}{\sqrt n},\qquad
SE(\bar Y_{14}-\bar Y_{10})=\sqrt{\frac{S_{14}^2}{n_{14}}+\frac{S_{10}^2}{n_{10}}}.
$$

Dùng t và bậc tự do của Chap 7 §7.2.4 cho các câu mean. Toàn bộ phép tính dùng mẫu sau lọc; coi bước lọc đã cố định trong mô hình suy luận này.

## Những bản đã làm để đối chiếu

| Notebook | Vai trò |
|---|---|
| [Bỏ top 0,1%](thu_nhap_4_cau_bo_top_0_1_phan_tram.ipynb) | **Bản chính hiện tại**, bốn câu hỏi sau lọc |
| [Bốn câu trên toàn mẫu](thu_nhap_4_cau_2010_2014.ipynb) | Giữ nguyên để đối chiếu ảnh hưởng của việc lọc |
| [Khảo sát ngưỡng thu nhập cao](khao_sat_nguong_thu_nhap_cao.ipynb) | 9 phương án; khảo sát mô tả trước khi chốt top 0,1% |
| [Có và không CPI](so_sanh_thu_nhap_co_va_khong_cpi.ipynb) | Bản trước, dùng toàn mẫu; không trộn kết quả với bản sau lọc |

| Chỉ tiêu | Toàn mẫu | Sau bỏ top 0,1% |
|---|---|---|
| Mean 2010 → 2014 | 18,257 → 20,861 | 17,598 → 20,543 |
| Thay đổi phương sai mẫu | −68,29% | +3,86% |
| Gap tuyệt đối 2010 → 2014 | 35,036 → 37,098 | 32,487 → 35,918 |

## File kiểm tra và cách chạy

- [Sổ mẫu trước/sau lọc](thu_nhap_bo_top_0_1_so_mau.csv).
- [20 hộ đã loại, có năm và dòng Excel](thu_nhap_bo_top_0_1_ho_bi_loai.csv).
- [Kết quả mean: n, SE, thống kê, p và CI](thu_nhap_bo_top_0_1_mean_tests.csv).
- Khảo sát ngưỡng: [theo năm](khao_sat_nguong_thu_nhap_cao_theo_nam.csv), [so sánh](khao_sat_nguong_thu_nhap_cao_so_sanh.csv), [phân phối](khao_sat_nguong_thu_nhap_cao_phan_phoi.csv).

Clone/download toàn repo để giữ đường dẫn `dataset/` và `bao_cao_vhlss/`. Đã chạy bằng **Python 3.12.3**. Cài thư viện bằng `python -m pip install -r bao_cao_vhlss/requirements_thu_nhap.txt`, mở notebook bằng VS Code/Jupyter, chọn môi trường Python rồi **Run All**. Có thể đọc ngay kết quả đã lưu trên GitHub mà không chạy lại.

Bản chính đã chạy 11 cell code: đối chiếu CPI từ nguồn Cục Thống kê, kiểm tra đúng 10 hộ/năm, nhãn Q, mean toàn mẫu từ các Q, SE theo công thức lớp và t/df/p/CI toàn mẫu, Q1–Q4 với SciPy; Excel gốc được giữ nguyên. Chỉ bổ sung nguồn CPI vào các notebook trước, không thay số CPI hoặc phép tính thu nhập.

**Giới hạn:** chưa có trọng số/tầng/cụm khảo sát và giá vùng; bộ lọc và nhãn Q được coi như đã cho, chưa tính riêng bất định các ngưỡng; các p/CI không bảo đảm đồng thời. Kết luận áp dụng cho phần hộ sau lọc theo mô hình làm việc, không có nghĩa mọi hộ đều tăng thu nhập hoặc mức sống toàn diện đã tốt hơn.
