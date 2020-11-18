import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
from Processing.Utils import convert_to_datetime
class Patient:
    def __init__(self, id, los,gender, age, comorbidity, weight, m3, m5, m7, m14, m30, itu3, itu5, itu7, itu14, itu30,
                 admitDate=None, deathDate=None, ituDate = None, deathperiod=-1, ituperiod=-1):


        print(" IN PATIENT", id, ", Admit Date: ", admitDate, "DEATH DATE: ", deathDate, "ITU DATE : ", ituDate)
        self.Patient_id = id
        self.Age = age
        self.Gender = gender


        if isinstance(deathDate, str)  and len(deathDate) <= 1:
            self.deathRange = -1
        elif (not (pd.isnull(deathDate)) and not (pd.isnull(admitDate))):
            AdmitDate = convert_to_datetime(admitDate)
            DeathDate = convert_to_datetime(deathDate)
            self.deathRange = DeathDate- AdmitDate
        else:
            self.deathRange = -1

        if isinstance(ituDate, str) and len(ituDate) <= 1:
            self.ituRange = -1
        elif not (pd.isnull(ituDate)) and not (pd.isnull(admitDate)):
            AdmitDate = convert_to_datetime(admitDate)
            ITUDate = convert_to_datetime(ituDate)
            self.ituRange = ITUDate- AdmitDate
        else:
            self.ituRange = -1

        self.AdmitDate = admitDate
        self.DeathDate = deathDate
        self.ITUDate = ituDate

        self.los = los
        self.M3 = m3
        self.M5 = m5
        self.M7 = m7
        self.M14 = m14
        self.M30 = m30

        self.ITU3 = itu3
        self.ITU5 = itu5
        self.ITU7 = itu7
        self.ITU14 = itu14
        self.ITU30 = itu30
        self.weight = weight
        self.comorbidity = comorbidity
        self.observations = []

    def addObservations( self, observations ):
        for o in observations:
            self.observations.append(o)

    def printString( self ):
        print(" Patient: ", self.Patient_id, self.Age, self.Gender)

    def printObservationVolume( self ):
        print(" Patient: ", self.Patient_id," has: ", len(self.observations), "observations")

    def getNumberOfObservations( self ):
        return len(self.observations)

    def as_dict(self):
        patient_row = {'PatientID' : self.Patient_id,
                       'Age' : self.Age,
                       'Gender' : self.Gender,
                       'los': self.los,
                       'comorbidity': self.comorbidity,
                       'weight': self.weight,
                       'DeathPeriod' : self.deathRange,
                       'ITUPeriod': self.ituRange,
                       'Mortality3Days': self.M3,
                       'Mortality5Days' : self.M5,
                       'Mortality7Days' : self.M7,
                       'Mortality14Days' : self.M14,
                       'Mortality30Days' : self.M30,
                       'ITUAdmission3Days': self.ITU3,
                       'ITUAdmission5Days': self.ITU5,
                       'ITUAdmission7Days': self.ITU7,
                       'ITUAdmission14Days': self.ITU14,
                       'ITUAdmission30Days': self.ITU30
                       }
        return patient_row