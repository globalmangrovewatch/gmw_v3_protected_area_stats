import rsgislib.tools.utils
import pandas
import numpy

protected_hchm_hists_file = 'protected_hchm_hists.json'
protected_hchm_hists_lut = rsgislib.tools.utils.read_json_to_dict(protected_hchm_hists_file)

out_data = dict()
out_data['WDPAID'] = list()
out_data['0-13'] = list()
out_data['13-26'] = list()
out_data['26-39'] = list()
out_data['39-52'] = list()
out_data['52-'] = list()

for wdpaid in protected_hchm_hists_lut:
    hgt_arr = numpy.array(protected_hchm_hists_lut[wdpaid], dtype=numpy.uint32)
    tot_hgt_count = numpy.sum(hgt_arr)
    if tot_hgt_count > 0:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-13'].append(numpy.sum(hgt_arr[0:13]) / tot_hgt_count)
        out_data['13-26'].append(numpy.sum(hgt_arr[13:26]) / tot_hgt_count)
        out_data['26-39'].append(numpy.sum(hgt_arr[26:39]) / tot_hgt_count)
        out_data['39-52'].append(numpy.sum(hgt_arr[39:52]) / tot_hgt_count)
        out_data['52-'].append(numpy.sum(hgt_arr[52:]) / tot_hgt_count)
    else:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-13'].append(0.0)
        out_data['13-26'].append(0.0)
        out_data['26-39'].append(0.0)
        out_data['39-52'].append(0.0)
        out_data['52-'].append(0.0)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_hgt_protect_area_bounds.csv")
df_stats.to_feather("gmw_v3_hgt_protect_area_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_hgt_protect_area_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_hgt_stats')
xlsx_writer.save()

