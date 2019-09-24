__author__ = 'Imam Omar Mochtar (iomarmochtar@gmail.com)'
__email__ = 'iomarmochtar@gmail.com'

from .viewset import JsonFileViewset
from .serializer import JsonFileSerializer


class RestJsonFileWrapper(object):

    @staticmethod
    def get_viewset(json_path, viewset=JsonFileViewset, serializer=JsonFileSerializer):
        """
        Viewset class generator
        """
        _vs = type('JsonViewSet', (viewset, ), {
            'json_path': json_path,
            'serializer_class': serializer,
        })
        return _vs
