from .server import Server

SERVERS = {
    'jp': {
        'ios_url': 'http://dl.padsv.gungho.jp/base.json',
        'android_url': 'http://patch-pad.gungho.jp/base_adr.json',
        'regions': [
            'japan'
        ]
    },
    'na': {
        'ios_url': 'http://patch-na-pad.gungho.jp/base-na.json',
        'android_url': 'http://patch-na-pad.gungho.jp/base-na-adr.json',
        'regions': [
            'north_america'
        ]
    },
    'ht': {
        'ios_url': 'http://dl.padsv.gungho.jp/base.ht-ios.json',
        'android_url': 'http://dl.padsv.gungho.jp/base.ht-adr.json',
        'regions': [
            'hong_kong'
        ]
    },
    'kr': {
        'ios_url': 'http://patch-kr-pad.gungho.jp/base.kr-ios.json',
        'android_url': 'http://patch-kr-pad.gungho.jp/base.kr-adr.json',
        'regions': [
            'korea'
        ]
    }
}


def load_servers(regions):
    for svr in SERVERS.values():
        new_server = Server(svr['ios_url'], svr['android_url'])
        for region_identifier in svr['regions']:
            region = getattr(regions, region_identifier)
            region.server = new_server
