# coding=utf-8

import platform
import tempfile
import cv2
import mapnik

from Chapter5.models import BoundaryCollection


class MapMakerApp(object):
    def __init__(self, output_image=None):
        """Application class."""
        self.output_image = output_image

    def display_map(self):
        """Opens and displays a map image file.

        :param image_file: Path to the image.
        """
        image = cv2.imread(self.output_image)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def create_map(self):
        """Creates a map and writes it to a file."""
        map = mapnik.Map(*self.map_size)
        mapnik.load_map(map, self.style_file)
        layers = map.layers
        for name, layer in self._layers.iteritems():
            new_layer = mapnik.Layer(name)
            new_layer.datasource = layer["data source"]
            new_layer.stylers.append(layer['style'])
            layers.append(new_layer)
        map.zoom_all()
        mapnik.render_to_file(map, self.output_image)

    def add_layer(self, geo_data, name, style='style1'):
        """Add data to the map to be displayed in a layer
        with a given style.

        :param geo_data: a BaseGeoCollection subclass instance.
        """
        if platform.system() == "Windows":
            print("Windows system")
            temp_file, filename = tempfile.mkstemp(dir="temp")
            print(temp_file, filename)
            geo_data.export_geojson(filename)
            data_source = mapnik.GeoJSON(file=filename)
        else:
            data_source = mapnik.Python(factory='MapDatasource',
                                        data=geo_data)
        layer = {"data source": data_source,
                 "data": geo_data,
                 "style": style}
        self._layers[name] = layer


if __name__ == '__main__':
    world_borders = BoundaryCollection(
        "../../data/world_borders_simple.shp")
    countries = world_borders.filter('name', 'China') + \
                world_borders.filter('name', 'India') + \
                world_borders.filter('name', 'Japan')
    map_app = MapMakerApp()
    map_app.add_layer(countries, 'countries')
    map_app.create_map()
    map_app.display_map()
