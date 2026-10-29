# Project Thống Kê: báo cáo VHLSS 2010 · 2012 · 2014

## Bản nộp chính (bám dàn ý Thẻ 2 của nhóm)

| Tệp | Nội dung |
|---|---|
| `bao_cao.pdf` / `bao_cao.tex` | **Báo cáo tiếng Việt, 28 trang** — 25 hình, 17 bảng, 10 hộp công thức |
| `bao_cao_en.pdf` / `bao_cao_en.tex` | **Báo cáo tiếng Anh**, bản dịch sát, cùng số liệu |
| `../report_EDA.ipynb` | Notebook EDA tiếng Việt, 34 ô mã, seaborn — sinh ra toàn bộ hình trong báo cáo |
| `../report_EDA_en.ipynb` | Notebook EDA tiếng Anh (đã đối chiếu: cho kết quả giống hệt bản tiếng Việt) |
| `figs_nb/`, `figs_nb_en/` | 26 hình mỗi bộ, do notebook lưu ra |

Cấu trúc báo cáo: **Phần 1** tổng quan dữ liệu · **Phần 2** xử lý dữ liệu (ô trống, chia nhóm, mean/median) · **Phần 3** phân tích (thu nhập – chi tiêu – tài sản) · kết luận · hạn chế · phụ lục mã nguồn. Mỗi mục phân tích có đủ *công thức → biểu đồ → mô tả → kết luận*.

Dựng lại từ đầu:
```
python report_EDA.ipynb        # chạy notebook -> figs_nb/
cd presentation && xelatex bao_cao.tex && xelatex bao_cao.tex
```

## Bản cũ (giữ lại để tham khảo)


## Báo cáo chi tiết

- `report.tex` / `report.pdf`: **37 trang A4**, bản đọc đầy đủ — 9 mục + 2 phụ lục (63 tỉnh, cách tái lập); 27 bảng, 23 hình.
- Mọi bảng số do `analysis/report_tables.py` sinh ra vào `tables/*.tex` rồi `\input` vào báo cáo, **không gõ số bằng tay**.
- Hình: 6 hình riêng của báo cáo (`analysis/figsR.py` → `figs/r01…r06.pdf`) + 15 hình dùng chung với bản trình bày (`figs/g*.pdf`).
- Biên dịch: `xelatex report.tex` (chạy 2 lần cho mục lục và tham chiếu).
- Thứ tự dựng lại từ đầu: `prep.py` → `report_tables.py` → `figsR.py` → `figs20.py` → `xelatex report.tex`.

## Bài thuyết trình

Có **hai bản**, dùng chung font, màu và hình:

| Bản | Tệp | Dung lượng | Dùng khi |
|---|---|---|---|
| Bản 20 phút | `slides_20min.tex` / `.pdf` | 20 trang | trình bày trên lớp, 3 phần: thu nhập – chi tiêu – tài sản |
| Bản đầy đủ | `slides.tex` / `.pdf` | 50 trang | bản lưu, 6 bước A–F + phần bên lề |

Bản 20 phút lấy hình từ `analysis/figs20.py` (tệp `figs/g*.pdf`) và số liệu từ `analysis/numbers20.json`.
Mạch: (0) chọn median thay mean → (1.1–1.3) khoảng cách thu nhập → (2.1–2.7) chi tiêu, chi vượt thu, cơ cấu → (3.1–3.4) tài sản → kết luận + hạn chế.

- `slides.pdf`: 49 trang, 16:9, theme pastel, font Be Vietnam Pro.
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
- `analysis/report_tables.py`: sinh 24 bảng LaTeX của báo cáo vào `tables/`, ghi `numbersR.json`.
- `analysis/figsR.py`: 12 hình riêng của báo cáo (`figs/r01…r12.pdf`): phân phối 4 nhóm Q, boxplot theo năm, thập phân vị, SD/CV, cơ cấu 13 khoản, sở hữu tài sản, **bản đồ nhiệt tương quan**, **boxplot có chấm** (63 tỉnh, giá nhà), **Pareto**, **bubble theo tỉnh**, rổ chi hộ vượt thu.
- `analysis/figs20.py`: vẽ 15 hình `figs/g01…g15` cho bản 20 phút, ghi số liệu vào `numbers20.json`. Chạy `CHECK=1 python analysis/figs20.py` để dò chữ đè nhau.
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
