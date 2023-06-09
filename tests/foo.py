uffs = [
    "Alpinion_L3-8_CPWC_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_CPWC_hypoechoic.uff",
    "Alpinion_L3-8_FI_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_FI_hypoechoic.uff",
    "ARFI_dataset.uff",
    "experimental_dynamic_range_phantom.uff",
    "experimental_STAI_dynamic_range.uff",
    "FieldII_CPWC_point_scatterers_res_v2.uff",
    #### "FieldII_P4_point_scatterers.uff",
    #### "FieldII_speckle_DMASsimulation300000pts.uff",
    "FieldII_speckle_simulation.uff",
    #### "FieldII_STAI_dynamic_range.uff",
    "FieldII_STAI_simulated_dynamic_range.uff",
    #### "FieldII_STAI_uniform_fov.uff",
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
    #### "uff_example.uff",
    "uff_linear_array.uff",
    "uff_linear_scan.uff",
    "uff_matrix_array.uff",
    "uff_point.uff",
    "uff_probe.uff",
    "uff_scan.uff",
    "uff_sector_scan.uff",
    "uff_wave.uff",
    #### "Verasonics_P2-4_apical_four_chamber.uff",
    "Verasonics_P2-4_parasternal_long_small.uff",
    "Verasonics_P2_4_parasternal_long.uff",
]


pngs = [
    "Alpinion_L3-8_CPWC_hyperechoic_scatterers.png",
    "Alpinion_L3-8_CPWC_hypoechoic.png",
    "Alpinion_L3-8_FI_hyperechoic_scatterers.png",
    "Alpinion_L3-8_FI_hypoechoic.png",
    "ARFI_dataset.png",
    "experimental_dynamic_range_phantom.png",
    "experimental_STAI_dynamic_range.png",
    "FieldII_STAI_dynamic_range.png",
    "FieldII_STAI_simulated_dynamic_range.png",
    "PICMUS_carotid_cross.png",
    "PICMUS_carotid_long.png",
    "PICMUS_experiment_contrast_speckle.png",
    "PICMUS_experiment_resolution_distortion.png",
    "PICMUS_simulation_contrast_speckle.png",
    "PICMUS_simulation_resolution_distortion.png",
    "Verasonics_P2-4_parasternal_long.png",
]
zips = [
    "ps.zip",
    "Verasonics_P2-4_parasternal_long.zip",
]
import h5py
import numpy as np


def h5_equals(hf1, hf2) -> bool:
    if dict(hf1.attrs) != dict(hf2.attrs):
        return False
    if isinstance(hf1, h5py.Dataset):
        if not np.array_equal(hf1[...], hf2[...]):
            return False
    elif isinstance(hf1, h5py.Group):
        if set(hf1.keys()) != set(hf2.keys()):
            return False
        for k in hf1.keys():
            v1, v2 = hf1[k], hf2[k]
            if not h5_equals(v1, v2):
                return False
    else:
        raise TypeError(f"Unknown type {type(hf1)}")
    return True


from pyuff.readers import Reader, ReaderKeyError

results = []


def compare_dicts(d1, d2):
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
            if v1 in ("int16", "double"):  # Ignore float precision (can be fixed)
                continue
            return False
    return True


def h5_equals(r1: Reader, r2: Reader) -> bool:
    if len(r1.obj_path) > 0:  # Ignore root attributes
        if not compare_dicts(dict(r1.attrs), dict(r2.attrs)):
            results.append({"attrs": [r1, r2]})
            return False
    with r1.h5_obj as hf1, r2.h5_obj as hf2:
        assert type(hf1) == type(hf2)
        if isinstance(hf1, h5py.Dataset):
            if not np.array_equal(hf1[...], hf2[...]):
                results.append({"dataset": [r1, r2]})
                return False
        elif isinstance(hf1, h5py.Group):
            for k in hf1.keys():
                if k not in hf2.keys():
                    if (
                        (k == "origo" and "origin" in r2)
                        or (k == "apex" and "origin" in r2)
                        or (k == "scan" and "focus" in r2)
                    ):
                        continue
                    results.append({"keys": [r1, r2]})
                    return False
            for k in r1.keys():
                try:
                    sub_r1 = r1[k]
                    k = "origin" if k in ["origo", "apex"] and k not in r2 else k
                    k = "focus" if k in ["scan"] and k not in r2 else k
                    sub_r2 = r2[k]
                    if not h5_equals(sub_r1, sub_r2):
                        results.append({"object": [r1, r2]})
                        return False
                except ReaderKeyError:
                    results.append({"object": [r1, r2]})
                    return False
        else:
            raise TypeError(f"Unknown type {type(r1)}")
    return True



def do_thing():
    import time

    import h5py
    from tqdm import tqdm
    from vbeam.util.download import cached_download

    import pyuff

    timings = {}

    pbar = tqdm(uffs)
    for uff_filename in pbar:
        pbar.set_description(uff_filename)
        filepath = cached_download(f"http://ustb.no/datasets/{uff_filename}")
        before = time.perf_counter()
        uff = pyuff.Uff(filepath)
        for k in uff:
            pyuff.eager_load(uff[k])
        after = time.perf_counter()
        timings[uff_filename] = after - before

        # Write the file to disk
        write_path = f"/home/magnusk/pyuff/tests/written/{uff_filename}"
        with h5py.File(write_path, "a") as file:
            for k in uff:
                v = uff[k]
                pyuff.write_object(file, v, k, overwrite=True)

        # Check if the files are the same
        read_uff = pyuff.Uff(filepath)
        written_uff = pyuff.Uff(write_path)
        for k1, k2 in zip(read_uff, written_uff):
            assert k1 == k2
            assert read_uff[k1] == written_uff[k2]
        h5_equals(Reader(filepath), Reader(write_path))
        print("LEN RESULTS:", len(results))

        # Save results (global var called results) to file
        import pickle

        with open("results.pkl", "wb") as f:
            pickle.dump(results, f)

    timings = sorted(timings.items(), key=lambda x: x[1])
    for t in timings:
        print(t)


if __name__ == "__main__":
    import cProfile
    import io
    import pstats
    from pstats import SortKey

    pr = cProfile.Profile()
    pr.enable()
    do_thing()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(50)
    print(s.getvalue())


# TODO: Verify structure
# TODO: Write back to file
# - ...and assert that the read-back file is the same as the written file

"""
ARFI_dataset.uff
- Har bare 1 wave (ikke en liste en gang). Sequence we et Wave objekt


uff.Window
- Hvorfor er window.sta det samme som window.tukey80?







"""
