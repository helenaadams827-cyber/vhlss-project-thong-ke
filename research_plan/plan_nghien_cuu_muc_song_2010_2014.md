# Plan nghiên cứu mức sống: 2010 và 2014

Cập nhật 08/11/2026. [Outline đọc nhanh](outline_muc_song_2010_2014.md) · [Các thước đo từ papers](thuoc_do_muc_song_tu_papers.md).

**Mạch bài:** thu nhập thực → khả năng trang trải toàn mẫu và Q1–Q4 → thành thị/nông thôn → chi giáo dục → từng tài sản riêng.

**Phạm vi đã chốt:** sáu câu; bỏ câu y tế, FGT chưa có ngưỡng, equivalence scale và chỉ số tài sản PCA. Chín tài sản, không xét `house`; one-way ANOVA có/không từng tài sản với hai phiên bản phương sai, không nhiều nhân tố/tương tác. Chênh lệch thu–chi D và tỷ lệ còn lại M chỉ mô tả; kiểm định khả năng trang trải dùng tỷ lệ chi vượt thu nhập. Chưa tính kết quả kiểm định thay đổi mức sống; đã chạy normality test và kiểm tra số đếm cho thu–chi, xem [diagnostics](kiem_tra_phan_phoi_thu_chi.md). Các test mean/ANOVA còn lại phải đạt kiểm tra của đúng mẫu trước khi diễn giải, không coi việc giữ câu hỏi là đã xác nhận điều kiện.

## 1. Định nghĩa dữ liệu và sample

- Mỗi quan sát là **một hộ trong một năm**. Mẫu thu nhập 2010 là vector giá trị của 9.399 hộ, không phải một số mean năm; 2014 tương tự với 9.398 hộ.
- Mẫu giữa hai năm coi là độc lập theo mô hình làm việc đã thống nhất. Không ghép hộ theo dòng, không paired t-test qua thời gian. Cùng hộ có thể xuất hiện ở nhiều câu, nên các câu không phải bằng chứng độc lập.
- Các khoản thu/chi là tổng cả năm, nghìn đồng. `income` là thu nhập cả hộ; `size` gồm mọi thành viên. `income / size` chưa phải thu nhập của mỗi người lao động. Mỗi hộ được tính trọng số bằng nhau.
- `nfood` không bao gồm các khoản chi riêng. `aid` là tiền chi chăm sóc người bệnh. `med` là tiền thuốc; `hins` là chi bảo hiểm.
- Giữ `Quart` gốc trước lọc thiếu; Q1 là nhóm thu nhập thấp nhất theo nhãn từng năm, chưa phải chuẩn nghèo tuyệt đối. Không theo cùng hộ và chưa tính riêng bất định của điểm cắt nhóm.
- Tài sản dương là có, 0 là không; thiếu/âm là chưa biết. Điện/nước/rác chỉ là khoản chi, chưa đo tiếp cận dịch vụ. Không xét `house` theo yêu cầu mới.
- Theo yêu cầu mới, chỉ ô `fuel` trống được gán 0 trong bản phân tích; không sửa Excel gốc và không gán 0 cho khoản thiếu khác. Đây là quy ước, không xác nhận hộ thực sự không chi nhiên liệu. Mỗi câu lọc đúng biến cần dùng, không dùng chung một complete-case mask cho mọi câu.
- Thiếu trọng số/PSU/tầng và mã theo dõi: các CI/p là suy luận theo mô hình làm việc, chưa hiệu chỉnh đầy đủ thiết kế khảo sát quốc gia.

## 2. Biến phân tích

Đặt $I=income$, $n=size$, $P_t=CPI_t$; $P_{2010}=100$, $P_{2014}=143.69$.

$$
y^N=I/n,\qquad y^R=(I/n)\frac{100}{P_t}.
$$

$$
C=rice+nrice+tobaco+nfood+edu+med+hins+aid+water+elec+garb+fuel+fhouse.
$$

