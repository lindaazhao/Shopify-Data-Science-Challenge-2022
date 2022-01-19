# Import necessary modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load & describe dataset
df = pd.read_csv('data_set.csv')
print('Order_Amount Column Description:\n', df['order_amount'].describe(), sep = '')
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
iqr_df = df[df['order_amount'] <= upper_limit]
iqr_df = iqr_df[iqr_df['order_amount'] >= lower_limit]

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
plt.suptitle('IQR on order_amount')
plt.show()

# Take newly calculated average order value with outliers according to IQR rule excluded
print('\nOrder_Amount Processed with Method 1:\n', iqr_df['order_amount'].describe(), sep='')


################################################################################
# Method 2: Use IQR on total_items
p25_2 = df['total_items'].quantile(0.25)
p75_2 = df['total_items'].quantile(0.75)

# Set upper and lower limits based on the IQR
iqr_2 = p75_2 - p25_2
upper_limit_2 = p75_2 + 1.5 * iqr_2
lower_limit_2 = max(p25_2 - 1.5 * iqr_2, 0)

print('iqr:', iqr_2)
print('upperlimit:', upper_limit_2)
print('lower_limit:', lower_limit_2)

# Create copy of dataset, exclude points outside the previously defined limits
iqr_items = df[df['total_items'] <= upper_limit_2]
iqr_items = iqr_items[iqr_items['total_items'] >= lower_limit_2]

# Plot raw data versus IQR-processed data
plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(df['order_amount'])
plt.subplot(2,2,2)
sns.boxplot(x=df['order_amount'])

plt.subplot(2,2,3)
sns.distplot(iqr_items['order_amount'])
plt.subplot(2,2,4)
sns.boxplot(x=iqr_items['order_amount'])
plt.suptitle('IQR on total_items')
plt.show()

# Take newly calculated average order value with outliers according to IQR rule excluded
print('\nOrder_Amount Processed with Method 2:\n', iqr_items['order_amount'].describe(), sep='')


################################################################################
# Method 3: Use IQR on shoe value (basically per shop)
df['item_value'] = df['order_amount'] / df['total_items']
p25_3 = df['item_value'].quantile(0.25)
p75_3 = df['item_value'].quantile(0.75)

# Set upper and lower limits based on the IQR
iqr_3 = p75_3 - p25_3
upper_limit_3 = p75_3 + 1.5 * iqr_3
lower_limit_3 = max(p25_3 - 1.5 * iqr_3, 0)

print('iqr:', iqr_3)
print('upperlimit:', upper_limit_3)
print('lower_limit:', lower_limit_3)

# Create copy of dataset, exclude points outside the previously defined limits
iqr_value = df[df['item_value'] <= upper_limit_3]
iqr_value = iqr_value[iqr_value['item_value'] >= lower_limit_3]

# Plot raw data versus IQR-processed data
plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(df['order_amount'])
plt.subplot(2,2,2)
sns.boxplot(x=df['order_amount'])

plt.subplot(2,2,3)
sns.distplot(iqr_value['order_amount'])
plt.subplot(2,2,4)
sns.boxplot(x=iqr_value['order_amount'])
plt.suptitle('IQR on item_value')
plt.show()

# Take newly calculated average order value with outliers according to IQR rule excluded
print('\nOrder_Amount Processed with Method 3:\n', iqr_value['order_amount'].describe(), sep='')


################################################################################
# Method 4: Determine 3 averages (central tendencies)
print('Order_Amount Column Description:\n', df['order_amount'].describe(), sep = '')
mode = df['order_amount'].mode()[0]
median = df['order_amount'].median()
mean = df['order_amount'].mean()

print("Central Tendency Measures:\n", "mode: ", mode, "\nmedian: ", median, "\nmean: ", mean, sep='')


################################################################################
# Method 5: Manually filter out orders I think are suspicious
manual_df = df[df['order_amount'] <= 20000]

# Plot raw data versus manually processed data
plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(df['order_amount'])
plt.subplot(2,2,2)
sns.boxplot(x=df['order_amount'])

plt.subplot(2,2,3)
sns.distplot(manual_df['order_amount'])
plt.subplot(2,2,4)
sns.boxplot(x=manual_df['order_amount'])
plt.suptitle('Manually processed data')
plt.show()

print('\nOrder_Amount Processed with Method 5:\n', manual_df['order_amount'].describe(), sep='')