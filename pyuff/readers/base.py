from contextlib import contextmanager
from typing import Sequence, Union

import h5py


class ReaderKeyError(KeyError):
    pass


class ReaderAttrsKeyError(KeyError):
    pass


class Reader:
    def __init__(
        self, filepath: Union[str, "Reader"], obj_path: Union[str, Sequence[str]] = ()
    ):
        if isinstance(filepath, Reader):
            assert (
                obj_path == ()
            ), "Cannot specify obj_path when filepath is a Reader. obj_path will be \
overwritten by the reader's obj_path."
            filepath, obj_path = filepath.filepath, filepath.obj_path
        self.filepath = filepath
        self.obj_path = (obj_path,) if isinstance(obj_path, str) else tuple(obj_path)

    def __getitem__(self, path: Union[str, Sequence[str]]) -> "Reader":
        "Return a new instance with the path appended to the current path."
        if isinstance(path, str):
            path = (path,)
        new_path = self.obj_path + tuple(path)
        new_reader = self.__class__(self.filepath, new_path)
        # Ensure that path exists
        with new_reader.h5_obj:  # <- raises ReaderKeyError if path does not exist
            return new_reader

    def keys(self):
        return list(self)  # See __iter__

    @property
    def attrs(self) -> dict:
        with self.h5_obj as obj:
            return dict(obj.attrs)

    def __iter__(self):
        with self.h5_obj as obj:
            if isinstance(obj, h5py.Group):
                yield from obj.keys()

    @property
    @contextmanager
    def h5_obj(self):
        try:
            with h5py.File(self.filepath, "r") as obj:
                for name in self.obj_path:
                    obj = obj[name]
                yield obj
        except ReaderAttrsKeyError as e:
            raise e  # Do not catch ReaderAttrsKeyError
        except KeyError as e:
            raise ReaderKeyError(
                f"Could not find object at path {self.obj_path}"
            ) from e

    def __repr__(self):
        return f"""Reader(
    filepath={self.filepath!r},
    obj_path={self.obj_path!r},
    keys={self.keys()!r},
)"""


class NoneReader(Reader):
    """NoneReader is used instead of None to avoid having to check for None everywhere.
    If a user tries to read from a NoneReader we raise an error."""

    def __init__(self):
        pass

    def __getitem__(self, path):
        raise ReaderKeyError("Reader not set.")

    @property
    def attrs(self):
        return {}  # Empty attrs

    def __iter__(self):
        return iter([])  # Empty iterator

    @property
    def h5_obj(self):
        raise ValueError("Reader not set.")

    def __repr__(self):
        return f"""NoneReader(<No reader has been set>)"""
