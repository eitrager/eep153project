import pandas as pd
import numpy as np
import plotly.express as px
import wbdata

def population(year,sex,age_range,place,graph = False):
    """
    year: must be 4 digit year
    sex: either "MA" for male or "FE" for female
    age_range: a list of min and max age ex. [5,20] for ages 5 to 20 years old
    place: 3 digit region code. ex "CHN" for China
    graph: optional arg to generate a line plot of the age ranges. Set to either True or False
    Example complete input: population(2021, 'FE', [7,23], 'JPN',graph = True)
    output: total pop and optional graph
    """
    first_term = "SP"
    second_term = "POP"
    if sex == "MA":
        age_ranges = generateageranges(first_term, second_term, age_range, "MA", place, f"{year}-01-01")
        agearrayspecific, popvalues = interpprep(age_ranges)
        age_array_all_years = interpfunc(popvalues, agearrayspecific, place, year, graph_values = graph)
        sliced_popvals = age_array_all_years[age_range[0]:age_range[1]]
        return np.sum(sliced_popvals)
    else:
        age_ranges = generateageranges(first_term, second_term, age_range, "FE", place, f"{year}-01-01")
        agearrayspecific, popvalues = interpprep(age_ranges)
        age_array_all_years = interpfunc(agearrayspecific, popvalues, place, year, graph_values = graph)
        sliced_popvals = age_array_all_years[age_range[0]:age_range[1]]
        return np.sum(sliced_popvals)
#helper functions below
def generateageranges (first_term, second_term, age_range, sex, countrylabel, yearstring):
    age_min = age_range[0] # assuming list input
    age_max = age_range[1]
    listcodes3slot = []
    ageexact = np.arange(age_min, age_max+1)
    for age in ageexact:
        code = ""
        # if age < 25:
        #     if age < 10:
        #         code = "AG0" + f"{age}"
        #     else:
        #         code = "AG" + f"{age}"
        # else:
        agelist = [
            "0004",
            "0509",
            "1014",
            "1519",
            "2024",
            "2529",
            "3034",
            "3539",
            "4044",
            "4549",
            "5054",
            "5559",
            "6064",
            "6569",
            "7074",
            "7579",
            "80UP"
        ]
    
    #next section
    total = 0
    counter = ageexact[0]
    fulldict= {}
    #print(agelist)
    for code in agelist:
        inputval = f"{first_term}.{second_term}.{code}.{sex}"
        var_label = f"{code}"
        counter += 1
        fulldict[inputval] = var_label
    totaldf = wbdata.get_dataframe(fulldict, country=countrylabel, parse_dates=True)
    filteryear = totaldf.loc[yearstring]
    #print(filteryear)
    return filteryear

def interpprep(bucketed_vals, interpolatetype = 'cubic', midpoint_selection = [2,7,12,17,22,27,32,37,42,47,52,57,62,67,72,77,89]):
    midpoints = (bucketed_vals[:-1])/5
    finalbucket = bucketed_vals[-1]/20 #not sure how much to divide by. just doing 20 for 20 items 80-100
    midpoints = pd.concat([midpoints, pd.Series([finalbucket])], ignore_index=True)
    #u can make outputs transparent below
    #print(f"midpoints are {midpoints}. These can be changed if we want to take a new approach to better account for very old ages (100+)")
    #print(f"ages are {midpoint_selection}")
    return midpoint_selection, midpoints

def interpfunc(age_midpoints, pop_values, country, year, max_age=100, graph_values = False):
    bucketed_vals = np.array(pop_values)
    midpoint_selection = np.array(age_midpoints)
    age_range = np.arange(0, max_age + 1)  # ages from 0 to max_age
    #interp time
    interpolated_values = np.interp(age_range, bucketed_vals, midpoint_selection)
    #optional graph
    if graph_values:
        popdf = pd.DataFrame({'Age': age_range, 'Population': interpolated_values})
        fig = px.line(popdf, x='Age', y='Population', title=f'Population Interpolation by Age for {country} in Year {year}')
        fig.show()
    return interpolated_values

