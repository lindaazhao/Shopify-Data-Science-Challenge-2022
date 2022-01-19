# Shopify Data Science Challenge 2022
## Table of Contents

- [Question 1](#question-1)
- [Question 2](#question-2)
- [Appendix: Question 1 Analysis](#appendix-question-1-analysis)

## Question 1

Given some [sample data](https://docs.google.com/spreadsheets/d/16i38oonuX1y1g7C_UAmiK9GkY7cS-64DfiDMNiR41LM/edit#gid=0), write a program to answer the following:

On Shopify, we have exactly 100 sneaker shops, and each of these shops sells only one model of shoe. We want to do some analysis of the average order value (AOV). When we look at orders data over a 30 day window, we naively calculate an AOV of $3145.13. Given that we know these shops are selling sneakers, a relatively affordable item, something seems wrong with our analysis.

#### **1. Think about what could be going wrong with our calculation. Think about a better way to evaluate this data.**

The current AOV calculation simply takes the average (mean) of the “order_amount” column. Doing so in this case fails to account for major outliers in the data that skew this average. In particular, User 607 has repeated orders totalling over $700,000, and Shop 78 sells a shoe worth over $25,000. These order amounts are significantly higher than the next highest amount ($1,760). 

I used several other methods of evaluating the data which are detailed in the [analysis section](#appendix-question-1-analysis). In general, the analysis consisted of two approaches: removing outliers and using other central tendency measures. 

I first graphed the given dataset and noticed it was heavily right-skewed in terms of both the order_amount and total_items attributes. As such, I used the interquartile range (IQR) proximity rule to determine the outliers, [as explained here](https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/box-whisker-plots/a/identifying-outliers-iqr-rule). I did this to several different attributes of the data and included each result in my analysis.

I also looked at the mode and median as alternative ways to represent the average order value. 

**TL;DR:** Current calculation is heavily skewed to the right due to some data points in order_amount being significantly higher than the rest. I filtered data by removing outliers using the IQR proximity rule and evaluated other averages. 


#### **2. What metric would you report for this dataset?**

Upon calculating an additional six AOVs based on the methods described, I would report the median order value (order_amount). There are many reasons behind this choice—the primary reason being that no data is removed. Even if some points seem like outliers, it is difficult to confidently determine which orders really are “fake” with the provided information. Given this uncertainty, taking the median reduces the direct impact of the orders that highly skew the mean value, while avoiding the need to remove these points altogether. 

Additionally, my manual processing method that does remove “suspicious” orders (outliers) results in a similar value (within 7%) as the median order value. This further validates my choice of reporting the median as the AOV, as it agrees with other potential AOVs that account for outliers.

Finally, my choice is influenced by the potential uses of this metric. If this number is shared with the shop owners, it should accurately represent the majority. Otherwise, if the reported AOV is highly skewed by one or two shops or customers, it is less helpful as a decision making tool for shops to compare their performance with others, or adjust their pricing, products, etc. In the presence of strong outliers, the median is highly capable of estimating the central value, thus providing an accurate reference point for shop owners.

#### **3. What is its value?**

The median order value is $284.00.

#### [Full Question 1 Solution Code](Data-Science-Question-1.py)

## Question 2

For this question you’ll need to use SQL. [Follow this link](https://www.w3schools.com/SQL/TRYSQL.ASP?FILENAME=TRYSQL_SELECT_ALL) to access the data set required for the challenge. Please use queries to answer the following questions. Paste your queries along with your final numerical answers below.

#### **1. How many orders were shipped by Speedy Express in total?**

Query:
```sql
SELECT 
    COUNT(*)
FROM Orders
JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID
WHERE Shippers.ShipperName = 'Speedy Express';
```

Result:
| Count(*) |
|-|
| 54 |

&nbsp;

#### **2. What is the last name of the employee with the most orders?** 

Query:
```sql
SELECT Employees.LastName, COUNT(*) AS NumOrders 
FROM Orders 
JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
GROUP BY Employees.EmployeeID, Employees.LastName
ORDER BY NumOrders DESC
LIMIT 1;

/* OR */

SELECT LastName, MAX(NumOrders) FROM
(
  SELECT COUNT(*) AS NumOrders, Employees.EmployeeID, Employees.LastName
  FROM Orders 
  JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
  GROUP BY Employees.EmployeeID, Employees.LastName
);
```

Result:
| LastName | NumOrders |
|-|-|
| Peacock | 40 | 

&nbsp;

#### **3. What product was ordered the most by customers in Germany?**

Query:
```sql
SELECT 
    Products.ProductName, 
    SUM(OrderDetails.Quantity) as NumOrders, 
    OrderDetails.ProductID, 
    Customers.Country 
FROM Orders
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
WHERE Customers.Country = 'Germany'
GROUP BY OrderDetails.ProductID, Customers.Country
ORDER BY NumOrders DESC
LIMIT 1;
```

Result:
| ProductName | NumOrders | ProductID | Country |
|-|-|-|-|
| Boston Crab Meat | 160| 40 | Germany |

#### [Full Question 2 Solution Code](Data-Science-Question-2.sql)

----------------

## Appendix: Question 1 Analysis

Methods used to process data and their results:
| Method | Description | Returned Value(s) |
|-|-|-|
| 1 | Eliminate outliers using IQR on the order_amount column | Mean: 293.73
| 2 | Eliminate outliers using IQR on the total_items column | Mean: 722.93
| 3 | Eliminate outliers using IQR on a manually created shoe_value column (order_amount / total_items) | Mean: 300.16
| 4 | Manually filter out orders I thought seemed unreasonable | Mean: 303.16
| 5 | Determine the 3 measures of central tendency (mode, median, mean) of the original data | Mode: 153.00 <br /> **Median: 284.00** <br /> Mean: 3145.128

Example code for Method 1 (code for all analysis methods is available [here](Data-Science-Question-1.py)):
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data_set.csv')

percentile25 = df['order_amount'].quantile(0.25)
percentile75 = df['order_amount'].quantile(0.75)

# Set upper and lower limits based on the IQR
iqr = percentile75 - percentile25
upper_limit = percentile75 + 1.5 * iqr
lower_limit = max(percentile25 - 1.5 * iqr, 0)

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
```

Output plot for Method 1 code above:

![Graph of original data and IQR processed data for method 1](assets/boxplot_light.png#gh-light-mode-only)
![Graph of original data and IQR processed data for method 1](assets/boxplot_dark.png#gh-dark-mode-only)

