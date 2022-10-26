# coding=utf-8
from osgeo import gdal
from models import Geocache, PointCollection
from utils.geo_functions import transform_geometries, open_vector_file, transform_points
import numpy as np
import math


def main():
    print("Hello geocaching APP!")


class GeocachingApp(PointCollection):
    def __init__(self, data_file=None, my_location=None):
        """Application class.

        :param data_file: An OGR compatible file
         with geocaching points.
        :param my_location: Coordinates of your location.
        """
        super(GeocachingApp, self).__init__(file_path=data_file)

        self._datasource = None
        self._transformed_geoms = None
        self._my_location = None
        self.distances = None

        if my_location:
            self.my_location = my_location

    def open_file(self, file_path):
        """Open a file containing geocaching data
        and prepare it for use.

        :param file_path:
        """
        self._datasource = open_vector_file(file_path)
        self._transformed_geoms = transform_geometries(
            self._datasource, 4326, 3395)

    def calculate_distances(self):
        """Calculates the distance between a
        set of points and a given location.

        :return: A list of distances in the same order as
         the points.
        """
        xa = self.my_location[0]
        ya = self.my_location[1]
        points = self._transformed_geoms
        distances = []
        for geom in points:
            vertical_distance = geom.GetY() - ya
            horizontal_distance = geom.GetX() - xa
            point_distance = math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)
            distances.append(point_distance)
        return distances

    def find_closest_point(self):
        """Find the closest point to a given location and
        return the cache that's on that point.

        :return: OGR feature containing the point.
        """
        # Part 1.
        distances = self.calculate_distances()
        index = np.argmin(distances)
        # Part 2.
        layer = self._datasource.GetLayerByIndex(0)
        feature = layer.GetFeature(index)
        print("Closest point at: {}m".format(distances[index]))
        return feature

    @property
    def my_location(self):
        return self._my_location

    @my_location.setter
    def my_location(self, coordinates):
        self._my_location = transform_points([coordinates])[0]


if __name__ == "__main__":
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    # Create the application:
    my_app = GeocachingApp()
    # Now we will call a method from the PointCollection class:
    my_app.import_data("../data/geocaching.gpx")