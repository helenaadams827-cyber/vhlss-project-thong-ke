# Project Thống Kê: VHLSS 2010–2014

Phân tích mô tả dữ liệu Khảo sát Mức sống Hộ gia đình Việt Nam (VHLSS) 2010, 2012 và 2014. Câu hỏi chính: hộ giàu và hộ nghèo chi tiêu, tích lũy khác nhau thế nào, và túi tiền hay nơi ở quyết định điều đó.

- Trang web tương tác: https://claude.ai/artifact/GbFPSQhTG4zJVDVfpjJU4h
- Bài thuyết trình: [`presentation/slides.pdf`](presentation/slides.pdf) (50 slide)

## Nội dung repo

| Đường dẫn | Nội dung |
|---|---|
| `processed/vhlss_merged.csv` | 3 đợt khảo sát gộp lại, chưa làm sạch (28.196 hộ × 31 cột) |
| `processed/vhlss_clean.csv` | dữ liệu đã làm sạch, có thêm nhóm tỉnh và các biến dẫn xuất (28.196 hộ × 50 cột); slide và web dùng file này |
| `presentation/analysis/` | code làm sạch (`prep.py`), vẽ hình (`figs1.py`, `figs2.py`, `figs3.py`), số liệu đã tính (`numbers*.json`) |
| `presentation/figs/` | các hình PDF dùng trong slide |
| `presentation/slides.tex`, `slides.pdf` | bài thuyết trình (Beamer, biên dịch bằng XeLaTeX) |
| `presentation/web/` | mã nguồn trang web; `project_thong_ke.html` là bản dựng sẵn, mở trực tiếp bằng trình duyệt |
| `presentation/fonts/` | font Be Vietnam Pro (giấy phép SIL OFL 1.1, xem `OFL.txt`) |

Hướng dẫn dựng lại và sửa slide, web: [`presentation/README.md`](presentation/README.md).

## Dữ liệu

Mỗi dòng là một hộ trong một năm khảo sát. Tiền tính bằng nghìn đồng/năm, theo giá của từng năm (chưa quy đổi lạm phát). Mỗi năm là một mẫu khác nhau: không có mã hộ để theo dõi cùng một hộ qua các năm, và không có trọng số mẫu.

### Cột có trong cả hai file

| Cột | Ý nghĩa |
|---|---|
| `Year` | năm khảo sát: 2010, 2012, 2014 |
| `province` | mã tỉnh (63 tỉnh) |
| `area` | 1 = thành thị, 2 = nông thôn |
| `size` | số người trong hộ |
| `income` | thu nhập cả hộ trong năm |
| `Inc_head` | thu nhập/người = `income` / `size` |
| `Quart` | nhóm thu nhập 1–4: tứ phân vị của `Inc_head` trên toàn mẫu từng năm (1 = 25% hộ nghèo nhất) |
| `rice`, `nrice` | chi gạo; chi thực phẩm khác gạo |
| `tobaco`, `nfood`, `edu` | chi thuốc lá; chi ngoài ăn uống (quần áo, đi lại, giải trí…); chi giáo dục |
| `med`, `hins`, `aid` | chi thuốc, viện phí; tiền tự đóng bảo hiểm y tế; chi hỗ trợ khám chữa bệnh |
| `water`, `elec`, `garb`, `fuel`, `fhouse` | tiền nước, điện, phí rác, nhiên liệu, sửa/xây nhà |
| `house` | giá trị căn nhà đang ở |
| `oto`, `moto`, `bicycle` | giá trị ô tô, xe máy, xe đạp |
| `tele`, `tv`, `emachine` | giá trị điện thoại, TV, máy giải trí |
| `hmachine`, `bed`, `tab` | giá trị máy gia dụng, giường, bàn ghế |

`vhlss_merged.csv` có thêm cột `year` trùng với `Year`.

### Cột thêm trong `vhlss_clean.csv`

| Cột | Ý nghĩa |
|---|---|
| `tier` | nhóm tỉnh T1–T4: tứ phân vị của hạng trung bình 3 năm, xếp theo median `Inc_head` của tỉnh (T1 = nghèo nhất) |
| `province_name`, `area_l` | tên tỉnh; "Thành thị" / "Nông thôn" |
| `tot` | tổng 13 khoản chi (trống nếu thiếu `nfood`) |
| `nec`, `unn` | chi thiết yếu (tầng 1–2 tháp Maslow: `rice nrice water elec fuel garb med hins aid fhouse`); chi không thiết yếu (`nfood edu tobaco`) |
| `food`, `util`, `health` | `rice + nrice`; `elec + water + fuel + garb`; `med + hins + aid` |
| `veh`, `tech`, `furn` | phương tiện (`oto + moto + bicycle`); công nghệ (`tele + tv + emachine`); nội thất (`bed + tab`) |
| `burden` | `nec` / `income` |
| `house_to_inc` | `house` / `income` (số năm thu nhập bằng giá trị căn nhà) |
| `overspend` | True nếu `tot` > `income` |
| `fuel_na`, `asset_na`, `house_na`, `nfood_na`, `neg_fixed` | cờ đánh dấu các ô đã xử lý khi làm sạch |

### Làm sạch (`presentation/analysis/prep.py`)

- Không xóa hộ nào.
- `fuel` trống (817 ô, gần hết ở năm 2014): điền 0 và gắn cờ `fuel_na`.
- 284 hộ thiếu cả 9 cột tài sản: điền 0 và gắn cờ `asset_na`.
- Giá trị tài sản âm (61 ô, 36 hộ): coi là ô trống.
- `house` trống: bỏ khi phân tích nhà; `fhouse` trống điền 0.
- 1 hộ thiếu `nfood`: bỏ khỏi phân tích chi tiêu.

## Nguồn

Khảo sát Mức sống Hộ gia đình Việt Nam (VHLSS) 2010, 2012, 2014, Tổng cục Thống kê.
