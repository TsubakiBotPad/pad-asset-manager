from .region import Region
from ..servers.load_servers import load_servers

REGIONS = [
    'Japan',
    'North America',
    'Korea',
    'Hong Kong',
]


class Regions:
    japan = Region('Japan')
    north_america = Region('North America')
    korea = Region('Korea')
    hong_kong = Region('Hong Kong')


regions = Regions()
load_servers(regions)
