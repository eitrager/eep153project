import pandas as pd
import numpy as np
import plotly.express as px
import wbdata
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import geopandas as gpd
pd.options.plotting.backend = "plotly"
import wbdata
import warnings
import plotly.colors as pc

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
    interpolated_values = np.interp(age_range, midpoint_selection, bucketed_vals)
    #optional graph
    if graph_values:
        popdf = pd.DataFrame({'Age': age_range, 'Population': interpolated_values})
        fig = px.line(popdf, x='Age', y='Population', title=f'Population Interpolation by Age for {country} in Year {year}')
        fig.show()
    return interpolated_values
def generate_graphs(lifedf, variable_labels):
    """
    Generate time-series graphs using Plotly, where each line represents a country,
    and each graph corresponds to a different statistic.

    Parameters:
        lifedf (DataFrame): DataFrame with life-related statistics.
        variable_labels (dict): Mapping of column names to descriptive labels.
    """
    for variable, label in variable_labels.items():
        fig = go.Figure()
        # quick check for existing variable
        if variable not in lifedf.columns:
            print(f"Skipping {variable}: Not found in DataFrame")
            continue
        for country in lifedf[variable].columns:
            data = lifedf[variable][country].dropna()  # Remove NaNs
            #adding country specific lines
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=data.values, 
                mode='lines+markers', 
                name=country
            ))
        fig.update_layout(
            title=f"{label} Over Time",
            xaxis_title="Year",
            yaxis_title="Value",
            legend_title="Country"
        )

        # Show the figure
        fig.show()

def overlay_population(country_name, df):
    """
    Function to overlay female and male population for a given country.

    Parameters:
    - country_name (str): The name of the country whose data will be plotted.
    - df (pd.DataFrame): The DataFrame containing the population data with MultiIndex columns.

    Returns:
    - A Plotly figure with the overlayed female and male population data.
    """
    
    # Check if the country exists in the subcolumns
    if country_name not in df.columns.get_level_values('country'):
        print(f"Country '{country_name}' not found in the dataset.")
        return
    
    # Extract the female and male population data for the country
    female = df[('Total Female', country_name)]
    male = df[('Total Male', country_name)]
    
    # Create a figure
    fig = go.Figure()
    
    # Add the female population plot
    fig.add_trace(go.Scatter(x=female.index, y=female, mode='lines+markers', name='Female', line=dict(dash='dash', color='blue')))
    
    # Add the male population plot
    fig.add_trace(go.Scatter(x=male.index, y=male, mode='lines+markers', name='Male', line=dict(dash='solid', color='red')))
    
    # Add title and labels
    fig.update_layout(title=f"Total Female and Male Population Over Time ({country_name})",
                      xaxis_title="Year",
                      yaxis_title="Population")
    
    # Show the plot
    fig.show()

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
        acronymfinder("United")
        # Output:
        # United Arab Emirates: ARE
        # United Kingdom: GBR
        # United States: USA
        
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

def overlay_population_multi(countries, df):
    """
    Function to overlay urban and rural population for multiple countries with distinct colors.

    Parameters:
    - countries (list): A list of country names to be plotted.
    - df (pd.DataFrame): The DataFrame containing the population data with MultiIndex columns.

    Returns:
    - A Plotly figure with the overlaid urban and rural population data for multiple countries.
    """

    fig = go.Figure()
    
    # Generate a list of distinct colors
    colors = pc.qualitative.Set1  # or try Set2, Dark2 for different palettes
    num_colors = len(colors)
    
    for i, country in enumerate(countries):
        if country not in df.columns.get_level_values('country'):
            print(f"Country '{country}' not found in the dataset.")
            continue
        
        # Extract the rural and urban population data for the country
        rural = df[('Total Rural', country)]
        urban = df[('Total Urban', country)]
        
        # Assign a unique color to each country (cycling through if more countries than colors)
        color = colors[i % num_colors]
        
        # Add the rural population plot (dashed line)
        fig.add_trace(go.Scatter(
            x=rural.index, y=rural, mode='lines', 
            name=f'Rural - {country}', line=dict(dash='dash', color=color)
        ))
        
        # Add the urban population plot (solid line)
        fig.add_trace(go.Scatter(
            x=urban.index, y=urban, mode='lines', 
            name=f'Urban - {country}', line=dict(dash='solid', color=color)
        ))

    # Add title and labels
    fig.update_layout(
        title="Total Rural and Urban Population Over Time",
        xaxis_title="Year",
        yaxis_title="Population",
        legend_title="Legend"
    )

    # Show the plot
    fig.show()
