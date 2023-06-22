from enum import Enum
from typing import TYPE_CHECKING, List, Type, Union

import numpy as np

from pyuff_ustb.readers.base import Reader

if TYPE_CHECKING:
    # Import type hint stuff here to avoid circular imports. TYPE_CHECKING is always
    # False at runtime, but is True when type checking.
    from pyuff_ustb.objects.uff import TUff


def read_potentially_list(
    reader: Reader,
    cls: Type["TUff"],
) -> Union["TUff", List["TUff"]]:
    """Read a Uff or a list of Uffs, depending on the "size"
    attribute. If size>1, then we have a list of objects."""
    n = reader.attrs.get("size", [0, 0])[1]
    if n > 1:
        return [cls(reader[k]) for k in reader.keys()]
    else:
        return cls(reader)


def read_list_of_strings(reader: Reader) -> Union[None, List[str]]:
    """Return a list of strings if the size of the read h5 object is greater than 0.
    Return None if n==0."""

    def parse(integer_list: List[int]) -> str:
        int_chars = np.squeeze(integer_list)  # A list of integers
        chars = [chr(int(c)) for c in int_chars]  # Convert the integers to chars
        value = "".join(chars)  # Join the chars into a string
        return value

    n = reader.attrs.get("size", [0, 0])[1]
    if n > 0:
        strs = []
        for k in reader.keys():
            with reader[k].read() as obj:
                strs.append(parse(obj))
        return strs
    else:
        with reader.read() as obj:
            return parse(list(obj))


def read_enum(reader: Reader, cls: Type[Enum]):
    with reader.read() as obj:
        return cls(np.squeeze(obj))


def read_scan(scan_reader: Reader):
    from pyuff_ustb.common import get_class_from_name
    from pyuff_ustb.objects.scans.scan import Scan

    cls = get_class_from_name(scan_reader.attrs["class"])
    assert issubclass(cls, Scan), "Expected class to be a subclass of Scan"
    return cls(scan_reader)


def read_probe(probe_reader: Reader):
    from pyuff_ustb.common import get_class_from_name
    from pyuff_ustb.objects.probes.probe import Probe

    cls = get_class_from_name(probe_reader.attrs["class"])
    assert issubclass(cls, Probe), "Expected class to be a subclass of Probe"
    return cls(probe_reader)
