# coding=utf-8
from osgeo import gdal
from models import PointCollection, BoundaryCollection
from utils.geo_functions import transform_geometries, open_vector_file, transform_points
import numpy as np
import math


def main():
    print("Hello geocaching APP!")


class GeocachingApp(object):
    def __init__(self,
                 geocaching_file=None,
                 boundary_file=None,
                 my_location=None):
        """Application class.

        :param geocaching_file: An OGR compatible file
         with geocaching points.
        :param boundary_file: A file with boundaries.
        :param my_location: Coordinates of your location.
        """
        self.geocaching_data = PointCollection(geocaching_file)
        self.boundaries = BoundaryCollection(boundary_file)
        self._my_location = None
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

    def filter_by_country(self, name):
        """Filter by a country with a given name.

        :param name: The name of the boundary (ex. county name)
        :return: PointCollection
        """
        boundary = self.boundaries.get_by_name(name)
        return self.geocaching_data.filter_by_boundary(boundary)

    @property
    def my_location(self):
        return self._my_location

    @my_location.setter
    def my_location(self, coordinates):
        self._my_location = transform_points([coordinates])[0]


if __name__ == "__main__":
    my_app = GeocachingApp("../data/geocaching.gpx",
                           "../data/world_borders_simple.shp")
    usa_boundary = my_app.boundaries.get_by_name('United States')
    result = my_app.geocaching_data.filter_by_boundary(
        usa_boundary)
    print(result)
