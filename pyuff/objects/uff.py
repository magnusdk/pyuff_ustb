from enum import Enum
from functools import cached_property
from typing import Any, List, Optional, Sequence, Tuple, TypeVar, Union

import h5py
import numpy as np

from pyuff.readers import Reader, ReaderKeyError, util
from pyuff.readers.lazy_arrays import LazyArray, LazyScalar

# A flag to enable equality checks with backwards compatibility for old files with
# different names for things.
_BACKWORDS_COMPATIBLE_EQUALS = True

TUff = TypeVar("TUff", bound="Uff")
T = TypeVar("T")  # A generic type


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


class Uff:
    _reader: Reader

    def __init__(self, _reader: Optional[Union[Reader, str]] = None, **kwargs):
        if isinstance(_reader, str):
            _reader = Reader(_reader)
        if not isinstance(_reader, Reader) and _reader is not None:
            raise TypeError(
                f"The first argument must be of type Reader or str (got \
{type(_reader)}). Try giving the arguments as keyword arguments instead."
            )

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._reader = _reader

    @optional_property
    def name(self):
        "Name of the dataset"
        return util.read_list_of_strings(self._reader["name"])

    @optional_property
    def reference(self):
        "Reference to the publication where it was used/acquired"
        return util.read_list_of_strings(self._reader["reference"])

    @optional_property
    def author(self):
        "Contact of the authors"
        return util.read_list_of_strings(self._reader["author"])

    @optional_property
    def version(self):
        "Version of the dataset"
        return util.read_list_of_strings(self._reader["version"])

    @optional_property
    def info(self):
        "Other information"
        return util.read_list_of_strings(self._reader["info"])

    def __getitem__(self, key: str) -> "Uff":
        return self.read(key)

    @property
    def _attrs(self) -> dict:
        """Return the attrs of the h5 object as a dict. Return an empty dict if no
        _reader is provided"""
        if self._reader is not None:
            with self._reader.h5_obj as obj:
                return dict(obj.attrs)
        else:
            return {}

    def read(self, name: str) -> "Uff":
        """Read an Uff object from the file. A Reader must be provided in order to read.

        >> uff = Uff("/path/to/some/file.uff")
        >> scan = uff.read("scan")
        """
        from pyuff.common import get_class_from_name

        with self._reader[name].h5_obj as obj:
            cls_name = obj.attrs["class"]
            cls = get_class_from_name(cls_name)
            if cls is None:
                raise NotImplementedError(
                    f"Class '{cls_name}' (at location '{name}') is not implemented."
                )
            return util.read_potentially_list(Reader(self._reader[name]), cls)

    def write(
        self,
        filepath: str,
        location: Union[str, Tuple[str, ...], List[str]],
        overwrite: bool = False,
    ):
        """Write the Uff to a file.

        Parameters
        ----------
        filepath : Union[str, h5py.File]
            The filepath to write to.
        location : Union[str, Tuple[str, ...], List[str]]
            The location in the h5 file to write to. Can be a tuple/list of strings
            representing a path into the h5 file, or a string with the path separated
            by slashes.
        overwrite : bool, optional
            Whether to overwrite the location if it already exists. If the location
            already exists and overwrite=False, a ValueError is raised.

        Example:
        Write channel data and a scan to a file:
        >> channel_data.write("my_channel_data.uff", "channel_data")
        >> scan.write("my_channel_data.uff", "scan")

        Writing multiple ChannelData objects to the same file (at nested locations):
        >> channel_data1.write("our_channel_data.uff", "magnus/channel_data")
        >> channel_data2.write("our_channel_data.uff", "anders/channel_data")
        >> channel_data3.write("our_channel_data.uff", "ole_marius/channel_data")
        """
        with h5py.File(filepath, "a") as hf:
            write_object(hf, self, location, overwrite=overwrite)

    def _preprocess_write(self, name: str, value):
        return value

    def _get_fields(self, skip_dependent_properties: bool = False) -> Sequence[str]:
        if type(self) is Uff:
            return self._reader.keys()
        else:
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

    def __iter__(self):
        return iter(self._get_fields())

    def __repr__(self) -> str:
        field_strs = [
            f"{field}={_present_field_value(getattr(self, field))}" for field in self
        ]
        return self.__class__.__name__ + "(" + ", ".join(field_strs) + ")"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if not _attrs_equal(self._attrs, other._attrs):
            return False
        for field in self._get_fields(skip_dependent_properties=True):
            value1 = getattr(self, field)
            value2 = getattr(other, field)
            if isinstance(value1, (np.ndarray, LazyArray, LazyScalar)):
                if not isinstance(value2, (np.ndarray, LazyArray, LazyScalar)):
                    return False
                if not np.array_equal(value1[...], value2[...]):
                    return False
            else:
                if value1 != value2:
                    return False
        return True


