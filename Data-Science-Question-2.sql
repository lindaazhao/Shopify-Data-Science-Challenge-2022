-- Shopify Summer 2022 Data Science Intern Challenge: Question 2
----------------------------------------------------------------

-- Part a) How many orders were shipped by Speedy Express in total?

/* 
Display number of orders shipped by Speedy Express 
by joining "Orders" and "Shippers" tables using ShipperID, 
then filtering for Shipper Name "Speedy Express" 
*/

SELECT 
    COUNT(*)
FROM Orders
JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID
WHERE Shippers.ShipperName = 'Speedy Express'; 


-- Part b) What is the last name of the employee with the most orders?

/* 
Display last name of employee with most orders, as well as their number 
of orders, by joining "Orders" and "Employees" tables using EmployeeID,
then counting orders (NumOrders) by employee, and taking the LastName 
corresponding to the largest value in NumOrders
*/

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


-- Part c) What product was ordered the most by customers in Germany?

/*
Display name of most ordered product in Germany with corresponding
number of orders and ID by joining "Orders", "OrderDetails", "Customers", 
and "Products" tables, then counting orders by ProductID and Country, 
and taking the ProductName corresponding to the largest value in NumOrders
*/

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

