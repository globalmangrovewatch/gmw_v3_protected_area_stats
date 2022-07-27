import geopandas
import pandas

vec_file = "/Users/pete/Dropbox/University/Research/Projects/GlobalMangroveWatch/202207_ProtectedAreas/WDPA-July22-PA_DEF-STATUS-MANGROVE.gpkg"
vec_lyr = "WDPA-July22-PA_DEF-STATUS-MANGROVE-2"

wpda_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
wpda_gpdf = wpda_gpdf.set_index("WDPAID")

extent_stats_file = "../06_merge_extent_stats/protected_area_v3_corrected_ext_stats.feather"
agb_hgt_stats_file = "../09_merge_agb_hgt_stats/protected_agb_hgt_summarised_base_stats.feather"
carbon_stats_file = "../10_calc_carbon_stats/02_merge_tile_stats/protected_carbon_summarised_base_stats.feather"

extent_stats_df = pandas.read_feather(extent_stats_file)
agb_hgt_stats_df = pandas.read_feather(agb_hgt_stats_file)
carbon_stats_df = pandas.read_feather(carbon_stats_file)

wpda_gpdf_join = wpda_gpdf.join(extent_stats_df.set_index("WDPAID"), on="WDPAID")
wpda_gpdf_join = wpda_gpdf_join.join(agb_hgt_stats_df.set_index("WDPAID"), on="WDPAID")
wpda_gpdf_join = wpda_gpdf_join.join(carbon_stats_df.set_index("WDPAID"), on="WDPAID")

wpda_gpdf_join.to_file("WDPA_July22_PA_DEF_STATUS_MANGROVE_GMW_Stats.gpkg", layer="WDPA_July22_PA_DEF_STATUS_MANGROVE_GMW_Stats", driver="GPKG")

