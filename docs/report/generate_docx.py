# -*- coding: utf-8 -*-

"""

Script to generate Bao_cao_DATK2_ATmega16_DHT11.docx strictly formatted according to

HUST / SEEE (Trường Điện - Điện tử, Đại học Bách khoa Hà Nội) guidelines.

"""



import os

import docx

from docx.shared import Inches, Pt, Cm, RGBColor

from docx.enum.text import WD_ALIGN_PARAGRAPH

from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

from docx.oxml import OxmlElement, parse_xml

from docx.oxml.ns import nsdecls, qn



def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):

    tcPr = cell._tc.get_or_add_tcPr()

    tcMar = OxmlElement('w:tcMar')

    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:

        node = OxmlElement(f'w:{m}')

        node.set(qn('w:w'), str(val))

        node.set(qn('w:type'), 'dxa')

        tcMar.append(node)

    tcPr.append(tcMar)



def set_table_borders(table, color="000000", sz="4", val="single"):

    tblPr = table._tbl.tblPr

    borders = parse_xml(

        f'<w:tblBorders {nsdecls("w")}>\n'

        f'  <w:top w:val="{val}" w:sz="8" w:space="0" w:color="{color}"/>\n'

        f'  <w:bottom w:val="{val}" w:sz="8" w:space="0" w:color="{color}"/>\n'

        f'  <w:left w:val="none"/>\n'

        f'  <w:right w:val="none"/>\n'

        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="CCCCCC"/>\n'

        f'  <w:insideV w:val="none"/>\n'

        f'</w:tblBorders>'

    )

    tblPr.append(borders)



def set_cell_shading(cell, color_hex="F2F2F2"):

    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')

    cell._tc.get_or_add_tcPr().append(shading)



def add_page_number_field(run):

    fldSimple = OxmlElement('w:fldSimple')

    fldSimple.set(qn('w:instr'), 'PAGE')

    run._r.append(fldSimple)



