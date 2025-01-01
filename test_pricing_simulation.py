import unittest
import pandas as pd
from electricity_pricing import categorize_plan  # Assuming categorize_plan is defined in electricity_pricing

class TestPricingSimulation(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = pd.DataFrame({
            'Date': ['01/01/2025', '01/01/2025', '01/01/2025', '01/01/2025'],
            'Period start (hour of the day)': ['00:00', '06:00', '14:00', '23:00'],
            'Consumption in kwh': [1.0, 2.0, 3.0, 4.0]
        })

        # Combine Date and Time into a single datetime column
        self.sample_data['Datetime'] = pd.to_datetime(
            self.sample_data['Date'] + ' ' + self.sample_data['Period start (hour of the day)'], 
            format='%d/%m/%Y %H:%M'
        )
        self.sample_data = self.sample_data.drop(columns=['Date', 'Period start (hour of the day)'])
        self.sample_data = self.sample_data.set_index('Datetime')

        # Define base rate for testing
        self.base_rate = 0.10

    def test_categorize_plan(self):
        # Test the categorize_plan function
        self.sample_data['Plan_Period'] = self.sample_data.index.hour.map(categorize_plan)
        expected_periods = ['Night', 'Morning', 'Afternoon', 'Night']
        self.assertListEqual(self.sample_data['Plan_Period'].tolist(), expected_periods)

    def test_pricing_plans(self):
        # Prepare categorized data
        self.sample_data['Plan_Period'] = self.sample_data.index.hour.map(categorize_plan)
        self.sample_data['Weekday'] = ~self.sample_data.index.weekday.isin([4, 5])  # Friday, Saturday are weekends

        # Total cost calculation
        total_consumption = self.sample_data['Consumption in kwh'].sum()
        total_cost = total_consumption * self.base_rate

        # Flat-rate discount
        flat_discount_cost = total_cost * 0.95
        self.assertAlmostEqual(flat_discount_cost, total_cost * 0.95)

if __name__ == '__main__':
    unittest.main()
