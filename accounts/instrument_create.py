from .models import Part


def main():
    Part.object.bulk_create([
        Instrument(name='ヴァイオリン', wind=False, woodwind=False, brass=False, string=True, short_name='Vn.'),
        Instrument(name='ヴィオラ', wind=False, woodwind=False, brass=False, string=True, short_name='Va.'),
        Instrument(name='チェロ', wind=False, woodwind=False, brass=False, string=True, short_name='Vc.'),
        Instrument(name='コントラバス', wind=False, woodwind=False, brass=False, string=True, short_name='Cb.'),
        Instrument(name='フルート', wind=True, woodwind=True, brass=False, string=False, short_name='Fl.'),
        Instrument(name='オーボエ', wind=True, woodwind=True, brass=False, string=False, short_name='Ob.'),
        Instrument(name='クラリネット', wind=True, woodwind=True, brass=False, string=False, short_name='Cl.'),
        Instrument(name='ファゴット', wind=True, woodwind=True, brass=False, string=False, short_name='Fg.'),

        Instrument(name='ホルン', wind=True, woodwind=False, brass=True, string=False, short_name='Hr.'),
        Instrument(name='トランペット', wind=True, woodwind=False, brass=True, string=False, short_name='Tp.'),
        Instrument(name='トロンボーン', wind=True, woodwind=False, brass=True, string=False, short_name='Tb.'),
        Instrument(name='チューバ', wind=True, woodwind=False, brass=True, string=False, short_name='Tu.'),

        Instrument(name='パーカッション', wind=False, woodwind=False, brass=False, string=False, short_name='Per.'),
        Instrument(name='その他', wind=False, woodwind=False, brass=False, string=False, short_name='Etc.'),
    ])
    return 0