def plot_rural_urban_ratio(countries, df):
    """
    Function to plot the proportion of rural to urban population for multiple countries with distinct colors.

    Parameters:
    - countries (list): A list of country names to be plotted.
    - df (pd.DataFrame): The DataFrame containing the population data with MultiIndex columns.

    Returns:
    - A Plotly figure with the proportion of rural to urban population over time for multiple countries.
    """

    fig = go.Figure()
    
    # Generate a list of distinct colors
    colors = pc.qualitative.Set1  # or try Set2, Dark2 for different palettes
    num_colors = len(colors)
    
    for i, country in enumerate(countries):
        if country not in df.columns.get_level_values('country'):
            print(f"Country '{country}' not found in the dataset.")
            continue
        
        # Extract the rural and urban population data for the country
        rural = df[('Total Rural', country)]
        urban = df[('Total Urban', country)]
        
        # Avoid division by zero
        rural_urban_ratio = rural / urban.replace(0, float('nan'))  # Replace 0 to prevent errors
        
        # Assign a unique color to each country (cycling through if more countries than colors)
        color = colors[i % num_colors]
        
        # Add the proportion plot
        fig.add_trace(go.Scatter(
            x=rural.index, 
            y=rural_urban_ratio, 
            mode='lines', 
            name=f'{country} (Rural/Urban)', 
            line=dict(color=color)
        ))

    # Add title and labels
    fig.update_layout(
        title="Rural to Urban Population Ratio Over Time",
        xaxis_title="Year",
        yaxis_title="Rural to Urban Ratio",
        legend_title="Legend",
        yaxis=dict(type='log'),  # Log scale if ratios vary significantly
    )

    # Show the plot
    fig.show()

def overlay_cereal_production_region(df):
    """
    Function to overlay total cereal production over time for the whole region.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame containing the cereal production data.
    
    Returns:
    - A Plotly figure with total cereal production for the region.
    """
    df = df.reset_index()
    # Group data by year and sum the production
    region_df = df.groupby('Date')['Cereal Production (MT)'].sum().reset_index()
    
    # Create a figure
    fig = go.Figure()
    
    # Add the total cereal production plot for the region
    fig.add_trace(go.Scatter(x=region_df['Date'], y=region_df['Cereal Production (MT)'], 
                             mode='lines+markers', name="Total Region", 
                             line=dict(dash='solid', color='red')))
    
    # Add title and labels
    fig.update_layout(title="Total Cereal Production Over Time (Region)",
                      xaxis_title="Year",
                      yaxis_title="Cereal Production (MT)")
    
    # Show the plot
    fig.show()
