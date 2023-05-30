uffs = [
    "Alpinion_L3-8_CPWC_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_CPWC_hypoechoic.uff",
    "Alpinion_L3-8_FI_hyperechoic_scatterers.uff",
    "Alpinion_L3-8_FI_hypoechoic.uff",
    "ARFI_dataset.uff",
    "experimental_dynamic_range_phantom.uff",
    "experimental_STAI_dynamic_range.uff",
    "FieldII_CPWC_point_scatterers_res_v2.uff",
    # "FieldII_P4_point_scatterers.uff",
    # "FieldII_speckle_DMASsimulation300000pts.uff",
    "FieldII_speckle_simulation.uff",
    # "FieldII_STAI_dynamic_range.uff",
    "FieldII_STAI_simulated_dynamic_range.uff",
    # "FieldII_STAI_uniform_fov.uff",
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
    "uff_example.uff",
    "uff_linear_array.uff",
    "uff_linear_scan.uff",
    "uff_matrix_array.uff",
    "uff_point.uff",
    "uff_probe.uff",
    "uff_scan.uff",
    "uff_sector_scan.uff",
    "uff_wave.uff",
    # "Verasonics_P2-4_apical_four_chamber.uff",
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


def do_thing():
    import time

    from pyuff import ChannelData, Uff
    from tqdm import tqdm

    from vbeam.util.download import cached_download

    timings = {}

    pbar = tqdm(uffs)
    for uff_filename in pbar:
        pbar.set_description(uff_filename)
        filepath = cached_download(f"http://ustb.no/datasets/{uff_filename}")
        before = time.perf_counter()
        uff = Uff(filepath)
        repr(uff)
        after = time.perf_counter()
        timings[uff_filename] = after - before

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
