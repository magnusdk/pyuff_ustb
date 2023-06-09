from typing import TYPE_CHECKING, List, Type, Union

import numpy as np

from pyuff.readers.base import Reader

if TYPE_CHECKING:
    # Import type hint stuff here to avoid circular imports. TYPE_CHECKING is always
    # False at runtime, but is True when type checking.
    from pyuff.objects.uff import TUff


def read_potentially_list(
    reader: Reader,
    cls: Type["TUff"],
) -> Union["TUff", List["TUff"]]:
    """Read a Uff or a list of Uffs, depending on the "size"
    attribute. If size>1, then we have a list of objects."""
    with reader.h5_obj as obj:
        n = obj.attrs["size"][1]
        if n > 1:
            return [cls(reader[k]) for k in obj]
        else:
            return cls(reader)


def read_list_of_strings(reader: Reader) -> Union[None, List[str]]:
    """Return a list of strings if the size of the read h5 object is greater than 0.
    Return None if n==0."""

    def parse(integer_list: List[int]) -> str:
        int_chars = np.squeeze(integer_list)  # A list of integers
        chars = [chr(c) for c in int_chars]  # Convert the integers to chars
        value = "".join(chars)  # Join the chars into a string
        return value

    with reader.h5_obj as obj:
        n = obj.attrs.get("size", [0, 0])[1]
        if n > 0:
            return [parse(obj[k]) for k in obj]
        else:
            return parse(obj)


def read_scan(scan_reader: Reader):
    from pyuff.common import get_class_from_name
    from pyuff.objects.scan import Scan

    with scan_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Scan), "Expected class to be a subclass of Scan"
        return cls(scan_reader)


def read_probe(probe_reader: Reader):
    from pyuff.common import get_class_from_name
    from pyuff.objects.probe import Probe

    with probe_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Probe), "Expected class to be a subclass of Probe"
        return cls(probe_reader)
