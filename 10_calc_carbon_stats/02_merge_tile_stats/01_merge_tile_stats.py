import os
import pprint
import tqdm

import rsgislib.vectorutils
import rsgislib.tools.utils

import pandas
import numpy

vec_protect_areas_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"
#out_path="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_protect_areas"
out_xtr_path="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_protect_areas_dec22"

protect_area_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_protect_areas_file)

tile_lut_file="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_tiles_lut.json"
tile_lut = rsgislib.tools.utils.read_json_to_dict(tile_lut_file)


out_data_dict = dict()
out_data_dict["WDPAID"] = list()
out_data_dict["soil_c_tot"] = list()
out_data_dict["soil_c_avg"] = list()
out_data_dict["tot_c_tot"] = list()
out_data_dict["tot_c_avg"] = list()
out_data_dict["tot_co2_tot"] = list()
out_data_dict["tot_co2_avg"] = list()

out_soil_c_hist = dict()
out_tot_c_hist = dict()
out_tot_co2_hist = dict()

for protect_area_lyr in tqdm.tqdm(protect_area_lyrs):
    #print(protect_area_lyr)
    soil_c_stats_dir = os.path.join(out_xtr_path, protect_area_lyr, "soil_c_tile_stats_dec22")
    tot_c_stats_dir = os.path.join(out_xtr_path, protect_area_lyr, "total_c_tile_stats_dec22")
    tot_co2_stats_dir = os.path.join(out_xtr_path, protect_area_lyr, "total_co2_tile_stats_dec22")

    protect_area_tiles = tile_lut[protect_area_lyr]
    first = True
    soil_c_area_tot = 0.0
    soil_c_count = 0.0
    soil_c_tot = 0.0
    tot_c_area_tot = 0.0
    tot_c_count = 0.0
    tot_c_tot = 0.0
    tot_co2_area_tot = 0.0
    tot_co2_count = 0.0
    tot_co2_tot = 0.0

    for protect_area_tile in protect_area_tiles:
        #print(protect_area_tile)
        stats_soil_c_file = os.path.join(soil_c_stats_dir, "{}_soil_c.json".format(protect_area_tile))
        stats_tot_c_file = os.path.join(tot_c_stats_dir, "{}_total_c.json".format(protect_area_tile))
        stats_tot_co2_file = os.path.join(tot_co2_stats_dir, "{}_total_co2.json".format(protect_area_tile))

        stats_soil_c_dict = rsgislib.tools.utils.read_json_to_dict(stats_soil_c_file)
        stats_tot_c_dict = rsgislib.tools.utils.read_json_to_dict(stats_tot_c_file)
        stats_tot_co2_dict = rsgislib.tools.utils.read_json_to_dict(stats_tot_co2_file)

        if first:
            first = False
            WDPAID = int(protect_area_lyr.replace("WDPAID_", ""))
            soil_c_area_tot = float(stats_soil_c_dict["carbon_area"])
            soil_c_count = float(stats_soil_c_dict["count"])
            soil_c_tot = float(stats_soil_c_dict["carbon"])
            tot_c_area_tot = float(stats_tot_c_dict["carbon_area"])
            tot_c_count = float(stats_tot_c_dict["count"])
            tot_c_tot = float(stats_tot_c_dict["carbon"])
            tot_co2_area_tot = float(stats_tot_co2_dict["carbon_area"])
            tot_co2_count = float(stats_tot_co2_dict["count"])
            tot_co2_tot = float(stats_tot_co2_dict["carbon"])

            out_soil_c_hist[WDPAID] = numpy.array(stats_soil_c_dict["hist"], dtype=numpy.uint32)
            out_tot_c_hist[WDPAID] = numpy.array(stats_tot_c_dict["hist"], dtype=numpy.uint32)
            out_tot_co2_hist[WDPAID] = numpy.array(stats_tot_co2_dict["hist"], dtype=numpy.uint32)
        else:
            soil_c_area_tot = soil_c_area_tot + float(stats_soil_c_dict["carbon_area"])
            soil_c_count = soil_c_count + float(stats_soil_c_dict["count"])
            soil_c_tot = soil_c_tot + float(stats_soil_c_dict["carbon"])
            tot_c_area_tot = tot_c_area_tot + float(stats_tot_c_dict["carbon_area"])
            tot_c_count = tot_c_count + float(stats_tot_c_dict["count"])
            tot_c_tot = tot_c_tot + float(stats_tot_c_dict["carbon"])
            tot_co2_area_tot = tot_co2_area_tot + float(stats_tot_co2_dict["carbon_area"])
            tot_co2_count = tot_co2_count + float(stats_tot_co2_dict["count"])
            tot_co2_tot = tot_co2_tot + float(stats_tot_co2_dict["carbon"])

            out_soil_c_hist[WDPAID] = out_soil_c_hist[WDPAID] + numpy.array(stats_soil_c_dict["hist"], dtype=numpy.uint32)
            out_tot_c_hist[WDPAID] = out_tot_c_hist[WDPAID] + numpy.array(stats_tot_c_dict["hist"], dtype=numpy.uint32)
            out_tot_co2_hist[WDPAID] = out_tot_co2_hist[WDPAID] + numpy.array(stats_tot_co2_dict["hist"], dtype=numpy.uint32)

    soil_c_avg = 0.0
    if soil_c_count > 0:
        soil_c_avg = soil_c_tot / soil_c_count

    tot_c_avg = 0.0
    if tot_c_count > 0.0:
        tot_c_avg = tot_c_tot / tot_c_count

    tot_co2_avg = 0.0
    if tot_co2_count > 0.0:
        tot_co2_avg = tot_co2_tot / tot_co2_count

    out_data_dict["WDPAID"].append(WDPAID)
    out_data_dict["soil_c_tot"].append(soil_c_area_tot)
    out_data_dict["soil_c_avg"].append(soil_c_avg)
    out_data_dict["tot_c_tot"].append(tot_c_area_tot)
    out_data_dict["tot_c_avg"].append(tot_c_avg)
    out_data_dict["tot_co2_tot"].append(tot_co2_area_tot)
    out_data_dict["tot_co2_avg"].append(tot_co2_avg)

df_stats = pandas.DataFrame.from_dict(out_data_dict)
df_stats.to_feather("protected_carbon_summarised_base_stats.feather")
df_stats.to_csv("protected_carbon_summarised_base_stats.csv")
excel_sheet = 'prot_carbon'
xls_writer = pandas.ExcelWriter("protected_carbon_summarised_base_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
xls_writer.save()

rsgislib.tools.utils.write_dict_to_json(out_soil_c_hist, "protected_soil_c_hists.json")
rsgislib.tools.utils.write_dict_to_json(out_tot_c_hist, "protected_tot_c_hists.json")
rsgislib.tools.utils.write_dict_to_json(out_tot_co2_hist, "protected_tot_co2_hists.json")
