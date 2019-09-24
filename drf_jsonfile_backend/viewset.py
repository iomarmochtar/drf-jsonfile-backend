__author__ = 'Imam Omar Mochtar (iomarmochtar@gmail.com)'
__email__ = 'iomarmochtar@gmail.com'

import os
import inspect
import json
from collections import OrderedDict
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import JsonFileSerializer
from .commons import Obj


class JsonFileViewset(viewsets.ViewSet):
    fields = []
    serializer_class = JsonFileSerializer
    base_obj_class = Obj
    data_obj_class = None
    json_path = None

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if not self.json_path:
            raise Exception('You must set json_path !!!')

        # if not exist then create initial one
        if not os.path.isfile(self.json_path):
            with open(self.json_path, 'w') as p:
                p.write("[]")

        # get available fields in serializer class
        mapper = inspect.getmembers(self.serializer_class, lambda x: isinstance(x, OrderedDict))
        self.fields = dict(mapper[0][1]).keys()
        self.data_obj_class = type('DataClass', (self.base_obj_class,), {k: None for k in self.fields})

    @property
    def _json(self):
        with open(self.json_path, 'r') as p:
            return json.loads(p.read())

    def _json_object(self, obj_id=None):
        result = OrderedDict()
        _counter = 1
        for row in self._json:
            fields = {k: row.get(k) for k in self.fields}
            # set the ID if not exists
            if not fields.get('id'):
                fields['id'] = _counter
            obj = self.data_obj_class(**fields)

            if obj_id is not None and obj_id == fields['id']:
                return obj
            result[fields['id']] = obj
            _counter += 1

        # if data was not found
        if obj_id is not None:
            raise KeyError('Not Found')

        return result

    @property
    def json_object(self):
        return self._json_object(obj_id=None)

    def json_save(self, rows):
        # sanitizing data for json write
        rows = [row if type(row) == dict else row.__dict__ for _, row in rows.items()]
        with open(self.json_path, 'w') as p:
            p.write(json.dumps(rows))

    ## CRUD

    def list(self, request):
        serializers = self.serializer_class(instance=self.json_object.values(), many=True)
        return Response(serializers.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            row = serializer.save()
            rows = self.json_object
            row.id = len(rows) + 1
            rows[row.id] = row
            self.json_save(rows)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            obj = self._json_object(obj_id=int(pk))
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        rows = self.json_object
        try:
            obj = rows[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            data=request.data, instance=obj)

        if serializer.is_valid():
            _obj = serializer.save()
            rows[_obj.id] = _obj
            self.json_save(rows)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rows = self.json_object
        try:
            obj = rows[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del rows[obj.id]
        self.json_save(rows)
        return Response(status=status.HTTP_204_NO_CONTENT)
