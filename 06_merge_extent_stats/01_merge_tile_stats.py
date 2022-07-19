import os
import pprint

import rsgislib.vectorutils
import rsgislib.tools.utils

vec_protect_areas_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"
out_path="/home/pete/Documents/gmw_protected_areas/data/gmw_ext_protect_areas"

protect_area_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_protect_areas_file)

tile_lut_file="/home/pete/Documents/gmw_protected_areas/data/gmw_ext_tiles_lut.json"
tile_lut = rsgislib.tools.utils.read_json_to_dict(tile_lut_file)

for protect_area_lyr in protect_area_lyrs:
    print(protect_area_lyr)
    ext_stats_dir = os.path.join(out_path, protect_area_lyr, "extent_tile_stats")
    chng_ext_stats_dir = os.path.join(out_path, protect_area_lyr, "chng_extent_tile_stats")

    protect_area_tiles = tile_lut[protect_area_lyr]
    for protect_area_tile in protect_area_tiles:
        print(protect_area_tile)
        stats_96_ext_file = os.path.join(ext_stats_dir, "{}_extent.json".format(protect_area_tile))
        stats_chng_ext_file = os.path.join(chng_ext_stats_dir, "{}_chng_extent.json".format(protect_area_tile))

        stats_96_ext_dict = rsgislib.tools.utils.read_json_to_dict(stats_96_ext_file)
        stats_chng_ext_dict = rsgislib.tools.utils.read_json_to_dict(stats_chng_ext_file)

        pprint.pprint(stats_96_ext_dict)
        pprint.pprint(stats_chng_ext_dict)
    break
