import os
import pprint

import rsgislib.vectorutils
import rsgislib.tools.utils

import pandas

vec_protect_areas_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"
out_path="/home/pete/Documents/gmw_protected_areas/data/gmw_ext_protect_areas"

protect_area_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_protect_areas_file)

tile_lut_file="/home/pete/Documents/gmw_protected_areas/data/gmw_ext_tiles_lut.json"
tile_lut = rsgislib.tools.utils.read_json_to_dict(tile_lut_file)

out_data_dict = dict()
out_data_dict["WDPAID"] = list()
out_data_dict["1996_ext"] = list()
out_data_dict["gain_2007"] = list()
out_data_dict["loss_2007"] = list()
out_data_dict["gain_2008"] = list()
out_data_dict["loss_2008"] = list()
out_data_dict["gain_2009"] = list()
out_data_dict["loss_2009"] = list()
out_data_dict["gain_2010"] = list()
out_data_dict["loss_2010"] = list()
out_data_dict["gain_2015"] = list()
out_data_dict["loss_2015"] = list()
out_data_dict["gain_2016"] = list()
out_data_dict["loss_2016"] = list()
out_data_dict["gain_2017"] = list()
out_data_dict["loss_2017"] = list()
out_data_dict["gain_2018"] = list()
out_data_dict["loss_2018"] = list()
out_data_dict["gain_2019"] = list()
out_data_dict["loss_2019"] = list()
out_data_dict["gain_2020"] = list()
out_data_dict["loss_2020"] = list()

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

        out_data_dict["WDPAID"].append(int(protect_area_lyr.replace("WDPAID_", "")))
        out_data_dict["1996_ext"].append(float(stats_96_ext_dict["area"]))
        out_data_dict["gain_2007"].append(float(stats_chng_ext_dict["2007"]["area"][0]))
        out_data_dict["loss_2007"].append(float(stats_chng_ext_dict["2007"]["area"][1]))
        out_data_dict["gain_2008"].append(float(stats_chng_ext_dict["2008"]["area"][0]))
        out_data_dict["loss_2008"].append(float(stats_chng_ext_dict["2008"]["area"][1]))
        out_data_dict["gain_2009"].append(float(stats_chng_ext_dict["2009"]["area"][0]))
        out_data_dict["loss_2009"].append(float(stats_chng_ext_dict["2009"]["area"][1]))
        out_data_dict["gain_2010"].append(float(stats_chng_ext_dict["2010"]["area"][0]))
        out_data_dict["loss_2010"].append(float(stats_chng_ext_dict["2010"]["area"][1]))
        out_data_dict["gain_2015"].append(float(stats_chng_ext_dict["2015"]["area"][0]))
        out_data_dict["loss_2015"].append(float(stats_chng_ext_dict["2015"]["area"][1]))
        out_data_dict["gain_2016"].append(float(stats_chng_ext_dict["2016"]["area"][0]))
        out_data_dict["loss_2016"].append(float(stats_chng_ext_dict["2016"]["area"][1]))
        out_data_dict["gain_2017"].append(float(stats_chng_ext_dict["2017"]["area"][0]))
        out_data_dict["loss_2017"].append(float(stats_chng_ext_dict["2017"]["area"][1]))
        out_data_dict["gain_2018"].append(float(stats_chng_ext_dict["2018"]["area"][0]))
        out_data_dict["loss_2018"].append(float(stats_chng_ext_dict["2018"]["area"][1]))
        out_data_dict["gain_2019"].append(float(stats_chng_ext_dict["2019"]["area"][0]))
        out_data_dict["loss_2019"].append(float(stats_chng_ext_dict["2019"]["area"][1]))
        out_data_dict["gain_2020"].append(float(stats_chng_ext_dict["2020"]["area"][0]))
        out_data_dict["loss_2020"].append(float(stats_chng_ext_dict["2020"]["area"][1]))
    break

df_stats = pandas.DataFrame.from_dict(out_data_dict)
df_stats.to_feather("protected_area_summarised_base_stats.feather")
df_stats.to_csv("protected_area_summarised_base_stats.csv")
excel_sheet = 'prot_area_ext'
xls_writer = pandas.ExcelWriter("protected_area_summarised_base_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
xls_writer.save()