def plot_popvcereal(df, country):
    """
    Plots an overlayed line plot of total population growth and cereal production over time for a given country.
    
    :param df: DataFrame containing agricultural and population data.
    :param country: String representing the country to plot.
    """
    # Convert 'Date' column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])

    # Extract Year from the Date column
    df["Year"] = df["Date"].dt.year

    # Ensure Year is the index
    df = df.set_index("Year")

    # Convert index to integer (if it's not already)
    df.index = df.index.astype(int)

    # Filter data for the selected country
    country_data = df[df['Country'] == country]

    # Create figure and primary y-axis
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Total Population", color='tab:blue')
    ax1.plot(country_data.index, country_data["Total Population"], color='tab:blue', label='Total Population')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for cereal production
    ax2 = ax1.twinx()
    ax2.set_ylabel("Cereal Production (MT)", color='tab:green')
    ax2.plot(country_data.index, country_data["Cereal Production (MT)"], color='tab:green', linestyle='dashed', label='Cereal Production')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    # Set x-axis limits
    ax1.set_xlim(1960, df.index.max())

    # Improve x-axis tick formatting (showing every 10 years)
    plt.xticks(range(1960, df.index.max() + 1, 10), rotation=45)

    # Set title
    fig.suptitle(f"{country}: Population Growth vs. Cereal Production")
    fig.tight_layout()
    
    plt.show()
# ^^individual overlayed plot for population and cereal production

def plot_popvcereal_interactive(df, countries):
    """
    Creates an interactive overlayed line plot of total population growth and cereal production 
    over time for multiple countries, assigning a unique color per country.

    :param df: DataFrame containing agricultural and population data
    :param countries: List of strings representing the countries to plot
    """
    
    fig = go.Figure()

    # Convert 'Date' column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])
    
    # Extract the Year from Date
    df["Year"] = df["Date"].dt.year

    # Define a color palette for different countries
    color_palette = [
        'blue', 'orange', 'green', 'red', 'purple', 'pink', 'brown', 'gray'
    ]
    
    country_colors = {country: color_palette[i % len(color_palette)] for i, country in enumerate(countries)}

    # Loop through each country and add two traces (Population & Cereal Production)
    for country in countries:
        country_data = df[df['Country'] == country]

        # Filter data to start from 1960 onwards
        country_data = country_data[country_data["Year"] >= 1960]

        color = country_colors[country]  # Assign unique color

        # Total Population Line (Primary Y-Axis, Solid)
        fig.add_trace(go.Scatter(
            x=country_data["Year"],  
            y=country_data["Total Population"],
            mode='lines',
            name=f"{country} - Population",
            line=dict(color=color, width=2),
            yaxis='y1',  # Assigns to primary y-axis
        ))

        # Cereal Production Line (Secondary Y-Axis, Dashed)
        fig.add_trace(go.Scatter(
            x=country_data["Year"],  
            y=country_data["Cereal Production (MT)"],
            mode='lines',
            name=f"{country} - Cereal Production",
            line=dict(color=color, dash='dot', width=2),
            yaxis='y2',  # Assigns to secondary y-axis
        ))

    # Layout adjustments for interactivity and readability
    fig.update_layout(
        title="Total Population vs. Cereal Production Over Time",
        xaxis=dict(title="Year", range=[1960, df["Year"].max()]),  # Ensure x-axis starts at 1960
        yaxis=dict(title="Total Population", color='black'),
        yaxis2=dict(
            title="Cereal Production (MT)",
            overlaying='y',  # Overlay second y-axis on the same plot
            side='right',
            color='black'
        ),
        legend=dict(title="Click to Toggle", orientation="h"),  # Interactive legend
    )

    # Show interactive plot
    fig.show()

