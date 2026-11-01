
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

SELECT u.last_name, u.first_name
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id
HAVING SUM(oi.quantity * oi.price) = (
    SELECT MAX(total) FROM (
        SELECT SUM(quantity * price) AS total
        FROM order_items
        GROUP BY order_id
    )
);

SELECT last_name, first_name
FROM users
WHERE user_id IN (SELECT user_id FROM orders);

SELECT last_name, first_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
);

SELECT product_name
FROM products
WHERE product_id NOT IN (
    SELECT si.product_id 
    FROM stock_items si
    INNER JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
);

SELECT u.last_name, u.first_name, 
       SUM(oi.quantity * oi.price) AS total_spent,
       RANK() OVER(ORDER BY SUM(oi.quantity * oi.price) DESC) AS rank
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;

SELECT o.order_id, u.last_name, u.first_name, o.order_date,
       ROW_NUMBER() OVER(PARTITION BY o.user_id ORDER BY o.order_date ASC) AS order_num
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id;

SELECT category, product_name, price,
       ROW_NUMBER() OVER(PARTITION BY category ORDER BY price DESC) AS rn
FROM products;

SELECT category, product_name, price
FROM (
    SELECT category, product_name, price,
           ROW_NUMBER() OVER(PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
) AS ranked_products
WHERE rn = 1;

SELECT o.order_id, o.order_date,
       SUM(oi.quantity * oi.price) AS order_total,
       SUM(SUM(oi.quantity * oi.price)) OVER(ORDER BY o.order_date) AS running_total
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date;

SELECT u.last_name, u.first_name, o.order_date,
       LAG(o.order_date) OVER(PARTITION BY o.user_id ORDER BY o.order_date) AS prev_order_date,
       julianday(o.order_date) - julianday(LAG(o.order_date) OVER(PARTITION BY o.user_id ORDER BY o.order_date)) AS days_diff
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id;