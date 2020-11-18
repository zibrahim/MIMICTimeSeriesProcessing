import pandas as pd
from Cohort.Cohort import Cohort
from Processing.Utils import convert_to_datetime
import time
from Processing.Clean import clean_cohort, clean_vitals, add_itureadmission
from Processing.Serialisation import jsonDump
import numpy as np
from datetime import datetime
from time import mktime

def main():
    #1. extract only first icu stay
    vitals_data = pd.read_csv("Data/TimeSeries.csv")

    itu_readmission_df = pd.DataFrame()
    hadm_ids = set(vitals_data['hadm_id'])

    vitals_data = vitals_data[~vitals_data['vitalid'].isin(['MeanBP2', 'SysBP2', 'DiasBP2'])]

    vitals_data_subset = pd.DataFrame(columns = vitals_data.columns)

    for idx in hadm_ids:
        admission_df = vitals_data.loc[vitals_data['hadm_id'] == idx]
        unique_icustays = set(admission_df['icustay_id'])
        if len(unique_icustays) > 1:
            aggregated_admission = admission_df.groupby('icustay_id').first()
            readmission_times =  aggregated_admission['time']
            sorted_readmission_times = sorted((time.strptime(d, "%d/%m/%y %H:%S") for d in readmission_times), reverse=False)
            itu_readmission_date = sorted_readmission_times[1]
            itu_readmission_date = datetime.fromtimestamp(mktime(itu_readmission_date))
            itu_readmission_df = itu_readmission_df.append({'hadm_id': int(idx) ,'readmission_time': itu_readmission_date}, ignore_index=True)
        else:
            itu_readmission_df = itu_readmission_df.append({'hadm_id': int(idx) ,'readmission_time': np.nan}, ignore_index=True)

        first_icustay = (admission_df['icustay_id']).iloc[0]
        icustay_df = vitals_data.loc[vitals_data['icustay_id'] == first_icustay]

        vitals_data_subset = vitals_data_subset.append(icustay_df, ignore_index=True)

    itu_readmission_df.columns =['hadm_id', 'readmission_time']
    itu_readmission_df.to_csv("Data/itureadmission.csv", index=False)
    vitals_data_subset.to_csv("Data/vitals_final.csv", index=False)


    vitals = pd.read_csv("Data/vitals_final.csv")
    cohort_data = pd.read_csv("Data/DemographicsOutcomes.csv")
    itu_readmission_df = pd.read_csv("Data/itureadmission.csv")

    cohort_data = add_itureadmission(cohort_data, itu_readmission_df)

    #obtain only patients whose time-series we have

    cohort_data = cohort_data[cohort_data['hadm_id'].isin(vitals['hadm_id'])]
    cohort_data = clean_cohort(cohort_data, vitals)

    cohort_data.to_csv("Data/DemographicsOutcomesCleaned.csv", index=False)

    vitals_data = clean_vitals(vitals)

    cohort = Cohort(cohort_data, 'hadm_id', "PneumoniamMIMIC")


    admission_ids = set(cohort_data.hadm_id)

    for idx in admission_ids :
        patientAdmissionDate = cohort_data.loc[cohort_data['hadm_id'] == idx].loc[:, 'admittime'].values[0]
        #print(" admission date before conversion: ", patientAdmissionDate, " and class: ", type(patientAdmissionDate))
        #patientAdmissionDate = datetime.strptime(str(patientAdmissionDate), '%d/%m/%y %H:%M')
        patientAdmissionDate = convert_to_datetime(patientAdmissionDate)

        vitals_for_patient = vitals_data.loc[vitals_data['hadm_id'] == idx]
        vitals_for_patient.drop(['subject_id', 'icustay_id'], axis=1, inplace=True)
        vitals_for_patient.columns = ['hadm_id', 'time', 'value', 'valuenum', 'valueuom', 'vitalid']

        vitals_for_patient['time'] = pd.to_datetime(vitals_for_patient['time'])
        vitals_for_patient['time'] = vitals_for_patient['time'].astype(str)

        if vitals_for_patient.shape[0]:
            cohort.addBloodObservations(idx, vitals_for_patient, patientAdmissionDate)

    jsonDump(cohort, "Data/Cohort.json")

if __name__ == "__main__":
    main()