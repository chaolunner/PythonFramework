# https://github.com/clarete/forbiddenfruit
import ctypes
import inspect
import builtins

from functools import wraps
from collections import defaultdict

__all__ = 'curse', 'curses', 'reverse'

Py_ssize_t = \
    hasattr(ctypes.pythonapi, 'Py_InitModule4_64') \
    and ctypes.c_int64 or ctypes.c_int


class PyObject(ctypes.Structure):
    pass


PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyObject)),
]


class SlotsProxy(PyObject):
    _fields_ = [('dict', ctypes.POINTER(PyObject))]


def patchable_builtin(klass):
    # It's important to create variables here, we want those objects alive
    # within this whole scope.
    name = klass.__name__
    target = klass.__dict__

    # Hardcore introspection to find the `PyProxyDict` object that contains the
    # precious `dict` attribute.
    proxy_dict = SlotsProxy.from_address(id(target))
    namespace = {}

    # This is the way I found to `cast` this `proxy_dict.dict` into a python
    # object, cause the `from_address()` function returns the `py_object`
    # version
    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(name),
        proxy_dict.dict,
    )
    return namespace[name]


@wraps(builtins.dir)
def __filtered_dir__(obj=None):
    name = hasattr(obj, '__name__') and obj.__name__ or obj.__class__.__name__
    if obj is None:
        # Return names from the local scope of the calling frame, taking into
        # account indirection added by __filtered_dir__
        calling_frame = inspect.currentframe().f_back
        return sorted(calling_frame.f_locals.keys())
    return sorted(set(__dir__(obj)).difference(__hidden_elements__[name]))


# Switching to the custom dir impl declared above
__hidden_elements__ = defaultdict(list)
__dir__ = dir
builtins.dir = __filtered_dir__


def curse(klass, attr, value, hide_from_dir=False):
    dikt = patchable_builtin(klass)

    old_value = dikt.get(attr, None)
    old_name = '_c_%s' % attr  # do not use .format here, it breaks py2.{5,6}
    if old_value:
        dikt[old_name] = old_value

    if old_value:
        dikt[attr] = value

        try:
            dikt[attr].__name__ = old_value.__name__
        except (AttributeError, TypeError):  # py2.5 will raise `TypeError`
            pass
        try:
            dikt[attr].__qualname__ = old_value.__qualname__
        except AttributeError:
            pass
    else:
        dikt[attr] = value

    if hide_from_dir:
        __hidden_elements__[klass.__name__].append(attr)


def reverse(klass, attr):
    dikt = patchable_builtin(klass)
    del dikt[attr]


def curses(klass, name):
    def wrapper(func):
        curse(klass, name, func)
        return func

    return wrapper
