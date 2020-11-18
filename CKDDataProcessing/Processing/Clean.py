import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

def clean_vitals(vitals):
    timeseries_columns = list(set(vitals['vitalid']))
    timeseries_columns.append('icustay_id')
    timeseries = pd.DataFrame(columns = timeseries_columns)
    return vitals
def add_itureadmission (cohort, itureadmission_df):
    result = pd.merge(cohort, itureadmission_df, on='hadm_id', how='inner')
    result.reset_index()
    return result

def clean_cohort(cohort, vitals):
    cohort['weight'] = None
    weights  = vitals.loc[vitals.vitalid=='Weightkg',:]
    for ind in cohort['hadm_id']:
        print(" processing ind's weight. id: ", ind)
        ind_weight = weights.loc[(weights.hadm_id ==ind)]
        ind_weight = ind_weight.valuenum
        if len(ind_weight) > 0:
            ind_weight = ind_weight.iloc[0]
        else:
            ind_weight = np.nan
        print(" \t the weight: ", ind_weight)
        cohort.loc[cohort['hadm_id']==ind, 'weight'] = ind_weight

    cohort.drop(['dob', 'subject_id'], inplace=True, axis=1)
    cohort['admittime'] = [x.replace(':00 ', '') for x in cohort['admittime']]
    cohort['gender'] = np.where(cohort['gender'] == "F", 1, 0)

    cohort['admittime'] = [datetime.strptime(x, '%d/%m/%y %H:%M') for x in cohort['admittime']]
    cohort['deathtime'] = ['' if str(x) =="nan" else datetime.strptime(x, '%d/%m/%y %H:%M') for x in cohort['deathtime'] ]
    cohort['readmission_time'] = ['' if str(x) =="nan" else datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in cohort['readmission_time'] ]

    death_period = []
    death_period_int = []

    itureadmission_period = []
    itureadmission_period_int = []

    mortality_3days = []
    mortality_5days = []
    mortality_7days = []
    mortality_14days = []
    mortality_30days = []

    itu_3days = []
    itu_5days = []
    itu_7days = []
    itu_14days = []
    itu_30days = []

    for index, row in cohort.iterrows():
        if pd.isnull(row['deathtime']):
            death_period.append(-1)
            mortality_3days.append(0)
            mortality_5days.append(0)
            mortality_7days.append(0)
            mortality_14days.append(0)
            mortality_30days.append(0)
        else:
            death_range = row['deathtime'] - row['admittime']
            death_range_int = int((str(death_range)).split('da')[0])
            death_period_int.append(death_range_int)
            death_period.append(death_range)

            if (death_range <= timedelta(days=3)) :
                mortality_3days.append(1)
                mortality_5days.append(1)
                mortality_7days.append(1)
                mortality_14days.append(1)
                mortality_30days.append(1)
            elif (death_range <= timedelta(days=5)) :
                mortality_3days.append(0)
                mortality_5days.append(1)
                mortality_7days.append(1)
                mortality_14days.append(1)
                mortality_30days.append(1)
            elif (death_range <= timedelta(days=7)) :
                mortality_3days.append(0)
                mortality_5days.append(0)
                mortality_7days.append(1)
                mortality_14days.append(1)
                mortality_30days.append(1)
            elif (death_range <= timedelta(days=14)) :
                mortality_3days.append(0)
                mortality_5days.append(0)
                mortality_7days.append(0)
                mortality_14days.append(1)
                mortality_30days.append(1)
            elif (death_range <= timedelta(days=30)):
                mortality_3days.append(0)
                mortality_5days.append(0)
                mortality_7days.append(0)
                mortality_14days.append(0)
                mortality_30days.append(1)
            else:
                mortality_3days.append(0)
                mortality_5days.append(0)
                mortality_7days.append(0)
                mortality_14days.append(0)
                mortality_30days.append(0)

        if pd.isnull(row['readmission_time']) or row['readmission_time'] =='':
            itureadmission_period.append(-1)
            itu_3days.append(0)
            itu_5days.append(0)
            itu_7days.append(0)
            itu_14days.append(0)
            itu_30days.append(0)
        else:
            itu_range = row['readmission_time'] - row['admittime']
            itu_range_int = int((str(itu_range)).split('da')[0])
            itureadmission_period_int.append(itu_range_int)
            itureadmission_period.append(itu_range)

            if (itu_range <= timedelta(days=3)) :
                itu_3days.append(1)
                itu_5days.append(1)
                itu_7days.append(1)
                itu_14days.append(1)
                itu_30days.append(1)
            elif (itu_range <= timedelta(days=5)) :
                itu_3days.append(0)
                itu_5days.append(1)
                itu_7days.append(1)
                itu_14days.append(1)
                itu_30days.append(1)
            elif (itu_range <= timedelta(days=7)) :
                itu_3days.append(0)
                itu_5days.append(0)
                itu_7days.append(1)
                itu_14days.append(1)
                itu_30days.append(1)
            elif (itu_range <= timedelta(days=14)) :
                itu_3days.append(0)
                itu_5days.append(0)
                itu_7days.append(0)
                itu_14days.append(1)
                itu_30days.append(1)
            elif (itu_range <= timedelta(days=30)):
                itu_3days.append(0)
                itu_5days.append(0)
                itu_7days.append(0)
                itu_14days.append(0)
                itu_30days.append(1)
            else:
                itu_3days.append(0)
                itu_5days.append(0)
                itu_7days.append(0)
                itu_14days.append(0)
                itu_30days.append(0)
    cohort['deathperiod'] = death_period
    cohort['3DM'] = mortality_3days
    cohort['5DM'] = mortality_5days
    cohort['7DM'] = mortality_7days
    cohort['14DM'] = mortality_14days
    cohort['30DM'] = mortality_30days

    cohort['ituperiod'] = itureadmission_period

    cohort['3DITU'] = itu_3days
    cohort['5DITU'] = itu_5days
    cohort['7DITU'] = itu_7days
    cohort['14DITU'] = itu_14days
    cohort['30DITU'] = itu_30days
    return cohort

def removeDateSuffix(df):
    dates = []
    for s in df:
        parts = s.split()
        parts[1] = parts[1].strip("stndrh") # remove 'st', 'nd', 'rd', ...
        dates.append(" ".join(parts))

    return dates

def updateDate(df):
    date_output_format = "%Y-%m-%d"

    dates = []
    for t in df:
        if t == '' or pd.isnull(t) :
            d = np.nan
        elif "-" in t :
            fmt = "%y-%m-%d"
            d = pd.to_datetime(t, format=fmt, exact=False, utc=True)
        elif "/" in t :
            fmt = "%d/%m/%y"
            d = pd.to_datetime(t, format=fmt, exact=False)
        else :
            fmt = None
            d = pd.to_datetime(t, format=fmt, exact=False)
        if pd.isnull(d):
            dates.append(np.nan)
        else:
            dates.append(d.strftime(date_output_format))
    return dates

def updateDateTime(df):
    date_output_format = "%Y-%m-%d %H:%M:%S"
    dates = []
    for t in df:
        if "-" in t :
            fmt = "%y-%m-%d %H:%M"
            d = pd.to_datetime(t, format=fmt, exact=False, utc=True)
        elif "/" in t :
            fmt = "%d/%m/%y %H:%M"
            d = pd.to_datetime(t, format=fmt, exact=False)
        else :
            fmt = None
            d = pd.to_datetime(t, format=fmt, exact=False)
        dates.append(d.strftime(date_output_format))
    return dates
