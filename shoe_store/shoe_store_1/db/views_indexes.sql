
CREATE VIEW v_orders_full AS
SELECT 
    o.order_id,
    o.order_date,
    u.last_name || ' ' || u.first_name AS client_fio,
    SUM(oi.quantity * oi.price) AS total_sum
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, u.last_name, u.first_name;

CREATE VIEW v_products_with_stock AS
SELECT 
    p.product_name,
    p.price,
    s.size_value,
    si.quantity_available
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN sizes s ON si.size_id = s.size_id;

CREATE VIEW v_user_stats AS
SELECT 
    u.last_name || ' ' || u.first_name AS client_fio,
    u.login,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.login;


CREATE INDEX idx_products_category ON products(category);

CREATE INDEX idx_orders_order_date ON orders(order_date);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_stock_items_product_id ON stock_items(product_id);
CREATE INDEX idx_stock_items_size_id ON stock_items(size_id);

CREATE INDEX idx_products_manufacturer_category ON products(manufacturer, category);

CREATE VIEW v_simple AS 
SELECT product_id, price 
FROM products
