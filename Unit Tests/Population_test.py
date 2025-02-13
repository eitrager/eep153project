import unittest
import numpy as np
from deliverable import population  # Assuming `population` is in deliverable_file.py

class TestPopulationFunction(unittest.TestCase):
    
    def test_valid_population_male(self):
        """Test valid population retrieval for males."""
        result = population(2025, "MA", [10, 20], "USA")
        self.assertIsInstance(result, int)  # Expected output should be an integer
    
    def test_valid_population_female(self):
        """Test valid population retrieval for females."""
        result = population(2025, "FE", [5, 18], "JPN")
        self.assertIsInstance(result, int)  # Expected output should be an integer

    def test_no_data_available(self):
        """Test case where no data is available (returning a string)."""
        result = population(1800, "MA", [0, 10], "CHN")  # Assuming data does not exist for 1800
        self.assertEqual(result, "No data for this year")

    def test_invalid_sex_input(self):
        """Test invalid sex input (should raise an error)."""
        with self.assertRaises(ValueError):
            population(2025, "INVALID", [10, 20], "USA")

    def test_invalid_year_input(self):
        """Test invalid year input (should raise an error)."""
        with self.assertRaises(TypeError):
            population("year", "MA", [5, 20], "USA")  # Year should be an integer

    def test_invalid_age_range(self):
        """Test invalid age range (negative or incorrect format)."""
        with self.assertRaises(ValueError):
            population(2025, "FE", [-5, 10], "USA")  # Negative age is not valid
        
        with self.assertRaises(ValueError):
            population(2025, "FE", [30], "USA")  # Age range should be two values

    def test_invalid_country_code(self):
        """Test invalid country code (should raise an error)."""
        with self.assertRaises(ValueError):
            population(2025, "MA", [0, 10], "INVALID")  # Country codes should be 3 letters

    def test_graph_argument(self):
        """Test the function when graph argument is True (should still return an integer)."""
        result = population(2025, "MA", [10, 20], "USA", graph=True)
        self.assertIsInstance(result, int)

if __name__ == '__main__':
    unittest.main()
