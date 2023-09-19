import copy
from enum import Enum
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import h5py
import numpy as np

from pyuff_ustb.readers import H5Reader, NoneReader, Reader, ReaderKeyError, util
from pyuff_ustb.readers.lazy_arrays import LazyArray, LazyScalar

# A flag to enable equality checks with backwards compatibility for old files with
# different names for things.
_BACKWORDS_COMPATIBLE_EQUALS = True

TUff = TypeVar("TUff", bound="Uff")
T = TypeVar("T")  # A generic type


class compulsory_property(cached_property, Generic[T]):
    "Properties needed in order to write an UFF file."

    def __get__(self, instance, owner=None) -> T:
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


if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Uff:
    """The base class of all UFF objects.

    Original authors:
        Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
    """

    _reader: Reader

    def __init__(self, _reader: Optional[Union[Reader, str]] = None, **kwargs):
        if isinstance(_reader, str):
            _reader = H5Reader(_reader)
        elif _reader is None:
            _reader = NoneReader()
        elif not isinstance(_reader, Reader):
            raise TypeError(
                f"The first argument must be of type Reader or str (got \
{type(_reader)}). Try giving the arguments as keyword arguments instead."
            )

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._reader = _reader

    @optional_property
    def name(self) -> Union[str, None]:
        "Name of the dataset"
        return util.read_list_of_strings(self._reader["name"])

    @optional_property
    def reference(self) -> Union[str, None]:
        "Reference to the publication where it was used/acquired"
        return util.read_list_of_strings(self._reader["reference"])

    @optional_property
    def author(self) -> Union[str, None]:
        "Contact of the authors"
        return util.read_list_of_strings(self._reader["author"])

    @optional_property
    def version(self) -> Union[str, None]:
        "Version of the dataset"
        return util.read_list_of_strings(self._reader["version"])

    @optional_property
    def info(self) -> Union[str, None]:
        "Other information"
        return util.read_list_of_strings(self._reader["info"])

    def __getitem__(self, key: str) -> "Uff":
        return self.read(key)

    @property
    def _attrs(self) -> dict:
        """Return the attrs of the h5 object as a dict. Return an empty dict if no
        _reader is provided"""
        return dict(self._reader.attrs)

    def read(self, name: str) -> "Uff":
        """Read an Uff object from the file. A Reader must be provided in order to read.

        >> uff = Uff("/path/to/some/file.uff")
        >> scan = uff.read("scan")
        """
        from pyuff_ustb.common import get_class_from_name

        reader = self._reader[name]
        cls_name = reader.attrs["class"]
        cls = get_class_from_name(cls_name)
        if cls is None:
            raise NotImplementedError(
                f"Class '{cls_name}' (at location '{name}') is not implemented."
            )
        return util.read_potentially_list(reader, cls)

    def write(
        self,
        filepath: str,
        location: Union[str, Tuple[str, ...], List[str]],
        overwrite: bool = False,
        ignore_missing_compulsory_fields: bool = False,
    ):
        """Write the Uff to a file.

        Args:
            filepath (Union[str, h5py.File]): The filepath (or ``h5py.File``) to write
                to.
            location (Union[str, Tuple[str, ...], List[str]]): The location in the h5
                file to write to. Can be a tuple/list of strings representing a path
                into the h5 file, or a string with the path separated by slashes.
            overwrite (bool): Whether to overwrite the location if it already exists.
                If the location already exists and ``overwrite=False``, a
                ``ValueError`` is raised. ``overwrite=False`` by default.
            ignore_missing_compulsory_fields (bool): Whether to ignore missing
                compulsory fields. If a compulsory field is not set then usually a
                ``ValueError`` is raised. Setting
                ``ignore_missing_compulsory_fields=True`` will ignore this error and
                write the object anyway. ``ignore_missing_compulsory_fields=False`` by
                default.

        Examples:
            We can write an object to a file like this:

            >>> import pyuff_ustb as pyuff
            >>> point = pyuff.Point(distance=0.0, azimuth=0.0, elevation=0.0)
            >>> point.write("my_point.uff", "point")

            If we try to write an object to the same location, we get an error:

            >>> point.write("my_point.uff", "point")
            Traceback (most recent call last):
                ...
            ValueError: Location 'point' already exists in the file 'my_point.uff'. Use overwrite=True to overwrite it.

            We can choose to overwrite the location by passing ``overwrite=True``:

            >>> point.write("my_point.uff", "point", overwrite=True)

            We can also write the object to another arbitrary location if we want:

            >>> point.write("my_point.uff", "sub_directory/point")

            Compulsory fields may not be None when writing an object to an UFF file (unless
            ``ignore_missing_compulsory_fields=True``).

            >>> point.distance = None
            >>> point.write("my_point.uff", "point2")
            Traceback (most recent call last):
                ...
            ValueError: The compulsory field 'distance' is set to None. Compulsory fields
            may not be None when writing an object to an UFF file. To ignore this error and write
            the object anyway, set ignore_missing_compulsory_fields=True.

            Note that even though the previous step failed, the file was still partially
            written to (we don't rollback changes when writing fails), so we will have to
            pass ``overwrite=True`` to write the object again.

            >>> point.write(
            ...     "my_point.uff",
            ...     "point2",
            ...     overwrite=True,
            ...     ignore_missing_compulsory_fields=True,
            ... )

            After running these steps, the file will contain the following fields:

            >>> uff = pyuff.Uff("my_point.uff")
            >>> uff
            Uff(point=Point(<...>), point2=Point(<...>), sub_directory=<...>)
        """
        with h5py.File(filepath, "a") as hf:
            write_object(
                hf,
                self,
                location,
                overwrite,
                ignore_missing_compulsory_fields,
            )

    def copy(self) -> "Uff":
        """Return a (deep) copy of the Uff object.

        In addition to the ``_reader``, all compulsory and optional fields are copied
        (deeply) *iff* they are loaded/cached. This means that if a field has not been
        read from the file, it will not be copied. This is to avoid unintended eager
        loading of data.

        See :meth:`Uff.__deepcopy__` for implementation details.

        Returns:
            Uff: A deep copy of this object.
        """
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        """Makes :class:`Uff` objects compatible with the ``copy`` module.

        The ``copy`` module is part of the standard Python library."""
        kwargs = {}
        for name in self._get_fields(skip_dependent_properties=True):
            # Only add the field if it is loaded/cached. When using cached_property,
            # the field will be added to the object's __dict__ the first time it is
            # accessed.
            if name in self.__dict__:
                kwargs[name] = copy.deepcopy(getattr(self, name), memo)
        return self.__class__(self._reader, **kwargs)

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
        field_strs = []
        for field in self._get_fields(skip_dependent_properties=True):
            try:
                if type(self) is Uff:
                    if "class" in self._reader[field].attrs:
                        value = self.read(field)
                    else:
                        value = "<...>"
                else:
                    value = getattr(self, field)
                if value is not None:
                    field_strs.append(f"{field}={_present_field_value(value)}")
            except NotImplementedError:
                field_strs.append(f"{field}=NotImplemented")
        single_line_joined = self.__class__.__name__ + "(" + ", ".join(field_strs) + ")"
        if len(single_line_joined) <= 80:
            # Represent it as a single line if it fits in 80 characters
            return single_line_joined
        else:
            # Otherwise represent it as a multiline string
            return (
                self.__class__.__name__ + "(\n    " + ",\n    ".join(field_strs) + "\n)"
            )

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        for field in self._get_fields(skip_dependent_properties=True):
            value1 = getattr(self, field)
            value2 = getattr(other, field)
            if isinstance(value1, (int, float, np.ndarray, LazyArray, LazyScalar)):
                if not isinstance(
                    value2, (int, float, np.ndarray, LazyArray, LazyScalar)
                ):
                    return False
                if not np.array_equal(np.array(value1), np.array(value2)):
                    return False
            else:
                if value1 != value2:
                    return False
        return True


