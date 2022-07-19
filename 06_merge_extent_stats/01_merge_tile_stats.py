import os
import pprint
import tqdm

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

for protect_area_lyr in tqdm.tqdm(protect_area_lyrs):
    #print(protect_area_lyr)
    ext_stats_dir = os.path.join(out_path, protect_area_lyr, "extent_tile_stats")
    chng_ext_stats_dir = os.path.join(out_path, protect_area_lyr, "chng_extent_tile_stats")

    protect_area_tiles = tile_lut[protect_area_lyr]
    first = True
    WDPAID = -1
    area96 = 0.0
    gain_2007 = 0.0
    loss_2007 = 0.0
    gain_2008 = 0.0
    loss_2008 = 0.0
    gain_2009 = 0.0
    loss_2009 = 0.0
    gain_2010 = 0.0
    loss_2010 = 0.0
    gain_2015 = 0.0
    loss_2015 = 0.0
    gain_2016 = 0.0
    loss_2016 = 0.0
    gain_2017 = 0.0
    loss_2017 = 0.0
    gain_2018 = 0.0
    loss_2018 = 0.0
    gain_2019 = 0.0
    loss_2019 = 0.0
    gain_2020 = 0.0
    loss_2020 = 0.0
    for protect_area_tile in protect_area_tiles:
        #print(protect_area_tile)
        stats_96_ext_file = os.path.join(ext_stats_dir, "{}_extent.json".format(protect_area_tile))
        stats_chng_ext_file = os.path.join(chng_ext_stats_dir, "{}_chng_extent.json".format(protect_area_tile))

        stats_96_ext_dict = rsgislib.tools.utils.read_json_to_dict(stats_96_ext_file)
        stats_chng_ext_dict = rsgislib.tools.utils.read_json_to_dict(stats_chng_ext_file)

        #pprint.pprint(stats_96_ext_dict)
        #pprint.pprint(stats_chng_ext_dict)
        if first:
            first = False
            WDPAID = int(protect_area_lyr.replace("WDPAID_", ""))
            area96 = float(stats_96_ext_dict["area"])
            gain_2007 = float(stats_chng_ext_dict["2007"]["area"][0])
            loss_2007 = float(stats_chng_ext_dict["2007"]["area"][1])
            gain_2008 = float(stats_chng_ext_dict["2008"]["area"][0])
            loss_2008 = float(stats_chng_ext_dict["2008"]["area"][1])
            gain_2009 = float(stats_chng_ext_dict["2009"]["area"][0])
            loss_2009 = float(stats_chng_ext_dict["2009"]["area"][1])
            gain_2010 = float(stats_chng_ext_dict["2010"]["area"][0])
            loss_2010 = float(stats_chng_ext_dict["2010"]["area"][1])
            gain_2015 = float(stats_chng_ext_dict["2015"]["area"][0])
            loss_2015 = float(stats_chng_ext_dict["2015"]["area"][1])
            gain_2016 = float(stats_chng_ext_dict["2016"]["area"][0])
            loss_2016 = float(stats_chng_ext_dict["2016"]["area"][1])
            gain_2017 = float(stats_chng_ext_dict["2017"]["area"][0])
            loss_2017 = float(stats_chng_ext_dict["2017"]["area"][1])
            gain_2018 = float(stats_chng_ext_dict["2018"]["area"][0])
            loss_2018 = float(stats_chng_ext_dict["2018"]["area"][1])
            gain_2019 = float(stats_chng_ext_dict["2019"]["area"][0])
            loss_2019 = float(stats_chng_ext_dict["2019"]["area"][1])
            gain_2020 = float(stats_chng_ext_dict["2020"]["area"][0])
            loss_2020 = float(stats_chng_ext_dict["2020"]["area"][1])
        else:
            area96 = area96 + float(stats_96_ext_dict["area"])
            gain_2007 = gain_2007 + float(stats_chng_ext_dict["2007"]["area"][0])
            loss_2007 = loss_2007 + float(stats_chng_ext_dict["2007"]["area"][1])
            gain_2008 = gain_2008 + float(stats_chng_ext_dict["2008"]["area"][0])
            loss_2008 = loss_2008 + float(stats_chng_ext_dict["2008"]["area"][1])
            gain_2009 = gain_2009 + float(stats_chng_ext_dict["2009"]["area"][0])
            loss_2009 = loss_2009 + float(stats_chng_ext_dict["2009"]["area"][1])
            gain_2010 = gain_2010 + float(stats_chng_ext_dict["2010"]["area"][0])
            loss_2010 = loss_2010 + float(stats_chng_ext_dict["2010"]["area"][1])
            gain_2015 = gain_2015 + float(stats_chng_ext_dict["2015"]["area"][0])
            loss_2015 = loss_2015 + float(stats_chng_ext_dict["2015"]["area"][1])
            gain_2016 = gain_2016 + float(stats_chng_ext_dict["2016"]["area"][0])
            loss_2016 = loss_2016 + float(stats_chng_ext_dict["2016"]["area"][1])
            gain_2017 = gain_2017 + float(stats_chng_ext_dict["2017"]["area"][0])
            loss_2017 = loss_2017 + float(stats_chng_ext_dict["2017"]["area"][1])
            gain_2018 = gain_2018 + float(stats_chng_ext_dict["2018"]["area"][0])
            loss_2018 = loss_2018 + float(stats_chng_ext_dict["2018"]["area"][1])
            gain_2019 = gain_2019 + float(stats_chng_ext_dict["2019"]["area"][0])
            loss_2019 = loss_2019 + float(stats_chng_ext_dict["2019"]["area"][1])
            gain_2020 = gain_2020 + float(stats_chng_ext_dict["2020"]["area"][0])
            loss_2020 = loss_2020 + float(stats_chng_ext_dict["2020"]["area"][1])

    out_data_dict["WDPAID"].append(WDPAID)
    out_data_dict["1996_ext"].append(area96)
    out_data_dict["gain_2007"].append(gain_2007)
    out_data_dict["loss_2007"].append(loss_2007)
    out_data_dict["gain_2008"].append(gain_2008)
    out_data_dict["loss_2008"].append(loss_2008)
    out_data_dict["gain_2009"].append(gain_2009)
    out_data_dict["loss_2009"].append(loss_2009)
    out_data_dict["gain_2010"].append(gain_2010)
    out_data_dict["loss_2010"].append(loss_2010)
    out_data_dict["gain_2015"].append(gain_2015)
    out_data_dict["loss_2015"].append(loss_2015)
    out_data_dict["gain_2016"].append(gain_2016)
    out_data_dict["loss_2016"].append(loss_2016)
    out_data_dict["gain_2017"].append(gain_2017)
    out_data_dict["loss_2017"].append(loss_2017)
    out_data_dict["gain_2018"].append(gain_2018)
    out_data_dict["loss_2018"].append(loss_2018)
    out_data_dict["gain_2019"].append(gain_2019)
    out_data_dict["loss_2019"].append(loss_2019)
    out_data_dict["gain_2020"].append(gain_2020)
    out_data_dict["loss_2020"].append(loss_2020)

df_stats = pandas.DataFrame.from_dict(out_data_dict)
df_stats.to_feather("protected_area_summarised_base_stats.feather")
df_stats.to_csv("protected_area_summarised_base_stats.csv")
excel_sheet = 'prot_area_ext'
xls_writer = pandas.ExcelWriter("protected_area_summarised_base_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
xls_writer.save()