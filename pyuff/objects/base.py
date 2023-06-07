from functools import cached_property
from typing import List, Optional, Sequence, Tuple, TypeVar, Union

import h5py
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

    def write(
        self,
        filepath: Union[str, h5py.File],
        location: Union[str, Tuple[str, ...], List[str]],
        overwrite: bool = False,
    ):
        """Write the PyuffObject to a file.

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
        >>> channel_data.write("my_channel_data.uff", "channel_data")
        >>> scan.write("my_channel_data.uff", "scan")

        Writing multiple ChannelData objects to the same file (at nested locations):
        >>> channel_data1.write("our_channel_data.uff", "magnus/channel_data")
        >>> channel_data2.write("our_channel_data.uff", "anders/channel_data")
        >>> channel_data3.write("our_channel_data.uff", "ole_marius/channel_data")
        """
        from pyuff.uff import get_name_from_class

        # Open file if filepath is a string
        if isinstance(filepath, str):
            hf = h5py.File(filepath, "a")
            must_close_file = True
        else:  # ... else assume it is a h5py.File
            assert isinstance(filepath, h5py.File)
            hf = filepath
            must_close_file = False

        # Parse location
        if isinstance(location, (tuple, list)):
            location = "/".join(location)
        # Check if location already exists and whether to overwrite it or raise an error
        if location in hf:
            if overwrite:
                # Delete the existing value so that we can write to the location
                del hf[location]
            else:
                raise ValueError(
                    f"Location {location} already exists in file {hf.filename}. Use \
overwrite=True to overwrite it."
                )

        # Actually create the group in the h5 object.
        group = hf.create_group(location)
        group.attrs["class"] = get_name_from_class(type(self))

        # Recursively add groups and datasets to the group
        for name in self._get_fields(skip_dependent_properties=True):
            # TODO: Check if field is compulsory. If it is, raise an error if it is None.
            # TODO: Check if data-structure is what we expect it to be.
            value = getattr(self, name)
            if isinstance(value, (np.ndarray, LazyArray, LazyScalar)):
                value = value[...]  # <- load the data if lazy
                if np.iscomplexobj(value):
                    complex_number_group = group.create_group(name)
                    complex_number_group.attrs["complex"] = np.array([1])  # True
                    complex_number_group.create_dataset("real", data=value.real)
                    complex_number_group.create_dataset("imag", data=value.imag)
                else:
                    dataset = group.create_dataset(name, data=value)
                    dataset.attrs["complex"] = np.array([0])  # False
            elif isinstance(value, PyuffObject):
                value.write(hf, location + "/" + name, overwrite=overwrite)

        # Remember to close the file afterwards (if we opened it)! :)
        if must_close_file:
            hf.close()

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

    def __eq__(self, other):
        if type(self) != type(other):
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


def _present_field_value(value):
    if isinstance(value, np.ndarray):
        return f"<Array shape={value.shape} dtype={value.dtype}>"
    return repr(value)
