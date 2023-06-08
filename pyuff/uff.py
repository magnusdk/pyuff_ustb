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
from pyuff.readers import Reader, util

# Used to get class from class name in attrs
_name2class = {
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
# Used to get class name from class
_class2name = {v: k for k, v in _name2class.items()}


def get_class_from_name(name: Union[str, bytes]) -> Union[Type[PyuffObject], None]:
    if isinstance(name, bytes):
        name = name.decode("utf-8")
    return _name2class.get(name, None)


def get_name_from_class(cls: Type[PyuffObject]) -> str:
    return _class2name[cls]


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
            return util.read_potentially_list(Reader(self.filepath, name), cls)

    def __getitem__(self, key: str) -> PyuffObject:
        return self.read(key)

    @property
    def fields(self):
        return dict(self.items())

    def keys(self):
        with File(self.filepath, "r") as file:
            return list(file.keys())

    def values(self):
        return [self.read(k) for k in self.keys()]

    def items(self):
        return zip(self.keys(), self.values())

    def __repr__(self) -> str:
        return f"""Uff(
    filepath='{self.filepath}',
    fields={pprint.pformat(self.fields)},
)"""

    def __iter__(self):
        return self.keys()
