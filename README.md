# PyUFF v2 (potentially, I don't know)
## Goals
- Easy to read and write UFF files
- Lazy loading of values from file
- Parallel reading (for streaming data)
- Easy to inspect content of `.h5` files

## Some design decisions
- Stricter data-structure than original pyuff because UFF objects and readers are coupled. For example: a `ChannelData` object (`pyuff.objects.channel_data.ChannelData`) has a field called `probe` which it explicitly reads from _"probe"_ (under the path for the channel data object) in the UFF file. The original pyuff reads the UFF-file in the same way that USTB does, where the class of the object is determined by the `class` attribute in the UFF file. This is not the case in pyuff_v2 — the class is determined by the field (`ChannelData.probe` in this case) and an error is thrown if it does not have the correct `class` attribute.
- (Almost) everything is lazy-loaded, meaning that only fields that are used will be loaded into memory. This means that it becomes faster to read UFF-files where we only care about a single field (for example when reading the `scan` field of a UFF-file that additionally has a really big `channel_data` field — the channel data will not be loaded into memory. Or if we only care about the `speed_of_sound` of the `channel_data` field, then only the speed of sound will be read from the .h5 file). It also means that we can support parallel reading of UFF-files or streaming of channel data from UFF-files.

## Some more comments on the code
- `@cached_property` means that when a user accesses the property, the returned value is cached. This means that a value will only be read from the .h5 file once, and we assume that the file doesn't change. The cache can be cleared by deleting the property from the object (Example: `del channel_data.probe`).
- A `LazyArray` represents a numpy array that can be read from the file. It is not actually read until some numpy function is applied to it or when slicing into it.
- Because everything is lazy-loaded from a file, there are a lot of opening and closing of files. I don't think this adds up to a lot of time, but I will perform some profiling of this.
- We strongly couple pyuff with the .h5 format, meaning that it becomes more difficult to support other file-format in the future. I assume this is not a problem.
- Fields that are not in the UFF specification are not read. This means that if a `ChannelData` object in an UFF file has a custom field called `my_field` (`"/channel_data/my_field"`) it can not be easily accessed.¨
