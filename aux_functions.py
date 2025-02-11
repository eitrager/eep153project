import pandas as pd
import numpy as np
import plotly.express as px
import wbdata
def acronymfinder(country): #helpful func to find region acronym by putting in full text
    """
    Finds and prints region acronyms (country IDs) by searching for a matching 
    country name containing the input string.

    This function retrieves a list of countries and their corresponding region 
    acronyms (IDs) using the `wbdata.get_countries()` method. It then searches 
    for country names that contain the given input string (case-insensitive) 
    and prints the matching country names along with their acronyms.

    Parameters:
        country (str): The substring to search for in country names.

    Returns:
        str: A message indicating no matching countries were found if no matches exist.
        None: If matches are found, it prints the matching country names and acronyms 
              and does not return a value.
    
    Example:
        # Assuming wbdata.get_countries() returns:
        # [{'name': 'United States', 'id': 'USA'}, {'name': 'United Kingdom', 'id': 'GBR'}, {'name': 'India', 'id': 'IND'}]
        
        acronymfinder("United")
        # Output:
        # United States: USA
        # United Kingdom: GBR
        
        result = acronymfinder("XYZ")
        # Output: 'no matching countries, please try a different input'
        print(result)
        # Output: 'no matching countries, please try a different input'
    """
    country_dict = wbdata.get_countries()
    matchedacronym = ""
    country_mapping = {country['name']: country['id'] for country in country_dict}
    output = False
    for country_name in country_mapping.keys():
        if country.lower() in country_name.lower():
            print(f"{country_name}: {country_mapping[country_name]}")
            output = True
    if not output:
        return 'no matching countries, please try a different input'


def population(year,sex,age_range,place,graph = False):
    """
    Calculate and visualize population data based on the given parameters.

    Parameters:
    -----------
    year : int
        A four-digit year (e.g., 2025).
    sex : str
        The sex category, either "MA" (male) or "FE" (female).
    age_range : list of int
        A list of two integers specifying the min and max age (e.g., [5, 20]).
    place : str
        A 3-character country code (e.g., "CHN" for China).
    graph : bool, optional
        Whether to generate a line plot (default is False).

    Returns:
    --------
    int
        The total population within the specified age range.

    Example:
    --------
    population(2021, "FE", [7, 23], "JPN", graph=True)
    """
    first_term = "SP"
    second_term = "POP"
    if sex == "MA":
        age_ranges = generateageranges(first_term, second_term, age_range, "MA", place, f"{year}-01-01")
        agearrayspecific, popvalues = interpprep(age_ranges)
        age_array_all_years = interpfunc(popvalues, agearrayspecific, place, year, graph_values = graph)
        sliced_popvals = age_array_all_years[age_range[0]:age_range[1]]
        finaloutput = np.sum(sliced_popvals)
        if finaloutput<2000:
            return "No data for this year"
        return finaloutput
    else:
        age_ranges = generateageranges(first_term, second_term, age_range, "FE", place, f"{year}-01-01")
        agearrayspecific, popvalues = interpprep(age_ranges)
        age_array_all_years = interpfunc(agearrayspecific, popvalues, place, year, graph_values = graph)
        sliced_popvals = age_array_all_years[age_range[0]:age_range[1]]
        finaloutput = np.sum(sliced_popvals)
        if finaloutput<2000:
            return "No data for this year"
        return finaloutput
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

