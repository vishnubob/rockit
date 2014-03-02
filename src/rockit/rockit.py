# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
from . utils import *
from solid import *
import logging

logger = logging.getLogger(__name__)

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
    def __init__(self, **conf):
        parts = {part.name: part(self, **conf.get(part.name, {})) for part in scan_parts()}
        self.parts = parts
        _dct = {}
        _dct["name"] = conf.get("name", "rocket")
        _dct["build"] = conf.get("build", [])
        if "all" in _dct["build"]:
            _dct["build"] = parts.keys()
        _dct.update(parts)
        super(Rockit, self).__init__(**_dct)

    def override(self, config):
        for (key, val) in config.items():
            keys = key.split('.')
            obj = self
            for _key in keys[:-1]:
                obj = getattr(obj, _key)
            setattr(obj, keys[-1], val)

    def get_build(self):
        return {part_name: self.parts[part_name].get_build() for part_name in self.parts}

class RockitPart(RockitObject):
    Defaults = {}
    Name = ''

    def __init__(self, rocket, **kw):
        self.rocket = rocket
        _dct = self.Defaults.copy()
        _dct.update(kw)
        super(RockitPart, self).__init__(**_dct)

    @cproperty
    @classmethod
    def name(cls):
        return cls.Name or cls.__name__

    @cproperty
    @classmethod
    def names(cls):
        if hasattr(super(cls.__class__), "names"):
            return [cls.Name] + super(cls, cls.__class__).names
        return [cls.Name]

    def get_build(self):
        if self.name in self.rocket.build:
            return self.render_scad()
        return ''

    def render_scad(self):
        return ''

