__author__ = 'Imam Omar Mochtar (iomarmochtar@gmail.com)'
__email__ = 'iomarmochtar@gmail.com'

class Obj(object):
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