Chỉ tính $C$ khi đủ cả 13 khoản hợp lệ sau khi gán `fuel` trống bằng 0; khoản khác còn thiếu thì không tính tổng cho hộ đó. Có 3 ô fuel trống năm 2010 và 813 năm 2014; sau xử lý còn 9/7 hộ thiếu `fhouse`. Đây là tổng chi/tiêu dùng theo quy ước của bài, chưa phải aggregate phúc lợi chính thức đầy đủ. Không cộng giá trị tài sản/nhà. Bỏ câu hỏi y tế riêng không loại `med`, `hins`, `aid` khỏi tổng chi.

$$
c^R=(C/n)\frac{100}{P_t},\qquad
D^R=((I-C)/n)\frac{100}{P_t}.
$$

$$
M=(I-C)/I\quad(I>0),\qquad Z=\mathbf1\{C>I\}.
$$

- $D^R$: chênh lệch thu–chi thực đầu người, thể hiện độ lớn tiền còn lại/thiếu theo các khoản ghi nhận.
- $M$: phần thu nhập còn lại tương đối. $M<0$ khi chi vượt thu; CPI chung triệt tiêu trong tỷ số.
- $Z$: hộ chi vượt thu nhập trong năm. $\hat p=\sum Z_i/N$ là tỷ lệ hộ có tình trạng này.
- Tính $I-C$ và $Z$ **trong từng hộ trước**. Thu nhập và chi tiêu của cùng hộ có thể tương quan; phương sai của $D^R$ phải tính trực tiếp từ các chênh lệch hộ, không cộng hai phương sai như hai mẫu độc lập.
- $D^R>0$ hoặc $M>0$ chưa tự là tiết kiệm thực tế, còn $Z=1$ chưa tự chứng minh không trả được chi phí: file thiếu nợ, tài sản thanh khoản và toàn bộ dòng tiền. Thu nhập trang trải mức chi thấp cũng chưa chứng minh nhu cầu đều được đáp ứng.

## 3. Quy tắc test và công thức dùng chung

### Test t hai mẫu — Independent two-sample t-test: unknown variances, not assumed equal

**Chap 7 §7.2.4, trang PDF 14.** Hai mẫu A/B độc lập, hai phương sai tổng thể chưa biết và không ép bằng nhau. Tên phần mềm thường là Welch two-sample t-test.

$$
\widehat\Delta=\bar X_A-\bar X_B,\quad
SE=\sqrt{S_A^2/n_A+S_B^2/n_B},\quad
T=\frac{\widehat\Delta-\Delta_0}{SE}.
$$

$$
\nu=\frac{(S_A^2/n_A+S_B^2/n_B)^2}
{(S_A^2/n_A)^2/(n_A-1)+(S_B^2/n_B)^2/(n_B-1)}.
$$

Dưới H₀ tại $\Delta_0=0$, dùng $T\approx t_\nu$. CI hai phía 95% là $\widehat\Delta\pm t_{\nu,0.975}SE$. $S_g^2$ dùng mẫu số $n_g-1$. Không cần chứng minh phương sai khác nhau trước khi dùng công thức.

Đây không phải one-sample test, không phải known-variance Z-test và không phải paired test. Độc lập, phương sai hữu hạn và xấp xỉ lấy mẫu phù hợp phải được xem xét; dữ liệu tiền lệch phải chưa cho t chính xác.

### P — Independent two-proportion Z-test

**Chap 7 §7.4, trang PDF 22.** Mỗi quan sát là chỉ báo Bernoulli. Với $H_0:p_A=p_B$:

$$
\hat p_g=x_g/n_g,\quad \hat p=(x_A+x_B)/(n_A+n_B),\qquad
Z_{test}=\frac{\hat p_A-\hat p_B}{\sqrt{\hat p(1-\hat p)(1/n_A+1/n_B)}}\approx N(0,1).
$$

CI chênh lệch tỷ lệ dùng SE không gộp:

$$
(\hat p_A-\hat p_B)\pm z_{0.975}
\sqrt{\hat p_A(1-\hat p_A)/n_A+\hat p_B(1-\hat p_B)/n_B}.
$$

Kiểm tra số có/không quan sát và kỳ vọng theo tỷ lệ gộp; lấy ngưỡng thận trọng ≥10 để dùng xấp xỉ. Đây là test hai tỷ lệ, không phải test mean với phương sai đã biết.