def generate_all_visualizations(countrydict, regionstring):
    """
    Generate and display multiple visualizations of agricultural production and population metrics
    for the specified countries and region.

    This function performs the following steps:
      1. Displays a markdown header indicating the region for which the graphs are being generated.
      2. Retrieves agricultural production data from the World Bank API using predefined variable labels,
         cleans and preprocesses the data, and prepares it for visualization.
      3. Retrieves population data (including total, female, male, rural, and urban population figures)
         from the World Bank API and restructures the data for plotting.
      4. Generates a series of plots:
                - A line plot showing "Total Population Over Time" for the region.
                - Overlaid population plots comparing urban and rural populations (via the `function`overlay_population_multi`).
                - A plot displaying the rural to urban population ratio (via the function `plot_rural_urban_ratio`).
                - Individual plots comparing population vs. cereal production for each country (via the function `plot_popvcereal`).
                - An interactive plot comparing population vs. cereal production across all countries
                  (via the function `plot_popvcereal_interactive`).

    Parameters
    ----------
    countrydict : dict
        A dictionary mapping World Bank country codes to their corresponding country names.
        Example:
            {
                "BGD": "Bangladesh",
                "BTN": "Bhutan",
                "IND": "India",
                "MDV": "Maldives",
                "NPL": "Nepal",
                "PAK": "Pakistan",
                "LKA": "Sri Lanka",
                "TSA": "South Asia (IDA & IBRD)"
            }
    regionstring : str
        A string representing the region name (e.g., 'South Asia') used in plot titles and headers.

    Returns
    -------
    None
        This function displays several visualizations and does not return any value.

    Notes
    -----
    - This function assumes that helper functions such as `overlay_population_multi`,
      `plot_rural_urban_ratio`, `plot_popvcereal`, and `plot_popvcereal_interactive` are defined
      in the scope.
    - Data is fetched using the `wbdata` package and is cleaned to remove missing values for key metrics.
    - The visualizations are displayed inline, typically within a Jupyter Notebook environment.
    
    Example
    -------
    >>> countries = {
            "BGD": "Bangladesh",
            "BTN": "Bhutan",
            "IND": "India",
            "MDV": "Maldives",
            "NPL": "Nepal",
            "PAK": "Pakistan",
            "LKA": "Sri Lanka",
            "TSA": "South Asia (IDA & IBRD)"
        }
    >>> generate_all_visualizations(countries, 'South Asia')
    """
    display(Markdown(f"## Relevant Deliverable Graphs for {regionstring}"))
    # making and prepping the df
    variable_labels_ag = {"AG.PRD.CREL.MT":"Cereal Production (MT)",
                   "AG.PRD.CROP.XD":"Crop Production Index",
                  "AG.PRD.FOOD.XD":"Food Production Index",
                   'SP.RUR.TOTL': 'Total Rural Population',
                   "SP.POP.TOTL":"Total Population"
                  # "EA.PRD.AGRI.KD":"Agricultural Value Added per Worker"
                  }
    SA_ag = wbdata.get_dataframe(variable_labels_ag, country = countrydict,parse_dates=True)
    SA_ag = SA_ag.reset_index()
    SA_ag = SA_ag.rename(columns={'date': 'Date', 'country':'Country'})
    SA_ag = SA_ag.set_index(['Date']).sort_index()
    SA_ag = SA_ag.dropna(subset=["Cereal Production (MT)", "Crop Production Index", "Food Production Index", 
                                "Total Rural Population", 'Total Population'])
    variable_labels_pop = {"SP.POP.TOTL":"Total Population", 
                   "SP.POP.TOTL.FE.IN":"Total Female",
                  "SP.POP.TOTL.MA.IN":"Total Male",
                  "SP.RUR.TOTL":"Total Rural",
                  "SP.URB.TOTL":"Total Urban"}
    SA_pop = wbdata.get_dataframe(variable_labels_pop, country = countrydict, parse_dates=True).squeeze()
    SA_pop = SA_pop.unstack('country')
    SA_pop = SA_pop.rename(columns={'date': 'Date'})
    SA_ag=SA_ag.reset_index()
    # pop graph
    SA_total = SA_pop["Total Population"]
    ploted = SA_total.plot(title=f"Total Population Over Time ({regionstring})")
    ploted.show()
    #population overlay multi urban rural
    listed_items = np.array(list(countrydict.values()))
    overlay_population_multi(listed_items, SA_pop)
    #rural urban ratio
    plot_rural_urban_ratio(listed_items, SA_pop)
    #individual pop vs cereal graphs
    for country in listed_items:
        plot_popvcereal(SA_ag, country)
    # all pop vs cereal graphs
    plot_popvcereal_interactive(SA_ag, listed_items)