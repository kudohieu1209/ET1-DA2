"""Build the editable SVG and its vector PDF for Figure 2.4.

Requires svglib and reportlab; uses Times New Roman / Courier New on Windows.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from svglib.fonts import register_font

HERE = Path(__file__).resolve().parent
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
root = ET.Element(f'{{{NS}}}svg', {
    'width': '180mm', 'height': '225mm', 'viewBox': '0 0 1080 1350',
    'role': 'img', 'aria-labelledby': 'title description',
})

def node(kind, parent=root, **attrs):
    return ET.SubElement(parent, f'{{{NS}}}{kind}', {k.replace('_', '-'): str(v) for k, v in attrs.items()})

node('title', id='title').text = 'Lưu đồ đo nhiệt độ, cảnh báo và xử lý lỗi'
node('desc', id='description').text = (
    'Khởi tạo, đọc DHT11, kiểm tra status, so sánh ngưỡng 30 độ C hoặc '
    'phân loại checksum và timeout, cập nhật LCD và LED, trễ 2 giây rồi đọc lại.'
)
node('rect', width=1080, height=1350, fill='white')
INK = '#344B5E'
LINE = '#607487'

def text(x, y, lines, size=26, bold=False, mono=False, color=INK, gap=33):
    family = 'Courier New' if mono else 'Times New Roman'
    for i, line in enumerate(lines):
        t = node('text', x=x, y=y + i * gap, text_anchor='middle',
                 font_family=family, font_size=size,
                 font_weight='bold' if bold else 'normal', fill=color)
        t.text = line

def box(cx, cy, w, h, fill='#F1F5F9', stroke=LINE, radius=10):
    node('rect', x=cx-w/2, y=cy-h/2, width=w, height=h, rx=radius,
         fill=fill, stroke=stroke, stroke_width=2)

def diamond(cx, cy, w, h):
    node('polygon', points=f'{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}',
         fill='#F8FAFC', stroke=LINE, stroke_width=2)

def path(points, arrow=True, color=LINE, width=2.3):
    node('polyline', points=' '.join(f'{x},{y}' for x,y in points),
         fill='none', stroke=color, stroke_width=width,
         stroke_linejoin='round', stroke_linecap='round')
    if arrow:
        (x0,y0),(x,y)=points[-2:]
        dx,dy=x-x0,y-y0
        length=(dx*dx+dy*dy)**0.5
        ux,uy=dx/length,dy/length
        bx,by=x-11*ux,y-11*uy
        node('polygon', points=f'{x},{y} {bx-4.5*uy},{by+4.5*ux} {bx+4.5*uy},{by-4.5*ux}', fill=color)

# A quiet central spine with two explicit branch decisions and four equal cards.
box(540,65,200,58,fill='white',stroke=INK,radius=29)
text(540,74,['Bắt đầu'],size=28,bold=True)
box(540,207,490,112)
text(540,192,['Tắt JTAG; khởi tạo LCD và LED', 'Hiện màn hình chào khoảng 1,5 s'],gap=34)
box(540,355,410,84)
text(540,347,['Đọc DHT11'],bold=True)
text(540,380,['Nhận mã trạng thái status'],size=24)
diamond(540,520,350,144)
text(540,513,['Đọc thành công?'],size=26)
text(540,548,['status == 0'],size=24,mono=True)

diamond(290,755,340,140)
text(290,764,['temp_int >= 30?'],size=24,mono=True)
diamond(800,755,340,140)
text(800,764,['status == -6?'],size=24,mono=True)

cards = [
    (165, '#FFF2F0', '#A85C54', 'CẢNH BÁO', ['Hiện nhiệt độ + *!', 'Bật 5 LED']),
    (415, '#F0F7F3', '#668673', 'BÌNH THƯỜNG', ['Hiện nhiệt độ', 'và ngưỡng; tắt LED']),
    (665, '#FFF8EB', '#9B824B', 'LỖI CHECKSUM', ['Hiện lỗi checksum', 'Tắt 5 LED']),
    (915, '#FFF8EB', '#9B824B', 'MẤT TÍN HIỆU', ['Hiện lỗi mất tín hiệu', 'Tắt 5 LED']),
]
for cx, fill, stroke, title, body in cards:
    box(cx,1000,220,150,fill=fill,stroke=stroke)
    text(cx,968,[title],size=21,bold=True,color=stroke)
    text(cx,1009,body,size=23,gap=34)

box(540,1220,410,80)
text(540,1228,['Trễ phần mềm 2 giây'],size=28)

path([(540,94),(540,151)])
path([(540,263),(540,313)])
path([(540,397),(540,448)])
path([(365,520),(290,520),(290,685)])
text(309,505,['Có'],size=24)
path([(715,520),(800,520),(800,685)])
text(781,505,['Không'],size=24)
path([(120,755),(90,755),(90,880),(165,880),(165,925)])
text(87,736,['Có'],size=24)
path([(290,825),(290,875),(415,875),(415,925)])
text(350,861,['Không'],size=24)
path([(630,755),(600,755),(600,880),(665,880),(665,925)])
text(592,736,['Có'],size=24)
path([(970,755),(1000,755),(1000,880),(915,880),(915,925)])
text(998,736,['Không'],size=24)
for cx, *_ in cards:
    path([(cx,1075),(cx,1125)],arrow=False)
path([(165,1125),(915,1125)],arrow=False)
path([(540,1125),(540,1180)])
path([(335,1220),(25,1220),(25,355),(335,355)])
text(134,1203,['Lặp lại'],size=23)

svg = HERE / 'main-flowchart.svg'
ET.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)

# Embed Unicode fonts so the report stays vector and the accents stay correct.
for name, file in [('Times New Roman','times.ttf'),
                   ('Times New Roman-Bold','timesbd.ttf'),
                   ('Courier New','cour.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
pdfmetrics.registerFontFamily('Times New Roman',normal='Times New Roman',bold='Times New Roman-Bold')
register_font('Times New Roman', 'C:/Windows/Fonts/times.ttf', rlgFontName='Times New Roman')
register_font('Times New Roman', 'C:/Windows/Fonts/timesbd.ttf', weight='bold', rlgFontName='Times New Roman-Bold')
register_font('Courier New', 'C:/Windows/Fonts/cour.ttf', rlgFontName='Courier New')
drawing = svg2rlg(str(svg))
renderPDF.drawToFile(drawing, str(HERE / 'main-flowchart.pdf'))
print('Built',svg,'and vector PDF')
