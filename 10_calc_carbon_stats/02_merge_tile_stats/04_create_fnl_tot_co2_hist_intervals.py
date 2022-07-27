import rsgislib.tools.utils
import pandas
import numpy

protected_agb_hists_file = 'protected_tot_co2_hists.json'
protected_agb_hists_lut = rsgislib.tools.utils.read_json_to_dict(protected_agb_hists_file)

out_data = dict()
out_data['WDPAID'] = list()
out_data['0-700'] = list()
out_data['700-1400'] = list()
out_data['1400-2100'] = list()
out_data['2100-2800'] = list()
out_data['2800-3500'] = list()
out_data['3500-'] = list()

for wdpaid in protected_agb_hists_lut:
    agb_arr = numpy.array(protected_agb_hists_lut[wdpaid], dtype=numpy.uint32)
    tot_agb_count = numpy.sum(agb_arr)
    if tot_agb_count > 0:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-700'].append(numpy.sum(agb_arr[0:28]) / tot_agb_count)
        out_data['700-1400'].append(numpy.sum(agb_arr[28:56]) / tot_agb_count)
        out_data['1400-2100'].append(numpy.sum(agb_arr[56:84]) / tot_agb_count)
        out_data['2100-2800'].append(numpy.sum(agb_arr[84:112]) / tot_agb_count)
        out_data['2800-3500'].append(numpy.sum(agb_arr[112:140]) / tot_agb_count)
        out_data['3500-'].append(numpy.sum(agb_arr[140:]) / tot_agb_count)
    else:
        out_data['WDPAID'].append(wdpaid)
        out_data['0-700'].append(0.0)
        out_data['700-1400'].append(0.0)
        out_data['1400-2100'].append(0.0)
        out_data['2100-2800'].append(0.0)
        out_data['2800-3500'].append(0.0)
        out_data['3500-'].append(0.0)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_tot_co2_protect_area_bounds.csv")
df_stats.to_feather("gmw_v3_tot_co2_protect_area_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_tot_co2_protect_area_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='tot_co2_hists')
xlsx_writer.save()

