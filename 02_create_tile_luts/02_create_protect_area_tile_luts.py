import rsgislib.vectorutils
import rsgislib.imageutils.imagelut
import rsgislib.tools.filetools
import rsgislib.tools.utils

img_lut_file = "/home/pete/Documents/gmw_protected_areas/data/gmw_protect_areas_imgs_lut.gpkg"

vec_file = "/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg"
vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_file)

gmw_ext_lut = dict()
gmw_srtm_lut = dict()

for vec_lyr in vec_lyrs:
    vec_bbox = rsgislib.vectorutils.get_vec_layer_extent(vec_file, vec_lyr)

    gmw_ext_imgs = rsgislib.imageutils.imagelut.query_img_lut(vec_bbox, img_lut_file, lyr_name="gmw_ext_1996")
    if len(gmw_ext_imgs) > 0:
        gmw_ext_lut[vec_lyr] = list()
        for img in gmw_ext_imgs:
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile = basename.split("_")[1]
            gmw_ext_lut[vec_lyr].append(tile)


    gmw_srtm_imgs = rsgislib.imageutils.imagelut.query_img_lut(vec_bbox, img_lut_file, lyr_name="gmw_agb_2020")
    if len(gmw_srtm_imgs) > 0:
        gmw_srtm_lut[vec_lyr] = list()
        for img in gmw_srtm_imgs:
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile = basename.split("_")[0]
            gmw_srtm_lut[vec_lyr].append(tile)

rsgislib.tools.utils.write_dict_to_json(gmw_ext_lut, "/home/pete/Documents/gmw_protected_areas/data/gmw_ext_tiles_lut.json")
rsgislib.tools.utils.write_dict_to_json(gmw_srtm_lut, "/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_tiles_lut.json")

print("There are {} features in extent LUT but {} protected areas.".format(len(gmw_ext_lut), len(vec_lyrs)))
print("There are {} features in srtm LUT but {} protected areas.".format(len(gmw_srtm_lut), len(vec_lyrs)))
