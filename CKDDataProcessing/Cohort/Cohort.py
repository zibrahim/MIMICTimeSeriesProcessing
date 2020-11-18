from datetime import datetime
import numpy as np
import pandas as pd

from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Utils import binSearch


class Cohort :
    def __init__ ( self, cohort_df=pd.DataFrame(), IDField='', title="") :
        self.name = title
        self.individuals = []
        self.individual_ids = []

        if len(IDField)> 0:
            unique_ids = np.sort(cohort_df[IDField].unique())

            for some_id in list(unique_ids):

                individual = Patient(cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:,'hadm_id'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'los'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'gender'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'age'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'comorbidity'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'weight'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '3DM'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '5DM'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '7DM'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '14DM'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '30DM'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '3DITU'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '5DITU'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '7DITU'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '14DITU'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, '30DITU'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'admittime'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'deathtime'].values[0],
                                 cohort_df.loc[cohort_df['hadm_id'] == some_id].loc[:, 'readmission_time'].values[0],
                                     -1,-1

                )
                self.individuals.append(individual)
                self.individual_ids.append(some_id)


    def addIndividual(self,p, pid ):
        self.individuals.append(p)
        self.individual_ids.append(pid)

    def addObservationsToIndividual( self, ids, observations ):
        i = binSearch(self.individual_ids, ids)
        self.individuals[i].addObservations(observations)

    def addBloodObservations (self, pid, bloods_for_patient, patientAdmissionDate ) :
        observations = []
        for index, row in bloods_for_patient.iterrows() :
            if not pd.isnull(row.vitalid) :
                obs = Observation("Vital",
                                  row.vitalid,
                                  datetime.strptime(row.time, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  row.valuenum,
                                  row.valueuom,
                                  row.value)

                observations.append(obs)
        self.addObservationsToIndividual(pid, observations)

    def clean( self ):
        remove_indices = []
        length = len(self.individuals)
        for i in range(length) :
            if len(getattr(self.individuals[i], 'observations')) == 0:
                remove_indices.append(i)

        for index in sorted(remove_indices, reverse=True) :
            del self.individuals[index]

    def getAllColumnNames( self ):

        all_column_names = [o.Name for p in self.individuals for o in p.observations]

        all_column_names = np.unique(all_column_names)

        all_column_names = np.insert(all_column_names, 0,"Mortality3Days")
        all_column_names = np.insert(all_column_names, 0,"Mortality5Days")
        all_column_names = np.insert(all_column_names, 0,"Mortality7Days")
        all_column_names = np.insert(all_column_names, 0,"Mortality14Days")
        all_column_names = np.insert(all_column_names, 0,"Mortality30Days")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission3Days")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission5Days")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission7Days")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission14Days")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission30Days")
        all_column_names = np.insert(all_column_names, 0,"Hour")
        all_column_names = np.insert(all_column_names, 0,"Age")
        all_column_names = np.insert(all_column_names, 0,"comorbidity")
        all_column_names = np.insert(all_column_names, 0,"weight")
        all_column_names = np.insert(all_column_names, 0,"PatientID")

        return all_column_names