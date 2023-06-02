from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

import numpy as np


@dataclass
class LazyOperation:
    transform_data: callable
    transform_index: Optional[callable] = None
    transform_shape: Optional[callable] = None


class LazyTranspose(LazyOperation):
    def __init__(self):
        def transform_index(k, shape: Tuple[int, ...]):
            if not isinstance(k, Sequence):
                k = [k]
            # Add enough new slices to match the number of dimensions
            k = [*k, *[slice(None) for _ in range(len(shape) - len(k))]]
            k = reversed(k)  # Reverse the order of the slices because of the transpose
            return tuple(k)

        def transform_shape(shape: Tuple[int, ...]):
            return tuple(reversed(shape))

        super().__init__(lambda x: x.T, transform_index, transform_shape)


def apply_lazy_operations_on_data(
    data: np.ndarray,
    operations: Sequence[LazyOperation],
) -> np.ndarray:
    for op in operations:
        data = op.transform_data(data)
    return data


def apply_lazy_operations_on_index(
    index,
    shape: Tuple[int, ...],
    operations: Sequence[LazyOperation],
) -> np.ndarray:
    for op in operations:
        if op.transform_index is not None:
            index = op.transform_index(index, shape)
        if op.transform_shape is not None:
            shape = op.transform_shape(shape)
    return index


def apply_lazy_operations_on_shape(
    shape: Tuple[int, ...],
    operations: Sequence[LazyOperation],
) -> np.ndarray:
    for op in operations:
        if op.transform_shape is not None:
            shape = op.transform_shape(shape)
    return shape


if __name__ == "__main__":
    T = LazyTranspose()
    Ts = [T, T, T]
    a = np.ones((2, 3, 4, 5))
    index = (slice(0, 1), 1)
    b = a.__getitem__(apply_lazy_operations_on_index(index, a.shape, Ts))
    b = apply_lazy_operations_on_data(b, Ts)
    print(b.shape)
    assert b.shape == (1, 3, 2)
