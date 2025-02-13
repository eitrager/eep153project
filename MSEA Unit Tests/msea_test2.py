import unittest
import pandas as pd

class TestMSEAData(unittest.TestCase):

    def test_total_population_calculation(self):
        """Test if the total population is calculated correctly for MSEA"""
        
        # Simulating the MSEA population data with simplified mock data for the purpose of the test
        mock_data = {
            'Year': ['1960', '1961', '1962'],
            'Total Population': [1266957390, 1303622480, 1341529700]
        }
        MSEA_pop = pd.DataFrame(mock_data)
        
        # Calculate total population for the region by summing across all years
        total_population_index = MSEA_pop["Total Population"].sum()
        
        # We know the expected result from mock data (summing the populations of 1960, 1961, 1962)
        expected_total_population = 1266957390 + 1303622480 + 1341529700
        self.assertEqual(total_population_index, expected_total_population)

    def test_dataframe_structure(self):
        """Test if the dataframe has correct columns and is structured properly"""
        
        # Simulating the MSEA population data
        mock_data = {
            'Year': ['1960', '1961', '1962'],
            'Total Population': [1266957390, 1303622480, 1341529700]
        }
        MSEA_pop = pd.DataFrame(mock_data)
        
        # Check if the DataFrame has the expected columns
        self.assertIn('Year', MSEA_pop.columns)
        self.assertIn('Total Population', MSEA_pop.columns)
        
        # Ensure it's a DataFrame
        self.assertIsInstance(MSEA_pop, pd.DataFrame)
        
    def test_display_first_rows(self):
        """Test if the first rows display correctly"""
        
        # Simulating the MSEA population data
        mock_data = {
            'Year': ['1960', '1961', '1962'],
            'Total Population': [1266957390, 1303622480, 1341529700]
        }
        MSEA_pop = pd.DataFrame(mock_data)
        
        # Check if the first 10 rows can be displayed correctly (there are only 3 rows in this mock data)
        displayed_data = MSEA_pop.head(10)
        self.assertEqual(len(displayed_data), 3)  # There are only 3 rows
        self.assertEqual(displayed_data.iloc[0]["Year"], '1960')  # Check the first year is correct

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)