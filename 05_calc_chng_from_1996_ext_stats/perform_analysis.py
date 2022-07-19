from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.tools.utils
import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)


def calc_unq_val_pxl_areas(pix_area_img, uid_img, gmw_img, unq_val_area_lut):
    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image: '{}'".format(uid_img))
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band: '{}'".format(uid_img))
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    img_pixarea_ds = gdal.Open(pix_area_img)
    if img_pixarea_ds is None:
        raise Exception("Could not open the pixel area input image: '{}'".format(pix_area_img))
    img_pixarea_band = img_pixarea_ds.GetRasterBand(1)
    if img_pixarea_band is None:
        raise Exception("Failed to read the pixel area image band: '{}'".format(pix_area_img))
    pxl_area_arr = img_pixarea_band.ReadAsArray()
    img_pixarea_ds = None

    img_gmw_ds = gdal.Open(gmw_img)
    if img_gmw_ds is None:
        raise Exception("Could not open the GMW input image: '{}'".format(gmw_img))
    img_gmw_band = img_gmw_ds.GetRasterBand(1)
    if img_gmw_band is None:
        raise Exception("Failed to read the GMW image band: '{}'".format(gmw_img))
    gmw_arr = img_gmw_band.ReadAsArray()
    img_gmw_ds = None

    msk_1 = numpy.zeros_like(uid_arr, dtype=bool)
    msk_1[(uid_arr == 1) & (uid_arr > 0) & (gmw_arr == 1)] = True

    msk_2 = numpy.zeros_like(uid_arr, dtype=bool)
    msk_2[(uid_arr == 1) & (uid_arr > 0) & (gmw_arr == 2)] = True

    unq_val_area_lut['count'] = [numpy.sum(msk_1), numpy.sum(msk_2)]
    unq_val_area_lut['area'] = [numpy.sum(pxl_area_arr[msk_1]), numpy.sum(pxl_area_arr[msk_2])]



class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        lut_vals = dict()
        for chng_year in self.params['chng_ext_imgs']:
            lut_vals[chng_year] = dict()
            lut_vals[chng_year]['count'] = 0
            lut_vals[chng_year]['area'] = [0.0, 0.0]

            calc_unq_val_pxl_areas(self.params['pxl_area'], self.params['roi_img'], self.params['chng_ext_imgs'][chng_year], lut_vals[chng_year])

            lut_vals[chng_year]['count'] = [int(lut_vals[chng_year]['count'][0]), int(lut_vals[chng_year]['count'][1])]
            lut_vals[chng_year]['area'] = [float(lut_vals[chng_year]['area'][0]), float(lut_vals[chng_year]['area'][1])]

        rsgislib.tools.utils.write_dict_to_json(lut_vals, self.params['out_file'])

    def required_fields(self, **kwargs):
        return ["chng_ext_imgs", "pxl_area", "roi_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = "file"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
