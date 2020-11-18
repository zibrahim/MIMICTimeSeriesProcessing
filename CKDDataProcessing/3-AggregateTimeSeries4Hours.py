import pandas as pd
import os
from Processing.Dictionaries import aggregation, outcomes, id
from Processing.CleanTimeSeries import remove_alpha, remove_nacolumns
def main():
    time_series = pd.read_csv("Data/TimeSeriesUpto0.csv")

    time_series = remove_alpha(time_series)
    time_series = remove_nacolumns(time_series)
    patient_ids = time_series['PatientID'].unique()

    #2. Create a new column, call it FourHourIndex
    time_series['FourHourIndex'] = -1
    new_time_series = pd.DataFrame(columns=time_series.columns)

    #3. Create a new column that aggregates every 4 hours into 1
    for p in patient_ids:
        patient_slice = time_series.loc[time_series.PatientID ==p,]
        patient_slice.reset_index()

        lower_limit = 0
        upper_limit = 3
        flag = False

        while (flag == False):
            if upper_limit >= len(patient_slice.index) :
                flag = True
                patient_slice.iloc[lower_limit:len(patient_slice.index),patient_slice.columns.get_loc('FourHourIndex')] = lower_limit

            else:
                patient_slice.iloc[lower_limit:upper_limit+1,patient_slice.columns.get_loc('FourHourIndex')] = lower_limit

            lower_limit = lower_limit + 4
            upper_limit = upper_limit + 4

        cvo2 = patient_slice['CentralvenousO2Saturation']
        creactiveprot = patient_slice['Creactiveprotein']
        if cvo2.isnull().values.all() or creactiveprot.isnull().values.all():
            print(" paitent", p, "has all nan CentralvenousO2Saturation")
        else:
            new_time_series = new_time_series.append(patient_slice, ignore_index=True)
    new_time_series.to_csv("Data/new_time_series_0.csv", index=False)

    new_time_series = pd.read_csv("Data/new_time_series_0.csv")
    os.remove("Data/new_time_series_0.csv")

    int_columns = [ "Day", "Hour", "Age",
                    "Mortality3Days", "Mortality7Days","Mortality14Days","Mortality30Days",
                    "OrdinalHour", "FourHourIndex"]

    new_time_series[int_columns] = new_time_series[int_columns].astype(int)

    na_columns = set(new_time_series.columns) - set(int_columns)
    na_columns = na_columns - set(['PatientID'])

    float_columns = list(set(new_time_series.columns)  - set(int_columns))
    new_time_series[float_columns] = new_time_series[float_columns].astype(float)

    aggregate_series = new_time_series.groupby(['PatientID', 'FourHourIndex']).aggregate(aggregation)
    #print(aggregate_series['PO2/FIO2'].isnull().sum() * 100 /len(aggregate_series['PO2/FIO2']))
    # 1. Identify columns where PO2/FIO2 is null but both FIO2 and PO2 are not null
    #matches = aggregate_series['PO2/FIO2'].isnull() & aggregate_series['FiO2'].notnull() & aggregate_series['PO2'].notnull()
    # 2. Calculate PO2/FIO2 for the columns using the individual PO2 and FIO2 values
    #aggregate_series.loc[matches, 'PO2/FIO2'] = aggregate_series.loc[matches, 'PO2']/aggregate_series.loc[matches, 'FiO2']

    #print(aggregate_series['PO2/FIO2'].isnull().sum() * 100 /len(aggregate_series['PO2/FIO2']))

    #print("dim before remove na ", aggregate_series.shape)
    aggregate_series.dropna(axis=1, how='all', inplace=True)
    #print("dim after remove na ", aggregate_series.shape)
    aggregate_series.to_csv("Data/TimeSeriesAggregated.csv", index=False)

if __name__ == "__main__" :
    main()