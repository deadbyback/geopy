# coding=utf-8
from osgeo import osr, ogr


def open_vector_file(file_path):
    """Opens a vector file compatible with OGR, get the first layer
    and returns the ogr datasource.

    :param str file_path: The full path to the file.
    :return: The ogr datasource.
    """
    datasource = ogr.Open(file_path)
    layer = datasource.GetLayerByIndex(0)
    print("Opening {}".format(file_path))
    print("Number of features: {}".format(
        layer.GetFeatureCount()))
    return datasource


def transform_geometries(datasource, src_epsg, dst_epsg):
    """Transform the coordinates of all geometries in
    the first layer.
    """

    # Part 1
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(src_epsg)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(dst_epsg)
    transformation = osr.CoordinateTransformation(src_srs, dst_srs)
    layer = datasource.GetLayerByIndex(0)

    # Part 2
    geoms = []
    layer.ResetReading()
    for feature in layer:
        geom = feature.GetGeometryRef().Clone()
        geom.Transform(transformation)
        geoms.append(geom)
    return geoms


def create_transform(src_epsg, dst_epsg):
    """Creates an OSR tranformation.

    :param src_epsg: EPSG code for the source geometry.
    :param dst_epsg: EPSG code for the destination geometry.
    :return: osr.CoordinateTransformation
    """
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(src_epsg)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(dst_epsg)
    return osr.CoordinateTransformation(src_srs, dst_srs)


def transform_points(points, src_epsg=4326, dst_epsg=3395):
    """Transform the coordinate reference system of a list of coordinates (a list of points)

     :param points:
     :param src_epsg: EPSG code for the source geometry.
     :param dst_epsg: EPSG code for the destination geometry.
     """
    transform = create_transform(src_epsg, dst_epsg)
    points = transform.TransformPoints(points)
    return points


if __name__ == "__main__":
    open_vector_file("../../data/geocaching.gpx")
