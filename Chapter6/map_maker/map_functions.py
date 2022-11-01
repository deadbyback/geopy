# coding=utf-8

import mapnik
import cv2


def display_map(image_file):
    """Opens and displays a map image file.

    :param image_file: Path to the image.
    """
    image = cv2.imread(image_file)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_map(shapefile, gpx_file, style_file, output_image,
               size=(800, 600)):
    """Creates a map from a XML file and writes it to an image.

    :param gpx_file:
    :param shapefile: Shapefile containing the data for the map.
    :param style_file: Mapnik XML file.
    :param output_image: Name of the output image file.
    :param size: Size of the map in pixels.
    """
    map = mapnik.Map(*size)
    mapnik.load_map(map, style_file)
    layers = map.layers

    # Add the shapefile.
    world_datasource = mapnik.Shapefile(file=shapefile)
    world_layer = mapnik.Layer('world')
    world_layer.datasource = world_datasource
    world_layer.styles.append('style1')
    layers.append(world_layer)

    # Add the shapefile.
    points_datasource = mapnik.Ogr(file=gpx_file, layer='waypoints')
    points_layer = mapnik.Layer('geocaching_points')
    points_layer.datasource = points_datasource
    points_layer.styles.append('style2')
    layers.append(points_layer)

    map.zoom_all()
    mapnik.render_to_file(map, output_image)


if __name__ == '__main__':
    map_image = '../output/world3.png'
    create_map('../../data/world_borders_simple.shp',
               '../../data/geocaching.gpx',
               '../map_maker/styles.xml', map_image, size=(1024, 500))
    display_map(map_image)