def eager_load(obj: T) -> T:
    """Eagerly and recursively load all the lazy fields in an object.

    ``pyuff_ustb`` is lazily loaded by default, meaning that most fields are not read
    from file until they are needed. This function will recursively load all such
    fields, ensuring that all :class:`~pyuff_ustb.readers.lazy_arrays.LazyArrays` and
    :class:`.LazyScalars` are converted to Numpy arrays.

    A new instance of the same type as the input object is returned, but with all its
    fields guaranteed to be loaded into memory.

    Args:
        obj (T): An object to eagerly load.

    Returns:
        T: A new object of the same type as the input object, with all its fields
            guaranteed to be loaded into memory.
    """
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
        return f"{value.__class__.__name__}(<...>)"
    elif isinstance(value, (list, tuple)):
        open_bracket = "[" if isinstance(value, list) else "("
        close_bracket = "]" if isinstance(value, list) else ")"
        if len(value) > 1:
            return f"<{open_bracket}{_present_field_value(value[0])}... ({len(value)} \
items in total){close_bracket}>"
        else:
            return f"{open_bracket}{_present_field_value(value[0])}{close_bracket}"
    elif isinstance(value, str):
        return value
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
    ignore_missing_compulsory_fields: bool = False,
):
    """Write an object to a HDF5 file.

    See :meth:`Uff.write` for more details."""
    from pyuff_ustb.common import get_name_from_class

    if isinstance(location, str):
        location = location.split("/")

    location_str = "/".join(location)
    if location_str in hf:
        if overwrite:
            # Delete the existing value so that we can write to the location
            del hf[location_str]
        else:
            raise ValueError(
                f"Location '{location_str}' already exists in the file '{hf.filename}'. Use \
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

        t = type(obj)
        for name in obj._get_fields(skip_dependent_properties=True):
            value = getattr(obj, name)
            if (
                value is None
                and isinstance(getattr(t, name), compulsory_property)
                and not ignore_missing_compulsory_fields
            ):
                raise ValueError(
                    f"""The compulsory field '{name}' is set to None. Compulsory fields 
may not be None when writing an object to an UFF file. To ignore this error and write 
the object anyway, set ignore_missing_compulsory_fields=True."""
                )
            value = obj._preprocess_write(name, value)
            write_object(
                hf,
                value,
                [*location, name],
                overwrite,
                ignore_missing_compulsory_fields,
            )

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
        obj = np.array(obj)  # <- Ensure array and load the data if lazy
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
                    hf,
                    v,
                    [*location, _item_name(name, i)],
                    overwrite,
                    ignore_missing_compulsory_fields,
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
                    hf,
                    v,
                    [*location, _item_name(name, i)],
                    overwrite,
                    ignore_missing_compulsory_fields,
                )

    elif isinstance(obj, Enum):
        name = location[-1]
        dataset = hf.create_dataset(location_str, data=np.array([[obj.value]]))
        dataset.attrs["class"] = get_name_from_class(type(obj))
        dataset.attrs["name"] = name

    elif obj is None:
        return  # Do nothing

    elif hasattr(obj, "__array__"):
        obj = np.array(obj)
        return write_object(
            hf, obj, location, overwrite, ignore_missing_compulsory_fields
        )

    else:
        name = location[-1]
        raise TypeError(
            f"Field {name} has type {type(obj)} which is not supported. \
If you think this is a mistake (it very well might be!) then make an issue on the \
repository."
        )


if __name__ == "__main__":
    import doctest
    import os

    doctest.testmod()
    os.system("rm -rf my_point.uff")