**Riêng câu 2b — muốn kiểm định tỷ lệ chi vượt thu giảm:** lấy A = 2014, B = 2010. Đặt $H_0:p_{14}\ge p_{10}$, $H_1:p_{14}<p_{10}$. Chap 7 §7.4 trình bày tại biên $p_{14}=p_{10}$, dùng đúng thống kê Z ở trên và p một phía trái $\Phi(Z_{test})$. Miền bác bỏ thô 5%: $Z_{test}<-1,645$; các kết luận trong danh sách chính dựa p đã điều chỉnh Holm. Có thể báo thêm cận trên một phía 95% cho $p_{14}-p_{10}$ bằng $\widehat\Delta_p+z_{0.95}SE_{unpooled}$; cận âm hỗ trợ hướng giảm. CI hai phía 95% ở trên vẫn báo để thể hiện độ lớn, nhưng không bắt buộc nằm dưới 0 để test một phía 5% bác bỏ.

Hướng giảm được chốt theo câu hỏi trước khi chạy test, không đổi hướng để lấy p nhỏ. Nếu dùng test hai phía 5% đã định trước và CI 95% của $p_{14}-p_{10}$ nằm hoàn toàn dưới 0, vẫn có bằng chứng tỷ lệ giảm; chỉ bác bỏ bằng nhau mà không xét chiều thì chưa đủ. Đây là tỷ lệ hộ, không phải mức tiền vượt thu có điều kiện trên $C>I$.

### Quy tắc đọc kết quả

Mức ý nghĩa $\alpha=5\%$; riêng tỷ lệ chi vượt thu dùng một phía trái, các test mean và tỷ lệ chi giáo dục giữ hai phía. ANOVA và χ² dùng miền bác bỏ phía phải cho giả thuyết có khác biệt. Báo estimate, CI và p phù hợp. “Có khác biệt” chưa xác định chiều tốt/xấu; không bác bỏ chưa chứng minh bằng nhau. CI 95% thông thường là khoảng riêng lẻ, chưa có bảo đảm đồng thời.

## 4. Câu hỏi và giả thuyết

### Câu 1 — Thu nhập thực đầu người có thay đổi không?

- **Biến:** $y^R$; đối chiếu $y^N$ trên cùng hồ sơ.
- **Mẫu:** toàn bộ hộ có thu nhập/quy mô hợp lệ của 2010 so với 2014.
- **Tham số:** $\Delta_y=E(y^R_{2014})-E(y^R_{2010})$.
- **H₀:** $\Delta_y=0$; **H₁:** $\Delta_y\ne0$.
- **Estimator/test:** chênh lệch hai mean; t hai mẫu, hai phía. Hai bản CPI trả lời thay đổi danh nghĩa và theo giá 2010; chúng không độc lập với nhau.
- Mean, median, phương sai, CV làm bối cảnh. Không đưa hai CV năm vào t-test và không suy CV thay đổi từ test mean.

### Câu 2 — Thu nhập có trang trải chi tiêu tốt hơn không?

Đặt $V_t=1$ khi đủ hồ sơ thu/chi/quy mô sau quy ước `fuel` trống = 0. Tham số có điều kiện trên $V_t=1$ và quy ước này; kết quả chưa tự suy rộng sang hộ còn thiếu chi.

| Đối chiếu | Tham số và giả thuyết | Estimator | Test |
|---|---|---|---|
| 2a: tiêu dùng thực | $\Delta_c=E(c^R_{14}\mid V_{14}=1)-E(c^R_{10}\mid V_{10}=1)$; H₀ = 0, H₁ ≠ 0 | Chênh lệch hai mean | t hai mẫu, hai phía |
| Mô tả chênh lệch thu–chi | Mức $D^R$ và chênh lệch mô tả giữa năm | Mean/median, độ phân tán của $D^R$ | Không test/CI mean D trong plan chính: đã phát hiện ảnh hưởng quan sát lớn |
| 2b: tỷ lệ chi vượt thu có giảm? | $p_t=P(C>I\mid V_t=1)$; H₀ $p_{14}\ge p_{10}$, H₁ $p_{14}<p_{10}$ | $\hat p_{14}-\hat p_{10}$ | P, một phía trái, pooled tại biên bằng nhau |

#### Phạm vi toàn mẫu và Q1–Q4 đã chốt

