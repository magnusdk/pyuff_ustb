from functools import cached_property
from typing import Optional, Sequence, TypeVar

import numpy as np

from pyuff.readers.base import Reader, ReaderKeyError
from pyuff.readers.lazy_arrays import LazyArray, LazyScalar

TPyuffObject = TypeVar("TPyuffObject", bound="PyuffObject")


class compulsory_property(cached_property):
    "Properties needed in order to write an UFF file."

    def __get__(self, instance, owner=None):
        try:
            return super().__get__(instance, owner)
        except ReaderKeyError:
            return None


class optional_property(cached_property):
    "Optional properties that can be written to an UFF file."

    def __get__(self, instance, owner=None):
        try:
            return super().__get__(instance, owner)
        except ReaderKeyError:
            return None


class dependent_property(property):
    """Properties that are dependent on other properties and are not read from or
    written to an UFF file."""


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
        self._reader = reader

    def eager_load(self: TPyuffObject) -> TPyuffObject:
        kwargs = {}
        for name in self._get_fields(skip_dependent_properties=True):
            value = getattr(self, name)
            if isinstance(value, (LazyArray, LazyScalar)):
                value = value[...]
            elif isinstance(value, PyuffObject):
                value = value.eager_load()
            kwargs[name] = value
        return self.__class__(**kwargs)

    def _get_fields(self, skip_dependent_properties: bool = False) -> Sequence[str]:
        t = type(self)
        return [
            attr
            for attr in dir(t)
            if isinstance(
                getattr(t, attr),
                (compulsory_property, optional_property)
                if skip_dependent_properties
                else (compulsory_property, optional_property, dependent_property),
            )
        ]

    def __repr__(self) -> str:
        field_strs = [
            f"{field}={_present_field_value(getattr(self, field))}"
            for field in self._get_fields()
        ]
        return self.__class__.__name__ + "(" + ", ".join(field_strs) + ")"


def _present_field_value(value):
    if isinstance(value, np.ndarray):
        return f"<Array shape={value.shape} dtype={value.dtype}>"
    return repr(value)
