# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
from . utils import *
from solid import *

class RockitObject(dict):
    def __getattr__(self, key):
        if key in self and self[key] != None:
            return self[key]
        return super(RockitObject, self).__getattribute__(key)

    def __setattr__(self, key, val):
        if key in self:
            self[key] = val
            return
        super(RockitObject, self).__setattr__(key, val)

class Rockit(RockitObject):
    def __init__(self, *parts, **kw):
        _dct = {part.name: part(rocket=self) for part in parts}
        super(Rockit, self).__init__(_dct)
        self.override(kw.get("override", {}))

    def override(self, config):
        for (key, val) in config.items():
            keys = key.split('.')
            obj = self
            for _key in keys[:-1]:
                obj = getattr(obj, _key)
            setattr(obj, keys[-1], val)

class RockitPart(RockitObject):
    Defaults = {"rocket": None}
    Name = ''

    def __init__(self, **kw):
        _dct = self.Defaults.copy()
        _dct.update(kw)
        super(RockitPart, self).__init__(**_dct)

    @cproperty
    @classmethod
    def name(cls):
        return cls.Name or cls.__name__

    def build(self):
        return ''