Đặt $g\in\{All,Q1,Q2,Q3,Q4\}$. Trong mỗi phạm vi, so hai mẫu hộ độc lập của 2010 và 2014. Với All bỏ điều kiện nhóm; với Q giữ nhãn Quart của chính năm đó:

$$
p_{g,t}=P(C>I\mid g_t,V_t=1),\qquad
\mu_{D,g,t}=E(D^R\mid g_t,V_t=1).
$$

| Chỉ tiêu, trong từng g | H₀ | H₁ | Estimator / test |
|---|---|---|---|
| Tỷ lệ chi vượt thu | $p_{g,14}-p_{g,10}\ge0$ | $p_{g,14}-p_{g,10}<0$ | $\hat p_{g,14}-\hat p_{g,10}$; P — hai tỷ lệ độc lập, một phía trái, pooled tại biên bằng nhau |

Có 5 giả thuyết tỷ lệ thu–chi chính, một phía trái 5%, chưa tính đối chiếu tiêu dùng 2a vẫn hai phía. $D^R$ và $M=(I-C)/I$ báo mô tả độ dư/thiếu trong cả năm phạm vi; bỏ năm test mean D và không thêm test mean M. Báo p thô và p Holm cho danh sách chính của toàn bài; cùng một giả thuyết không được đưa vào nhiều lần vì xuất hiện ở nhiều phần trình bày.

Mỗi dòng kiểm định tỷ lệ dự kiến gồm: phạm vi, n hai năm, tỷ lệ hai năm, thay đổi 2014−2010 theo điểm phần trăm, CI 95%, thống kê Z, p thô, p Holm và note về mẫu/diagnostics. $D^R$ báo mô tả cùng đơn vị tiền giá 2010/người/năm, không kèm p/CI mean D.

Toàn mẫu có cùng các hộ của bốn Q, nên các kết quả không độc lập. Đây là thay đổi theo thời gian **trong từng phạm vi**, không phải kiểm định Q1 khác Q4 hay mức cải thiện đồng đều. Không suy khác biệt giữa hai mức thay đổi từ việc một p có ý nghĩa còn p kia không. “Phạm vi cả nước” chỉ phạm vi mẫu; chưa có trọng số để gọi là ước lượng quốc gia đầy đủ.

Kiểm tra phân phối/đuôi của $D^R$ và số có/không của Z riêng cho từng g/năm. Báo tỷ lệ thiếu trước/sau xử lý fuel và số hộ được bổ sung trong đủ năm phạm vi, không chỉ toàn mẫu hoặc Q1.

**Diễn giải Q1 trong bảng Q1–Q4:** dùng chính kiểm định tỷ lệ chi vượt thu đã có của Q1; thêm mức thu nhập, tiêu dùng thực, $D^R$ và $M$ làm bối cảnh mô tả. Không đặt lại câu hỏi Q1 hoặc thêm kiểm định một phía cho tiêu dùng Q1. Đây là so nhóm thu nhập thấp nhất theo nhãn từng năm, không theo cùng hộ hay đo giảm nghèo tuyệt đối. Không test thu nhập Q4 khác Q1 như một phát hiện mới.

$D^R$ trả lời độ lớn dư/thiếu; $p$ trả lời bao nhiêu hộ thiếu theo dòng thu/chi ghi nhận. Đọc cùng mức thu nhập/tiêu dùng và phân phối $M$; không dùng một mean dương để kết luận tất cả hộ trang trải đủ. Việc tiêu dùng tăng không được mặc định là tốt khi không xét nguồn lực và nhu cầu.

**Quy ước fuel và kiểm tra ảnh hưởng:** tổng 13 khoản có fuel trống = 0 là bản chính. Không gán 0 cho `fhouse` còn thiếu. Đặt tỷ lệ mô tả bản chính cạnh tỷ lệ trên nhóm đủ chi và có fuel được ghi nhận, báo n tương ứng để thấy ảnh hưởng của việc bổ sung hộ. Đối chiếu này không xác nhận giá trị nhiên liệu bị thiếu thực sự bằng 0. [Sổ mẫu](financial_sample_audit.csv) lưu số ô gán và số đếm nhóm có fuel ghi nhận; Excel gốc được giữ nguyên.

### Câu 3 — Thành thị/nông thôn thay đổi thế nào?

