"""Module containing common utility functions, such as getting the right Uff-class from 
a string and vice-versa."""

from typing import Type, Union

from pyuff_ustb.objects import (
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
    Scan,
    SectorScan,
    Uff,
    Wave,
    Wavefront,
    Window,
)

# Used to get class from class name in attrs
_name2class = {
    "uff": Uff,
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
    "uff.sector_scan": SectorScan,
    "uff.scan": Scan,
    "uff.linear_scan": LinearScan,
    "uff.wave": Wave,
    "uff.wavefront": Wavefront,
    "uff.window": Window,
}
# Used to get class name from class
_class2name = {v: k for k, v in _name2class.items()}


def get_class_from_name(name: Union[str, bytes]) -> Union[Type[Uff], None]:
    if isinstance(name, bytes):
        name = name.decode("utf-8")
    return _name2class.get(name, None)


def get_name_from_class(cls: Type[Uff]) -> str:
    return _class2name[cls]
