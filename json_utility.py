import json


class JsonUtility(object):
    mappings = {}

    @classmethod
    def class_mapper(cls, d):
        for keys, cls2 in cls.mappings.items():
            if keys.issuperset(d.keys()):  # are all required arguments present?
                return cls2(**d)
        else:
            return d

    @classmethod
    def complex_handler(cls, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            raise TypeError("Object of type %s with value of %s is not JSON serializable" % (type(obj), repr(obj)))

    @classmethod
    def register(cls, cls2):
        cls.mappings[frozenset(tuple([attr for attr, val in cls2().__dict__.items()]))] = cls2
        return cls2

    @classmethod
    def to_json(cls, obj):
        return json.dumps(obj.__dict__, default=cls.complex_handler, indent=4)

    @classmethod
    def from_json(cls, json_str):
        return json.loads(json_str, object_hook=cls.class_mapper)

    @classmethod
    def to_file(cls, obj, path):
        with open(path, 'w') as json_file:
            json_file.writelines([cls.to_json(obj)])
        return path

    @classmethod
    def from_file(cls, file_path):
        result = None
        with open(file_path, 'r') as json_file:
            result = cls.from_json(json_file.read())
        return result