**3a:** với từng khu vực $a$ và chỉ tiêu $X\in\{y^R,c^R\}$, ước lượng $\Delta_{a,X}=E(X_{14}\mid a)-E(X_{10}\mid a)$, thêm điều kiện hợp lệ của X. Giả thuyết tham chiếu H₀ $\Delta_{a,X}=0$, H₁ khác 0; ưu tiên estimate/CI theo công thức t hai mẫu khi diagnostics phù hợp, không thêm mọi p vào luận điểm chính. Tỷ lệ chi vượt thu báo mô tả/CI theo khu vực; $D^R$ và $M$ chỉ mô tả, không thêm test/CI mean.

**3b:** riêng 2014, so tiêu dùng thành thị với nông thôn: H₀ $\mu_{c,U}=\mu_{c,R}$; H₁ khác nhau. Test t hai mẫu, hai phía. Kiểm định này chưa trả lời khoảng cách đã thu hẹp từ 2010.

### Câu 4 — Giáo dục: nhiều hộ có chi hay nhóm có chi chi nhiều hơn?

- **4a:** $D_e=1\{edu>0\}$; $p_{e,t}=P(edu_t>0)$. H₀ $p_{e,14}=p_{e,10}$; H₁ khác nhau. Estimator là chênh lệch tỷ lệ; P hai phía. Giữ chi 0, loại thiếu.
- **4b:** $e^R=(edu/size)100/CPI$, chỉ trong nhóm `edu > 0`. H₀ $E(e^R_{14}\mid edu>0)=E(e^R_{10}\mid edu>0)$; H₁ khác nhau. Estimator chênh lệch mean có điều kiện; t hai mẫu hai phía.
- Trên hồ sơ hợp lệ chung, $E(e^R)=P(edu>0)E(e^R\mid edu>0)$: thay đổi mean chung có thể nằm ở một hoặc cả hai thành phần. Không gọi hai kết quả là độc lập.
- Thiếu số người đi học/kết quả giáo dục: chưa đo được tiếp cận, chất lượng hoặc chi mỗi người học. CPI chung chưa là giá giáo dục riêng.

### Câu 5 — Sở hữu tài sản có liên quan Quart không? — Chap 9

Chín biến: `oto`, `moto`, `bicycle`, `bed`, `tab`, `tele`, `tv`, `emachine`, `hmachine`. Bỏ `house`. Chỉ báo $A_j=1$ nếu giá trị dương, 0 nếu 0; thiếu/âm chưa xác định.

Với tài sản j/năm t: $p_{j,q,t}=P(A_j=1\mid Q=q,t)$.

- **H₀:** $p_{j,1,t}=p_{j,2,t}=p_{j,3,t}=p_{j,4,t}$; **H₁:** có ít nhất hai tỷ lệ khác nhau.
- **Estimator:** $\hat p_{j,q,t}=x_{j,q,t}/n_{j,q,t}$; báo tỷ lệ và chênh lệch để thể hiện độ lớn liên hệ.
- **Mẫu:** hộ có Q và tài sản j hợp lệ trong một năm; không lọc theo đủ chín tài sản hoặc đủ chi.
- **Test:** Pearson chi-square independence, bảng 4 × 2, df = 3 — Chap 9 §9.2, trang PDF 11–13.

$$
E_{qa}=R_qC_a/N,\qquad
\chi^2=\sum_{q,a}(O_{qa}-E_{qa})^2/E_{qa}\approx\chi^2_3.
$$

Có 18 bảng dự kiến. Đã kiểm tra cả 18 bảng có kỳ vọng tối thiểu ≥5, nhỏ nhất khoảng 20,16; chưa tính χ²/p. Số kỳ vọng là điều kiện, không bắt buộc mọi số quan sát ≥5. Không yêu cầu phương sai thu nhập bằng nhau hay thu nhập chuẩn. Bác bỏ chưa nói mọi cặp Q đều khác; hai p riêng qua năm chưa là test thay đổi mối liên hệ.

### Câu 6 — One-way ANOVA riêng từng tài sản — Chap 8

**Câu hỏi đã chốt:** trong một Q và năm cố định, thu nhập thực của hộ có và không có tài sản j có khác nhau không?

