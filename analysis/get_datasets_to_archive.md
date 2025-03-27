```python
from datetime import datetime

import jupyter_black
import pandas as pd

jupyter_black.load()
```


```python
# URL of dataset CSV. Be sure to regenerate for the
# current year before running.
DATASET_INFO_CSV = (
    "https://raw.githubusercontent.com/OCHA-DAP/"
    + "hdx-analysis-scripts/gh-pages/datasets_info/datasets.csv"
)
# We only want to consider datasets 5 years or older
# e.g. In January 2022, we archived datasets created
# before 31 December 2016. UPPER_BOUND_YEAR should
# be used with an exclusive < (i.e. dataset years < UPPER_BOUND_YEAR)
UPPER_BOUND_YEAR = datetime.today().year - 5
# Max number of downloads in the past 5 years
MAX_DOWNLOADS = 1_000
# List of orgs whose datasets are excluded from archiving. This list is provided by DPT. This uses org display names because that is what is in the source CSV, but a more reliable approach would be to use org IDs
# Exclusion of orgs is now disabled.
# EXCLUDED_ORGS = [
#     "OurAirports",
#     "HDX",
#     "Central Emergency Response Fund",
#     "OCHA Financial Tracking System (FTS)",
#     "INFORM",
#     "Humanitarian Exchange Language (#HXL)",
#     "ReliefWeb",
# ]

# Some reporting stats:
dsets_initial = 0
dsets_publicNoArchiveNotRequestable = 0
dsets_notOngoing = 0
dsets_createYear = 0
dsets_refEndYear = 0
dsets_lt1000Dl = 0
dsets_notCOD = 0
```


```python
UPPER_BOUND_YEAR
```




    2020




```python
# Takes awhile to read in because it's a large file
df = pd.read_csv(DATASET_INFO_CSV)
```


```python
# The number of rows
df.shape[0]

dsets_initial = len(df)
```


```python
# Let's look at the column names
df.columns
```




    Index(['name', 'title', 'id', 'downloads last 5 years', 'date created',
           'date metadata updated', 'date data updated', 'updated last 3 months',
           'updated previous quarter', 'reference period start',
           'reference period end', 'update frequency', 'last modified fresh',
           'end date up to date', 'organisation', 'data link', 'data type', 'url',
           'is cod', 'tags', 'public', 'requestable', 'archived',
           'updated by cod script', 'formerly updated by cod script',
           'updated by non-cod script', 'date updated by script',
           'updated_by_script<<last_modified', 'last_modified<<updated_by_script'],
          dtype='object')




```python
# We want datasets that are public and not archived and not requestable
df_publicnoarchive = df.loc[
    (df["public"] == "Y") & (df["archived"] == "N") & (df["requestable"] == "N")
]
df_publicnoarchive.shape[0]

dsets_publicNoArchiveNotRequestable = len(df_publicnoarchive)
```


```python
# Drop datasets that belong to one of the excluded orgs
# df_publicnoarchive = df_publicnoarchive.loc[
#     ~df_publicnoarchive["organisation"].isin(EXCLUDED_ORGS)
# ]
# df_publicnoarchive.shape[0]
```


```python
# We only want to consider datasets that were created more than 5 years ago and
# whose reference period end is more than 5 years ago, but first we have to get
# rid of anything where reference period end = "ongoing"
df_publicnoarchive = df_publicnoarchive.loc[
    (df_publicnoarchive["reference period end"] != "ongoing")
]

df_publicnoarchive.shape[0]

dsets_notOngoing = len(df_publicnoarchive)
```


```python
df_publicnoarchive_5yo = df_publicnoarchive.loc[
    (pd.to_datetime(df_publicnoarchive["date created"]).dt.year < UPPER_BOUND_YEAR)
]
df_publicnoarchive_5yo.shape[0]

dsets_createYear = len(df_publicnoarchive_5yo)
```


```python
# Confirm maximum creation date is < UPPER_BOUND_YEAR
df_publicnoarchive_5yo["date created"].max()
```




    '2019-12-27T14:50:35.529853'




```python
df_publicnoarchive_5yo = df_publicnoarchive_5yo.loc[
    (
        pd.to_datetime(df_publicnoarchive["reference period end"]).dt.year
        < UPPER_BOUND_YEAR
    )
]
df_publicnoarchive_5yo.shape[0]

dsets_refEndYear = len(df_publicnoarchive_5yo)
```


```python
# Confirm maximum ref period end date is < UPPER_BOUND_YEAR
df_publicnoarchive_5yo["reference period end"].max()
```




    '2019-12-31T23:59:59+00:00'




```python
# Datasets must have < 1000 download counts
df_publicnoarchive_5yo_lt1000dl = df_publicnoarchive_5yo.loc[
    df_publicnoarchive_5yo["downloads last 5 years"] < MAX_DOWNLOADS
]
df_publicnoarchive_5yo_lt1000dl.shape[0]

dsets_lt1000Dl = len(df_publicnoarchive_5yo_lt1000dl)
```


```python
# Datasets must not be CODs
df_publicnoarchive_5yo_lt1000dl_notcod = df_publicnoarchive_5yo_lt1000dl.loc[
    df_publicnoarchive_5yo_lt1000dl["is cod"] == "N"
]
df_publicnoarchive_5yo_lt1000dl_notcod.shape[0]

dsets_notCOD = len(df_publicnoarchive_5yo_lt1000dl_notcod)
```


```python
# Write to CSV
df_publicnoarchive_5yo_lt1000dl_notcod.to_csv("output.csv", index=False)
```


```python
# Some reporting

print(f"Initial number of datasets: {dsets_initial}")
print(
    f"After filtering by public, non-archived, non-requestable: {dsets_publicNoArchiveNotRequestable}"
)
print(f"After filtering by not ongoing: {dsets_notOngoing}")
print(f"After filtering by create year > 5 years: {dsets_createYear}")
print(f"After filtering by reference period end > 5 years: {dsets_refEndYear}")
print(f"After filtering by lifetime downloads < 1000: {dsets_lt1000Dl}")
print(f"After filtering by not COD: {dsets_notCOD}")
```

    Initial number of datasets: 26882
    After filtering by public, non-archived, non-requestable: 18063
    After filtering by not ongoing: 17036
    After filtering by create year > 5 years: 8327
    After filtering by reference period end > 5 years: 807
    After filtering by lifetime downloads < 1000: 613
    After filtering by not COD: 608
    


```python
# # Utility to get datasets with >= MAX_DOWNLOADS
# df_publicnoarchive_5yo_gte1000dl = df_publicnoarchive_5yo.loc[
#     df_publicnoarchive_5yo["downloads last 5 years"] >= MAX_DOWNLOADS
# ]
# df_publicnoarchive_5yo_gte1000dl_notcod = df_publicnoarchive_5yo_gte1000dl.loc[
#     df_publicnoarchive_5yo_gte1000dl["is cod"] == "N"
# ]

# # # Remove unneeded columns
# df_publicnoarchive_5yo_gte1000dl_notcod = df_publicnoarchive_5yo_gte1000dl_notcod.loc[
#     :, ["name", "downloads last 5 years", "organisation"]
# ]
# df_publicnoarchive_5yo_gte1000dl_notcod.to_csv(
#     "publicNoArchive_5yo_gte1000dl_notcod.csv", index=False
# )
# df_publicnoarchive_5yo_gte1000dl_notcod.shape[0]
```
