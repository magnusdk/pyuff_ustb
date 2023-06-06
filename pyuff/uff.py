import pprint
from typing import Type, Union

from h5py import File

from pyuff.objects import (
    Apodization,
    BeamformedData,
    ChannelData,
    CurvilinearArray,
    CurvilinearMatrixArray,
    LinearArray,
    LinearScan,
    MatrixArray,
    Phantom,
    Point,
    Probe,
    Pulse,
    PyuffObject,
    Scan,
    SectorScan,
    Wave,
    Wavefront,
    Window,
)
from pyuff.readers import Reader


def get_class_from_name(name: Union[str, bytes]) -> Union[Type[PyuffObject], None]:
    class_dict = {
        "uff.apodization": Apodization,
        "uff.beamformed_data": BeamformedData,
        "uff.channel_data": ChannelData,
        "uff.curvilinear_array": CurvilinearArray,
        "uff.curvilinear_matrix_array": CurvilinearMatrixArray,
        "uff.linear_array": LinearArray,
        "uff.matrix_array": MatrixArray,
        "uff.phantom": Phantom,
        "uff.point": Point,
        "uff.probe": Probe,
        "uff.pulse": Pulse,
        "uff.pyuff_object": PyuffObject,
        "uff.sector_scan": SectorScan,
        "uff.scan": Scan,
        "uff.linear_scan": LinearScan,
        "uff.wave": Wave,
        "uff.wavefront": Wavefront,
        "uff.window": Window,
    }
    if isinstance(name, bytes):
        name = name.decode("utf-8")
    return class_dict.get(name, None)


class Uff:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read(self, name: str) -> PyuffObject:
        with File(self.filepath, "r") as file:
            obj = file[name]
            cls_name = obj.attrs["class"]
            cls = get_class_from_name(cls_name)
            if cls is None:
                raise NotImplementedError(
                    f"Class '{cls_name}' (at location '{name}') is not implemented."
                )
            return cls(Reader(self.filepath, name))

    def __getitem__(self, key: str) -> PyuffObject:
        return self.read(key)

    @property
    def fields(self):
        return dict(self)

    def keys(self):
        with File(self.filepath, "r") as file:
            return list(file.keys())

    def __repr__(self) -> str:
        return f"""Uff(
    filepath='{self.filepath}',
    fields={pprint.pformat(self.fields)},
)"""

    def __iter__(self):
        for k in self.keys():
            yield k, self.read(k)
        return
