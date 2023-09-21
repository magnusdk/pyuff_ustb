import os
import tempfile

import h5py
import numpy as np
import pytest

import pyuff_ustb as pyuff
from pyuff_ustb.common import get_class_from_name
from pyuff_ustb.objects.uff import dependent_property
from pyuff_ustb.readers import H5Reader, ReaderKeyError
from pyuff_ustb.readers.lazy_arrays import LazyArray

# Default download location when using vbeam.util.download.cached_download
_data_folder = os.path.expanduser("~/.vbeam_downloads/ustb.no/datasets/")
# NOTE: You must have downloaded all the following files to run these tests!
_uff_filenames = [
    "Alpinion_L3-8_CPWC_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_CPWC_hypoechoic.uff",
    "Alpinion_L3-8_FI_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_FI_hypoechoic.uff",
    "ARFI_dataset.uff",
    "experimental_dynamic_range_phantom.uff",
    "experimental_STAI_dynamic_range.uff",
    "FieldII_CPWC_point_scatterers_res_v2.uff",
    ## "FieldII_P4_point_scatterers.uff",
    ## "FieldII_speckle_DMASsimulation300000pts.uff",
    "FieldII_speckle_simulation.uff",
    ## "FieldII_STAI_dynamic_range.uff",
    "FieldII_STAI_simulated_dynamic_range.uff",
    ## "FieldII_STAI_uniform_fov.uff",
    "FI_P4_cysts_center.uff",
    "FI_P4_point_scatterers.uff",
    "L7_CPWC_193328.uff",
    "L7_FI_carotid_cross_1.uff",
    "L7_FI_carotid_cross_2.uff",
    "L7_FI_carotid_cross_sub_2.uff",
    "L7_FI_IUS2018.uff",
    "L7_FI_Verasonics_CIRS_points.uff",
    "L7_FI_Verasonics_CIRS.uff",
    "L7_FI_Verasonics.uff",
    "PICMUS_carotid_cross.uff",
    "PICMUS_carotid_long.uff",
    "PICMUS_experiment_contrast_speckle.uff",
    "PICMUS_experiment_resolution_distortion.uff",
    "PICMUS_simulation_contrast_speckle.uff",
    "PICMUS_simulation_resolution_distortion.uff",
    "reference_RTB_data.uff",
    "SWE_L7_type_III.uff",
    "SWE_L7_type_I.uff",
    "SWE_L7_type_IV.uff",
    "test01.uff",
    "uff_apodization.uff",
    "uff_beamformed_data.uff",
    "uff_channel_data.uff",
    "uff_curvilinear_array.uff",
    ## "uff_example.uff",
    "uff_linear_array.uff",
    "uff_linear_scan.uff",
    "uff_matrix_array.uff",
    "uff_point.uff",
    "uff_probe.uff",
    "uff_scan.uff",
    "uff_sector_scan.uff",
    "uff_wave.uff",
    ## "Verasonics_P2-4_apical_four_chamber.uff",
    "Verasonics_P2-4_parasternal_long_small.uff",
    "Verasonics_P2_4_parasternal_long.uff",
]


@pytest.fixture(params=_uff_filenames)
def uff_filepath(request: pytest.FixtureRequest):
    """Any test-function that references this function by name in their arguments will
    be run once for each filename.

    For example:
    >>> def test_reading_eagerly(uff_filepath):  # uff_filepath referenced in arguments
    ...    print(uff_filepath)
    ...    assert True  # <- some arbitrary assertion on the uff file
    will print the path to each file in _uff_filenames and make some test assertions."""
    return _data_folder + request.param


def test_reading_eagerly(uff_filepath):
    # Load each object in the uff file eagerly
    uff = pyuff.Uff(uff_filepath)
    for k in uff:
        pyuff.eager_load(uff[k])


def _eager_read_dependent_properties(obj):
    if isinstance(obj, LazyArray):
        return np.array(obj)
    elif isinstance(obj, pyuff.Uff):
        kwargs = {}
        for name in obj._get_fields(skip_dependent_properties=True):
            kwargs[name] = _eager_read_dependent_properties(getattr(obj, name))
        for name in obj._get_fields(only_dependent_properties=True):
            _eager_read_dependent_properties(getattr(obj, name))
        return obj.__class__(**kwargs)
    elif isinstance(obj, (list, tuple)):
        return [_eager_read_dependent_properties(o) for o in obj]
    elif isinstance(obj, dict):
        return {k: _eager_read_dependent_properties(v) for k, v in obj.items()}
    else:
        return obj


def test_reading_dependent_properties(uff_filepath):
    # Load each object in the uff file eagerly
    uff = pyuff.Uff(uff_filepath)
    for k in uff:
        try:
            _eager_read_dependent_properties(uff[k])
        except ValueError as e:
            # Some datasets are missing compulsory fields. Let's ignore them.
            if str(e) in [
                "The 'probe' parameter is not set.",
                "Gamma is not defined for this phantom",
            ]:
                continue
            else:
                raise e
        except NotImplementedError:
            # Some things are not implemented yet. Let's ignore them.
            continue


