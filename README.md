# PyUFF ([USTB](https://www.ustb.no/))
An implementation of [USTB's](https://www.ustb.no/) [ultrasound file format (UFF)](https://www.ustb.no/examples/uff/) in Python.

_Note that this project only implements USTB's version of UFF, which is considered version `0.0.1`. Multiple versions of UFF exists, for example check out [uff-reader](https://github.com/waltsims/uff-reader). However, if you only planning to use USTB's version of UFF then you have come to the right place :)_

## Installing
Run the following command in your Python virtual environment:
```bash
python -m pip install pyuff-ustb
```
To verify that the installation was successful, run the following command:
```bash
python -c "import pyuff_ustb; print(pyuff_ustb.__version__)"
```

## Reading UFF files
```python
import pyuff_ustb as pyuff

uff = pyuff.Uff(filepath)
print(uff)  # <- print the keys of the UFF file
channel_data = uff.read("channel_data")
scan = uff.read("scan")
```

## Writing UFF files
```python
import pyuff_ustb as pyuff
import numpy as np

scan = pyuff.LinearScan(
    x_axis=np.linspace(-10e3, 10e3, 128),
    z_axis=np.linspace(0, 80e3, 128),
)
scan.write("my_scan.uff", "scan")
# To overwrite an existing field in the file, pass overwrite=True like so:
scan.write("my_scan.uff", "scan", overwrite=True)
```

## UFF object structure
See the modules under `pyuff_ustb/objects` for all implemented UFF objects. The most important ones are [`ChannelData`](pyuff_ustb/objects/channel_data.py) and [`Scan`](pyuff_ustb/objects/scan.py).

- `ChannelData` contains the raw ultrasound data under the `data` (`channel_data.data`) property and other important beamforming properties such as `sampling_frequency` and `probe` setup, etc.
- `Scan` is primarily a container of the points that are to be beamformed.

Check out the source code under `pyuff_ustb/objects/channel_data.py` in your favorite code editor to get a better understanding of the UFF object structure.

## Lazy loading
PyUFF strives to only load what you need in order to speed up the reading process. This is done by using lazy loaded properties. Lazy loaded values are only actually read from the file when they are used. This is contrary to _eager loading_ where _all_ values are automatically read from the file when the object is created. Another potential benefit from lazy loading is that it enables streaming of data from the file, which may speed up the reading process even further. Streaming of PyUFF data is not implemented yet.

In general, all UFF object fields are of the type `cached_property`. When a `cached_property` is accessed for the first time, its code will run, and the returned value will be cached, meaning that for most PyUFF fields, values are only read from a file once. The `cached_property` is further split into two types:

- `compulsory_property`: fields that must be set in an object in order to _write_ to a file.
- `optional_property`: optional fields that may be None when writing to a file.

Additionally, there is `dependent_property`, which is **_not_** cached nor read from a file — instead, it is calculated from other compulsory and/or optional properties in the object. All properties of the PyUFF objects are decorated with either `@compulsory_property`, `@optional_property` or `@dependent_property`.

To invalidate a property from the cache (in order to re-read it from the file), simply delete the property from the object. Example:
```python
obj = uff.read("channel_data")
data = obj.data[...]  # <- This will read the data from the file
data = obj.data[...]  # <- Subsequent calls do not read from the file
del obj.data  # <- This deletes the data from the cache
data = obj.data[...]  # <- The data is read again
```

You can still eagerly load all values from the file by calling `pyuff_ustb.eager_load` on the object. Note that `eager_load` does not update the object `(but may read and cache properties)` but returns a new copy. Example:
```python
obj = uff.read("channel_data")
# Eagerly load all values (this usually takes a few seconds, depending on the file size)
# pyuff_ustb.eager_load returns a copy of the object, leaving the original unchanged (though perhaps with cached properties).
obj = pyuff_ustb.eager_load(obj)
```
