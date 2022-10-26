# coding=utf-8

from osgeo import gdal
from pprint import pprint
from utils.geo_functions import open_vector_file, transform_geometry, convert_length_unit
import os
from shapely.geometry import Point
from shapely import wkb, wkt


class BaseGeoObject(object):
    """Base class for a single geo object."""
    def __init__(self, geometry, attributes=None):
        self.geom = geometry
        self.attributes = attributes
        self.wm_geom = None

        # Makes a lookup table of case-insensitive attributes.
        self._attributes_lowercase = {}
        for key in self.attributes.keys():
            self._attributes_lowercase[key.lower()] = key

    def transformed_geom(self):
        """Returns the geometry transformed into WorldMercator
        coordinate system.
        """
        if not self.wm_geom:
            geom = transform_geometry(self.geom.wkb)
            self.wm_geom = wkb.loads(geom)
        return self.wm_geom

    def get_attribute(self, attr_name, case_sensitive=False):
        """Gets an attribute by its name.

        :param attr_name: The name of the attribute.
        :param case_sensitive: True or False.
        """
        if not case_sensitive:
            attr_name = attr_name.lower()
            attr_name = self._attributes_lowercase[attr_name]
        return self.attributes[attr_name]

    def __repr__(self):
        raise NotImplementedError


class Geocache(BaseGeoObject):
    """This class represents a single geocaching point."""

    def __init__(self, geometry, attributes=None):
        super(Geocache, self).__init__(geometry, attributes)

    def __repr__(self):
        name = self.attributes.get('name', 'Unnamed')
        return "{} {}  -  {}".format(self.geom.x,
                                     self.geom.y, name)


class Boundary(BaseGeoObject):
    """Represents a single geographic boundary."""

    def __repr__(self):
        return self.get_attribute('name')


class BaseGeoCollection(object):
    """This class represents a collection of spatial data."""

    def __init__(self, file_path=None):
        self.data = []
        self.epsg = None

        if file_path:
            self.import_data(file_path)

    def __add__(self, other):
        self.data += other.data
        return self

    def import_data(self, file_path):
        """Opens an vector file compatible with OGR and parses
         the data.

        :param str file_path: The full path to the file.
        """
        features, metadata = open_vector_file(file_path)
        self._parse_data(features)
        self.epsg = metadata['epsg']
        print("File imported: {}".format(file_path))

    def _parse_data(self, features):
        raise NotImplementedError

    def describe(self):
        print("SRS EPSG code: {}".format(self.epsg))
        print("Number of features: {}".format(len(self.data)))

    def get_by_name(self, name):
        """Find an object by its name attribute and returns it."""
        for item in self.data:
            if item.get_attribute('name') == name:
                return item
        raise LookupError(
            "Object not found with the name: {}".format(name))

    def filter_by_boundary(self, boundary):
        """Filters the data by a given boundary"""
        result = []
        for item in self.data:
            if item.geom.within(boundary.geom):
                result.append(item)
        return result

    def filter(self, attribute, value):
        """Filters the collection by an attribute.

        :param attribute: The name of the attribute to filter by.
        :param value: The filtering value.
        """
        result = self.__class__()
        for item in self.data:
            if hasattr(item, attribute) and getattr(item, attribute) == value:
                result.data.append(item)
        return result


class PointCollection(BaseGeoCollection):
    """This class represents a collection of
    geocaching points.
    """

    def _parse_data(self, features):
        """Transforms the data into Geocache objects.

        :param features: A list of features.
        """
        for feature in features:
            coords = feature['geometry']['coordinates']
            real_coords = [float(item) for item in coords]
            point = Point(real_coords)
            attributes = feature['properties']
            cache_point = Geocache(point, attributes=attributes)
            self.data.append(cache_point)


class BoundaryCollection(BaseGeoCollection):
    """This class represents a collection of
    geographic boundaries.
    """

    def _parse_data(self, features):
        for feature in features:
            geom = feature['geometry']['coordinates']
            attributes = feature['properties']
            polygon = wkt.loads(geom)
            boundary = Boundary(geometry=polygon,
                                attributes=attributes)
            self.data.append(boundary)


class LineString(BaseGeoObject):
    """Represents a single linestring."""

    def __repr__(self):
        unit = 'km'
        return "{}  ({}{})".format(self.get_attribute('name'),
                                   self.length(unit), unit)

    def length(self, unit='km'):
        """Convenience method that returns the length of the
        linestring in a given unit.

        :param unit: The desired output unit.
        """
        return convert_length_unit(self.transformed_geom().length,
                                   unit)


class LineStringCollection(BaseGeoCollection):
    """Represents a collection of linestrings."""

    def _parse_data(self, features):
        for feature in features:
            geom = feature['geometry']['coordinates']
            attributes = feature['properties']
            line = wkt.loads(geom)
            linestring = LineString(geometry=line,
                                    attributes=attributes)
            self.data.append(linestring)


if __name__ == '__main__':
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    world = BoundaryCollection("../data/world_borders_simple.shp")
    geocaching_points = PointCollection("../data/geocaching.gpx")
    usa_boundary = world.get_by_name('United States')
    result = geocaching_points.filter_by_boundary(usa_boundary)
    for item in result:
        print(item)
