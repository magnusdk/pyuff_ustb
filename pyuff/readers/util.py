from typing import TYPE_CHECKING, List, Type, TypeVar, Union

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


def read_scan(scan_reader: Reader):
    from pyuff.objects.scan import Scan
    from pyuff.common import get_class_from_name

    with scan_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Scan), "Expected class to be a subclass of Scan"
        return cls(scan_reader)


def read_probe(probe_reader: Reader):
    from pyuff.objects.probe import Probe
    from pyuff.common import get_class_from_name

    with probe_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Probe), "Expected class to be a subclass of Probe"
        return cls(probe_reader)
