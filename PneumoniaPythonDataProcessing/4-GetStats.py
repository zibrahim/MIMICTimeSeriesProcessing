import pandas as pd
from Processing.Utils import get_distribution_percentages, get_distribution_counts
from sklearn.preprocessing import MinMaxScaler
def main():
    aggregate_series = pd.read_csv("Data/TimeSeriesAggregated.csv")
    cohort = pd.read_csv("Data/DemographicsOutcomesCleaned.csv")
    unique_admissions = set(aggregate_series['PatientID'])
    print(" number of records: ", aggregate_series.shape[0], "unique admissions: ", len(unique_admissions))
    cohort_subset = cohort.loc[cohort['hadm_id'].isin(unique_admissions)]
    print(" Female percentages ", get_distribution_percentages(cohort_subset['gender']))
    print(" Female counts ", get_distribution_counts(cohort_subset['gender']))
    print(" Age stats", cohort_subset['age'].describe())
    print(" Weight stats", cohort_subset['weight'].describe())
    print(" Comorbidity stats", cohort_subset['comorbidity'].describe())

    X = (cohort_subset['comorbidity']).to_numpy()
    X = X.reshape(-1,1)
    scaler = MinMaxScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    X = pd.Series(X[:,0])
    print(" Comorbidity rescaled stats",  X.describe())



    death_columns = cohort_subset['deathperiod'].copy()
    death_columns_bool = [0 if x =='-1'  else 1 for x in death_columns ]
    print(" Death perentages: ", get_distribution_percentages(death_columns_bool))
    print(" Death counts: ", get_distribution_counts(death_columns_bool))

    print(cohort.columns)
    death_periods_int = [0 if x =='-1' else int(x.split('da')[0]) for x in death_columns]
    death_periods_int = [x for x in death_periods_int if x > 0]

    print(" Death periods stats", pd.Series(death_periods_int).describe())

    itu_columns = cohort_subset['ituperiod'].copy()

    itu_periods_int = [0 if x =='-1' else int(x.split('da')[0]) for x in itu_columns]
    itu_periods_int = [x for x in itu_periods_int if x > 0]
    print(" ITU periods stats", pd.Series(itu_periods_int).describe())

    m5 = aggregate_series['Mortality5Days']
    print(" Death 5D perentages: ", get_distribution_percentages(m5))
    print(" Death 5D counts: ", get_distribution_counts(m5))


    m7= aggregate_series['Mortality7Days']
    print(" Death 7D perentages: ", get_distribution_percentages(m7))
    print(" Death 7D counts: ", get_distribution_counts(m7))


    m14 = aggregate_series['Mortality14Days']
    print(" Death 14D perentages: ", get_distribution_percentages(m14))
    print(" Death 14D counts: ", get_distribution_counts(m14))


    m30 = aggregate_series['Mortality30Days']
    print(" Death 30D perentages: ", get_distribution_percentages(m30))
    print(" Death 30D counts: ", get_distribution_counts(m30))


    itu5 = aggregate_series['ITUAdmission5Days']
    print(" ITU 5D perentages: ", get_distribution_percentages(itu5))
    print(" ITU 5D counts: ", get_distribution_counts(itu5))

    itu7 = aggregate_series['ITUAdmission7Days']
    print(" ITU 7D perentages: ", get_distribution_percentages(itu7))
    print(" ITU 7D counts: ", get_distribution_counts(itu7))

    itu14 = aggregate_series['ITUAdmission14Days']
    print(" ITU 14D perentages: ", get_distribution_percentages(itu14))
    print(" ITU 14D counts: ", get_distribution_counts(itu14))

    itu30 = aggregate_series['ITUAdmission30Days']
    print(" ITU 30D perentages: ", get_distribution_percentages(itu30))
    print(" ITU 30D counts: ", get_distribution_counts(itu30))

    print(" dim of original", cohort_subset.shape)
    cohort_subset2 = cohort_subset.loc[cohort['age']> 0 ]
    print("dim of age > 0, " , cohort_subset2.shape)
    print(" AGE SUMMARY: ")
    print(cohort_subset2['age'].describe())
    cohort_subset2 = cohort_subset2.loc[cohort['weight'].isna()==False]

    print("dim of age > 0 and weight > 0 , " , cohort_subset2.shape)

    print(" WEIGHT summary")
    print(cohort_subset2['weight'].describe())


    print(cohort_subset['comorbidity'].describe())

if __name__ == "__main__" :
    main()