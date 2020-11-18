from Cohort.Cohort import Cohort
from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Utils import getDayWrapper, getHourWrapper
import json
import numpy as np
from datetime import timedelta
import pandas as pd

class CohortEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, timedelta):
            return str(obj)
        else:
            return super(CohortEncoder, self).default(obj)

def jsonDump ( cohort, filename ) :
        json_dict = {}
        individuals = []
        for ind in cohort.individuals :
            person_dic = ind.as_dict()
            print(person_dic)
            i = 0
            observations = []
            for obs in ind.__getattribute__("observations") :
                observations.append(obs.as_dict(ind.Patient_id))
                i = i + 1
            person_dic["observations"] = observations
            individuals.append(person_dic)

        json_dict["cohort"] = cohort.name
        json_dict["patients"] = individuals

        with open(filename, "w") as outfile :
            json.dump(json_dict, outfile, cls=CohortEncoder,indent=4, sort_keys=True)


def jsonRead(fileName):

    with open(fileName) as f :
        cohort_dict = json.load(f)
        patients = cohort_dict['patients']
        cohort = Cohort(cohort_dict['cohort'])

        for p in patients:
            patient = Patient(p['PatientID'], p['los'], p['Gender'], p['Age'],p['comorbidity'], p['weight'],
                              p["Mortality3Days"],
                              p["Mortality5Days"],
                              p["Mortality7Days"],
                              p["Mortality14Days"],
                              p["Mortality30Days"],
                              p["ITUAdmission3Days"],
                              p["ITUAdmission5Days"],
                              p["ITUAdmission7Days"],
                              p["ITUAdmission14Days"],
                              p["ITUAdmission30Days"],
                              deathperiod = p["DeathPeriod"],
                              ituperiod = p['ITUPeriod'])

            observations_dictionary = p['observations']
            observations = []
            for o in observations_dictionary:
                new_obs =  Observation(o['ObservationType'],
                                       o['ObservationName'],
                                       o['ObservationOrdinalTime'],
                                       o['ObservationValue'],
                                       o['ObservationUnit'],
                                       o['ObservationText'])

                observations.append(new_obs)

            patient.addObservations(observations)
            cohort.addIndividual(patient, p['PatientID'])

    return cohort

def makeTimeSeriesOneDay ( cohort ) :
    column_names = cohort.getAllColumnNames()
    TimeSeriesDF = pd.DataFrame(columns=column_names)
    PatientDF = pd.DataFrame(columns=column_names)
    cohort.clean()
    for ind in cohort.individuals :
        observation_list = getattr(ind, 'observations')

        observation_list = [x for x in observation_list if x.Name in column_names]

        observation_df = pd.DataFrame.from_records([o.as_dict(ind.Patient_id) for o in observation_list])
        observation_df['Day'] = observation_df.apply(lambda x : getDayWrapper(x['ObservationOrdinalTime']),
                                                     axis=1)
        observation_df['Hour'] = observation_df.apply(lambda x : getHourWrapper(x['ObservationOrdinalTime']),
                                                      axis=1)

        observation_df['Day'] = observation_df['Day'].astype(int)
        observation_df['Hour'] = observation_df['Hour'].astype(int)

        # Subset observations to include days 0 to 2
        observation_df = observation_df.loc[observation_df.Day >= 0]
        observation_df = observation_df.loc[observation_df.Day <= 1]

        days = pd.Series([0,1])

        PatientDF['Day'] = days.repeat(24)

        PatientDF.loc[PatientDF.Day == 0, "Hour"] = range(0, 24)
        PatientDF.loc[PatientDF.Day == 1, "Hour"] = range(24, 48)

        PatientDF.loc[PatientDF.Day == 0, "OrdinalHour"] = range(0, 24)
        PatientDF.loc[PatientDF.Day == 1, "OrdinalHour"] = range(0, 24)

        PatientDF['PatientID'] = ind.Patient_id
        PatientDF['Age'] = ind.Age
        PatientDF['weight'] = ind.weight
        PatientDF['comorbidity'] = ind.comorbidity


        PatientDF["Mortality3Days"] = ind.M3 if not pd.isnull(ind.M3) else 0
        PatientDF["Mortality5Days"] = ind.M5 if not pd.isnull(ind.M5) else 0
        PatientDF["Mortality7Days"] = ind.M7 if not pd.isnull(ind.M7) else 0
        PatientDF["Mortality14Days"] = ind.M14 if not pd.isnull(ind.M14) else 0
        PatientDF["Mortality30Days"] = ind.M30 if not pd.isnull(ind.M30) else 0

        PatientDF["ITUAdmission3Days"] = ind.ITU3 if not pd.isnull(ind.ITU3) else 0
        PatientDF["ITUAdmission5Days"] = ind.ITU5 if not pd.isnull(ind.ITU5) else 0
        PatientDF["ITUAdmission7Days"] = ind.ITU7 if not pd.isnull(ind.ITU7) else 0
        PatientDF["ITUAdmission14Days"] = ind.ITU14 if not pd.isnull(ind.ITU14) else 0
        PatientDF["ITUAdmission30Days"] = ind.ITU30 if not pd.isnull(ind.ITU30) else 0


        for index, row in observation_df.iterrows() :
            ob_name = row['ObservationName']
            ob_value = row['ObservationValue']
            ob_hour = row['Hour']
            ob_day = row['Day']

            PatientDF.loc[(PatientDF.Day == ob_day) & (PatientDF.OrdinalHour == ob_hour), ob_name] = ob_value
        TimeSeriesDF = TimeSeriesDF.append((PatientDF))
    
    
    TimeSeriesDF.to_csv("Data/TimeSeriesUpto0.csv", index=False)
    observation_df.to_csv("Data/obs.csv", index=False)