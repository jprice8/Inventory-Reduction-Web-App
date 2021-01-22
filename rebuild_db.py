import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import datetime as dt

from sec_vars import DB_PW, DB_OWNER

# create sql engine variables
source_engine = create_engine(f"postgresql://{DB_OWNER}:{DB_PW}@localhost:5432/turnoverdash")
target_engine = create_engine(f"postgresql://{DB_OWNER}:{DB_PW}@localhost:5432/reductionapp")

# read in invcounts table and drop non-imms
invcounts_source = pd.read_sql_table('invcounts', source_engine)
invcounts_source = invcounts_source.dropna(subset=["imms"])

# clean uoms to have them standardized:
# 1. strip out numbers, blank spaces and slashes from uom
# 2. upper case all uoms
invcounts_source.uom = invcounts_source.uom.replace(r'\d', '', regex=True)
invcounts_source.uom = invcounts_source.uom.str.strip('/ ')
invcounts_source.uom = invcounts_source.uom.str.upper()
invcounts_source.uom = invcounts_source.uom.replace('', np.nan)
invcounts_source = invcounts_source.dropna(subset=["uom"])

# Issue data upload
###############################################################################
# source data
issue_source = pd.read_sql_table('issue_detail_full', source_engine)
issue_source = issue_source.rename(columns={'facility_number': 'fac'})
bk_joe = invcounts_source.groupby(['fac', 'period', 'imms', 'uom']).agg({'qty': ['sum']})

# pivot quantity out on facility, period, and imms #
piv = pd.pivot_table(invcounts_source, values='qty', index=['fac', 'period', 'imms', 'uom'],
    aggfunc=np.sum)

# reset the index
piv.reset_index(level=piv.index.names, inplace=True)

# filter the pivot down to the most recent counts
most_recent = piv.period.sort_values(ascending=False).reset_index(drop=True)
most_recent_count=piv[piv['period']==most_recent[0]].reset_index(drop=True)

# now we have the most recent counts.
# Let us now try to apply a function to each row that will agg issues.
# or use numpy where to sum

# filter issues for 2020 only
issues2020 = issue_source[issue_source['issue_date'].dt.year == 2020]

# group the issues dataframe by imms and facility and sum the qty 
i2020 = issues2020.groupby(['fac', 'imms', 'uom'], as_index=False)['qty'].sum()

# merge grouped issues on grouped counts
invcount_nov_issues = most_recent_count.merge(i2020, how="left", on=["fac", "imms", "uom"])

# rename similar columns
invcount_nov_issues = invcount_nov_issues.rename(columns={'qty_x': 'count_qty', 
    'qty_y': 'issue_qty'})


# PO upload
###############################################################################
po_source = pd.read_sql_table('po_detail', source_engine)

# filter pos for 2020 only
po2020 = po_source[po_source['poDate'].dt.year == 2020]

# create new column for po qty in luom using given coversion factor
po2020['luom_po_qty'] = po2020['poQty'] * po2020['poUOM_mult']

# group the issues dataframe by imms and facility and sum the qty 
p2020 = po2020.groupby(['fac', 'imms', 'poUOM'], as_index=False)['luom_po_qty'].sum()

# rename poUOM to uom in order to join tables
p2020 = p2020.rename(columns={'poUOM': 'uom'})

# merge grouped issues on grouped counts
invcount_joined = invcount_nov_issues.merge(p2020, how="left", on=["fac", "imms", "uom"])
invcount_joined = invcount_joined.fillna(0)

invcount_joined.count_qty = invcount_joined.count_qty.astype('int')
invcount_joined.luom_po_qty = invcount_joined.luom_po_qty.astype('int')
invcount_joined.issue_qty = invcount_joined.issue_qty.astype('int')

# Merge back descriptive fields for inventory  
###############################################################################
# going to use the item master to populate descriptive information to joined table

# load in item master
itemmaster = pd.read_sql_table('item_master', source_engine)

# only need the first 40 columns
items = itemmaster.iloc[:, :40]
items = items.rename(columns={'MMISItemNo': 'imms', 'TenetFacilityNo': 'fac'})

# calculate weighted average cost for each item
items['wt_avg_cost'] = items['DefaultUOMPrice'] / items['DefaultUOMConv']

# Clean up the item master fields
cleaned_items = items[['fac', 'TenetFacilityName', 'imms', 'Mfr', 'MfrCat', 'ItemDesc', 
                       'MMISItemCreateDate', 'Vend', 'VendCat', 'DefaultUOM', 'DefaultUOMConv', 
                       'DefaultUOMPrice', 'UOM1', 'CONV1', 'wt_avg_cost']]

cleaned_items = cleaned_items.rename(columns={'TenetFacilityName': 'facility_name', 
    'Mfr': 'mfr', 'MfrCat': 'mfr_cat_no', 'ItemDesc': 'description', 
    'MMISItemCreateDate': 'imms_create_date', 'Vend': 'vendor', 
    'VendCat': 'vend_cat_no', 'DefaultUOM': 'uom',
    'DefaultUOMConv': 'uom_conv', 'DefaultUOMPrice': 'uom_price', 
    'UOM1': 'luom', 'CONV1': 'luom_no_of_units'})

cleaned_items.fac = cleaned_items.fac.astype('str')
cleaned_items.imms = cleaned_items.imms.astype('str')

invcount_joined.fac = invcount_joined.fac.astype('str')
invcount_joined.imms = invcount_joined.imms.astype('str')

cleaned_items.fac = cleaned_items.fac.str.strip()
cleaned_items.imms = cleaned_items.imms.str.strip()

invcount_joined.fac = invcount_joined.fac.str.strip()
invcount_joined.imms = invcount_joined.imms.str.strip()

# some facilities showing duplicate imms # based off of different UOMs...
# to normalize, I will sort for lowest default uom then
# remove items with duplicate imms no's.
cleaned_items = cleaned_items.sort_values(by='luom_price', ascending=True, ignore_index=True)

# need to pull out items for each facility individually and remove duplicate imms #'s
# then concat them back together before merging
bmc = cleaned_items[cleaned_items['fac'] == '939']
mtb = cleaned_items[cleaned_items['fac'] == '971']
slb = cleaned_items[cleaned_items['fac'] == '952']
nbh = cleaned_items[cleaned_items['fac'] == '968']
rhh = cleaned_items[cleaned_items['fac'] == '872']
ncb = cleaned_items[cleaned_items['fac'] == '954']

bmc = bmc.drop_duplicates(subset=['imms'], keep='first')
mtb = mtb.drop_duplicates(subset=['imms'], keep='first')
slb = slb.drop_duplicates(subset=['imms'], keep='first')
nbh = nbh.drop_duplicates(subset=['imms'], keep='first')
rhh = rhh.drop_duplicates(subset=['imms'], keep='first')
ncb = ncb.drop_duplicates(subset=['imms'], keep='first')

new_items = pd.concat([bmc, mtb, slb, nbh, rhh, ncb], ignore_index=True)

# merge new items with joined counts
final = invcount_joined.merge(new_items, how="left", on=['fac', 'imms', 'uom'])

#drop items that item master could not pick up
final = final.dropna().reset_index(drop=True)

# change UOM conv's to integers
final.uom_conv = final.uom_conv.astype('int')
final.luom_no_of_units = final.luom_no_of_units.astype('int')

# calculate ext cost column
final['ext_cost'] = final['count_qty'] * final['wt_avg_cost']
# add default measures
final['reduction_qty'] = 0
final['isTarget'] = False

# upload count usage table to database
final.to_sql(
    name="target_countusagelist",
    con=target_engine,
    if_exists="append",
    index="id",
)