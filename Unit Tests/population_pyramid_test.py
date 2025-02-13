import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch
from Deliverables import plot_population_pyramid

class TestPlotPopulationPyramid(unittest.TestCase):

    @patch("matplotlib.pyplot.show")  # Mock plt.show() to avoid displaying the plot
    def test_valid_population_pyramid(self, mock_show):
        # Create mock data in expected format
        age_bins = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", 
                    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
        
        columns = [f"Male {bin}" for bin in age_bins] + [f"Female {bin}" for bin in age_bins]
        index = pd.MultiIndex.from_tuples([("USA", "2025-01-01")], names=["Country", "Date"])
        
        # Mock population values
        data = np.random.randint(1000000, 5000000, size=(1, len(columns)))  # Random values in millions
        
        df = pd.DataFrame(data, index=index, columns=columns)

        # Call the function (should not raise errors)
        plot_population_pyramid(df, "USA", "2025-01-01")

        # Ensure plt.show() was called (meaning plotting was attempted)
        mock_show.assert_called_once()

    def test_missing_data(self):
        df = pd.DataFrame()  # Empty DataFrame

        # Expecting a KeyError but should not crash
        with self.assertLogs() as log:
            plot_population_pyramid(df, "USA", "2025-01-01")
        
        # Ensure error message is printed
        self.assertIn("Data not available for USA on 2025-01-01", log.output[0])

if __name__ == "__main__":
    unittest.main()
