The project allows to choose the right electricity pricing plan based on hostorical usage data.
How to run it:
1. Login into you Electricity company account and download historical usage data to produce a csv with the following columns: Date, Period start (hour of the day), Consumption in kwh (see the sample_data.csv in data folder)
2. Put this file into data folder (either override sample_data.csv or adjust the file name in electricity_pricing.py
3. The current plans are hard-coded as per Cellcom company pricing offers. Feel free to modify the code to match your preferred company plans.
4. Run   electricity_pricing.py

Sample output:
Pricing Plan Costs:
Total cost without discounts: $668.91
Flat-rate discount cost: $635.46
Weekday morning discount cost: $654.40
Afternoon discount cost: $631.33
Night discount cost: $638.13
