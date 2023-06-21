from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, Protocol, Sequence, Union

import h5py
import numpy as np


class ReaderKeyError(KeyError):
    pass


class ReaderAttrsKeyError(KeyError):
    pass


class NumpyLike(Protocol):
    shape: tuple
    dtype: type

    def __getitem__(self, key):
        ...


class ReaderAttrs(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as e:
            raise ReaderAttrsKeyError() from e


@dataclass
class Reader(ABC):
    path: Sequence[str] = ()

    def __getitem__(self, path: Union[str, Sequence[str]]) -> "Reader":
        "Return a new instance of the Reader with the path appended to the current path."
        return self.append_path(path)

    def __iter__(self):
        return iter(self.keys())

    @abstractmethod
    def append_path(self, path: Union[str, Sequence[str]]) -> "Reader":
        ...

    @abstractmethod
    def keys(self) -> Iterable:
        ...

    @property
    @abstractmethod
    def attrs(self) -> ReaderAttrs:
        ...

    @abstractmethod
    @contextmanager
    def read(self) -> Iterator[Union[NumpyLike, Any]]:
        ...


class H5Reader(Reader):
    def __init__(
        self,
        filepath: Union[str, "Reader"],
        path: Union[str, Sequence[str]] = (),
    ):
        if isinstance(filepath, H5Reader):
            assert (
                path == ()
            ), "Cannot specify path when filepath is a H5Reader. path will be \
overwritten by the reader's obj_path."
            filepath, path = filepath.filepath, filepath.path

        assert isinstance(
            filepath, str
        ), f"filepath must be a string. Got a {type(filepath)}"
        assert isinstance(
            path, (str, tuple, list)
        ), f"path must be a string, tuple or list. Got a {type(path)}"

        self.filepath = filepath
        self.path = (path,) if isinstance(path, str) else tuple(path)

    def append_path(self, path: Union[str, Sequence[str]]) -> "H5Reader":
        if isinstance(path, str):
            path = (path,)
        new_path = self.path + tuple(path)
        new_obj = self.__class__(self.filepath, new_path)
        with new_obj.read():  # <- raises ReaderKeyError if path does not exist
            return new_obj

    def keys(self) -> list:
        with self.read() as obj:
            if isinstance(obj, h5py.Group):
                return list(obj.keys())
            else:
                return []

    @property
    def attrs(self) -> dict:
        try:
            with self.read() as obj:
                return ReaderAttrs(obj.attrs)
        except KeyError as e:
            return None

    @contextmanager
    def read(self) -> Iterator[Union[h5py.Group, h5py.Dataset]]:
        try:
            with h5py.File(self.filepath, "r") as obj:
                for name in self.path:
                    obj = obj[name]
                yield obj
        except ReaderAttrsKeyError as e:
            raise e  # Do not catch ReaderAttrsKeyError
        except KeyError as e:
            raise ReaderKeyError(f"Could not find object at path {self.path}") from e

    def __repr__(self):
        return f"""H5Reader(
    filepath={self.filepath!r},
    obj_path={self.path!r},
    keys={self.keys()!r},
)"""


class NoneReader(Reader):
    """NoneReader is used instead of None to avoid having to check for None everywhere.
    If a user tries to read from a NoneReader we raise an error."""

    def __getitem__(self, path):
        raise ReaderKeyError("Reader not set.")

    def append_path(self) -> "NoneReader":
        return NoneReader()

    def keys(self) -> list:
        return []

    @property
    def attrs(self) -> dict:
        return ReaderAttrs()

    def read(self):
        raise ValueError("Reader not set.")

    def __repr__(self):
        return f"""NoneReader(<No reader has been set>)"""
