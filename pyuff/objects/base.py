from functools import cached_property
from typing import Optional, Sequence

from pyuff.readers.base import Reader
from pyuff.readers.lazy_arrays import LazyArray, LazyScalar
from typing import TypeVar

TPyuffObject = TypeVar("TPyuffObject", bound="PyuffObject")


class PyuffObject:
    _reader: Reader

    def __init__(self, reader: Optional[Reader] = None, **kwargs):
        if not isinstance(reader, Reader) and reader is not None:
            raise TypeError(
                f"The first argument must be of type Reader (got {type(reader)}). Try \
giving the arguments as keyword arguments instead."
            )

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._reader = reader if reader is not None else Reader(None)

    def eager_load(self: TPyuffObject) -> TPyuffObject:
        kwargs = {}
        for name in self._get_fields():
            value = getattr(self, name)
            if isinstance(value, (LazyArray, LazyScalar)):
                value = value[...]
            elif isinstance(value, PyuffObject):
                value = value.eager_load()
            kwargs[name] = value
        return self.__class__(**kwargs)

    def _get_fields(self) -> Sequence[str]:
        t = type(self)
        return [
            attr
            for attr in dir(t)
            if isinstance(getattr(t, attr), (property, cached_property))
        ]

    def __repr__(self) -> str:
        field_strs = [f"{field}={getattr(self, field)}" for field in self._get_fields()]
        return self.__class__.__name__ + "(" + ", ".join(field_strs) + ")"
