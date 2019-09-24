Django Rest Framework - Json File Backend
=========================================

An alternative to database backend as my personal usage. you may not use this in high concurrent traffic because there is no locking mechanism in same resource.

Example
=======

```python
from rest_framework import serializers, routers
from drf_jsonfile_backend import JsonFileSerializer, RestJsonFileWrapper

# extending base json serializer class
class MySerializer(JsonFileSerializer):
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=('male', 'female')) 
    address = serializers.CharField(max_length)

# in urls.py
viewset = RestJsonFileWrapper.get_viewset(json_path='path_to.json', serializer=MySerializer)
router = routers.DefaultRouter()
router.register(r'test', viewset, 'test')

urlpatterns = [
    path('api/', include(router.urls))
]
```
