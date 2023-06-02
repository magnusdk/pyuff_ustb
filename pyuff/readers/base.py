from contextlib import contextmanager
from typing import Sequence, Union

import h5py


class Reader:
    def __init__(
        self, filepath: Union[str, "Reader"], obj_path: Union[str, Sequence[str]] = ()
    ):
        if isinstance(filepath, Reader):
            assert (
                obj_path == ()
            ), "Cannot specify obj_path when filepath is a Reader. obj_path will be \
overwritten by the reader's obj_path."
            filepath, obj_path = filepath.h5_filepath, filepath.h5_obj_path
        self.h5_filepath = filepath
        self.h5_obj_path = (obj_path,) if isinstance(obj_path, str) else tuple(obj_path)

    def __getitem__(self, path: Union[str, Sequence[str]]) -> Union["Reader", None]:
        "Return a new instance with the path appended to the current path."
        if isinstance(path, str):
            path = (path,)
        reader = self.__class__(self.h5_filepath, self.h5_obj_path + tuple(path))
        return reader if reader.path_exists() else None

    @property
    def keys(self):
        return list(self)  # See __iter__

    def __iter__(self):
        with self.h5_obj as obj:
            if isinstance(obj, h5py.Group):
                yield from obj.keys()

    def path_exists(self) -> bool:
        try:
            with self.h5_obj:
                return True
        except KeyError:
            return False

    @property
    @contextmanager
    def h5_obj(self):
        with h5py.File(self.h5_filepath, "r") as obj:
            for name in self.h5_obj_path:
                obj = obj[name]
            yield obj

    def __repr__(self):
        return f"""Reader(
    filepath={self.h5_filepath!r},
    obj_path={self.h5_obj_path!r},
    keys={self.keys!r},
)"""
