# coding=utf-8

import mapnik
import cv2


def create_map(shapefile, style_file, output_image, size=(800, 600)):
    """Creates a map from a XML file and writes it to an image.

    :param shapefile: Shapefile containing the data for the map.
    :param style_file: Mapnik XML file.
    :param output_image: Name of the output image file.
    :param size: Size of the map in pixels.
    """
    map = mapnik.Map(*size)
    mapnik.load_map(map, style_file)

    data_source = mapnik.Shapefile(file=shapefile)
    layers = map.layers
    layer = layers[0]
    layer.datasource = data_source

    map.zoom_all()
    mapnik.render_to_file(map, output_image)


def display_map(image_file):
    """Opens and displays a map image file.

    :param image_file: Path to the image.
    """
    image = cv2.imread(image_file)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    map_image = '../output/world3.png'
    create_map('../../data/world_borders_simple.shp',
               'map_style.xml',map_image, size=(1024, 500))
    display_map(map_image)