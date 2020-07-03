from models import Instrument


def main():
    Instrument.object.bulk_create([
        Instrument(name='ヴァイオリン', section_name='弦', short_name='Vn'),
        Instrument(name='ヴィオラ', section_name='弦', short_name='Va'),
        Instrument(name='チェロ', section_name='弦', short_name='Vc'),
        Instrument(name='コントラバス', section_name='弦', short_name='Cb'),
        Instrument(name='フルート', section_name='木', short_name='Fl'),
        Instrument(name='オーボエ', section_name='木', short_name='Ob'),
        Instrument(name='クラリネット', section_name='木', short_name='Cl'),
        Instrument(name='ファゴット', section_name='木', short_name='Fg'),
        Instrument(name='ホルン', section_name='金', short_name='Hr'),
        Instrument(name='トランペット', section_name='金', short_name='Tp'),
        Instrument(name='トロンボーン', section_name='金', short_name='Tb'),
        Instrument(name='チューバ', section_name='金', short_name='Tu'),
        Instrument(name='パーカッション', section_name='打', short_name='Per'),
        Instrument(name='ピアノ', section_name='鍵', short_name='Pf'),
    ])
    return 0
