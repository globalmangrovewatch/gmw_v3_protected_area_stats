import rsgislib.imageutils.imagelut
import glob

vec_lut_file = "/home/pete/Documents/gmw_protected_areas/data/gmw_protect_areas_imgs_lut.gpkg"

input_imgs = glob.glob("/home/pete/Documents/gmw_protected_areas/data/gmw_extents/gmw_v3_1996/*.tif")
rsgislib.imageutils.imagelut.create_img_extent_lut(input_imgs, vec_file=vec_lut_file, vec_lyr="gmw_ext_1996", out_format="GPKG", ignore_none_imgs = False, out_proj_wgs84 = False, overwrite_lut_file = False)

input_imgs = glob.glob("/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_agb_hchm/agb_mng_mjr_2020_tif/*.tif")
rsgislib.imageutils.imagelut.create_img_extent_lut(input_imgs, vec_file=vec_lut_file, vec_lyr="gmw_agb_2020", out_format="GPKG", ignore_none_imgs = False, out_proj_wgs84 = False, overwrite_lut_file = False)


