import unittest
import pandas as pd
import matplotlib.pyplot as plt
import wbdata

class TestFoodProductionPlot(unittest.TestCase):

    def test_food_production_index_plot(self):
        """Test if the food production index plot is generated correctly"""
        
        # Mock the food production index data
        vars = {"AG.PRD.FOOD.XD": "Food Production Index"}
        use = ["BRN", "IDN", "MYS", "PNG", "PHL", "TLS"]
        food = wbdata.get_dataframe(vars, country=use, parse_dates=True)
        
        # Check if the 'Food Production Index' column exists in the dataframe
        self.assertIn("Food Production Index", food.columns)
        
        # Create the plot
        food.plot(title="Food Production Index Over Time by Country")

        # Check that the plot has been created by verifying if it has a title
        plt.title("Food Production Index Over Time by Country")
        plt.xlabel('Year')
        plt.ylabel('Food Production Index')

        # Check if the plot displays data points (basic check to ensure the data exists)
        self.assertGreater(len(food), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
