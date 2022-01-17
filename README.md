# Shopify Data Science Challenge 2022

## Question 1

Given some [sample data](https://docs.google.com/spreadsheets/d/16i38oonuX1y1g7C_UAmiK9GkY7cS-64DfiDMNiR41LM/edit#gid=0), write a program to answer the following:

On Shopify, we have exactly 100 sneaker shops, and each of these shops sells only one model of shoe. We want to do some analysis of the average order value (AOV). When we look at orders data over a 30 day window, we naively calculate an AOV of $3145.13. Given that we know these shops are selling sneakers, a relatively affordable item, something seems wrong with our analysis.

1. Think about what could be going wrong with our calculation. Think about a better way to evaluate this data.
2. What metric would you report for this dataset?
3. What is its value?

## Question 2

For this question you’ll need to use SQL. [Follow this link](https://www.w3schools.com/SQL/TRYSQL.ASP?FILENAME=TRYSQL_SELECT_ALL) to access the data set required for the challenge. Please use queries to answer the following questions. Paste your queries along with your final numerical answers below.

**1. How many orders were shipped by Speedy Express in total?**

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

**2. What is the last name of the employee with the most orders?** 

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

**3. What product was ordered the most by customers in Germany?**

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