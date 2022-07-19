import geopandas
import tqdm

## Stop FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version.
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


vec_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE.gpkg"
vec_lyr = "WDPA-July22-PA_DEF-STATUS-MANGROVE-2"

base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
unq_vals = base_gpdf["WDPAID"].unique()
print(unq_vals.shape)

out_vec_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"

for uiq_area in tqdm.tqdm(unq_vals):
    uiq_gpdf = base_gpdf[base_gpdf["WDPAID"] == uiq_area]
    uid_lyr = "WDPAID_{}".format(int(uiq_area))
    uiq_gpdf.to_file(out_vec_file, layer=uid_lyr, driver="GPKG")
