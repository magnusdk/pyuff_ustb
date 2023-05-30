from typing import Optional

from pyuff.readers.base import Reader


def read_sequence(sequence_reader: Optional[Reader]):
    if sequence_reader is None:
        return None

    from pyuff.objects.wave import Wave

    with sequence_reader.h5_obj as h5_obj:
        n = h5_obj.attrs["size"][1]
        if n > 1:
            waves = []
            for k in h5_obj:
                waves.append(Wave(sequence_reader[k]))
            return waves
        else:
            return Wave(sequence_reader)
