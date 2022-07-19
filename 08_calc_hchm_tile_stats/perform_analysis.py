from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.tools.utils
import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)


def calc_unq_val_pxl_areas(vals_img, uid_img, unq_val_area_lut):
    img_vals_ds = gdal.Open(vals_img)
    if img_vals_ds is None:
        raise Exception("Could not open the values input image: '{}'".format(uid_img))
    img_vals_band = img_vals_ds.GetRasterBand(1)
    if img_vals_band is None:
        raise Exception("Failed to read the values image band: '{}'".format(uid_img))
    vals_arr = img_vals_band.ReadAsArray()
    img_vals_ds = None

    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image: '{}'".format(uid_img))
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band: '{}'".format(uid_img))
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    msk = numpy.zeros_like(uid_arr, dtype=bool)
    msk[(uid_arr == 1) & (uid_arr > 0) & (vals_arr > 0)] = True

    if numpy.sum(msk) > 0:
        unq_val_area_lut['count'] = numpy.sum(msk)
        unq_val_area_lut['hchm'] = numpy.sum(vals_arr[msk])

        vals_unq_val_arr = vals_arr[msk].flatten()
        vals_hist, bin_edges = numpy.histogram(vals_unq_val_arr, bins=71, range=(0, 71))
        unq_val_area_lut['hist'] = unq_val_area_lut['hist'] + vals_hist

class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        lut_vals = dict()
        lut_vals['count'] = 0
        lut_vals['hchm'] = 0.0
        lut_vals['hist'] = numpy.zeros((71), dtype=numpy.uint32)

        calc_unq_val_pxl_areas(self.params['hgt_img'], self.params['roi_img'], lut_vals)

        lut_vals['count'] = int(lut_vals['count'])
        lut_vals['hchm'] = float(lut_vals['hchm'])

        rsgislib.tools.utils.write_dict_to_json(lut_vals, self.params['out_file'])

    def required_fields(self, **kwargs):
        return ["hgt_img", "roi_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = "file"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()