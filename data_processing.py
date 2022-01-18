# Import necessary modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load & describe dataset
df = pd.read_csv('data_set.csv')
print(df['order_amount'].describe())
# Notice that the stdev is much larger than the mean

################################################################################

# Method 1: Since this is a heavily right (positively) skewed distribution, use the inter-quartile range (IQR) rule on order_amount
percentile25 = df['order_amount'].quantile(0.25)
percentile75 = df['order_amount'].quantile(0.75)

# Set upper and lower limits based on the IQR
iqr = percentile75 - percentile25
upper_limit = percentile75 + 1.5 * iqr
lower_limit = max(percentile25 - 1.5 * iqr, 0)

print('iqr:', iqr)
print('upperlimit:', upper_limit)
print('lower_limit:', lower_limit)

# Create copy of dataset, exclude points outside the previously defined limits
iqr_df = df[df['order_amount'] < upper_limit]
iqr_df = iqr_df[iqr_df['order_amount'] > lower_limit]

# Plot raw data versus IQR-processed data
plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(df['order_amount'])
plt.subplot(2,2,2)
sns.boxplot(x=df['order_amount'])

plt.subplot(2,2,3)
sns.distplot(iqr_df['order_amount'])
plt.subplot(2,2,4)
sns.boxplot(x=iqr_df['order_amount'])
plt.show()

# Take newly calculated average order value with outliers according to IQR rule excluded
print(iqr_df['order_amount'].describe())

################################################################################

# Method 2: Use IQR on total_items


# Method 3: Use IQR on shoe value


# Method 4: Combine filters from Methods 2 and 3


# Method 5: Determine 3 averages (central tendencies)
mode = df['order_amount'].mode()[0]
median = df['order_amount'].median()
mean = df['order_amount'].mean()

print("mode:", mode, "\nmedian:", median, "\nmean:", mean)

# Method 6: Manually filter out orders I think are suspicious