def _attrs_equal(attrs1: dict, attrs2: dict) -> bool:
    if attrs1.keys() != attrs2.keys():
        return False
    for k in attrs1.keys():
        v1, v2 = attrs1[k], attrs2[k]
        if isinstance(v1, np.ndarray):
            if not isinstance(v2, np.ndarray):
                return False
            if not np.array_equal(v1, v2):
                return False
        elif isinstance(v1, (str, bytes)):
            if not isinstance(v2, (str, bytes)):
                return False
            v1 = v1.decode("utf-8") if isinstance(v1, bytes) else v1
            v2 = v2.decode("utf-8") if isinstance(v2, bytes) else v2
            if v1 != v2:
                if _BACKWORDS_COMPATIBLE_EQUALS:
                    if not {v1, v2} == {"scan", "focus"}:
                        return False
                else:
                    return False
    return True


def eager_load(obj: T) -> T:
    if isinstance(obj, (LazyArray, LazyScalar)):
        return np.array(obj)
    elif isinstance(obj, Uff):
        kwargs = {}
        for name in obj._get_fields(skip_dependent_properties=True):
            kwargs[name] = eager_load(getattr(obj, name))
        return obj.__class__(**kwargs)
    elif isinstance(obj, (list, tuple)):
        return [eager_load(o) for o in obj]
    elif isinstance(obj, dict):
        return {k: eager_load(v) for k, v in obj.items()}
    else:
        return obj


def _present_field_value(value):
    if isinstance(value, np.ndarray):
        return f"<Array shape={value.shape} dtype={value.dtype}>"
    elif isinstance(value, Uff):
        return f"{value.__class__.__name__}(...)"
    elif isinstance(value, (list, tuple)):
        open_bracket = "[" if isinstance(value, list) else "("
        close_bracket = "]" if isinstance(value, list) else ")"
        return f"<{open_bracket}{_present_field_value(value[0])}... ({len(value)} \
items in total){close_bracket}>"
    else:
        return repr(value)


def _item_name(name: str, i: int) -> str:
    """Present a name for an item in a list.

    >>> _item_name("sequence", 0)
    'sequence_0001'
    >>> _item_name("sequence", 99)
    'sequence_0100'
    >>> _item_name("sequence", 9999)  # Supports more than 4 digits
    'sequence_10000'
    """
    # :04d means that leading zeros are added if the number of digits is less than 4.
    return f"{name}_{(i+1):04d}"


