# coding=utf-8

from osgeo import gdal
from pprint import pprint
from utils.geo_functions import open_vector_file
import os


class Geocache(object):
    """This class represents a single geocaching point."""

    def __init__(self, lat, lon, attributes=None):
        self.lat = lat
        self.lon = lon
        self.attributes = attributes

    @property
    def coordinates(self):
        return self.lat, self.lon


class PointCollection(object):
    def __init__(self, file_path=None):
        """This class represents a group of vector data."""
        self.data = []
        self.epsg = None

        if file_path:
            self.import_data(file_path)

    def __add__(self, other):
        self.data += other.data
        return self

    def import_data(self, file_path):
        """Opens a vector file compatible with OGR and parses
         the data.

        :param str file_path: The full path to the file.
        """
        features, metadata = open_vector_file(file_path)
        self._parse_data(features)
        self.epsg = metadata['epsg']
        print("File imported: {}".format(file_path))

    def _parse_data(self, features):
        """Transforms the data into Geocache objects.

        :param features: A list of features.
        """
        for feature in features:
            geom = feature['geometry']['coordinates']
            attributes = feature['properties']
            cache_point = Geocache(geom[0], geom[1], attributes=attributes)
            self.data.append(cache_point)

    def describe(self):
        print("SRS EPSG code: {}".format(self.epsg))
        print("Number of features: {}".format(len(self.data)))


if __name__ == '__main__':
    gdal.PushErrorHandler('CPLQuietErrorHandler')

    my_data = PointCollection("../data/geocaching.gpx")
    my_other_data = PointCollection("../data/geocaching.shp")
    merged_data = my_data + my_other_data
    merged_data.describe()
