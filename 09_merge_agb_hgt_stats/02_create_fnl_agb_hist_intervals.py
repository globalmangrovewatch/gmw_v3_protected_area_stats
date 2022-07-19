import rsgislib.tools.utils
import pandas
import numpy

protected_agb_hists_file = 'protected_agb_hists.json'
protected_agb_hists_lut = rsgislib.tools.utils.read_json_to_dict(protected_agb_hists_file)

out_data = dict()
out_data['WDPAID'] = list()
out_data['0-250'] = list()
out_data['250-500'] = list()
out_data['500-750'] = list()
out_data['750-1000'] = list()
out_data['1000-'] = list()

for wdpaid in protected_agb_hists_lut:
    agb_arr = numpy.array(protected_agb_hists_lut[wdpaid], dtype=numpy.uint32)
    tot_agb_count = numpy.sum(agb_arr)
    if tot_agb_count > 0:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-250'].append(numpy.sum(agb_arr[0:10])/tot_agb_count)
        out_data['250-500'].append(numpy.sum(agb_arr[10:20])/tot_agb_count)
        out_data['500-750'].append(numpy.sum(agb_arr[20:30])/tot_agb_count)
        out_data['750-1000'].append(numpy.sum(agb_arr[30:40])/tot_agb_count)
        out_data['1000-'].append(numpy.sum(agb_arr[40:])/tot_agb_count)
    else:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-250'].append(0.0)
        out_data['250-500'].append(0.0)
        out_data['500-750'].append(0.0)
        out_data['750-1000'].append(0.0)
        out_data['1000-'].append(0.0)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_agb_protect_area_bounds.csv")
df_stats.to_feather("gmw_v3_agb_protect_area_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_agb_protect_area_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()

