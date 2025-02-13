import unittest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from unittest.mock import patch
from Deliverables import animated_population_pyramid_wide 

class TestAnimatedPopulationPyramidWide(unittest.TestCase):

    @patch("plotly.graph_objects.Figure.show")  # Mock Plotly show() to avoid rendering
    def test_valid_animation(self, mock_show):
        # Create mock data
        age_bins = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", 
                    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
        columns = [f"Male {bin}" for bin in age_bins] + [f"Female {bin}" for bin in age_bins]
        
        index = pd.MultiIndex.from_tuples(
            [("USA", "2000-01-01"), ("USA", "2005-01-01"), ("USA", "2010-01-01")],
            names=["country", "date"]
        )
        
        # Generate random population data
        data = np.random.randint(1000000, 5000000, size=(len(index), len(columns)))

        df = pd.DataFrame(data, index=index, columns=columns)

        # Call the function
        fig = animated_population_pyramid_wide(df, "USA", animate_by="year")

        # Ensure the function returns a Plotly Figure
        self.assertIsInstance(fig, go.Figure)

    def test_invalid_animate_by(self):
        # Create an empty DataFrame
        df = pd.DataFrame()

        with self.assertRaises(ValueError) as context:
            animated_population_pyramid_wide(df, "USA", animate_by="invalid_option")

        self.assertEqual(str(context.exception), "animate_by must be either 'year' or 'date'.")

if __name__ == "__main__":
    unittest.main()
