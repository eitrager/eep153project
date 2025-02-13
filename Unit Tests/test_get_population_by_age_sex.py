import unittest
import pandas as pd
from unittest.mock import patch
from Deliverables import get_population_by_age_sex  # Assuming your function is in deliverable_file.py

class TestGetPopulationByAgeSex(unittest.TestCase):

    @patch('deliverable_file.wbdata.get_dataframe')
    def test_valid_country_code(self, mock_wbdata):
        """Test fetching population data for a valid country code."""
        mock_data = pd.DataFrame({
            'Male 0-4': [500000, 520000],
            'Female 0-4': [480000, 500000]
        }, index=[('USA', 2020), ('USA', 2021)])

        mock_wbdata.return_value = mock_data

        result = get_population_by_age_sex(['USA'])
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (2, 2))  # Expecting 2 rows, 2 columns
        self.assertIn('Male 0-4', result.columns)
        self.assertIn('Female 0-4', result.columns)

    @patch('deliverable_file.wbdata.get_dataframe')
    def test_valid_multiple_countries(self, mock_wbdata):
        """Test fetching population data for multiple countries."""
        mock_data = pd.DataFrame({
            'Male 0-4': [500000, 520000, 300000],
            'Female 0-4': [480000, 500000, 290000]
        }, index=[('USA', 2020), ('USA', 2021), ('CAN', 2020)])

        mock_wbdata.return_value = mock_data

        result = get_population_by_age_sex(['USA', 'CAN'])
        self.assertEqual(len(result), 3)  # 3 rows for USA & CAN

    @patch('deliverable_file.wbdata.get_dataframe')
    def test_invalid_country_code(self, mock_wbdata):
        """Test function with an invalid country code."""
        mock_wbdata.return_value = pd.DataFrame()

        result = get_population_by_age_sex(['XXX'])  # Assuming 'XXX' is invalid
        self.assertTrue(result.empty)

    @patch('deliverable_file.wbdata.get_dataframe')
    def test_empty_country_list(self, mock_wbdata):
        """Test function with an empty country list."""
        mock_wbdata.return_value = pd.DataFrame()

        result = get_population_by_age_sex([])
        self.assertTrue(result.empty)

    @patch('deliverable_file.wbdata.get_dataframe')
    def test_country_all_option(s
