from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os

import rsgislib.tools.filetools
import rsgislib.tools.utils
import rsgislib.vectorutils

logger = logging.getLogger(__name__)


class GenTaskCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs["out_path"]):
            os.mkdir(kwargs["out_path"])

        protect_area_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(
            kwargs["vec_protect_areas_file"]
        )
        tile_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["tile_lut_file"])

        for protect_area_lyr in protect_area_lyrs:
            protect_area_tiles = tile_lut[protect_area_lyr]
            out_protect_dir = os.path.join(kwargs["out_path"], protect_area_lyr)
            if not os.path.exists(out_protect_dir):
                os.mkdir(out_protect_dir)

            roi_dir = os.path.join(out_protect_dir, "extent")
            if not os.path.exists(roi_dir):
                os.mkdir(roi_dir)

            out_dir = os.path.join(out_protect_dir, "agb_tile_stats")
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)

            for protect_area_tile in protect_area_tiles:
                agb_img_file = rsgislib.tools.filetools.find_file_none(
                    kwargs["agb_img_dir"], f"*{protect_area_tile}*.tif"
                )
                if agb_img_file is None:
                    raise Exception("No AGB Image file: {}".format(protect_area_tile))

                pxl_area_img_file = rsgislib.tools.filetools.find_file_none(
                    kwargs["pxl_area_dir"], f"*{protect_area_tile}*.kea"
                    )
                if pxl_area_img_file is None:
                    raise Exception("No reference file: {}".format(protect_area_tile))

                roi_img = os.path.join(
                    roi_dir, "{}_protect_area_extent.kea".format(protect_area_tile)
                    )

                out_file = os.path.join(
                    out_dir, "{}_agb.json".format(protect_area_tile)
                )
                if not os.path.exists(out_file):
                    c_dict = dict()
                    c_dict["agb_img"] = agb_img_file
                    c_dict["pxl_area"] = pxl_area_img_file
                    c_dict["roi_img"] = roi_img
                    c_dict["out_file"] = out_file
                    self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            vec_protect_areas_file="/home/pete/Documents/gmw_protected_areas/data/protected_areas/WDPA-July22-PA_DEF-STATUS-MANGROVE_ind_sites.gpkg",
            tile_lut_file="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_tiles_lut.json",
            agb_img_dir="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_agb_hchm/agb_mng_mjr_2020_tif",
            pxl_area_dir="/home/pete/Documents/gmw_protected_areas/data/gmw_srtm_agb_hchm/pxl_areas",
            out_path="/home/pete/Documents/gmw_protected_areas/data/gmw_ext_protect_areas",
        )

        self.pop_params_db()
        self.create_shell_exe(
            run_script="run_exe_analysis.sh",
            cmds_sh_file="cmds_lst.sh",
            n_cores=50,
            db_info_file="pbpt_db_conn_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = "python {}".format(py_script)

    process_tools_mod = "perform_analysis"
    process_tools_cls = "PerformAnalysis"

    create_tools = GenTaskCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./gmw_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
