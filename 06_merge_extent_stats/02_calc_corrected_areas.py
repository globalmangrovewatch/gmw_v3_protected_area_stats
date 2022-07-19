import pandas

extent_file = "protected_area_summarised_base_stats.feather"

extent_stats_df = pandas.read_feather(extent_file)

gain_cols = ["gain_2007", "gain_2008", "gain_2009", "gain_2010", "gain_2015", "gain_2016", "gain_2017", "gain_2018", "gain_2019", "gain_2020"]
loss_cols = ["loss_2007", "loss_2008", "loss_2009", "loss_2010", "loss_2015", "loss_2016", "loss_2017", "loss_2018", "loss_2019", "loss_2020"]

# Mangrove area correction factor
mng_om = (100-85.63061873343034)/100
mng_com = (100 - 89.28977298408603)/100
print(f"mng_om = {mng_om}")
print(f"mng_com = {mng_com}")

# Mangrove loss correction factor
loss_om = (100-73.77949765590216)/100
loss_com = (100-51.42118863049095)/100
print(f"loss_om = {loss_om}")
print(f"loss_com = {loss_com}")

# Mangrove gain correction factor
gain_om = (100-69.97109826589596)/100
gain_com = (100-50.0)/100
print(f"gain_om = {gain_om}")
print(f"gain_com = {gain_com}")


extent_corr_stats_df = extent_stats_df.copy()

# Apply gain correction factor
extent_corr_stats_df[gain_cols] = extent_corr_stats_df[gain_cols] + (extent_corr_stats_df[gain_cols] * gain_om) - (extent_corr_stats_df[gain_cols] * gain_com)

# Apply loss correction factor
extent_corr_stats_df[loss_cols] = extent_corr_stats_df[loss_cols] + (extent_corr_stats_df[loss_cols] * loss_om) - (extent_corr_stats_df[loss_cols] * loss_com)

gmw_chng_years = [2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]
for chng_year in gmw_chng_years:
    extent_corr_stats_df[f"{chng_year}_ext"] = extent_corr_stats_df["1996_ext"] - extent_corr_stats_df[f"loss_{chng_year}"] + extent_corr_stats_df[f"gain_{chng_year}"]

extent_corr_stats_df.to_csv("protected_area_v3_corrected_ext_chng_stats.csv")
extent_corr_stats_df.to_feather("protected_area_v3_corrected_ext_chng_stats.feather")
extent_corr_stats_df.to_excel("protected_area_v3_corrected_ext_chng_stats.xlsx")

extent_corr_stats_df = extent_corr_stats_df.drop(columns=gain_cols)
extent_corr_stats_df = extent_corr_stats_df.drop(columns=loss_cols)

extent_corr_stats_df.to_csv("protected_area_v3_corrected_ext_stats.csv")
extent_corr_stats_df.to_feather("protected_area_v3_corrected_ext_stats.feather")
extent_corr_stats_df.to_excel("protected_area_v3_corrected_ext_stats.xlsx")
