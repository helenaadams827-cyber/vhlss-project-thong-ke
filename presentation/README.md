# Project Thống Kê: bài thuyết trình và trang web VHLSS

## Bài thuyết trình
- `slides.pdf`: 50 trang (tối đa cho phép), 16:9, theme pastel, font Be Vietnam Pro.
- `slides.tex`: nguồn Beamer. Biên dịch bằng `xelatex slides.tex` và chạy **hai lần**. Font lấy từ `fonts/`.
- Cách sửa:
  - Mã bước: `\code{A1}`.
  - Tiêu đề (câu kết luận): `\frametitle{...}`.
  - Dòng giả thuyết: `\framesubtitle{\hyp{...}{U|M|B}}`, với U = Ủng hộ, M = Một phần, B = Bác bỏ.
  - Chân trang: `\meta{thước đo}{biểu đồ}{kiến thức}`.
  - Hình rộng kèm thẻ nhận xét: `\figcards{hình}{số cột}{\card{..}\card{..}}`. Chiều cao hình tự co theo lượng chữ trong thẻ.
  - Hình trái, thẻ phải: `\sidecards{hình}{tỷ lệ bề rộng}{\card{..}}`.
  - Màu từng bước khai báo bằng `\setstep{A}{...}`.
- Tên thành viên: sửa dòng `Thành viên nhóm: ……` ở slide tiêu đề.

## Trang web
- Link: https://claude.ai/artifact/GbFPSQhTG4zJVDVfpjJU4h
- Link đang ở chế độ “Anyone with the link”: ai có link đều mở được. Muốn đổi, vào nút **Share** trên trang.
- Mục "Hỏi dữ liệu" dùng Claude trên tài khoản của người xem; lần hỏi đầu trình duyệt sẽ xin phép.
- Mọi biểu đồ trên trang được tính trực tiếp từ dữ liệu nhúng trong trang (28.196 hộ).
- Mã nguồn nằm trong `web/`:

  | Tệp | Nội dung |
  |---|---|
  | `app_head.html` | tiêu đề trang, font |
  | `app_style.css` | màu pastel, giao diện sáng/tối |
  | `app_body.html` | khung trang |
  | `app_charts.js` | bộ vẽ biểu đồ SVG |
  | `app_engine.js` | biến, biểu thức, truy vấn |
  | `app_content.js` | các thẻ phân tích |
  | `app_main.js` | hỏi dữ liệu, tự khám phá |

- Dựng lại trang: `cd web && python build_web.py`, kết quả là `project_thong_ke.html`.

## Phân tích
- `analysis/prep.py`: làm sạch dữ liệu, ghi ra `../processed/vhlss_clean.csv`.
- `analysis/figs1.py`, `figs2.py`, `figs3.py`: vẽ hình vào `figs/` và ghi số liệu vào `numbers1/2/3.json`.
  - `figs3.py` vẽ:
    - F2–F4 (đủ sống, để dành);
    - A3 (đường CV qua năm + 63 tỉnh), A4 (thập phân vị), C5 (heatmap chi tiêu);
    - các bản `*t_*.pdf` có panel xu hướng 2010 → 2014 (B2, C2, C4, D2, I1–I2, I9);
    - E1 (lưới xu hướng), E4b (thứ hạng tỉnh qua 3 năm), E5 (thay đổi 2010 → 2014).
  - `CHECK=1 python figsX.py` in ra các chỗ chữ đè nhau trong hình.
  - `figs2.py` có heatmap tương quan tài sản ở D5.
- `analysis/style.py`: bảng màu pastel (đã chạy validate_palette) và font Be Vietnam Pro.
- Cần Python 3 với `pandas`, `numpy`, `matplotlib` (`pip install pandas numpy matplotlib`). Slide cần XeLaTeX (TeX Live) có gói `metropolis`, `tcolorbox`, `polyglossia`.

Chạy lại toàn bộ:

    cd analysis && for f in prep figs1 figs2 figs3; do python $f.py; done
    cd .. && xelatex slides.tex && xelatex slides.tex
    cd web && python build_web.py
