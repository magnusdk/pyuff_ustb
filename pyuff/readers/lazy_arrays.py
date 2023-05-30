from dataclasses import dataclass

from pyuff.readers import Reader


@dataclass
class LazyArray:
    reader: Reader

    def __getitem__(self, k):
        with self.reader.h5_obj as h5_obj:
            is_complex = h5_obj.attrs["complex"][0]
            if is_complex:
                real = h5_obj["real"].__getitem__(k)
                imag = h5_obj["imag"].__getitem__(k)
                value = real + 1j * imag
            else:
                value = h5_obj.__getitem__(k)
            return value

    @property
    def shape(self):
        with self.reader.h5_obj as h5_obj:
            is_complex = h5_obj.attrs["complex"][0]
            if is_complex:
                return h5_obj["real"].shape
            return h5_obj.shape

    @property
    def ndim(self):
        with self.reader.h5_obj as h5_obj:
            is_complex = h5_obj.attrs["complex"][0]
            if is_complex:
                return h5_obj["real"].ndim
            return h5_obj.ndim

    def __len__(self):
        with self.reader.h5_obj as h5_obj:
            is_complex = h5_obj.attrs["complex"][0]
            if is_complex:
                return len(h5_obj["real"])
            return len(h5_obj)

    def __array__(self):
        return self[...]
