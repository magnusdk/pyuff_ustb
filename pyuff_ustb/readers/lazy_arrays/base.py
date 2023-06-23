from dataclasses import dataclass
from functools import reduce
from typing import Sequence, Tuple

import numpy as np

from pyuff_ustb.readers import Reader
from pyuff_ustb.readers.lazy_arrays.lazy_operations import (
    LazyOperation,
    LazyTranspose,
    apply_lazy_operations_on_data,
    apply_lazy_operations_on_index,
    apply_lazy_operations_on_shape,
)


@dataclass(frozen=True)
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
        is_complex = np.squeeze(self._reader.attrs["complex"])
        if is_complex:
            with self._reader["real"].read() as obj:
                real = obj
                k = apply_lazy_operations_on_index(k, real.shape, self._lazy_operations)
                real = real.__getitem__(k)
            with self._reader["imag"].read() as obj:
                imag = obj.__getitem__(k)
            value = real + 1j * imag
        else:
            with self._reader.read() as obj:
                k = apply_lazy_operations_on_index(k, obj.shape, self._lazy_operations)
                value = obj.__getitem__(k)
        return apply_lazy_operations_on_data(value, self._lazy_operations)

    @property
    def T(self):
        return LazyArray(self._reader, (*self._lazy_operations, LazyTranspose()))

    @property
    def shape(self) -> Tuple[int, ...]:
        is_complex = np.squeeze(self._reader.attrs["complex"])
        reader = self._reader["real"] if is_complex else self._reader
        with reader.read() as obj:
            shape = obj.shape
        return apply_lazy_operations_on_shape(shape, self._lazy_operations)

    @property
    def size(self) -> int:
        return reduce(lambda x, y: x * y, self.shape)

    @property
    def ndim(self) -> int:
        return len(self.shape)

    @property
    def dtype(self) -> np.dtype:
        if np.squeeze(self._reader.attrs["complex"]):
            # NOTE: Complex numbers may have a different number of bits than stated
            return np.complex128
        with self._reader.read() as obj:
            return obj.dtype

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
        super().__init__(reader, (lazy_squeeze, *lazy_operations))
