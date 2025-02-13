import unittest
import wbdata
import pandas as pd
import warnings

class TestMSEAData(unittest.TestCase):

    def test_msea_data(self):
        """Test if the MSEA data includes the expected countries."""
        
        # List of countries we expect to have data for
        expected_countries = ["Brunei Darussalam", "Indonesia", "Malaysia", "Papua New Guinea", "Philippines", "Timor-Leste"]
        
        # Fetch the population data for the specified countries
        variable_labels = {
            "SP.POP.TOTL": "Total Population",
            "SP.POP.TOTL.FE.IN": "Total Female",
            "SP.POP.TOTL.MA.IN": "Total Male",
            "SP.RUR.TOTL": "Total Rural",
            "SP.URB.TOTL": "Total Urban"
        }
        
        countries = {
            "BRN": "Brunei Darussalam",
            "IDN": "Indonesia",
            "MYS": "Malaysia",
            "PNG": "Papua New Guinea",
            "PHL": "Philippines",
            "TLS": "Timor-Leste"
        }
        
        # Fetch the data
        MSEA_pop = wbdata.get_dataframe(variable_labels, country=countries, parse_dates=True)
        
        # Ensure that MSEA_pop is a DataFrame
        self.assertIsInstance(MSEA_pop, pd.DataFrame)
        
        # Reset the index to ensure country names are in the columns
        MSEA_pop = MSEA_pop.reset_index()
        
        # Check if the countries appear in the rows (as index or columns)
        country_columns = MSEA_pop['country'].unique()  # Get the unique country names from the 'country' column
        
        # Ensure all expected countries are in the country list
        for country in expected_countries:
            self.assertTrue(country in country_columns, f"{country} not found in the data.")
        
        print("Test Passed: All expected countries are found in the data.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)