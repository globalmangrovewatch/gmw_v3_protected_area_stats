import rsgislib.tools.utils
import pandas
import numpy

protected_hchm_hists_file = 'protected_hchm_hists.json'
protected_hchm_hists_lut = rsgislib.tools.utils.read_json_to_dict(protected_hchm_hists_file)

out_data = dict()
out_data['WDPAID'] = list()
out_data['0-5'] = list()
out_data['5-10'] = list()
out_data['10-15'] = list()
out_data['15-20'] = list()
out_data['20-65'] = list()

for wdpaid in protected_hchm_hists_lut:
    hgt_arr = numpy.array(protected_hchm_hists_lut[wdpaid], dtype=numpy.uint32)
    tot_hgt_count = numpy.sum(hgt_arr)
    if tot_hgt_count > 0:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-5'].append(numpy.sum(hgt_arr[0:5]) / tot_hgt_count)
        out_data['5-10'].append(numpy.sum(hgt_arr[5:10]) / tot_hgt_count)
        out_data['10-15'].append(numpy.sum(hgt_arr[10:15]) / tot_hgt_count)
        out_data['15-20'].append(numpy.sum(hgt_arr[15:20]) / tot_hgt_count)
        out_data['20-65'].append(numpy.sum(hgt_arr[20:]) / tot_hgt_count)
    else:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-5'].append(0.0)
        out_data['5-10'].append(0.0)
        out_data['10-15'].append(0.0)
        out_data['15-20'].append(0.0)
        out_data['20-65'].append(0.0)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_hgt_protect_area_bounds.csv")
df_stats.to_feather("gmw_v3_hgt_protect_area_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_hgt_protect_area_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_hgt_stats')
xlsx_writer.save()

