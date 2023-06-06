from typing import Optional

from pyuff.readers.base import Reader


def read_sequence(sequence_reader: Reader):
    from pyuff.objects.wave import Wave

    with sequence_reader.h5_obj as obj:
        n = obj.attrs["size"][1]
        if n > 1:
            waves = []
            for k in obj:
                waves.append(Wave(sequence_reader[k]))
            return waves
        else:
            return Wave(sequence_reader)


def read_scan(scan_reader: Reader):
    from pyuff.objects.scan import Scan
    from pyuff.uff import get_class_from_name

    with scan_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Scan), "Expected class to be a subclass of Scan"
        return cls(scan_reader)


def read_probe(probe_reader: Reader):
    from pyuff.objects.probe import Probe
    from pyuff.uff import get_class_from_name

    with probe_reader.h5_obj as obj:
        cls = get_class_from_name(obj.attrs["class"])
        assert issubclass(cls, Probe), "Expected class to be a subclass of Probe"
        return cls(probe_reader)
