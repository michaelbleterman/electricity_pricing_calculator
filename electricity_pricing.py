import pandas as pd

# Load the data
file_path = r'data/sample_data.csv' # Replace with the actual file path
data = pd.read_csv(file_path)

# Combine Date and Time to create a proper datetime column
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Period start (hour of the day)'], format='%d/%m/%Y %H:%M')
data = data.drop(columns=['Date', 'Period start (hour of the day)'])

# Set the datetime column as the index
data = data.set_index('Datetime')

# Resample data into hourly and daily consumption
hourly_consumption = data['Consumption in kwh'].resample('H').sum()
daily_consumption = data['Consumption in kwh'].resample('D').sum()

# Categorize hours into pricing plan periods
def categorize_plan(hour):
    if 23 <= hour <= 24 or 0 <= hour < 7:  # Night: 23:00 - 07:00
        return 'Night'
    elif 14 <= hour < 20:  # Afternoon: 14:00 - 20:00
        return 'Afternoon'
    elif 7 <= hour < 17:  # Morning: 07:00 - 17:00
        return 'Morning'
    else:
        return 'Other'

hourly_consumption = hourly_consumption.reset_index()
hourly_consumption['Plan_Period'] = hourly_consumption['Datetime'].dt.hour.apply(categorize_plan)

# Adjust weekends to Fridays and Saturdays
hourly_consumption['Weekday'] = ~hourly_consumption['Datetime'].dt.weekday.isin([4, 5])  # True for Sunday to Thursday

# Define the base rate
base_rate = 0.10  # Adjust if needed

# Calculate total cost without discounts
total_cost = daily_consumption.sum() * base_rate

# Plan 1: Flat-rate discount (5%)
flat_discount_cost = total_cost * 0.95

# Plan 2: Weekday morning discount (15%)
weekday_morning = hourly_consumption[
    (hourly_consumption['Plan_Period'] == 'Morning') & hourly_consumption['Weekday']
]
weekday_morning_discount = weekday_morning['Consumption in kwh'].sum() * base_rate * 0.15
weekday_morning_cost = total_cost - weekday_morning_discount

# Plan 3: Afternoon discount (18%)
afternoon = hourly_consumption[hourly_consumption['Plan_Period'] == 'Afternoon']
afternoon_discount = afternoon['Consumption in kwh'].sum() * base_rate * 0.18
afternoon_discount_cost = total_cost - afternoon_discount

# Plan 4: Night discount (20%)
night = hourly_consumption[hourly_consumption['Plan_Period'] == 'Night']
night_discount = night['Consumption in kwh'].sum() * base_rate * 0.20
night_discount_cost = total_cost - night_discount

# Print results
print("Pricing Plan Costs:")
print(f"Total cost without discounts: ${total_cost:.2f}") 
print(f"Flat-rate discount cost: ${flat_discount_cost:.2f}")
print(f"Weekday morning discount cost: ${weekday_morning_cost:.2f}")
print(f"Afternoon discount cost: ${afternoon_discount_cost:.2f}")
print(f"Night discount cost: ${night_discount_cost:.2f}")

# Validation with typical days
#print("\nValidation with Typical Days:")
#for day, group in hourly_consumption.groupby(hourly_consumption['Datetime'].dt.date):
#    daily_cost = group['Consumption in kwh'].sum() * base_rate
#    morning_cost = group[(group['Plan_Period'] == 'Morning') & group['Weekday']]['Consumption in kwh'].sum() * base_rate * 0.85
#    afternoon_cost = group[group['Plan_Period'] == 'Afternoon']['Consumption in kwh'].sum() * base_rate * 0.82
#    night_cost = group[group['Plan_Period'] == 'Night']['Consumption in kwh'].sum() * base_rate * 0.80
#    print(f"Date: {day} | Flat: ${daily_cost * 0.95:.2f}, Morning: ${morning_cost:.2f}, Afternoon: ${afternoon_cost:.2f}, Night: ${night_cost:.2f}")
