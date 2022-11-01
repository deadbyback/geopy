# coding=utf-8

import mapnik

from Chapter5.map_maker import MapMakerApp
from Chapter5.models import BoundaryCollection, PointCollection


class MapDatasource(mapnik.PythonDatasource):
    """Implementation of Mapnik's PythonDatasource."""

    def __init__(self, data):
        data_type = mapnik.DataType.vector
        if isinstance(data, PointCollection):
            geometry_type = mapnik.GeometryType.Point
        elif isinstance(data, BoundaryCollection):
            geometry_type = mapnik.GeometryType.Polygon
        else:
            raise TypeError

        super(MapDatasource, self).__init__(
            envelope=None, geometry_type=geometry_type,
            data_type=data_type)

        self.data = data

    def features(self, query=None):
        keys = ['name',]
        features = []
        for item in self.data.data:
            features.append([item.geom.wkb, {'name': item.name}])
        return mapnik.PythonDatasource.wkb_features(keys, features)
