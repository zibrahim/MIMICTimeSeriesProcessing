
def intersection_listcomprehension(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def intersection(a_subset, a_set):
    intersect = []
    for c in a_set:
        if c in a_subset:
            intersect.append(c)
    return intersect


def merge_INR(df):

    for index, row in df.iterrows():
        if row['INR'] == "see INRW" or row['INR'] =="See INRW" or row['INR'] == "SEE INRW":
            row['INR'] = row["INR (warfarin)"]
        if row['INR']=="" and not(row["INR (warfarin)"]==""):
            row['INR'] = row["INR (warfarin)"]

    df = df.drop(['INR (warfarin)'], axis=1)
    df = df.drop(['INR 50/50'], axis=1)
    return df


def remove_nacolumns(df):
    df = df.dropna(axis=1, how='all')
    return df

def remove_alpha(df):
    df = df.replace("[^0-9.-]", '', regex=True)
    return df