- **Biến kết quả:** $y^R$, không phải mã Q.
- **Một factor duy nhất:** sở hữu j, hai mức 0/1. Năm và Q chỉ chọn mẫu. Không two-factor, không multifactor, không interaction, không repeated measures.
- **Mẫu 1:** hộ sở hữu j trong Q/năm đang xét, thu nhập/quy mô và j hợp lệ.
- **Mẫu 0:** hộ không sở hữu j trong đúng Q/năm đó, cùng điều kiện hợp lệ. Không cần đủ những tài sản khác.
- **H₀:** $\mu_{1,j,q,t}=\mu_{0,j,q,t}$; **H₁:** khác nhau.
- **Estimator:** $\widehat\delta_{j,q,t}=\bar y^R_{1,j,q,t}-\bar y^R_{0,j,q,t}$.

Đây là mối liên hệ thô trong phạm vi Q/năm, không điều chỉnh cho tài sản khác và chưa là tác động nhân quả. Khi giữ nhãn Q cố định, việc thu nhập bị giới hạn trong khoảng nhóm cũng cần được lưu ý khi đọc phân phối/CI.

## 5. Hai phiên bản one-way ANOVA

Hai bản dùng cùng tài sản, Q, năm và **đúng cùng hộ**. Hệ số/chênh lệch mean giống nhau; cách chuẩn hóa thống kê và độ bất định khác nhau. Không dùng HC3/Wald trong thiết kế mới này.

### A — Unknown but equal population variances: standard one-way ANOVA

**Chap 8 §8.1, trang PDF 6–8.** Với nhóm $g\in\{0,1\}$, $N=n_0+n_1$, $k=2$:

$$
SS_B=\sum_g n_g(\bar y_g-\bar y)^2,\quad
SS_E=\sum_g\sum_i(y_{ig}-\bar y_g)^2,\quad SS_T=SS_B+SS_E.
$$

| Nguồn | SS | df | MS | F |
|---|---|---|---|---|
| Giữa hai nhóm | $SS_B$ | 1 | $MS_B=SS_B$ | $MS_B/MS_E$ |
| Trong nhóm | $SS_E$ | $N-2$ | $MS_E=SS_E/(N-2)$ | |
| Tổng | $SS_T$ | $N-1$ | | |

Dưới H₀ và mô hình độc lập, chuẩn, phương sai chung: $F\sim F_{1,N-2}$. Phương sai chung **chưa biết**, ước lượng bằng $MS_E$; không phải known variance.

Với hai nhóm, $F=T_{pooled}^2$, trong đó t gộp phương sai là Chap 7 §7.2.3, trang 13. Hai phép này trả lời cùng H₀ và có cùng p hai phía; không báo chúng như hai bằng chứng độc lập.

### B — Unknown variances, not assumed equal: Welch one-way ANOVA

Với đúng hai nhóm, dùng thống kê t và df của công thức t hai mẫu ở mục 3 rồi trình bày:

$$
F_W=T_{unequal}^2\approx F_{1,\nu}\quad\text{dưới H}_0.
$$

Vì vậy công thức thực chất đã có ở Chap 7 §7.2.4. Đây là cách biểu diễn hai nhóm của Welch one-way ANOVA; không phải $MS_B/MS_E$ cổ điển khi phương sai khác nhau. CI chênh lệch mean dùng SE/df riêng ở mục 3. Tên và cách xử lý phương sai của hai phiên bản được đối chiếu với [tài liệu one-way ANOVA](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html).

Hai bản vẫn có cùng bảng SS mô tả dữ liệu gốc; không tạo bảng SS giả để làm $F_W$ bằng tỷ số MS cổ điển. Bản B là kết quả chính khi cho phép phương sai khác nhau; bản A là đối chiếu dưới giả định cổ điển. Không chọn theo p nhỏ hơn.

### Đầu ra và số lượng phép kiểm định

