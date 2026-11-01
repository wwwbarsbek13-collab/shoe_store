SELECT u.user_id, u.last_name, u.first_name, u.login, r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id;

SELECT product_id, product_name, category, manufacturer, price
FROM products;

SELECT size_id, size_value
FROM sizes;

SELECT o.order_id, o.order_date, o.status,
       u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client_fio
FROM orders o
JOIN users u ON o.user_id = u.user_id;

SELECT si.stock_item_id, p.product_name, s.size_value, si.quantity
FROM stock_items si
JOIN products p ON si.product_id = p.product_id
JOIN sizes s ON si.size_id = s.size_id;