def test_reading_and_writing(uff_filepath):
    read_uff = pyuff.Uff(uff_filepath)

    # Make a temporary h5py file to write to that is deleted at the end of the test
    with tempfile.NamedTemporaryFile(suffix=".uff") as tmp:
        with h5py.File(tmp.name, "w") as h5_file:
            # Load and write each object in the uff file
            for k in read_uff:
                v = pyuff.eager_load(read_uff[k])
                pyuff.write_object(
                    h5_file, v, k, overwrite=True, ignore_missing_compulsory_fields=True
                )

        # Read the written file and compare its objects to the ones in the original
        written_uff = pyuff.Uff(tmp.name)
        for k1, k2 in zip(read_uff, written_uff):
            assert k1 == k2, "Keys do not match"
            assert read_uff[k1] == written_uff[k2], "Values do not match"

        # Compare the h5 files directly
        assert _h5_equals(
            read_uff._reader, written_uff._reader
        ), "H5 files do not match"


def test_writing_point():
    point = pyuff.Point(distance=0, azimuth=0, elevation=0)
    with tempfile.NamedTemporaryFile(suffix=".uff") as file:
        point.write(file.name, "point")
        # Compare the results
        uff = pyuff.Uff(file.name)
        assert uff.read("point") == point


def test_writing_missing_compulsory_fields():
    wave = pyuff.Wave()
    with tempfile.NamedTemporaryFile(suffix=".uff") as file:
        with pytest.raises(ValueError):
            # Writing an object with missing compulsory fields should raise an error
            wave.write(file.name, "wave")

    with tempfile.NamedTemporaryFile(suffix=".uff") as file:
        # With ignore_missing_compulsory_fields=True we write the object anyway
        wave.write(file.name, "point", ignore_missing_compulsory_fields=True)
        # Compare the results
        uff = pyuff.Uff(file.name)
        assert uff.read("point") == wave


def _compare_dicts(d1: dict, d2: dict):
    for k in d1.keys():
        if k not in d2.keys():
            return False
        v1, v2 = d1[k], d2[k]
        # Decode bytes for strings
        v1 = v1.decode("utf-8") if isinstance(v1, bytes) else v1
        v2 = v2.decode("utf-8") if isinstance(v2, bytes) else v2
        # Ignore slashes in strings
        v1 = v1.replace("/", "") if isinstance(v1, str) else v1
        v2 = v2.replace("/", "") if isinstance(v2, str) else v2
        if isinstance(v1, np.ndarray):
            if not np.array_equal(v1, v2):
                return False
        elif v1 != v2:
            # Ignore float precision
            if v1 in ("int16", "double"):
                continue
            # Backwards compatibility
            if (
                ({v1, v2} == {"scan", "focus"})
                or ({v1, v2} == {"origin", "apex"})
                or ({v1, v2} == {"origin", "origo"})
            ):
                continue
            return False
    return True


def _is_dependent_property(hf: h5py.Group, k: str):
    cls = get_class_from_name(hf.attrs["class"])
    attr = getattr(cls, k)
    return isinstance(attr, dependent_property)


def _h5_equals(r1: H5Reader, r2: H5Reader) -> bool:
    if len(r1.path) > 0:  # Ignore root attributes
        if not _compare_dicts(dict(r1.attrs), dict(r2.attrs)):
            return False
    with r1.read() as hf1, r2.read() as hf2:
        assert type(hf1) == type(hf2)
        if isinstance(hf1, h5py.Dataset):
            v1, v2 = np.squeeze(hf1[...]), np.squeeze(hf2[...])
            if not np.array_equal(v1, v2):
                return False
        elif isinstance(hf1, h5py.Group):
            for k in hf1.keys():
                if k not in hf2.keys():
                    # Backwards compatibility
                    if (
                        (k == "origo" and "origin" in r2)
                        or (k == "apex" and "origin" in r2)
                        or (k == "scan" and "focus" in r2)
                        # Dependent properties does not need to match because we don't
                        # write them.
                        or _is_dependent_property(hf1, k)
                        or (
                            k in ["x", "y", "z"]
                            and issubclass(
                                get_class_from_name(r1.attrs["class"]),
                                (
                                    pyuff.LinearScan,
                                    pyuff.SectorScan,
                                ),
                            )
                        )
                    ):
                        continue
                    return False
            for k in r1.keys():
                try:
                    sub_r1 = r1[k]
                    # Backwards compatibility
                    k = "origin" if k in ["origo", "apex"] and k not in r2 else k
                    k = "focus" if k in ["scan"] and k not in r2 else k
                    sub_r2 = r2[k]
                    if not _h5_equals(sub_r1, sub_r2):
                        return False
                except ReaderKeyError:
                    if k in ["x", "y", "z"] and issubclass(
                        get_class_from_name(r1.attrs["class"]),
                        (
                            pyuff.LinearScan,
                            pyuff.SectorScan,
                        ),
                    ):
                        continue
                    # Dependent properties does not need to match because we don't
                    # write them.
                    if _is_dependent_property(hf1, k):
                        continue
                    return False
        else:
            raise TypeError(f"Unknown type {type(r1)}")
    return True
