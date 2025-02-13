import unittest
import pandas as pd

class TestMSEAData(unittest.TestCase):

    def test_merge_population_agriculture(self):
        """Test if the population and agriculture data are correctly merged on the 'Year' column"""

        # Mock population data
        total_population_data = {
            'Year': pd.to_datetime(['1960-01-01', '1961-01-01', '1962-01-01', '1963-01-01', '1964-01-01']),
            'Total Population': [126695739.0, 130362248.0, 134152970.0, 138061414.0, 142098093.0]
        }

        # Mock agriculture data
        total_crop_data = {
            'Year': pd.to_datetime(['1960-01-01', '1961-01-01', '1962-01-01', '1963-01-01', '1964-01-01']),
            'Total Crop Production Index': [0.00, 200.60, 204.88, 199.19, 198.19]
        }

        # Creating DataFrames
        total_population_df = pd.DataFrame(total_population_data)
        total_crop_df = pd.DataFrame(total_crop_data)

        # Merging DataFrames on 'Year'
        combined_df = total_population_df.merge(total_crop_df, on='Year', how='inner')

        # Test if the DataFrame has the expected columns
        expected_columns = ['Year', 'Total Population', 'Total Crop Production Index']
        self.assertTrue(all(col in combined_df.columns for col in expected_columns), "One or more columns are missing.")

        # Test if the merge worked correctly by checking the values in the merged DataFrame
        self.assertEqual(combined_df.loc[0, 'Total Population'], 126695739.0, "Total Population value is incorrect for 1960.")
        self.assertEqual(combined_df.loc[0, 'Total Crop Production Index'], 0.00, "Crop Production Index value is incorrect for 1960.")

    def test_display_first_rows(self):
        """Test if the first few rows of the merged data are displayed correctly"""
        
        # Mock population data
        total_population_data = {
            'Year': pd.to_datetime(['1960-01-01', '1961-01-01', '1962-01-01', '1963-01-01', '1964-01-01']),
            'Total Population': [126695739.0, 130362248.0, 134152970.0, 138061414.0, 142098093.0]
        }

        # Mock agriculture data
        total_crop_data = {
            'Year': pd.to_datetime(['1960-01-01', '1961-01-01', '1962-01-01', '1963-01-01', '1964-01-01']),
            'Total Crop Production Index': [0.00, 200.60, 204.88, 199.19, 198.19]
        }

        # Creating DataFrames
        total_population_df = pd.DataFrame(total_population_data)
        total_crop_df = pd.DataFrame(total_crop_data)

        # Merging DataFrames on 'Year'
        combined_df = total_population_df.merge(total_crop_df, on='Year', how='inner')

        # Check if the first row of data displays correctly
        first_rows = combined_df.head(2)
        self.assertEqual(first_rows.shape[0], 2, "The first rows are not displayed correctly.")
        
        # Verify the presence of columns
        self.assertIn('Total Population', first_rows.columns, "Column 'Total Population' is missing.")
        self.assertIn('Total Crop Production Index', first_rows.columns, "Column 'Total Crop Production Index' is missing.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
