
SELECT 
    product_name, 
    price, 
    calc_discount(price, 20) AS price_with_discount
FROM products;

SELECT 
    format_full_name(last_name, first_name, middle_name) AS formatted_name
FROM users;

SELECT 
    oi.order_id,
    pluralize_items(SUM(oi.quantity)) AS items_count
FROM order_items oi
GROUP BY oi.order_id;

SELECT 
    format_full_name(u.last_name, u.first_name, u.middle_name) AS client_name,
    calc_discount(SUM(oi.quantity * oi.price), 10) AS discounted_total
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;

SELECT 
    format_full_name(u.last_name, u.first_name, u.middle_name) AS client_name,
    SUM(oi.quantity * oi.price) AS total_spent,
    get_client_tier(SUM(oi.quantity * oi.price)) AS tier
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;