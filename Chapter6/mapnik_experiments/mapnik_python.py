# coding=utf-8

import mapnik


# Create a Map
map = mapnik.Map(800, 600)
# Set the background color of the map.
map.background = mapnik.Color('white')

# Create a Style and a Rule.
style = mapnik.Style()
rule = mapnik.Rule()

# Create a PolygonSymbolizer to fill the polygons and
# add it to the rule.
polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill = mapnik.Color('#f2eff9')
rule.symbols.append(polygon_symbolizer)
# Create a LineSymbolizer to style the polygons borders and
# add it to the rule.
line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
line_symbolizer.stroke_opacity = 0.1
rule.symbols.append(line_symbolizer)

# Add the rule to the style.
style.rules.append(rule)

# Add the Style to the Map.
map.append_style('My Style', style)

# Create a data source from a shapefile.
data = mapnik.Shapefile(file='../../data/world_borders_simple.shp')

# Create a layer giving it the name 'world'.
layer = mapnik.Layer('world')
# Set the layer data source and add the style to the layer.
layer.datasource = data
layer.styles.append('My Style')
# Add the layer to the map.
map.layers.append(layer)

# Zoom the map to the extent of all layers.
map.zoom_all()
# Write the map to a image.
mapnik.render_to_file(map,'../output/world.png', 'png')