def create_report_docx(output_path):

    doc = docx.Document()

    

    # Page setup

    section = doc.sections[0]

    section.page_width = Cm(21.0)

    section.page_height = Cm(29.7)

    section.top_margin = Cm(2.0)

    section.bottom_margin = Cm(2.0)

    section.left_margin = Cm(2.0)

    section.right_margin = Cm(2.0)

    

    # Styles

    normal_style = doc.styles['Normal']

    normal_style.font.name = 'Times New Roman'

    normal_style.font.size = Pt(13)

    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    

    def add_para(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, 

                 space_before=0, space_after=6, line_spacing=1.3, first_indent=1.0, font_size=13):

        p = doc.add_paragraph()

        p.alignment = align

        p.paragraph_format.space_before = Pt(space_before)

        p.paragraph_format.space_after = Pt(space_after)

        p.paragraph_format.line_spacing = line_spacing

        if first_indent > 0:

            p.paragraph_format.first_line_indent = Cm(first_indent)

        if text:

            run = p.add_run(text)

            run.font.name = 'Times New Roman'

            run.font.size = Pt(font_size)

            run.bold = bold

            run.italic = italic

        return p



    def add_heading_1(text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p.paragraph_format.space_before = Pt(16)

        p.paragraph_format.space_after = Pt(12)

        p.paragraph_format.line_spacing = 1.3

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.keep_with_next = True

        run = p.add_run(text.upper())

        run.font.name = 'Times New Roman'

        run.font.size = Pt(16)

        run.bold = True

        return p



    def add_heading_2(text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p.paragraph_format.space_before = Pt(14)

        p.paragraph_format.space_after = Pt(6)

        p.paragraph_format.line_spacing = 1.3

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.keep_with_next = True

        run = p.add_run(text)

        run.font.name = 'Times New Roman'

        run.font.size = Pt(14)

        run.bold = True

        return p



    def add_heading_3(text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p.paragraph_format.space_before = Pt(10)

        p.paragraph_format.space_after = Pt(4)

        p.paragraph_format.line_spacing = 1.3

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.keep_with_next = True

        run = p.add_run(text)

        run.font.name = 'Times New Roman'

        run.font.size = Pt(13)

        run.bold = True

        run.italic = True

        return p



    def add_table_caption(text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p.paragraph_format.space_before = Pt(10)

        p.paragraph_format.space_after = Pt(4)

        p.paragraph_format.keep_with_next = True

        p.paragraph_format.first_line_indent = Cm(0)

        run = p.add_run(text)

        run.font.name = 'Times New Roman'

        run.font.size = Pt(12)

        run.bold = True

        return p



    def add_figure_caption(text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p.paragraph_format.space_before = Pt(4)

        p.paragraph_format.space_after = Pt(12)

        p.paragraph_format.first_line_indent = Cm(0)

        run = p.add_run(text)

        run.font.name = 'Times New Roman'

        run.font.size = Pt(12)

        run.italic = True

        return p



    def add_code_block(code_text):

        p = doc.add_paragraph()

        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p.paragraph_format.space_before = Pt(4)

        p.paragraph_format.space_after = Pt(8)

        p.paragraph_format.line_spacing = 1.05

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.left_indent = Cm(0.5)

        run = p.add_run(code_text)

        run.font.name = 'Consolas'

        run.font.size = Pt(9.5)

        run.font.color.rgb = RGBColor(30, 30, 30)

        return p



    # ----------------------------------------------------

    # COVER PAGE (SECTION 0)

    # ----------------------------------------------------

    cover_table = doc.add_table(rows=1, cols=1)

    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    cover_table.autofit = False

    cover_table.columns[0].width = Cm(16.5)

    

    cell = cover_table.cell(0, 0)

    set_cell_margins(cell, top=260, bottom=260, left=320, right=320)

    

    tcPr = cell._tc.get_or_add_tcPr()

    tcBorders = parse_xml(

        f'<w:tcBorders {nsdecls("w")}>\n'

        f'  <w:top w:val="double" w:sz="12" w:space="0" w:color="000000"/>\n'

        f'  <w:left w:val="double" w:sz="12" w:space="0" w:color="000000"/>\n'

        f'  <w:bottom w:val="double" w:sz="12" w:space="0" w:color="000000"/>\n'

        f'  <w:right w:val="double" w:sz="12" w:space="0" w:color="000000"/>\n'

        f'</w:tcBorders>'

    )

    tcPr.append(tcBorders)

    

    cp = cell.paragraphs[0]

    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp.paragraph_format.space_before = Pt(8)

    cp.paragraph_format.space_after = Pt(2)

    cp.paragraph_format.line_spacing = 1.2

    cp.paragraph_format.first_line_indent = Cm(0)

    r = cp.add_run("ĐẠI HỌC BÁCH KHOA HÀ NỘI\nTRƯỜNG ĐIỆN – ĐIỆN TỬ")

    r.font.name = 'Times New Roman'

    r.font.size = Pt(17)

    r.bold = True

    

    cp_line = cell.add_paragraph()

    cp_line.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_line.paragraph_format.space_before = Pt(2)

    cp_line.paragraph_format.space_after = Pt(14)

    cp_line.paragraph_format.first_line_indent = Cm(0)

    r_line = cp_line.add_run("—————————————")

    r_line.font.name = 'Times New Roman'

    r_line.font.size = Pt(11)

    r_line.bold = True

    

    # Logo

    cp_logo = cell.add_paragraph()

    cp_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_logo.paragraph_format.space_before = Pt(0)

    cp_logo.paragraph_format.space_after = Pt(16)

    cp_logo.paragraph_format.first_line_indent = Cm(0)

    logo_path = os.path.join(os.path.dirname(output_path), "img", "logo.png")

    if not os.path.exists(logo_path):

        logo_path = "report/src/img/logo.png"

    if os.path.exists(logo_path):

        cp_logo.add_run().add_picture(logo_path, height=Cm(3.8))

    

    # Title

    cp_title = cell.add_paragraph()

    cp_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_title.paragraph_format.space_before = Pt(6)

    cp_title.paragraph_format.space_after = Pt(6)

    cp_title.paragraph_format.line_spacing = 1.2

    cp_title.paragraph_format.first_line_indent = Cm(0)

    r_title = cp_title.add_run("BÁO CÁO\nĐỒ ÁN THIẾT KẾ II")

    r_title.font.name = 'Times New Roman'

    r_title.font.size = Pt(20)

    r_title.bold = True

    

    cp_lbl = cell.add_paragraph()

    cp_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_lbl.paragraph_format.space_before = Pt(4)

    cp_lbl.paragraph_format.space_after = Pt(2)

    cp_lbl.paragraph_format.first_line_indent = Cm(0)

    r_lbl = cp_lbl.add_run("ĐỀ TÀI:")

    r_lbl.font.name = 'Times New Roman'

    r_lbl.font.size = Pt(14)

    r_lbl.bold = True

    

    cp_topic = cell.add_paragraph()

    cp_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_topic.paragraph_format.space_before = Pt(2)

    cp_topic.paragraph_format.space_after = Pt(26)

    cp_topic.paragraph_format.line_spacing = 1.2

    cp_topic.paragraph_format.first_line_indent = Cm(0)

    r_topic = cp_topic.add_run("THIẾT KẾ HỆ THỐNG ĐO NHIỆT ĐỘ\nVÀ CẢNH BÁO NGƯỠNG SỬ DỤNG ATMEGA16")

    r_topic.font.name = 'Times New Roman'

    r_topic.font.size = Pt(15)

    r_topic.bold = True

    

    # Info table inside cover

    info_tbl = cell.add_table(rows=5, cols=3)

    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    info_tbl.autofit = False

    col_widths = [Cm(4.8), Cm(3.8), Cm(2.4)]

    for row in info_tbl.rows:

        for idx_w, w in enumerate(col_widths):

            row.cells[idx_w].width = w

    

    # Merge cols 1 & 2 for rows 0, 3, 4

    info_tbl.cell(0, 1).merge(info_tbl.cell(0, 2))

    info_tbl.cell(3, 1).merge(info_tbl.cell(3, 2))

    info_tbl.cell(4, 1).merge(info_tbl.cell(4, 2))



    def style_info_cell(c, text, is_bold=False):

        set_cell_margins(c, top=40, bottom=40, left=80, right=80)

        p = c.paragraphs[0]

        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        p.paragraph_format.space_before = Pt(2)

        p.paragraph_format.space_after = Pt(2)

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.left_indent = Cm(0)

        p.paragraph_format.right_indent = Cm(0)

        if text:

            r = p.add_run(text)

            r.font.name = 'Times New Roman'

            r.font.size = Pt(12.5)

            r.bold = is_bold



    # Row 0: Giảng viên hướng dẫn

    style_info_cell(info_tbl.cell(0, 0), "Giảng viên hướng dẫn:", True)

    style_info_cell(info_tbl.cell(0, 1), "ThS. Vũ Hồng Vinh", False)



    # Row 1: Sinh viên 1

    style_info_cell(info_tbl.cell(1, 0), "Sinh viên thực hiện:", True)

    style_info_cell(info_tbl.cell(1, 1), "Mai Duy Hiếu", False)

    style_info_cell(info_tbl.cell(1, 2), "20223967", False)



    # Row 2: Sinh viên 2

    style_info_cell(info_tbl.cell(2, 0), "", False)

    style_info_cell(info_tbl.cell(2, 1), "Hoàng Quốc Hưng", False)

    style_info_cell(info_tbl.cell(2, 2), "20233758", False)



    # Row 3: Mã lớp học

    style_info_cell(info_tbl.cell(3, 0), "Mã lớp học:", True)

    style_info_cell(info_tbl.cell(3, 1), "772642", False)



    # Row 4: Nhóm thực hiện

    style_info_cell(info_tbl.cell(4, 0), "Nhóm thực hiện:", True)

    style_info_cell(info_tbl.cell(4, 1), "Nhóm 4", False)

        

    cp_foot = cell.add_paragraph()

    cp_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cp_foot.paragraph_format.space_before = Pt(28)

    cp_foot.paragraph_format.space_after = Pt(8)

    cp_foot.paragraph_format.first_line_indent = Cm(0)

    r_foot = cp_foot.add_run("Hà Nội, 11/2026")

    r_foot.font.name = 'Times New Roman'

    r_foot.font.size = Pt(13)

    r_foot.bold = True



    # ----------------------------------------------------

    # SECTION 1: FRONTMATTER (Roman page numbering: i, ii, iii...)

    # ----------------------------------------------------

    sec_front = doc.add_section(docx.enum.section.WD_SECTION_START.NEW_PAGE)

    sec_front.top_margin = Cm(2.0)

    sec_front.bottom_margin = Cm(2.0)

    sec_front.left_margin = Cm(3.0)

    sec_front.right_margin = Cm(2.0)

    

    footer_front = sec_front.footer

    footer_p = footer_front.paragraphs[0]

    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_p.paragraph_format.first_line_indent = Cm(0)

    footer_run = footer_p.add_run()

    footer_run.font.name = 'Times New Roman'

    footer_run.font.size = Pt(12)

    add_page_number_field(footer_run)

    

    sectPr = sec_front._sectPr

    pgNumType = OxmlElement('w:pgNumType')

    pgNumType.set(qn('w:fmt'), 'roman')

    pgNumType.set(qn('w:start'), '1')

    sectPr.append(pgNumType)

    

    # --- LỜI NÓI ĐẦU ---

    add_heading_1("LỜI NÓI ĐẦU")

    add_para(

        "Trong bối cảnh phát triển mạnh mẽ của khoa học kỹ thuật và cuộc cách mạng công nghiệp 4.0, các hệ thống nhúng thông minh, "

        "đo lường tự động và giám sát môi trường ngày càng đóng vai trò thiết yếu trong đời sống và sản xuất. Đặc biệt, thông số nhiệt độ và "

        "độ ẩm là hai yếu tố vật lý cơ bản ảnh hưởng trực tiếp đến sự vận hành ổn định của hệ thống máy chủ dữ liệu (Data Center), quy trình ấp nở "

        "và bảo quản nông sản, nhà kính nông nghiệp công nghệ cao, cũng như an toàn lao động trong nhà xưởng công nghiệp. Việc xây dựng một hệ thống "

        "giám sát nhiệt độ tin cậy, có khả năng hiển thị thời gian thực và tự động đưa ra cảnh báo khi vượt ngưỡng cho phép là bài toán kỹ thuật mang tính thực tiễn rất cao."

    )

    add_para(

        "Học phần Đồ án Thiết kế II là cơ hội quan trọng giúp sinh viên ngành Kỹ thuật Điện tử – Viễn thông củng cố, liên kết các kiến thức nền tảng "

        "về cấu trúc máy tính, kỹ thuật vi xử lý, kỹ thuật lập trình C nhúng và thiết kế giao tiếp ngoại vi để giải quyết một bài toán kỹ thuật trọn vẹn "

        "từ thiết kế sơ đồ nguyên lý, xây dựng phần mềm cho tới thử nghiệm trên kit thực tế."

    )

    add_para(

        "Đề tài “Thiết kế hệ thống đo nhiệt độ và cảnh báo ngưỡng sử dụng ATmega16” được thực hiện nhằm xây dựng "

        "một mô hình đo lường số hoàn chỉnh. Hệ thống sử dụng vi điều khiển AVR ATmega16 làm trung tâm xử lý, giao tiếp trực tiếp với cảm biến số DHT11 "

        "qua đường truyền 1-Wire Single-Bus, xuất dữ liệu trực quan lên màn hình tinh thể lỏng LCD 1602 (chế độ 4-bit bus) và kích hoạt dàn đèn LED "

        "cảnh báo khi nhiệt độ đo được vượt ngưỡng an toàn (30°C)."

    )

    add_para(

        "So với các giải pháp đo nhiệt độ sử dụng cảm biến tương tự truyền thống (như LM35), việc sử dụng cảm biến số DHT11 mang lại nhiều ưu điểm "

        "vượt trội: khả năng chống nhiễu cao trên đường truyền tín hiệu số, tích hợp đo đồng thời nhiệt độ và độ ẩm môi trường, kiểm tra mã bù lỗi "

        "(Checksum 8-bit) đảm bảo dữ liệu không bị sai lệch. Đồng thời, đồ án cũng giải quyết triệt để các bài toán kỹ thuật thực tế trên Kit phần cứng "

        "như xử lý xung đột chân ngoại vi JTAG trên PORT C, cấu hình nguồn xung nhịp dao động nội 8.0 MHz bằng Fuse Bits và tối ưu hóa tài nguyên chân xuất nhập GPIO."

    )

    add_para(

        "Chúng em xin bày tỏ lòng biết ơn chân thành và sâu sắc nhất tới thầy ThS. Vũ Hồng Vinh, giảng viên Trường Điện – Điện tử, "

        "Đại học Bách khoa Hà Nội, người đã tận tình định hướng, chỉ bảo và tạo mọi điều kiện thuận lợi nhất giúp chúng em hoàn thành tốt đồ án này. "

        "Chúng em cũng xin trân trọng cảm ơn các thầy cô giáo trong Trường Điện – Điện tử đã trang bị cho chúng em những nền tảng kiến thức quý báu trong suốt quá trình học tập."

    )

    add_para(

        "Do thời gian thực hiện có hạn và kinh nghiệm thực tế của bản thân còn hạn chế, báo cáo chắc chắn không tránh khỏi những thiếu sót nhất định. "

        "Chúng em rất mong nhận được những lời nhận xét, góp ý quý báu của thầy cô và các bạn để đề tài được hoàn thiện hơn nữa."

    )

    

    p_sig = doc.add_paragraph()

    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    p_sig.paragraph_format.space_before = Pt(16)

    p_sig.paragraph_format.space_after = Pt(2)

    p_sig.paragraph_format.first_line_indent = Cm(0)

    r_sig1 = p_sig.add_run("Hà Nội, tháng 11 năm 2026\n")

    r_sig1.font.name = 'Times New Roman'

    r_sig1.font.size = Pt(12)

    r_sig1.italic = True

    r_sig_title = p_sig.add_run("Sinh viên thực hiện\n\n")

    r_sig_title.font.name = 'Times New Roman'

    r_sig_title.font.size = Pt(12)

    r_sig_title.bold = True

    r_sig2 = p_sig.add_run("Mai Duy Hiếu\nHoàng Quốc Hưng")

    r_sig2.font.name = 'Times New Roman'

    r_sig2.font.size = Pt(12.5)

    r_sig2.bold = True

    

    # --- MỤC LỤC ---

    doc.add_page_break()

    add_heading_1("MỤC LỤC")

    

    toc_items = [

        ("LỜI NÓI ĐẦU", "i", True),

        ("DANH MỤC HÌNH VẼ", "iii", True),

        ("DANH MỤC BẢNG", "iv", True),

        ("CHƯƠNG 1. GIỚI THIỆU TỔNG QUAN PHẦN CỨNG VÀ LINH KIỆN", "1", True),

        ("   1.1 Vi điều khiển ATmega16", "1", False),

        ("   1.2 Mạch Kit thực hành vi điều khiển họ AVR", "4", False),

        ("   1.3 Cảm biến số nhiệt độ và độ ẩm DHT11", "5", False),

        ("   1.4 Màn hình hiển thị tinh thể lỏng LCD 1602", "8", False),

        ("   1.5 Khối cảnh báo và chỉ thị LED", "9", False),

        ("CHƯƠNG 2. THIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG", "10", True),

        ("   2.1 Thiết kế kiến trúc phần cứng và sơ đồ nguyên lý", "10", False),

        ("   2.2 Xây dựng thuật toán và phần mềm điều khiển", "12", False),

        ("   2.3 Quy trình biên dịch và nạp firmware", "16", False),

        ("CHƯƠNG 3. KẾT QUẢ THỰC NGHIỆM", "18", True),

        ("   3.1 Kết quả thực nghiệm trên phần cứng", "18", False),

        ("   3.2 Đánh giá kết quả thực nghiệm", "20", False),

        ("CHƯƠNG 4. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "24", True),

        ("   4.1 Kết luận", "24", False),

        ("   4.2 Hạn chế của đề tài", "25", False),

        ("   4.3 Hướng phát triển mở rộng", "25", False),

        ("TÀI LIỆU THAM KHẢO", "27", True),

        ("PHỤ LỤC: TOÀN BỘ MÃ NGUỒN CHƯƠNG TRÌNH", "28", True),

        ("   Phụ lục A: File mã nguồn chính tempsen.c", "28", False),

        ("   Phụ lục B: Thư viện điều khiển LCD hunget_lcd.h", "33", False),

    ]

    

    toc_tbl = doc.add_table(rows=len(toc_items), cols=2)

    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    toc_tbl.autofit = False

    toc_tbl.columns[0].width = Cm(14.5)

    toc_tbl.columns[1].width = Cm(1.5)

    

    for idx, (title, pnum, is_bold) in enumerate(toc_items):

        c0 = toc_tbl.cell(idx, 0)

        c1 = toc_tbl.cell(idx, 1)

        p0 = c0.paragraphs[0]

        p0.paragraph_format.space_before = Pt(1)

        p0.paragraph_format.space_after = Pt(1)

        p0.paragraph_format.line_spacing = 1.15

        p0.paragraph_format.first_line_indent = Cm(0)

        r0 = p0.add_run(title)

        r0.font.name = 'Times New Roman'

        r0.font.size = Pt(12)

        r0.bold = is_bold

        

        p1 = c1.paragraphs[0]

        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        p1.paragraph_format.space_before = Pt(1)

        p1.paragraph_format.space_after = Pt(1)

        p1.paragraph_format.line_spacing = 1.15

        p1.paragraph_format.first_line_indent = Cm(0)

        r1 = p1.add_run(pnum)

        r1.font.name = 'Times New Roman'

        r1.font.size = Pt(12)

        r1.bold = is_bold



    # --- DANH MỤC HÌNH VẼ ---

    doc.add_page_break()

    add_heading_1("DANH MỤC HÌNH VẼ")

    

    lof_items = [

        ("Hình 1.1", "Sơ đồ phân bố chân của vi điều khiển ATmega16 dạng đóng vỏ DIP-40", "2"),

        ("Hình 1.2", "Sơ đồ bố trí linh kiện trên Kit phát triển vi điều khiển AVR", "4"),

        ("Hình 2.1", "Sơ đồ kết nối liên khối chi tiết của hệ thống", "10"),

        ("Hình 2.2", "Sơ đồ nguyên lý mạch Kit vi điều khiển ATmega16", "11"),

        ("Hình 2.3", "Mô hình thiết kế 3D của bo mạch Kit trên phần mềm Altium Designer", "12"),

        ("Hình 2.4", "Giao diện phần mềm ProgISP khi nạp firmware và cấu hình Fuse Bits 0xD9E4", "17"),

        ("Hình 3.1", "Hình ảnh thực tế hệ thống vận hành trong các kịch bản thử nghiệm", "19"),

    ]

    lof_tbl = doc.add_table(rows=len(lof_items), cols=3)

    lof_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    lof_tbl.autofit = False

    lof_tbl.columns[0].width = Cm(2.2)

    lof_tbl.columns[1].width = Cm(12.3)

    lof_tbl.columns[2].width = Cm(1.5)

    

    for idx, (h_num, h_title, pnum) in enumerate(lof_items):

        c0 = lof_tbl.cell(idx, 0)

        c1 = lof_tbl.cell(idx, 1)

        c2 = lof_tbl.cell(idx, 2)

        for c, text, align, bold in [(c0, h_num, WD_ALIGN_PARAGRAPH.LEFT, True),

                                     (c1, h_title, WD_ALIGN_PARAGRAPH.LEFT, False),

                                     (c2, pnum, WD_ALIGN_PARAGRAPH.RIGHT, False)]:

            p = c.paragraphs[0]

            p.alignment = align

            p.paragraph_format.space_before = Pt(3)

            p.paragraph_format.space_after = Pt(3)

            p.paragraph_format.first_line_indent = Cm(0)

            r = p.add_run(text)

            r.font.name = 'Times New Roman'

            r.font.size = Pt(12)

            r.bold = bold



    # --- DANH MỤC BẢNG ---

    doc.add_page_break()

    add_heading_1("DANH MỤC BẢNG")

    

    lot_items = [

        ("Bảng 1.1", "Thông số kỹ thuật chính của vi điều khiển ATmega16", "2"),

        ("Bảng 1.2", "Đặc tính kỹ thuật của cảm biến số DHT11", "6"),

        ("Bảng 1.3", "Bảng ánh xạ kết nối chân giữa giắc J7 trên Kit, màn hình LCD 1602 và ATmega16", "8"),

        ("Bảng 2.1", "Bảng tổng hợp kết nối tín hiệu phần cứng của hệ thống", "11"),

        ("Bảng 3.1", "Bảng tổng hợp các kịch bản kiểm tra và kết quả đánh giá hệ thống", "19"),

    ]

    lot_tbl = doc.add_table(rows=len(lot_items), cols=3)

    lot_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    lot_tbl.autofit = False

    lot_tbl.columns[0].width = Cm(2.2)

    lot_tbl.columns[1].width = Cm(12.3)

    lot_tbl.columns[2].width = Cm(1.5)

    

    for idx, (t_num, t_title, pnum) in enumerate(lot_items):

        c0 = lot_tbl.cell(idx, 0)

        c1 = lot_tbl.cell(idx, 1)

        c2 = lot_tbl.cell(idx, 2)

        for c, text, align, bold in [(c0, t_num, WD_ALIGN_PARAGRAPH.LEFT, True),

                                     (c1, t_title, WD_ALIGN_PARAGRAPH.LEFT, False),

                                     (c2, pnum, WD_ALIGN_PARAGRAPH.RIGHT, False)]:

            p = c.paragraphs[0]

            p.alignment = align

            p.paragraph_format.space_before = Pt(3)

            p.paragraph_format.space_after = Pt(3)

            p.paragraph_format.first_line_indent = Cm(0)

            r = p.add_run(text)

            r.font.name = 'Times New Roman'

            r.font.size = Pt(12)

            r.bold = bold



    # ----------------------------------------------------

    # SECTION 2: BODY CHAPTERS (Arabic numerals: 1, 2, 3...)

    # ----------------------------------------------------

    sec_body = doc.add_section(docx.enum.section.WD_SECTION_START.NEW_PAGE)

    sec_body.top_margin = Cm(2.0)

    sec_body.bottom_margin = Cm(2.0)

    sec_body.left_margin = Cm(3.0)

    sec_body.right_margin = Cm(2.0)

    

    footer_body = sec_body.footer

    footer_bp = footer_body.paragraphs[0]

    footer_bp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_bp.paragraph_format.first_line_indent = Cm(0)

    footer_brun = footer_bp.add_run()

    footer_brun.font.name = 'Times New Roman'

    footer_brun.font.size = Pt(12)

    add_page_number_field(footer_brun)

    

    sectPr_b = sec_body._sectPr

    pgNumType_b = OxmlElement('w:pgNumType')

    pgNumType_b.set(qn('w:fmt'), 'decimal')

    pgNumType_b.set(qn('w:start'), '1')

    sectPr_b.append(pgNumType_b)



    # ====================================================

    # CHƯƠNG 1

    # ====================================================

    add_heading_1("CHƯƠNG 1. GIỚI THIỆU TỔNG QUAN PHẦN CỨNG VÀ LINH KIỆN")

    

    add_heading_2("1.1 Vi điều khiển ATmega16")

    add_heading_3("1.1.1 Tổng quan kiến trúc và đặc tính kỹ thuật")

    add_para(

        "ATmega16 là một trong những dòng vi điều khiển 8-bit họ AVR phổ biến nhất của hãng Atmel (nay thuộc Microchip Technology), "

        "được thiết kế dựa trên kiến trúc RISC (Reduced Instruction Set Computer) tiên tiến với tập lệnh rút gọn gồm 131 lệnh đa số thực thi "

        "trong một chu kỳ xung nhịp đơn lẻ. Nhờ thông lượng xử lý đạt tới 1 MIPS trên mỗi MHz tần số hoạt động, vi điều khiển mang lại "

        "hiệu suất tính toán tối ưu song song với khả năng tiết kiệm năng lượng vượt trội."

    )

    

    img_pinout = os.path.join(os.path.dirname(output_path), "img", "atmega_sodo.png")

    if os.path.exists(img_pinout):

        p_img = doc.add_paragraph()

        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_img.paragraph_format.first_line_indent = Cm(0)

        p_img.add_run().add_picture(img_pinout, width=Cm(13.5))

        add_figure_caption("Hình 1.1: Sơ đồ phân bố chân của vi điều khiển ATmega16 dạng đóng vỏ DIP-40")

    

    add_table_caption("Bảng 1.1: Thông số kỹ thuật chính của vi điều khiển ATmega16")

    t1_data = [

        ("Kiến trúc CPU", "8-bit AVR RISC với 32 thanh ghi làm việc đa năng 8-bit"),

        ("Bộ nhớ Flash chương trình", "16 Kbytes (In-System Reprogrammable Flash, độ bền 10.000 lần ghi/xóa)"),

        ("Bộ nhớ SRAM nội", "1 Kbyte (1024 Bytes)"),

        ("Bộ nhớ EEPROM nội", "512 Bytes (Lưu trữ dữ liệu không mất khi mất nguồn, độ bền 100.000 lần)"),

        ("Tần số xung nhịp tối đa", "0 – 16 MHz (Điện áp 4.5V – 5.5V)"),

        ("Số chân I/O khả trình", "32 chân chia làm 4 cổng 8-bit (PORT A, PORT B, PORT C, PORT D)"),

        ("Bộ định thời (Timer/Counter)", "2 bộ Timer 8-bit và 1 bộ Timer 16-bit đa chức năng"),

        ("Các kênh PWM", "4 kênh điều chế độ rộng xung phần cứng"),

        ("Bộ chuyển đổi ADC", "8 kênh ADC 10-bit tích hợp sẵn trên PORT A"),

        ("Giao tiếp truyền thông", "USART lập trình được, SPI (Serial Peripheral Interface), I2C/TWI"),

        ("Giao diện gỡ lỗi phần cứng", "Chuẩn JTAG (IEEE std. 1149.1) hỗ trợ On-Chip Debug"),

        ("Điện áp hoạt động", "4.5V – 5.5V đối với ATmega16 chuẩn (2.7V – 5.5V đối với ATmega16L)")

    ]

    t1 = doc.add_table(rows=len(t1_data)+1, cols=2)

    t1.alignment = WD_TABLE_ALIGNMENT.CENTER

    t1.columns[0].width = Cm(5.2)

    t1.columns[1].width = Cm(10.8)

    set_table_borders(t1)

    

    t1.cell(0, 0).paragraphs[0].add_run("Thông số").bold = True

    t1.cell(0, 1).paragraphs[0].add_run("Giá trị định mức / Đặc tính kỹ thuật").bold = True

    set_cell_shading(t1.cell(0, 0))

    set_cell_shading(t1.cell(0, 1))

    

    for r_idx, (k, v) in enumerate(t1_data):

        c0 = t1.cell(r_idx+1, 0)

        c1 = t1.cell(r_idx+1, 1)

        c0.paragraphs[0].add_run(k).bold = True

        c1.paragraphs[0].add_run(v)

        c0.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

        c1.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

        c0.paragraphs[0].paragraph_format.space_before = Pt(2)

        c0.paragraphs[0].paragraph_format.space_after = Pt(2)

        c1.paragraphs[0].paragraph_format.space_before = Pt(2)

        c1.paragraphs[0].paragraph_format.space_after = Pt(2)

        c0.paragraphs[0].paragraph_format.line_spacing = 1.15

        c1.paragraphs[0].paragraph_format.line_spacing = 1.15



    add_heading_3("1.1.2 Cấu trúc các cổng vào/ra (I/O Ports) và chức năng trong đồ án")

    add_para(

        "Vi điều khiển ATmega16 trang bị 32 chân vào ra hai chiều, được phân bổ đều cho 4 cổng ngoại vi ký hiệu từ A đến D. "

        "Mỗi cổng được kiểm soát độc lập bởi 3 thanh ghi: DDRx (hướng vào/ra), PORTx (ghi dữ liệu hoặc bật trở kéo lên) và PINx (đọc dữ liệu chân)."

    )

    add_para(

        "Trong đề tài, chân PA1 đóng vai trò là đường truyền giao tiếp 1-Wire hai chiều với cảm biến số DHT11. "

        "Các chân PC4 – PC7 đảm nhiệm bus dữ liệu 4-bit (D4 – D7) của màn hình LCD 1602. "

        "Các chân PD5, PD6, PD7 là các đường tín hiệu điều khiển LCD (RW, RS, EN), và các chân PD0 – PD4 điều khiển dàn 5 LED cảnh báo ngưỡng."

    )



    add_heading_3("1.1.3 Xung nhịp hệ thống và phân tích xung đột ngoại vi JTAG")

    add_para(

        "Trên Kit thực hành vi điều khiển của Trường Điện – Điện tử (ĐHBK Hà Nội), vị trí thạch anh ngoài XT1 để trống. "

        "Do đó, vi điều khiển được thiết lập chạy bằng dao động RC nội tần số 8.0 MHz (Low Fuse Byte = 0xE4). "

        "Mặc định xuất xưởng, tính năng JTAG trên cổng C được bật (JTAGEN = 0), khóa cứng hai chân PC4 và PC5 ở chế độ gỡ lỗi phần cứng, "

        "khiến LCD không thể nhận lệnh khởi tạo. Hệ thống xử lý triệt để xung đột bằng cách tắt JTAG qua Fuse Bits (High Fuse = 0xD9) "

        "kết hợp ghi hai lần liên tiếp thanh ghi phần mềm MCUCSR = (1 << JTD)."

    )



    add_heading_2("1.2 Mạch Kit thực hành vi điều khiển họ AVR")

    add_para(

        "Mạch Kit thực hành vi điều khiển AVR sử dụng trong đề tài là module chuẩn phục vụ giảng dạy tại Trường Điện – Điện tử, ĐHBK Hà Nội. "

        "Kit tích hợp đế nạp khóa đòn bẩy ZIF Socket DIP-40, mạch ổn áp 5V LM7805, cổng nạp ISP 10 chân IDC-10, hàng rào cắm mở rộng J7 cho LCD 1602 "

        "kèm biến trở VR1 chỉnh độ tương phản, cùng hệ thống LED đơn và phím bấm chức năng."

    )

    img_kit = os.path.join(os.path.dirname(output_path), "img", "atmega_kit_2d.png")

    if os.path.exists(img_kit):

        p_img = doc.add_paragraph()

        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_img.paragraph_format.first_line_indent = Cm(0)

        p_img.add_run().add_picture(img_kit, width=Cm(13.5))

        add_figure_caption("Hình 1.2: Sơ đồ bố trí linh kiện trên Kit phát triển vi điều khiển AVR")



    add_heading_2("1.3 Cảm biến số nhiệt độ và độ ẩm DHT11")

    add_para(

        "DHT11 là cảm biến số tích hợp vi xử lý 8-bit bên trong để số hóa và hiệu chuẩn dữ liệu. "

        "Cảm biến gồm một phần tử màng polymer nhạy ẩm kiểu điện trở (Resistive Humidity Sensor) để đo độ ẩm tương đối và một nhiệt điện trở NTC có hệ số nhiệt âm để đo nhiệt độ môi trường. "

        "Chuẩn giao tiếp 1-Wire Single-Bus yêu cầu một điện trở kéo lên nguồn 5V trên chân DATA."

    )

    

    add_table_caption("Bảng 1.2: Đặc tính kỹ thuật của cảm biến số DHT11")

    t2_data = [

        ("Điện áp hoạt động", "3.3V – 5.5V DC"),

        ("Dải đo nhiệt độ", "0°C – 50°C"),

        ("Độ chính xác đo nhiệt độ", "±2.0°C"),

        ("Độ phân giải nhiệt độ", "1.0°C (hoặc 0.1°C ở các phiên bản nâng cấp)"),

        ("Dải đo độ ẩm", "20% – 90% RH"),

        ("Độ chính xác đo độ ẩm", "±5.0% RH"),

        ("Độ phân giải độ ẩm", "1% RH"),

        ("Chu kỳ lấy mẫu tối thiểu", "≥ 1.0 giây (Khuyến nghị 2.0 giây theo tài liệu của Aosong để đảm bảo ổn định)"),

        ("Dòng điện tiêu thụ", "0.5 mA – 2.5 mA khi đo; 100 µA – 150 µA khi chờ"),

        ("Chuẩn giao tiếp", "1-Wire Single-Bus (Đường truyền dữ liệu đơn tuyến số)")

    ]

    t2 = doc.add_table(rows=len(t2_data)+1, cols=2)

    t2.alignment = WD_TABLE_ALIGNMENT.CENTER

    t2.columns[0].width = Cm(5.2)

    t2.columns[1].width = Cm(10.8)

    set_table_borders(t2)

    t2.cell(0, 0).paragraphs[0].add_run("Thông số kỹ thuật").bold = True

    t2.cell(0, 1).paragraphs[0].add_run("Giá trị danh định").bold = True

    set_cell_shading(t2.cell(0, 0))

    set_cell_shading(t2.cell(0, 1))

    for r_idx, (k, v) in enumerate(t2_data):

        c0 = t2.cell(r_idx+1, 0)

        c1 = t2.cell(r_idx+1, 1)

        c0.paragraphs[0].add_run(k).bold = True

        c1.paragraphs[0].add_run(v)

        c0.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

        c1.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

        c0.paragraphs[0].paragraph_format.space_before = Pt(2)

        c0.paragraphs[0].paragraph_format.space_after = Pt(2)

        c1.paragraphs[0].paragraph_format.space_before = Pt(2)

        c1.paragraphs[0].paragraph_format.space_after = Pt(2)

        c0.paragraphs[0].paragraph_format.line_spacing = 1.15

        c1.paragraphs[0].paragraph_format.line_spacing = 1.15



    add_para(

        "Cần nhấn mạnh rằng giao thức truyền thông một dây (Single-Bus) của DHT11 do nhà sản xuất Aosong thiết kế là giao thức điểm–điểm chuyên biệt, "

        "hoàn toàn không tương thích với chuẩn công nghiệp Dallas/Maxim 1-Wire (vốn sử dụng mã định danh ROM 64-bit, khe thời gian do Master điều khiển và hỗ trợ đa điểm). "

        "Giao thức của DHT11 truyền gói tin 40-bit gồm 5 byte: phần nguyên độ ẩm, phần thập phân độ ẩm, phần nguyên nhiệt độ, "

        "phần thập phân nhiệt độ và byte Checksum kiểm tra lỗi. Mỗi bit bắt đầu bằng xung LOW 50µs; nếu xung HIGH tiếp theo kéo dài 26–28µs là bit '0', "

        "nếu kéo dài ~70µs là bit '1'. Thuật toán lấy mẫu tại thời điểm 38µs sau xung LOW giúp nhận dạng chính xác giá trị bit."

    )



    add_heading_2("1.4 Màn hình hiển thị tinh thể lỏng LCD 1602")

    add_para(

        "Màn hình LCD 1602 hiển thị 2 dòng, mỗi dòng 16 ký tự ma trận điểm 5x8 pixels dựa trên vi mạch Hitachi HD44780. "

        "Hệ thống vận hành ở chế độ 4-bit bus: mỗi byte được chia thành 2 nibble truyền lần lượt qua các chân PC4 – PC7, "

        "tiết kiệm 4 chân GPIO của vi điều khiển."

    )

    

    add_table_caption("Bảng 1.3: Bảng ánh xạ kết nối chân giữa giắc J7 trên Kit, LCD 1602 và ATmega16")

    t3_data = [

        ("1", "VSS", "GND", "Cực âm nguồn nuôi (0V)"),

        ("2", "VDD", "VCC", "Cực dương nguồn nuôi (+5V)"),

        ("3", "V0", "VR1", "Điện áp chỉnh độ tương phản hiển thị"),

        ("4", "RS", "PD6", "Chọn thanh ghi (0: Lệnh; 1: Dữ liệu)"),

        ("5", "RW", "PD5", "Chọn chiều đọc/ghi (Kéo 0: Ghi vào LCD)"),

        ("6", "E", "PD7", "Chốt xung kích hoạt (Enable Strobe)"),

        ("7–10", "D0–D3", "PC0–PC3", "4 bit dữ liệu thấp (Không dùng ở chế độ 4-bit)"),

        ("11", "D4", "PC4", "Đường truyền dữ liệu bit 4"),

        ("12", "D5", "PC5", "Đường truyền dữ liệu bit 5"),

        ("13", "D6", "PC6", "Đường truyền dữ liệu bit 6"),

        ("14", "D7", "PC7", "Đường truyền dữ liệu bit 7"),

        ("15", "A", "VCC", "Cực Anot đèn nền LED Backlight"),

        ("16", "K", "GND", "Cực Katot đèn nền LED Backlight")

    ]

    t3 = doc.add_table(rows=len(t3_data)+1, cols=4)

    t3.alignment = WD_TABLE_ALIGNMENT.CENTER

    t3.columns[0].width = Cm(1.6)

    t3.columns[1].width = Cm(2.2)

    t3.columns[2].width = Cm(2.2)

    t3.columns[3].width = Cm(10.0)

    set_table_borders(t3)

    t3.cell(0, 0).paragraphs[0].add_run("Chân J7").bold = True

    t3.cell(0, 1).paragraphs[0].add_run("Tên chân").bold = True

    t3.cell(0, 2).paragraphs[0].add_run("Chân MCU").bold = True

    t3.cell(0, 3).paragraphs[0].add_run("Chức năng kỹ thuật").bold = True

    for c_i in range(4):

        set_cell_shading(t3.cell(0, c_i))

    for r_idx, row in enumerate(t3_data):

        for c_idx in range(4):

            cell_item = t3.cell(r_idx+1, c_idx)

            cell_item.paragraphs[0].add_run(row[c_idx])

            cell_item.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

            cell_item.paragraphs[0].paragraph_format.space_before = Pt(2)

            cell_item.paragraphs[0].paragraph_format.space_after = Pt(2)

            cell_item.paragraphs[0].paragraph_format.line_spacing = 1.15



    add_heading_2("1.5 Khối cảnh báo và chỉ thị LED")

    add_para(

        "Dàn 5 LED đơn cảnh báo trên Kit được nối vào các chân PD0 – PD4 theo cấu hình tích cực mức thấp (Active Low). "

        "Khi MCU xuất mức logic 0, LED sáng (báo động vượt ngưỡng quá nhiệt). Khi MCU xuất mức 1, LED tắt (nhiệt độ an toàn)."

    )



    # ====================================================

    # CHƯƠNG 2

    # ====================================================

    doc.add_page_break()

    add_heading_1("CHƯƠNG 2. THIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG")

    

    add_heading_2("2.1 Thiết kế kiến trúc phần cứng và sơ đồ nguyên lý")

    add_para(

        "Hệ thống phân tầng rõ ràng gồm 5 khối: Khối nguồn nuôi hỗ trợ 2 đường cấp nguồn độc lập (nguồn ngoài 9V–12V qua IC ổn áp LM7805 hoặc nguồn 5V trực tiếp từ cổng USB máy tính qua cáp nạp USBasp), Khối vi điều khiển trung tâm (ATmega16), "

        "Khối cảm biến số (DHT11 trên chân PA1), Khối hiển thị (LCD 1602 trên PC4–PC7 và PD5–PD7) và Khối cảnh báo (5 LED trên PD0–PD4)."

    )

    

    img_wiring = os.path.join(os.path.dirname(output_path), "img", "system_wiring.png")

    if os.path.exists(img_wiring):

        p_wiring = doc.add_paragraph()

        p_wiring.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_wiring.paragraph_format.first_line_indent = Cm(0)

        p_wiring.add_run().add_picture(img_wiring, width=Cm(14.0))

        add_figure_caption("Hình 2.1: Sơ đồ kết nối liên khối chi tiết của hệ thống")

    

    img_sch = os.path.join(os.path.dirname(output_path), "img", "schematic.png")

    if os.path.exists(img_sch):

        p_img = doc.add_paragraph()

        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_img.paragraph_format.first_line_indent = Cm(0)

        p_img.add_run().add_picture(img_sch, width=Cm(15.0))

        add_figure_caption("Hình 2.2: Sơ đồ nguyên lý mạch Kit vi điều khiển ATmega16")

    

    img_3d = os.path.join(os.path.dirname(output_path), "img", "atmega_kit_3d.png")

    if os.path.exists(img_3d):

        add_para(

            "Dựa trên sơ đồ nguyên lý, mô hình thiết kế mạch in PCB và phối cảnh 3D của hệ thống được hoàn thiện trên phần mềm Altium Designer:"

        )

        p_3d = doc.add_paragraph()

        p_3d.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_3d.paragraph_format.first_line_indent = Cm(0)

        p_3d.add_run().add_picture(img_3d, width=Cm(11.5))

        add_figure_caption("Hình 2.3: Mô hình thiết kế 3D của bo mạch Kit trên phần mềm Altium Designer")

    

    add_table_caption("Bảng 2.1: Bảng tổng hợp kết nối tín hiệu phần cứng của hệ thống")

    t4_data = [

        ("Cảm biến DHT11", "DATA", "Chân 39 (PA1)", "Giao tiếp 1-Wire hai chiều (có trở kéo nội/ngoài)"),

        ("Cảm biến DHT11", "VCC, GND", "Chân 10, 11", "Nguồn nuôi +5V DC và Mass chung"),

        ("Màn hình LCD", "RS, RW, EN", "PD6, PD5, PD7", "Các đường tín hiệu chọn thanh ghi, chiều ghi và chốt xung"),

        ("Màn hình LCD", "D4 – D7", "PC4 – PC7", "Bus truyền dữ liệu 4-bit (Nibble cao và Nibble thấp)"),

        ("Khối cảnh báo", "LED 1 – 5", "PD0 – PD4", "Dàn 5 LED đơn cảnh báo ngưỡng quá nhiệt (Active Low)")

    ]

    t4 = doc.add_table(rows=len(t4_data)+1, cols=4)

    t4.alignment = WD_TABLE_ALIGNMENT.CENTER

    t4.columns[0].width = Cm(3.2)

    t4.columns[1].width = Cm(2.4)

    t4.columns[2].width = Cm(3.2)

    t4.columns[3].width = Cm(7.2)

    set_table_borders(t4)

    t4.cell(0, 0).paragraphs[0].add_run("Khối chức năng").bold = True

    t4.cell(0, 1).paragraphs[0].add_run("Chân linh kiện").bold = True

    t4.cell(0, 2).paragraphs[0].add_run("Chân MCU").bold = True

    t4.cell(0, 3).paragraphs[0].add_run("Chức năng kỹ thuật").bold = True

    for c_i in range(4):

        set_cell_shading(t4.cell(0, c_i))

    for r_idx, row in enumerate(t4_data):

        for c_idx in range(4):

            cell_item = t4.cell(r_idx+1, c_idx)

            cell_item.paragraphs[0].add_run(row[c_idx])

            cell_item.paragraphs[0].paragraph_format.first_line_indent = Cm(0)

            cell_item.paragraphs[0].paragraph_format.space_before = Pt(2)

            cell_item.paragraphs[0].paragraph_format.space_after = Pt(2)

            cell_item.paragraphs[0].paragraph_format.line_spacing = 1.15



    add_heading_2("2.2 Xây dựng thuật toán và phần mềm điều khiển")

    add_para(

        "Chương trình chính được tổ chức theo kiến trúc vòng lặp điều khiển tuần tự gồm các pha xử lý:"

    )

    add_para(

        "1. Khởi tạo: Ghi thanh ghi MCUCSR hai lần để tắt JTAG; khởi tạo LCD 4-bit; cấu hình PD0–PD4 là Output và kéo lên mức 1 để tắt LED ban đầu; "

        "hiển thị màn hình chào mừng 'DA2: DO NHIET DO' / 'DHT11 SENSOR' trong 1.5 giây."

    )

    add_para(

        "2. Vòng lặp chính (chu kỳ lấy mẫu 2.0 giây): Gọi hàm DHT11_Read(). "

        "Nhánh 1 -- Đọc thành công (status == 0): Hiển thị nhiệt độ chuẩn 16 ký tự 'Temp: XX.Y °C   ' lên dòng 1 LCD. "

        "So sánh nhiệt độ với ngưỡng 30°C: nếu >= 30°C thì hiển thị 'HIGH Th: 30°C *!' và bật 5 LED (PORTD &= 0xE0); "

        "nếu < 30°C thì hiển thị 'HIGH Th: 30°C   ' và tắt 5 LED (PORTD |= 0x1F). "

        "Nhánh 2 -- Lỗi Checksum (status == -6): Hiển thị 'DHT11: Sum Error' / 'Checksum Invalid' và tắt dàn LED. "

        "Nhánh 3 -- Lỗi mất kết nối / Timeout (status < 0): Hiển thị 'DHT11: No Signal' / 'Check Pin PA1   ' và tắt dàn LED theo trạng thái xác định."

    )



    add_heading_3("2.2.1 Cơ chế bảo vệ Timeout chống treo CPU")

    add_para(

        "Tất cả các vòng lặp chờ sườn xung trong hàm DHT11_Read() đều được gài biến đếm timeout = 10000. "

        "Nếu sau 10.000 chu kỳ lặp mà trạng thái chân PA1 không đổi (do đứt dây hoặc cảm biến hỏng), hàm lập tức thoát ra an toàn "

        "và trả về mã lỗi âm, ngăn ngừa hoàn toàn nguy cơ vi điều khiển bị treo cứng."

    )



    add_heading_3("2.2.2 Kỹ thuật che mặt nạ bit trên PORT D")

    add_para(

        "Vì các chân PD5–PD7 điều khiển LCD và PD0–PD4 điều khiển LED dùng chung thanh ghi PORTD, thuật toán sử dụng phép toán logic bit: "

        "Bật LED bằng PORTD &= 0xE0 (giữ nguyên 3 bit cao, kéo 5 bit thấp về 0); "

        "Tắt LED bằng PORTD |= 0x1F (giữ nguyên 3 bit cao, kéo 5 bit thấp lên 1). "

        "Kỹ thuật này đảm bảo khối cảnh báo không bao giờ làm xáo trộn tín hiệu giao tiếp màn hình."

    )



    add_heading_2("2.3 Quy trình biên dịch và nạp firmware")

    add_para(

        "Mã nguồn được biên dịch tự động bằng Makefile với bộ công cụ avr-gcc: tối ưu hóa dung lượng (-Os), vi điều khiển (-mmcu=atmega16), "

        "tần số xung nhịp (-DF_CPU=8000000UL). Lệnh avr-objcopy trích xuất file tempsen.hex tiêu chuẩn Intel HEX."

    )

    add_para(

        "Các bước nạp chương trình chuẩn hóa vào vi điều khiển ATmega16 trên Kit:"

    )

    add_para("1. Kết nối mạch nạp USBasp giữa cổng USB của máy tính và cổng ISP trên Kit.")

    add_para("2. Khởi chạy phần mềm ProgISP 1.72.")

    add_para("3. Tại mục Select Chip, chọn chính xác tên vi điều khiển: ATMEGA16.")

    add_para("4. Nhấn nút RD (Read) trên giao diện để kiểm tra kết nối phần cứng; phần mềm đọc và báo chuỗi nhận diện ID: 1E : 94 : 03.")

    add_para("5. Thiết lập cấu hình Fuse Bits: Nhập mã 0xD9E4 vào ô Program Fuse (High Fuse = 0xD9, Low Fuse = 0xE4). Tích chọn ô vuông kiểm tra Program Fuse.")

    add_para("6. Nạp file mã máy vào bộ đệm: Nhấn nút Load Flash, chọn đường dẫn tới file src/tempsen.hex.")

    add_para("7. Nhấn nút Auto để thực thi tuần tự các bước: Xóa chip (Erase), Ghi Flash (Write Flash), Kiểm tra lại (Verify Flash) và Ghi cầu chì (Write Fuse). Khi phần mềm báo dòng chữ Successfully done, vi điều khiển lập tức khởi động lại và bắt đầu chạy chương trình.")

    

    img_progisp = os.path.join(os.path.dirname(output_path), "img", "progisp_setup.png")

    if os.path.exists(img_progisp):

        p_prg = doc.add_paragraph()

        p_prg.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_prg.paragraph_format.first_line_indent = Cm(0)

        p_prg.add_run().add_picture(img_progisp, width=Cm(12.5))

        add_figure_caption("Hình 2.4: Giao diện phần mềm ProgISP khi nạp firmware và cấu hình Fuse Bits 0xD9E4")



    # ====================================================

    # CHƯƠNG 3

    # ====================================================

    doc.add_page_break()

    add_heading_1("CHƯƠNG 3. KẾT QUẢ THỰC NGHIỆM")

    

    add_heading_2("3.1 Kết quả thực nghiệm trên phần cứng")

    add_para(

        "Hệ thống đã được kiểm nghiệm thực tế trên Kit phát triển AVR tại phòng thí nghiệm Trường Điện – Điện tử. "

        "Các trạng thái hoạt động được ghi nhận ổn định, chính xác theo đúng thiết kế."

    )

    

    img_actual = os.path.join(os.path.dirname(output_path), "img", "actual_system.png")

    img_disconnect = os.path.join(os.path.dirname(output_path), "img", "sensor_disconnect.png")

    if os.path.exists(img_actual) and os.path.exists(img_disconnect):

        tbl_img = doc.add_table(rows=2, cols=2)

        tbl_img.alignment = WD_TABLE_ALIGNMENT.CENTER

        tbl_img.autofit = False

        col_w = [Cm(7.8), Cm(7.8)]

        for r in tbl_img.rows:

            for c_idx, w in enumerate(col_w):

                r.cells[c_idx].width = w

        

        c00 = tbl_img.cell(0, 0)

        p00 = c00.paragraphs[0]

        p00.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p00.paragraph_format.first_line_indent = Cm(0)

        p00.paragraph_format.space_before = Pt(2)

        p00.paragraph_format.space_after = Pt(2)

        p00.add_run().add_picture(img_actual, width=Cm(7.2))

        

        c01 = tbl_img.cell(0, 1)

        p01 = c01.paragraphs[0]

        p01.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p01.paragraph_format.first_line_indent = Cm(0)

        p01.paragraph_format.space_before = Pt(2)

        p01.paragraph_format.space_after = Pt(2)

        p01.add_run().add_picture(img_disconnect, width=Cm(7.2))

        

        c10 = tbl_img.cell(1, 0)

        p10 = c10.paragraphs[0]

        p10.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p10.paragraph_format.first_line_indent = Cm(0)

        p10.paragraph_format.space_before = Pt(2)

        p10.paragraph_format.space_after = Pt(6)

        r10 = p10.add_run("(a) Màn hình LCD khi cảnh báo quá nhiệt (31.5°C)")

        r10.font.name = 'Times New Roman'

        r10.font.size = Pt(11)

        r10.font.italic = True

        

        c11 = tbl_img.cell(1, 1)

        p11 = c11.paragraphs[0]

        p11.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p11.paragraph_format.first_line_indent = Cm(0)

        p11.paragraph_format.space_before = Pt(2)

        p11.paragraph_format.space_after = Pt(6)

        r11 = p11.add_run("(b) Màn hình LCD khi không có tín hiệu từ cảm biến")

        r11.font.name = 'Times New Roman'

        r11.font.size = Pt(11)

        r11.font.italic = True

        

        add_figure_caption("Hình 3.1: Hình ảnh thực tế hệ thống vận hành trong các kịch bản thử nghiệm")

    elif os.path.exists(img_actual):

        p_act = doc.add_paragraph()

        p_act.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_act.paragraph_format.first_line_indent = Cm(0)

        p_act.add_run().add_picture(img_actual, width=Cm(10.5))

        add_figure_caption("Hình 3.1: Hình ảnh thực tế hệ thống vận hành trong trạng thái cảnh báo quá nhiệt (31.5°C)")

    

    add_table_caption("Bảng 3.1: Bảng tổng hợp các kịch bản kiểm tra và kết quả đánh giá hệ thống")

    t5_data = [

        ("Khởi động hệ thống", "Thực nghiệm trên Kit phần cứng", "–", "Dòng 1: DA2: DO NHIET DO\nDòng 2: DHT11 SENSOR", "Tắt toàn bộ"),

        ("Nhiệt độ bình thường", "Thực nghiệm trên Kit phần cứng", "26.5°C", "Dòng 1: Temp: 26.5 °C\nDòng 2: HIGH Th: 30°C", "Tắt toàn bộ"),

        ("Nhiệt độ vượt ngưỡng", "Thực nghiệm trên Kit phần cứng", "31.5°C", "Dòng 1: Temp: 31.5 °C\nDòng 2: HIGH Th: 30°C *!", "Bật sáng cả 5 LED"),

        ("Mất tín hiệu cảm biến", "Thực nghiệm trên Kit (Rút chân PA1)", "Không xác định", "Dòng 1: DHT11: No Signal\nDòng 2: Check Pin PA1", "Tắt toàn bộ (Xác định)"),

        ("Sai mã Checksum", "Phân tích giải thuật mã nguồn", "Không xác định", "Dòng 1: DHT11: Sum Error\nDòng 2: Checksum Invalid", "Tắt toàn bộ (Xác định)")

    ]

    t5 = doc.add_table(rows=len(t5_data)+1, cols=5)

    t5.alignment = WD_TABLE_ALIGNMENT.CENTER

    t5.autofit = False

    col_w = [Cm(2.8), Cm(3.0), Cm(1.6), Cm(5.6), Cm(3.0)]

    for r in t5.rows:

        for c_idx, w in enumerate(col_w):

            r.cells[c_idx].width = w

    set_table_borders(t5)

    

    headers = [

        "Kịch bản kiểm tra",

        "Phương pháp xác minh",

        "Nhiệt độ",

        "Nội dung hiển thị trên LCD 1602",

        "Trạng thái dàn LED"

    ]

    for c_idx, h_text in enumerate(headers):

        cell_h = t5.cell(0, c_idx)

        p = cell_h.paragraphs[0]

        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p.paragraph_format.first_line_indent = Cm(0)

        p.paragraph_format.space_before = Pt(4)

        p.paragraph_format.space_after = Pt(4)

        r = p.add_run(h_text)

        r.font.name = 'Times New Roman'

        r.font.size = Pt(11)

        r.bold = True

        set_cell_shading(cell_h)

        

    col_aligns = [

        WD_ALIGN_PARAGRAPH.LEFT,

        WD_ALIGN_PARAGRAPH.LEFT,

        WD_ALIGN_PARAGRAPH.CENTER,

        WD_ALIGN_PARAGRAPH.LEFT,

        WD_ALIGN_PARAGRAPH.CENTER

    ]

    

    for r_idx, row in enumerate(t5_data):

        for c_idx in range(5):

            cell_item = t5.cell(r_idx+1, c_idx)

            p = cell_item.paragraphs[0]

            p.alignment = col_aligns[c_idx]

            p.paragraph_format.first_line_indent = Cm(0)

            p.paragraph_format.space_before = Pt(3)

            p.paragraph_format.space_after = Pt(3)

            p.paragraph_format.line_spacing = 1.15

            

            raw_val = row[c_idx]

            if c_idx == 3:

                # Format LCD lines cleanly with bold label and monospace code

                lines = raw_val.split('\n')

                for l_i, l_text in enumerate(lines):

                    if l_i > 0:

                        p.add_run('\n')

                    if ': ' in l_text:

                        lbl_part, code_part = l_text.split(': ', 1)

                        r_lbl = p.add_run(lbl_part + ': ')

                        r_lbl.font.name = 'Times New Roman'

                        r_lbl.font.size = Pt(10.5)

                        r_lbl.bold = True

                        r_code = p.add_run(code_part)

                        r_code.font.name = 'Consolas'

                        r_code.font.size = Pt(10)

                    else:

                        r = p.add_run(l_text)

                        r.font.name = 'Times New Roman'

                        r.font.size = Pt(10.5)

            else:

                r = p.add_run(raw_val)

                r.font.name = 'Times New Roman'

                r.font.size = Pt(11)

                if c_idx == 0:

                    r.bold = True



    add_heading_2("3.2 Đánh giá kết quả thực nghiệm")

    add_para(

        "Qua quá trình thử nghiệm thực tế trên phần cứng Kit vi điều khiển, hệ thống đã đạt được các kết quả kỹ thuật đề ra: "

        "giao tiếp Aosong 1-Wire ổn định giữa ATmega16 và cảm biến DHT11 với chu kỳ 2.0 giây; thuật toán Checksum cộng 8-bit hỗ trợ phát hiện lỗi bit truyền dữ liệu do biến dạng tín hiệu (dù có giới hạn toán học không bắt được mọi tổ hợp lỗi bù trừ đồng thời); "

        "kết quả thử nghiệm thực tế trên Kit (Hình 3.1a) ghi nhận LCD hiển thị giá trị 31.5°C kèm ký hiệu cảnh báo '*!' và kích hoạt 5 LED cảnh báo (lưu ý tài liệu Aosong quy định độ phân giải danh định 1°C, báo cáo chỉ ghi nhận hiển thị trực tiếp trên LCD trong phiên thử nghiệm mà không khẳng định độ phân giải phần cứng vượt chuẩn); "

        "hệ thống phân định rõ hai cơ chế bảo vệ độc lập: bộ đếm Timeout ngăn treo vi điều khiển khi mất kết nối cảm biến vật lý, trong khi Checksum loại bỏ gói tin sai lệch do can nhiễu, chủ động đưa 5 LED về mức tắt xác định (PORTD |= 0x1F) và hiển thị thông điệp chẩn đoán chi tiết trên LCD."

    )



    # ====================================================

    # CHƯƠNG 4

    # ====================================================

    doc.add_page_break()

    add_heading_1("CHƯƠNG 4. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    

    add_heading_2("4.1 Kết luận")

    add_para(

        "Đề tài Đồ án Thiết kế II đã hoàn thành xuất sắc các mục tiêu đề ra: nắm vững kiến trúc vi điều khiển AVR ATmega16, "

        "thành thạo lập trình C bare-metal, làm chủ giao thức truyền thông 1-Wire số với cảm biến DHT11, "

        "tối ưu hóa giao tiếp LCD 1602 chế độ 4-bit và dàn LED cảnh báo qua kỹ thuật che mặt nạ bit PORTD. "

        "Hệ thống đạt độ ổn định cao, phản ứng chính xác khi nhiệt độ vượt ngưỡng an toàn và xử lý lỗi linh hoạt khi mất kết nối."

    )



    add_heading_2("4.2 Hạn chế của đề tài")

    add_para(

        "Cảm biến DHT11 có dải đo hẹp (0°C – 50°C), sai số ±2°C và tốc độ lấy mẫu chậm (1.5s – 2.0s). "

        "Ngưỡng nhiệt độ cảnh báo 30°C hiện đang được gán cố định trong code, chưa có bàn phím tương tác để thay đổi trực tiếp trên phần cứng. "

        "Hệ thống chưa có bộ nhớ lưu trữ lịch sử đo lường và chưa hỗ trợ truyền dữ liệu không dây."

    )



    add_heading_2("4.3 Hướng phát triển mở rộng")

    add_para(

        "1. Nâng cấp cảm biến công nghiệp độ chính xác cao: DHT22, Sensirion SHT30/SHT35 hoặc Bosch BME280."

    )

    add_para(

        "2. Tích hợp bàn phím ma trận 4x4 kết hợp còi báo buzzer: Cho phép người dùng trực tiếp cài đặt ngưỡng cảnh báo và lưu vào bộ nhớ EEPROM nội của vi điều khiển."

    )

    add_para(

        "3. Tích hợp kết nối không dây IoT: Sử dụng mô-đun Wi-Fi ESP8266/ESP32 hoặc LoRa để đẩy dữ liệu lên Cloud Server (MQTT, Blynk, ThingsBoard) "

        "giúp giám sát biểu đồ nhiệt độ và nhận thông báo cảnh báo từ xa qua điện thoại thông minh."

    )



    # ====================================================

    # TÀI LIỆU THAM KHẢO

    # ====================================================

    doc.add_page_break()

    add_heading_1("TÀI LIỆU THAM KHẢO")

    

    refs = [

        "[1] Atmel Corporation, 'ATmega16/ATmega16L 8-bit AVR Microcontroller with 16K Bytes In-System Programmable Flash Datasheet', Document Rev. 2466T–AVR–07/10, San Jose, CA, USA, 2010.",

        "[2] Aosong Electronics Co., Ltd, 'DHT11 Humidity & Temperature Sensor Product Manual', Guangzhou Aosong Electronics Co., Ltd, Guangzhou, China, 2015.",

        "[3] Hitachi Semiconductor and Integrated Circuits, 'HD44780U (Dot Matrix Liquid Crystal Display Controller/Driver) Technical Data', Rev. 0.0, Tokyo, Japan, 1998.",

        "[4] Trường Điện – Điện tử (Viện Điện tử – Viễn thông), Đại học Bách khoa Hà Nội, 'Tài liệu hướng dẫn thực hành và sơ đồ nguyên lý Kit vi điều khiển AVR ATmega16', Hà Nội, 2022.",

        "[5] Ngô Diên Tập, 'Kỹ thuật vi điều khiển và ứng dụng – Lập trình họ vi điều khiển AVR', Nhà xuất bản Khoa học và Kỹ thuật, Hà Nội, 2012.",

        "[6] Free Software Foundation, 'AVR-GCC and AVR Libc User Manual – A C runtime library for Atmel AVR microcontrollers', https://www.nongnu.org/avr-libc/, truy cập tháng 10/2026.",

        "[7] Trường Điện – Điện tử, Đại học Bách khoa Hà Nội, 'Quy định về thể thức văn bản và cấu trúc báo cáo Đồ án môn học – Đồ án tốt nghiệp bậc đại học', Hà Nội, 2023."

    ]

    for r_item in refs:

        p_ref = doc.add_paragraph()

        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        p_ref.paragraph_format.space_before = Pt(2)

        p_ref.paragraph_format.space_after = Pt(4)

        p_ref.paragraph_format.line_spacing = 1.2

        p_ref.paragraph_format.first_line_indent = Cm(0)

        p_ref.paragraph_format.left_indent = Cm(1.0)

        run = p_ref.add_run(r_item)

        run.font.name = 'Times New Roman'

        run.font.size = Pt(12)



    # ====================================================

    # PHỤ LỤC

    # ====================================================

    doc.add_page_break()

    add_heading_1("PHỤ LỤC: TOÀN BỘ MÃ NGUỒN CHƯƠNG TRÌNH")

    

    add_heading_2("Phụ lục A: File mã nguồn chính tempsen.c")

    src_c_path = "src/tempsen.c"

    if os.path.exists(src_c_path):

        with open(src_c_path, "r", encoding="utf-8") as f:

            code_c = f.read()

        add_code_block(code_c)

        

    doc.add_page_break()

    add_heading_2("Phụ lục B: Thư viện điều khiển LCD hunget_lcd.h")

    src_h_path = "src/hunget_lcd.h"

    if os.path.exists(src_h_path):

        with open(src_h_path, "r", encoding="utf-8") as f:

            code_h = f.read()

        add_code_block(code_h)



    doc.save(output_path)

    print(f"Report DOCX successfully generated at: {output_path}")



if __name__ == "__main__":

    out_file = os.path.join(os.path.dirname(__file__), "Bao_cao_DATK2_ATmega16_DHT11.docx")

    create_report_docx(out_file)

