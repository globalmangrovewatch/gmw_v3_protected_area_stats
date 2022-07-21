import rsgislib.tools.utils
import pandas
import numpy

protected_agb_hists_file = 'protected_agb_hists.json'
protected_agb_hists_lut = rsgislib.tools.utils.read_json_to_dict(protected_agb_hists_file)

out_data = dict()
out_data['WDPAID'] = list()
out_data['0-50'] = list()
out_data['50-100'] = list()
out_data['100-150'] = list()
out_data['150-250'] = list()
out_data['250-1500'] = list()

for wdpaid in protected_agb_hists_lut:
    agb_arr = numpy.array(protected_agb_hists_lut[wdpaid], dtype=numpy.uint32)
    tot_agb_count = numpy.sum(agb_arr)
    if tot_agb_count > 0:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-50'].append(numpy.sum(agb_arr[0:2]) / tot_agb_count)
        out_data['50-100'].append(numpy.sum(agb_arr[2:4]) / tot_agb_count)
        out_data['100-150'].append(numpy.sum(agb_arr[4:6]) / tot_agb_count)
        out_data['150-250'].append(numpy.sum(agb_arr[6:10]) / tot_agb_count)
        out_data['250-1500'].append(numpy.sum(agb_arr[10:]) / tot_agb_count)
    else:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-50'].append(0.0)
        out_data['50-100'].append(0.0)
        out_data['100-150'].append(0.0)
        out_data['150-250'].append(0.0)
        out_data['250-1500'].append(0.0)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_agb_protect_area_bounds.csv")
df_stats.to_feather("gmw_v3_agb_protect_area_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_agb_protect_area_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()

