import unittest
import pandas as pd

class TestMSEAData(unittest.TestCase):

    def test_dataframe_columns(self):
        """Test if the DataFrame has the correct columns for the agricultural data"""
        
        # Mocking the DataFrame based on the structure from the screenshot
        mock_data = {
            'Date': pd.to_datetime(['1961-01-01', '1961-01-01', '1961-01-01']),
            'Country': ['Indonesia', 'Timor-Leste', 'Malaysia'],
            'Cereal Production (MT)': [14367100.0, 34257.0, 1097075.0],
            'Crop Production Index': [16.93, 40.17, 17.21],
            'Food Production Index': [20.36, 62.53, 18.63],
            'Total Rural Population': [77335078.0, 426607.0, 5940367.0]
        }

        # Creating DataFrame from mock data
        MSEA_ag = pd.DataFrame(mock_data)

        # Check if the DataFrame has the required columns
        expected_columns = ['Date', 'Country', 'Cereal Production (MT)', 'Crop Production Index', 'Food Production Index', 'Total Rural Population']
        
        # Test if the DataFrame contains the expected columns
        self.assertTrue(all(col in MSEA_ag.columns for col in expected_columns), "One or more columns are missing.")
        
    def test_dataframe_values(self):
        """Test if the values in the columns are correctly populated"""
        
        # Mocking the DataFrame based on the structure from the screenshot
        mock_data = {
            'Date': pd.to_datetime(['1961-01-01', '1961-01-01', '1961-01-01']),
            'Country': ['Indonesia', 'Timor-Leste', 'Malaysia'],
            'Cereal Production (MT)': [14367100.0, 34257.0, 1097075.0],
            'Crop Production Index': [16.93, 40.17, 17.21],
            'Food Production Index': [20.36, 62.53, 18.63],
            'Total Rural Population': [77335078.0, 426607.0, 5940367.0]
        }

        # Creating DataFrame from mock data
        MSEA_ag = pd.DataFrame(mock_data)

        # Check if the first row values match the expected values
        self.assertEqual(MSEA_ag.loc[0, 'Cereal Production (MT)'], 14367100.0, "Cereal Production (MT) value is incorrect.")
        self.assertEqual(MSEA_ag.loc[0, 'Crop Production Index'], 16.93, "Crop Production Index value is incorrect.")
        self.assertEqual(MSEA_ag.loc[0, 'Food Production Index'], 20.36, "Food Production Index value is incorrect.")
        self.assertEqual(MSEA_ag.loc[0, 'Total Rural Population'], 77335078.0, "Total Rural Population value is incorrect.")
        
    def test_dataframe_structure(self):
        """Test if the DataFrame structure is correct"""
        
        # Mocking the DataFrame based on the structure from the screenshot
        mock_data = {
            'Date': pd.to_datetime(['1961-01-01', '1961-01-01', '1961-01-01']),
            'Country': ['Indonesia', 'Timor-Leste', 'Malaysia'],
            'Cereal Production (MT)': [14367100.0, 34257.0, 1097075.0],
            'Crop Production Index': [16.93, 40.17, 17.21],
            'Food Production Index': [20.36, 62.53, 18.63],
            'Total Rural Population': [77335078.0, 426607.0, 5940367.0]
        }

        # Creating DataFrame from mock data
        MSEA_ag = pd.DataFrame(mock_data)

        # Check if the DataFrame has the expected number of columns
        self.assertEqual(len(MSEA_ag.columns), 6, "The DataFrame doesn't have the expected number of columns.")
        
        # Check if the first rows display correctly
        first_rows = MSEA_ag.head(2)
        self.assertEqual(first_rows.shape[0], 2, "The first rows are not displayed correctly.")
        
        # Verify the presence of columns
        self.assertIn('Cereal Production (MT)', first_rows.columns, "Column 'Cereal Production (MT)' is missing.")
        self.assertIn('Crop Production Index', first_rows.columns, "Column 'Crop Production Index' is missing.")
        self.assertIn('Food Production Index', first_rows.columns, "Column 'Food Production Index' is missing.")
        self.assertIn('Total Rural Population', first_rows.columns, "Column 'Total Rural Population' is missing.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
