# Đối chiếu CPI với Cục Thống kê

Đã tra cứu lại ngày **10/11/2026**. **CPI dùng trong bài vẫn là 2010 = 100; 2014 = 143,69**, cùng gốc năm 2010. Không cần thay các kết quả thu nhập đã tính.

## Phân biệt các số CPI

| Chỉ tiêu | 2010 | 2014 |
|---|---:|---:|
| CPI bình quân năm, **năm trước = 100** | 109,19 | 104,09 |
| Mức tăng CPI bình quân so với năm trước | 9,19% | 4,09% |
| CPI tháng 12, **tháng 12 năm trước = 100** | 111,75 | 101,84 |
| CPI bình quân, **cùng gốc 2010 = 100** — dùng cho bài | **100,00** | **143,69** |

Nguồn trực tiếp:

- [Báo cáo kinh tế–xã hội năm 2010](https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2019/04/tinh-hinh-kinh-te-xa-hoi-thang-12-va-nam-2010/): phần giá tiêu dùng.
- [Báo cáo kinh tế–xã hội năm 2014](https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2019/07/tinh-hinh-kinh-te-xa-hoi-nam-2014/): phần giá tiêu dùng và chú thích [4].
- [Niên giám thống kê 2017](https://www.nso.gov.vn/wp-content/uploads/2019/10/Nien-giam-2017-pdf.pdf): **bảng 250, trang in 629**, cột 2010/2014, dòng **“Năm 2010 = 100”** xác nhận **100,00 / 143,69**. Đây là kiểm tra lại cùng hai năm trong một bảng niên giám của cơ quan thống kê.

**109,19 và 104,09 có hai năm so sánh khác nhau.** Không chia 104,09 cho 109,19 để quy giá 2014 về 2010. Chọn 2010 = 100 là đặt năm gốc, không có nghĩa giá năm 2010 không tăng so với 2009.

## Kiểm tra bằng cách nối chỉ số bình quân năm

Các mức tăng bình quân trong báo cáo 2014 và chú thích [4]:

| Năm | Tăng so với năm trước | Chỉ số năm trước = 100 |
|---|---:|---:|
| 2011 | 18,58% | 118,58 |
| 2012 | 9,21% | 109,21 |
| 2013 | 6,60% | 106,60 |
| 2014 | 4,09% | 104,09 |

$$
CPI_{2014\mid2010=100}
=100\times1,1858\times1,0921\times1,0660\times1,0409
=143,694473792\approx143,69.
$$

Đây là phép tính lại từ các tỷ lệ công bố đã làm tròn, khớp chỉ số cùng gốc đến hai chữ số thập phân. Không nhân thêm mức tăng năm 2010 vì điểm xuất phát đã là giá năm 2010.

## Áp dụng vào thu nhập

Vì `income` là thu nhập **cả năm**, dùng CPI bình quân năm:

$$
income_{2014}^{giá\ 2010}=income_{2014}\times\frac{100}{143,69}
=\frac{income_{2014}}{1,4369}.
$$

Thu nhập năm 2010 giữ nguyên. Phương sai đổi theo bình phương hệ số quy đổi. CPI chung chưa điều chỉnh chênh lệch giá giữa địa bàn hoặc rổ tiêu dùng từng hộ.

[CSV tỷ lệ và nguồn để kiểm tra từ code](cpi_doi_chieu_nguon_cuc_thong_ke.csv) · [CSV chỉ số đang dùng](cpi_2010_2014.csv) · [README thu nhập](README_thu_nhap.md).
