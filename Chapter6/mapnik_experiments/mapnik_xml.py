# coding=utf-8

import mapnik


map = mapnik.Map(800, 600)
mapnik.load_map(map, 'map_style.xml')
map.zoom_all()
mapnik.render_to_file(map, '../output/world2.png')