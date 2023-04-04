#pad\_asset_manager


##Description

A Python package for the popular iOS & Android game "Puzzle & Dragons" (PAD).

#Installation
```
pip install pad_asset_manager
```

#Example Usage
```py
>>> import pad_asset_manager as padtools
>>> na_server = padtools.regions.north_america.server
>>> jp_server = padtools.regions.japan.server
>>> na_server.version
'20.40'
>>> jp_server.version
'20.61'
>>> len(na_server.assets)
8661
>>> len(jp_server.assets)
10002
>>> jp_server.assets[0].url
'https://dl.padsv.gungho.jp/ext/mon2303312000111144657726426bd3bcd5e4/mons_001.bc'

```