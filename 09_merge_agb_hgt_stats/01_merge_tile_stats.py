import os
import pprint
import tqdm

import rsgislib.vectorutils
import rsgislib.tools.utils

import pandas
import numpy

vec_protect_areas_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"
out_path="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_protect_areas"

protect_area_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_protect_areas_file)

tile_lut_file="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_tiles_lut.json"
tile_lut = rsgislib.tools.utils.read_json_to_dict(tile_lut_file)


out_data_dict = dict()
out_data_dict["WDPAID"] = list()
out_data_dict["agb_tot"] = list()
out_data_dict["agb_avg"] = list()
out_data_dict["hchm_avg"] = list()

out_agb_hist = dict()
out_hchm_hist = dict()

for protect_area_lyr in tqdm.tqdm(protect_area_lyrs):
    #print(protect_area_lyr)
    agb_stats_dir = os.path.join(out_path, protect_area_lyr, "agb_tile_stats")
    hgt_stats_dir = os.path.join(out_path, protect_area_lyr, "hchm_tile_stats")

    protect_area_tiles = tile_lut[protect_area_lyr]
    first = True
    agb_area_tot = 0.0
    agb_count = 0.0
    agb_tot = 0.0
    hchm_tot = 0.0
    hchm_count = 0.0

    for protect_area_tile in protect_area_tiles:
        #print(protect_area_tile)
        stats_agb_file = os.path.join(agb_stats_dir, "{}_agb.json".format(protect_area_tile))
        stats_hgt_file = os.path.join(hgt_stats_dir, "{}_hchm.json".format(protect_area_tile))

        stats_agb_dict = rsgislib.tools.utils.read_json_to_dict(stats_agb_file)
        stats_hgt_dict = rsgislib.tools.utils.read_json_to_dict(stats_hgt_file)

        #pprint.pprint(stats_agb_dict)
        #pprint.pprint(stats_hgt_dict)

        if first:
            first = False
            WDPAID = int(protect_area_lyr.replace("WDPAID_", ""))
            agb_area_tot = float(stats_agb_dict["agb_area"])
            agb_count = float(stats_agb_dict["count"])
            agb_tot = float(stats_agb_dict["agb"])
            hchm_tot = float(stats_hgt_dict["hchm"])
            hchm_count = float(stats_hgt_dict["count"])
            out_agb_hist[WDPAID] = numpy.array(stats_agb_dict["hist"], dtype=numpy.uint32)
            out_hchm_hist[WDPAID] = numpy.array(stats_hgt_dict["hist"], dtype=numpy.uint32)
        else:
            agb_area_tot = agb_area_tot + float(stats_agb_dict["agb_area"])
            agb_count = agb_count + float(stats_agb_dict["count"])
            agb_tot = agb_tot + float(stats_agb_dict["agb"])
            hchm_tot = hchm_tot + float(stats_hgt_dict["hchm"])
            hchm_count = hchm_count + float(stats_hgt_dict["count"])

            out_agb_hist[WDPAID] = out_agb_hist[WDPAID] + numpy.array(stats_agb_dict["hist"], dtype=numpy.uint32)
            out_hchm_hist[WDPAID] = out_hchm_hist[WDPAID] + numpy.array(stats_hgt_dict["hist"], dtype=numpy.uint32)

    agb_avg = 0.0
    if agb_count > 0:
        agb_avg = agb_tot / agb_count
    hchm_avg = 0.0
    if hchm_count > 0.0:
        hchm_avg = hchm_tot / hchm_count
    out_data_dict["WDPAID"].append(WDPAID)
    out_data_dict["agb_tot"].append(agb_area_tot)
    out_data_dict["agb_avg"].append(agb_avg)
    out_data_dict["hchm_avg"].append(hchm_avg)

df_stats = pandas.DataFrame.from_dict(out_data_dict)
df_stats.to_feather("protected_agb_hgt_summarised_base_stats.feather")
df_stats.to_csv("protected_agb_hgt_summarised_base_stats.csv")
excel_sheet = 'prot_agb_hgt'
xls_writer = pandas.ExcelWriter("protected_agb_hgt_summarised_base_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
xls_writer.save()

rsgislib.tools.utils.write_dict_to_json(out_agb_hist, "protected_agb_hists.json")
rsgislib.tools.utils.write_dict_to_json(out_hchm_hist, "protected_hchm_hists.json")
