import numpy as np
lower_limit = {
    'Lymphocytes': 1.3,
    'Neutrophils' : 2.2,
    'ALT': 5,
    'PLT' : 150,
    'Hb' : 130,
    'WBC' : 3.7,
    'C-Reactive-Protein' : 0,
    'Albumin' : 35,
    'Creatinine' : 45,
    'Urea' : 3.3,
    'Troponin-T': 0,
    'CRP': 0,
    'Ferritin': 30,
    'Lactate-Dehydrogenase': 0,
    'Creatine-Kinase' : 0,
    'Troponin-I': 0,
    'Lactate' : 0.6,
    'Aspartate-Transaminase' : 10,
    'Estimated-GFR': 0,
    'NT-pro-BNP' : 0,
    'HbA1c' : 4,
}


upper_limit = {
    'Lymphocytes': 4,
    'Neutrophils' : 6.3,
    'ALT': 55,
    'PLT' : 450,
    'Hb' : 167,
    'WBC' : 9.5,
    'C-Reactive-Protein' : 5,
    'Albumin' : 50,
    'Creatinine' : 120,
    'Urea' : 6.7,
    'Troponin-T': 0,
    'CRP': 0,
    'Ferritin': 30,
    'Lactate-Dehydrogenase': 240,
    'Creatine-Kinase' : 0,
    'Troponin-I': 0,
    'Lactate' : 0.6,
    'Aspartate-Transaminase' : 10,
    'Estimated-GFR': 0,
    'NT-pro-BNP' : 0,
    'HbA1c' : 4,
}

column_types = {
 'labs': ['ALT', 'Blood Lactate', 'C-Reactive-Protein', 'Creatinine', 'D-Dimer',
        'INR', 'Lactate (plasma)', 'Lactate-Dehydrogenase',
       'Protein/Creatinine Ratio', 'Random-Urine-Creatinine', 'Reticulocyte HB Content', 'Troponin-T',
       'Urea', 'Urea (Post dialysis)', 'Urea Reduction Ratio', 'Albumin', 'Bicarbonate','DiasBP', 'Estimated-GFR', 'Ferritin', 'HBA1c-DCCT',
         'HBA1c-IFCC',  'Hb', 'PLT','SysBP', 'Venous Bicarbonate',    'pO2(a,T)/FIO2', 'pO2(a)/FIO2', 'PCO2', 'PO2', 'Venous PO2', 'Venous PCO2', 'PCV', 'U-albumin/creat. ratio', 'Urine Albumin conc.', 'cHCO3',
          'Biochemistry (Glucose)', 'CSF Glucose', 'Fasting Glucose.', 'FiO2', 'Fluid Glucose.', 'Glucose (whole blood)',
'Glucose 0 min (spec)', 'Glucose 120 min (spec)', 'Neutrophils', 'Lymphocytes', 'Lymphocytes (LYMP)', 'NT-pro-BNP','PH', 'Random Glucose:' ,
'Random Urine pH', 'Trucount WBC',  'Urine Glucose', 'Venous pH', 'WBC', 'WBC count (CSF)',  'WBC count (Fluid)',
'WBC count (PD fluid)', 'pH on 1l', 'pH(T)'],
'vitals': ['Temperature', 'OxygenSaturation', 'RespirationRate', 'SupplementalOxygen',
 'OxygenDelivery', 'OxygenLitres', 'HeartRate', 'SystolicBP', 'DiastolicBP',
 'PainScore', 'GCSEye', 'GCSVerbal', 'GCSMotor', 'NEWS2score']
}

imputation_method_complete = {
 'max': ['ALT','Anticoagulant clinic INR', 'Blood Lactate', 'C-Reactive-Protein', 'Creatinine', 'D-Dimer',
        'INR', 'INR (warfarin)', 'INR 50/50',  'Lactate (CSF)', 'Lactate (plasma)', 'Lactate-Dehydrogenase',
       'Protein/Creatinine Ratio', 'Random-Urine-Creatinine', 'Reticulocyte HB Content', 'Troponin-I', 'Troponin-T',
       'Urea', 'Urea (Post dialysis)', 'Urea Reduction Ratio'],
 'min': ['Albumin', 'Bicarbonate','DiasBP', 'Estimated-GFR', 'Ferritin', 'Fluid Albumin.', 'HBA1c-DCCT',
         'HBA1c-IFCC',  'Hb', 'HbA1c',  'PLT','SysBP', 'Venous Bicarbonate',    'pO2(a,T)/FIO2', 'pO2(a)/FIO2'],

'mode': ['PCO2', 'PO2', 'Venous PO2', 'Venous PCO2', 'PCV', 'U-albumin/creat. ratio', 'Urine Albumin conc.',
    'Urine Creatinine excr.', 'Urine Glucose', 'Urine Urea',
    'Urine Urea excr.', 'cHCO3'],
'mean': ['Biochemistry (Glucose)', 'CSF Glucose', 'Fasting Glucose.', 'FiO2', 'Fluid Glucose.', 'Glucose (whole blood)',
'Glucose 0 min (spec)', 'Glucose 120 min (spec)', 'Lymphocytes', 'Lymphocytes (LYMP)', 'NT-pro-BNP','PH', 'Random Glucose:' ,
'Random Urine pH', 'Trucount WBC',  'Urine Glucose', 'Venous pH', 'WBC', 'WBC count (CSF)',  'WBC count (Fluid)',
'WBC count (PD fluid)', 'pH on 1l', 'pH(T)']
}

aggregation = { #ZI Check Aggregation function is appropriate
    'PatientID' : 'first',
    'Hour': 'first',
    'Mortality3Days' : 'first',
    'Mortality5Days' : 'first',
    'Mortality7Days' : 'first',
    'Mortality14Days' : 'first',
    'Mortality30Days' : 'first',
    'Age': 'first',
    'comorbidity': 'first',
    'weight': 'first',
    'ALT' : 'max',
    'AST' : 'max',
    'Albumin' : 'min',
    'Bilirubin':'max',
    'CaO2':'min',
    'CentralvenousO2Saturation':'min',
    'Centralvenouspressure':'min',
    'Creatinine' : 'max',
    'Creactiveprotein' : 'max',
    'DiasBP1' : 'min',
    'Fibrinogen':'max',
    'Fio2' : 'max',
    'Haemoglobin' : 'min',
    'Heartrate':'min',
    'INR': 'max',
    'Lactatedehydrogenase':'max',
    'Lymphocytes' : 'mean',
    'MeanBP1': 'min',
    'Neutrophils' : 'mean',
    'PTT' : 'max',
    'PaCO2': 'max',
    'PaO2': 'max',
    'PeripheralO2Saturation': 'max',
    'Platelets': 'min',
    'SysBP1' : 'min',
    'PvCO2': 'max',
    'Sao2': 'max',
    'SpontaneousResRate': 'max',
    'Temperature': 'max',
    'Urea' : 'max',
    'WBC' : 'max'
}

outcomes = ['Mortality5Days','Mortality7Days', 'Mortality14Days', 'Mortality30Days',
             'ITUAdmission5Days','ITUAdmission7Days', 'ITUAdmission14Days', 'ITUAdmission30Days']

id = 'PatientID'