- **9 bảng tổng hợp**, mỗi bảng một tài sản; tách 2010/2014 và Q1–Q4 thành tám dòng đối chiếu. Mỗi dòng báo n có/không, mean, chênh lệch/CI, F A và df/p A, F Welch và df/p B, p Holm B, diagnostics/trạng thái đủ điều kiện. Bảng SS–df–MS chi tiết cho từng đối chiếu đặt ngay dưới hoặc trong phụ lục notebook.
- Tối đa $9\times4\times2=72$ đối chiếu có/không; hai phiên bản của mỗi đối chiếu là phân tích độ nhạy cùng dữ liệu, không phải hai nghiên cứu độc lập.
- Nếu một nhóm không có hộ, không có đối chiếu. Nếu chỉ có một hộ, không ước lượng được phương sai riêng cho B: báo mô tả và trạng thái thiếu thông tin thay vì ép p. Việc n ≥2 cũng chưa tự bảo đảm xấp xỉ tốt; kiểm tra mất cân đối/đuôi/ảnh hưởng riêng.
- Một năm có p nhỏ và năm kia không chưa kiểm định khác biệt của hai chênh lệch. Thiết kế đơn giản mới **không có kiểm định tương tác/thay đổi liên hệ qua năm**; chỉ đặt các ước lượng/CI cạnh nhau. Muốn kết luận trực tiếp về thay đổi cần một câu hỏi và test bổ sung được bàn riêng.
- Không bác bỏ H₀ chưa chứng minh tài sản không còn phân biệt thu nhập về mặt kinh tế hoặc đã phổ biến.

## 6. Distribution check, estimators và nhiều phép kiểm định

**Phạm vi Chap 9 đã chốt:** dùng normality test và Pearson χ² independence; không thêm Mann–Whitney, Kruskal–Wallis hay các phép rank/resampling vào plan. Chỉ thêm phương pháp khi câu hỏi/điều kiện thực sự đòi hỏi, không vì dữ liệu hộ không chuẩn mà tự đổi tham số mean.

**Diagnostics đã thực hiện:** [bảng kiểm tra thu–chi](kiem_tra_phan_phoi_thu_chi.md) bao gồm 10 mẫu D, 10 mẫu M và điều kiện số đếm của năm đối chiếu tỷ lệ. JB bác bỏ chuẩn ở các mẫu liên tục; một hộ đóng góp 78,41% SS của D toàn mẫu 2010, 82,46% trong Q4. Vì ảnh hưởng mạnh này, bỏ test/CI mean D khỏi plan chính, giữ mô tả; không phải cứ JB bác bỏ là phải bỏ test t. Các số đếm tỷ lệ đều đạt ngưỡng ≥10. Đây chưa phải kết quả test thay đổi giữa năm; các mean thu nhập/tiêu dùng/giáo dục và mẫu tài sản vẫn cần diagnostics riêng.

- **Lecture 4/Chap 4:** tham số do câu hỏi quyết định. Mean dùng $\bar X$; tỷ lệ dùng $\hat p$; estimator khác estimate. Mean không chệch trong mô hình iid có kỳ vọng hữu hạn, chưa bảo đảm CI/p chính xác hoặc sửa được mẫu thiếu.
- **Chap 2–3:** số hộ/0/thiếu, histogram hoặc Q–Q, mean/median/variance/skewness/kurtosis, ảnh hưởng quan sát lớn; phân phối lấy mẫu/CLT. Không tự nhận n >30 đủ với đuôi mạnh.
- **Chap 9, trang 21:** JB chẩn đoán chuẩn với $m_r=N^{-1}\sum(x_i-\bar x)^r$, $g_1=m_3/m_2^{3/2}$, $g_2=m_4/m_2^2-3$:

$$
JB=N(g_1^2/6+g_2^2/24)\approx\chi^2_2\quad\text{dưới H}_0\text{ chuẩn}.
$$

JB áp dụng giá trị hộ/nhóm, không kiểm tra trực tiếp phân phối mean; không dùng cho chỉ báo sở hữu/Bernoulli. Bác bỏ chuẩn chưa tự cấm suy luận mean xấp xỉ; không bác bỏ cũng chưa chứng minh chuẩn. Kiểm tra đúng nhóm sở hữu/tài sản/Q/năm, không mượn diagnostics toàn mẫu.

Phương sai mẫu khác chưa chứng minh tổng thể khác; phương sai mẫu gần cũng chưa chứng minh phương sai chung. Bản A cần đọc theo các giả định của nó, B vẫn cần độc lập và xấp xỉ phù hợp. Thiếu thông tin thiết kế khảo sát chưa được giải quyết bằng bất cứ công thức trên.

