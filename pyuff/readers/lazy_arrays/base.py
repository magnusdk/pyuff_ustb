from dataclasses import dataclass
from functools import reduce
from typing import Sequence, Tuple, Union

import h5py
import numpy as np

from pyuff.readers import Reader, ReaderAttrsKeyError
from pyuff.readers.lazy_arrays.lazy_operations import (
    LazyOperation,
    LazyTranspose,
    apply_lazy_operations_on_data,
    apply_lazy_operations_on_index,
    apply_lazy_operations_on_shape,
)


def _attrs_get(obj: Union[h5py.Group, h5py.Dataset], key: str):
    try:
        return obj.attrs[key]
    except KeyError as e:
        raise ReaderAttrsKeyError() from e


@dataclass
class LazyArray:
    _reader: Reader
    _lazy_operations: Sequence[LazyOperation] = ()

    def __post_init__(self):
        if not isinstance(self._reader, Reader):
            raise TypeError(
                f"Expected a Reader object, got {type(self._reader)} instead."
            )

    def __repr__(self):
        return f"<LazyArray shape={self.shape} dtype={self.dtype}>"

    def __getitem__(self, k) -> np.ndarray:
        with self._reader.h5_obj as obj:
            is_complex = _attrs_get(obj, "complex")[0]
            if is_complex:
                real = obj["real"]
                imag = obj["imag"]
                k = apply_lazy_operations_on_index(k, real.shape, self._lazy_operations)
                value = real.__getitem__(k) + 1j * imag.__getitem__(k)
            else:
                k = apply_lazy_operations_on_index(k, obj.shape, self._lazy_operations)
                value = obj.__getitem__(k)
            return apply_lazy_operations_on_data(value, self._lazy_operations)

    @property
    def T(self):
        return LazyArray(self._reader, self._lazy_operations + (LazyTranspose(),))

    @property
    def shape(self) -> Tuple[int, ...]:
        with self._reader.h5_obj as obj:
            is_complex = _attrs_get(obj, "complex")[0]
            shape = obj["real"].shape if is_complex else obj.shape
            return apply_lazy_operations_on_shape(shape, self._lazy_operations)

    @property
    def size(self) -> int:
        return reduce(lambda x, y: x * y, self.shape)

    @property
    def ndim(self) -> int:
        return len(self.shape)

    @property
    def dtype(self) -> np.dtype:
        with self._reader.h5_obj as obj:
            is_complex = _attrs_get(obj, "complex")[0]
            # NOTE: Complex numbers may have a different number of bits than stated
            return np.complex128 if is_complex else obj.dtype

    def __len__(self) -> int:
        if self.ndim == 0:
            raise TypeError("len() of unsized object")
        return self.shape[0]

    # Conversion operations
    def __array__(self):
        return self[...]

    def __jax_array__(self):
        import jax.numpy as jnp

        return jnp.array(self[...])

    def __float__(self):
        return float(self[...])

    def __int__(self):
        return float(self[...])

    # Math operations
    def __add__(self, other):
        return self[...] + other

    def __sub__(self, other):
        return self[...] - other

    def __mul__(self, other):
        return self[...] * other

    def __truediv__(self, other):
        return self[...] / other

    def __radd__(self, other):
        return other + self[...]

    def __rsub__(self, other):
        return other - self[...]

    def __rmul__(self, other):
        return other * self[...]

    def __rtruediv__(self, other):
        return other / self[...]

    # Check for equality
    def __eq__(self, other):
        return np.array_equal(self[...], other)


class LazyScalar(LazyArray):
    def __init__(
        self,
        reader: Reader,
        lazy_operations: Sequence[LazyOperation] = (),
    ):
        def transform_shape(shape: Tuple[int, ...]):
            # If you think that this assertion should not fail, then it might be a bug
            # and we should use LazyArray instead for the given value.
            assert all(dim == 1 for dim in shape), "Expected a scalar value."
            return ()

        lazy_squeeze = LazyOperation(np.squeeze, transform_shape=transform_shape)
        super().__init__(reader, tuple([lazy_squeeze, *lazy_operations]))
