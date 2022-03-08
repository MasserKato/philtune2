from .models import Part


def main():
    Part.objects.bulk_create([
        Part(name='ヴァイオリン', wind=False, woodwind=False, brass=False, string=True, short_name='Vn.'),
        Part(name='ヴィオラ', wind=False, woodwind=False, brass=False, string=True, short_name='Va.'),
        Part(name='チェロ', wind=False, woodwind=False, brass=False, string=True, short_name='Vc.'),
        Part(name='コントラバス', wind=False, woodwind=False, brass=False, string=True, short_name='Cb.'),
        Part(name='フルート', wind=True, woodwind=True, brass=False, string=False, short_name='Fl.'),
        Part(name='オーボエ', wind=True, woodwind=True, brass=False, string=False, short_name='Ob.'),
        Part(name='クラリネット', wind=True, woodwind=True, brass=False, string=False, short_name='Cl.'),
        Part(name='ファゴット', wind=True, woodwind=True, brass=False, string=False, short_name='Fg.'),

        Part(name='ホルン', wind=True, woodwind=False, brass=True, string=False, short_name='Hr.'),
        Part(name='トランペット', wind=True, woodwind=False, brass=True, string=False, short_name='Tp.'),
        Part(name='トロンボーン', wind=True, woodwind=False, brass=True, string=False, short_name='Tb.'),
        Part(name='チューバ', wind=True, woodwind=False, brass=True, string=False, short_name='Tu.'),

        Part(name='パーカッション', wind=False, woodwind=False, brass=False, string=False, short_name='Per.'),
        Part(name='その他', wind=False, woodwind=False, brass=False, string=False, short_name='Etc.'),
    ])
    return 0