**Nhiều kiểm định:** khóa danh sách p chính trước khi xét p; dùng Holm cho các test chính câu 1, tiêu dùng 2a, năm tỷ lệ ở câu 2, câu 3b, 4, 5 và bản B của 6 đủ điều kiện. Không đưa test mean D vào danh sách. Nếu dùng p danh nghĩa để kết luận thì đưa vào danh sách. A báo p theo giả định để đối chiếu, không dùng làm lựa chọn thay thế khi B không đạt. JB là diagnostics riêng; các bảng chỉ CI không bị âm thầm thêm p. Holm không khắc phục p đầu vào kém tin cậy. CI thường chưa được điều chỉnh đồng thời.

## 7. Sổ mẫu đã kiểm tra

Các n sau chỉ là kiểm tra hồ sơ hợp lệ, chưa là kết quả giả thuyết. Khi triển khai phải tái tạo đúng bộ lọc và báo lại n.

| Đối chiếu | 2010 | 2014 |
|---|---|---|
| Thu nhập đầu người | 9.399 | 9.398 |
| Tiêu dùng, $D^R$, $M$, chỉ báo chi vượt thu nhập, sau quy ước fuel | 9.390 | 9.391 |
| Q1 đủ chi cho kiểm định tỷ lệ và mô tả thu–chi | 2.346 | 2.350 |
| Q2 đủ chi cho kiểm định tỷ lệ và mô tả thu–chi | 2.347 | 2.349 |
| Q3 đủ chi cho kiểm định tỷ lệ và mô tả thu–chi | 2.349 | 2.346 |
| Q4 đủ chi cho kiểm định tỷ lệ và mô tả thu–chi | 2.348 | 2.346 |
| Giáo dục có/không chi | 9.399 | 9.398 |
| Giáo dục thực/người trong nhóm chi dương | 5.963 | 5.637 |

| Khu vực | Thu nhập 2010 | Thu nhập 2014 | Đủ chi 2010 | Đủ chi 2014 |
|---|---|---|---|---|
| Thành thị | 2.649 | 2.781 | 2.648 | 2.781 |
| Nông thôn | 6.750 | 6.617 | 6.742 | 6.610 |

Hồ sơ hợp lệ từng tài sản (có Q; thu nhập/quy mô hiện đều hợp lệ) là tổng hai nhóm có/không trước tách Q:

| Tài sản | 2010 | 2014 |
|---|---|---|
| `oto` | 9.222 | 9.354 |
| `moto` | 9.218 | 9.353 |
| `bicycle` | 9.221 | 9.354 |
| `bed` | 9.214 | 9.351 |
| `tab` | 9.219 | 9.354 |
| `tele` | 9.217 | 9.353 |
| `tv` | 9.218 | 9.354 |
| `emachine` | 9.221 | 9.354 |
| `hmachine` | 9.218 | 9.353 |

Bảng n có/không theo từng Q/năm/tài sản sẽ đi cùng 9 bảng tổng hợp. Tài sản khác nhau không bắt buộc cùng complete cases; A/B của cùng đối chiếu phải cùng hộ. Câu 5 mỗi tài sản/năm là một bảng 4 × 2; câu 6 tách thêm Q rồi so hai nhóm trong Q đó.

## 8. Triển khai sáu câu đã giữ lại

Mỗi câu: Markdown câu hỏi/biến/parameter/estimator/H₀–H₁ → code tạo biến và bộ lọc/n → diagnostics → tính từng bước statistic/df/CI/p → đối chiếu thư viện → note diễn giải và giới hạn. Code dùng tên như `real_income_per_person`, `real_income_expense_balance_per_person`, `expenses_exceed_income`, `owns_tv`.

Không còn câu hỏi y tế hay các hướng chưa chốt từ papers trong phạm vi triển khai. Bỏ các đối chiếu tài sản không đủ điều kiện khỏi suy luận, chỉ báo mô tả/trạng thái thiếu thông tin; không ép đủ 72 p-value. Đã chạy normality test và kiểm tra số đếm thu–chi; chưa chạy test thay đổi 2010–2014, chưa điền kết luận mức sống, chưa tạo báo cáo PDF.
