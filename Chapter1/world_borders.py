from osgeo import gdal, ogr

# Open the shapefile and get the first layer.
datasource = ogr.Open("../data/world_borders_simple.shp")
layer = datasource.GetLayerByIndex(0)
print("Number of features: {}".format(layer.GetFeatureCount()))

# Inspect the fields available in the layer.
feature_definition = layer.GetLayerDefn()
for field_index in range(feature_definition.GetFieldCount()):
    field_definition = feature_definition.GetFieldDefn(field_index)
    print("\t{}\t{}\t{}".format(field_index,
                                field_definition.GetTypeName(),
                                field_definition.GetName()))

# Print a list of country names.
layer.ResetReading()
for feature in layer:
    print(feature.GetFieldAsString(4))