def write_object(
    hf: h5py.File,
    obj: Any,
    location: Union[str, Sequence[str]],
    overwrite: bool = False,
):
    from pyuff.common import get_name_from_class

    if isinstance(location, str):
        location = location.split("/")

    location_str = "/".join(location)
    if location_str in hf:
        if overwrite:
            # Delete the existing value so that we can write to the location
            del hf[location_str]
        else:
            raise ValueError(
                f"Location {location} already exists in file {hf.filename}. Use \
overwrite=True to overwrite it."
            )

    if isinstance(obj, Uff):
        name = obj._attrs.get("name", location[-1])
        group = hf.create_group(location_str)
        for k in obj._attrs:
            # Copy over attributes
            group.attrs[k] = obj._attrs[k]
        group.attrs["class"] = get_name_from_class(type(obj))
        group.attrs["name"] = name
        group.attrs["array"] = np.array([0])  # False
        group.attrs["size"] = np.array([1, 1])

        for name in obj._get_fields(skip_dependent_properties=True):
            value = getattr(obj, name)
            value = obj._preprocess_write(name, value)
            write_object(hf, value, [*location, name], overwrite=overwrite)

    elif isinstance(obj, str):
        name = location[-1]
        int_chars = np.array([ord(c) for c in obj], dtype=np.uint16)
        # Strings are usually stored as (N,1) arrays in UFF files, let's do the same.
        int_chars = np.expand_dims(int_chars, 1)
        dataset = hf.create_dataset(location_str, data=int_chars)
        dataset.attrs["class"] = "char"
        dataset.attrs["name"] = name

    elif isinstance(obj, (int, float, np.ndarray, LazyArray, LazyScalar)):
        name = location[-1]
        is_scalar = isinstance(obj, LazyScalar)
        obj = np.array(obj)  # <- Ensure array and load the data if lazy
        if is_scalar:
            # Scalar values are usually stored as (1,1) arrays in UFF files, let's do
            # the same.
            obj = np.expand_dims(obj, [0, 1])
        # We always write *.attrs["class"] = "single". I don't think it matters.
        if np.iscomplexobj(obj):
            group = hf.create_group(location_str)
            group.attrs["class"] = "single"
            group.attrs["name"] = name
            group.attrs["complex"] = np.array([1])  # True
            group.attrs["imaginary"] = np.array([0])  # False

            real_dataset = group.create_dataset("real", data=obj.real)
            real_dataset.attrs["imaginary"] = np.array([0])  # False
            real_dataset.attrs["class"] = "single"
            real_dataset.attrs["name"] = name

            imag_dataset = group.create_dataset("imag", data=obj.imag)
            imag_dataset.attrs["imaginary"] = np.array([1])  # True
            imag_dataset.attrs["class"] = "single"
            imag_dataset.attrs["name"] = name
        else:
            dataset = hf.create_dataset(location_str, data=obj)
            dataset.attrs["class"] = "single"
            dataset.attrs["name"] = name
            dataset.attrs["complex"] = np.array([0])  # False
            dataset.attrs["imaginary"] = np.array([0])  # False

    elif isinstance(obj, (list, tuple)):
        name = location[-1]
        first_obj = obj[0]
        assert all(
            type(o) == type(first_obj) for o in obj
        ), "All items in a list must have the same type."

        # If it is a list of strings then it is a cell
        if isinstance(first_obj, str):
            group = hf.create_group(location_str)
            group.attrs["class"] = "cell"
            group.attrs["name"] = name
            group.attrs["array"] = np.array([1])  # True
            group.attrs["size"] = np.array([1, len(obj)])
            for i, v in enumerate(obj):
                write_object(
                    hf, v, [*location, _item_name(name, i)], overwrite=overwrite
                )
        # Otherwise it is a list of Uff objects
        else:
            group = hf.create_group(location_str)
            group.attrs["class"] = get_name_from_class(type(first_obj))
            group.attrs["name"] = name
            group.attrs["array"] = np.array([1])  # True
            group.attrs["size"] = np.array([1, len(obj)])
            for i, v in enumerate(obj):
                assert isinstance(
                    v, Uff
                ), "Assume list items are always Uffs. Create a issue on \
    the repository if you think this is not the case."
                write_object(
                    hf, v, [*location, _item_name(name, i)], overwrite=overwrite
                )

    elif isinstance(obj, Enum):
        name = location[-1]
        dataset = hf.create_dataset(location_str, data=np.array([[obj.value]]))
        dataset.attrs["class"] = get_name_from_class(type(obj))
        dataset.attrs["name"] = name

    elif obj is None:
        return  # Do nothing

    else:
        name = location[-1]
        raise TypeError(
            f"Field {name} has type {type(obj)} which is not supported. \
If you think this is a mistake (it very well might be!) then make an issue on the \
repository."
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()