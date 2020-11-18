from Processing.Serialisation import jsonRead, makeTimeSeriesOneDay
def main():
    cohort = jsonRead("Data/Cohort.json")
    makeTimeSeriesOneDay(cohort)

if __name__ == "__main__":
    main()