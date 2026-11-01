CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    changed_at TEXT DEFAULT (datetime('now'))
);
CREATE TRIGGER IF NOT EXISTS trg_audit_price_update
AFTER UPDATE ON products
FOR EACH ROW
WHEN OLD.price != NEW.price
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value, new_value)
    VALUES ('products', 'UPDATE', NEW.product_id, CAST(OLD.price AS TEXT), CAST(NEW.price AS TEXT));
END;

CREATE TRIGGER IF NOT EXISTS trg_audit_order_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value, new_value)
    VALUES ('orders', 'DELETE', OLD.order_id, NULL, NULL);
END;

CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = datetime('now') WHERE user_id = NEW.user_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_stock_auto_decrease
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE stock_items
    SET quantity_available = quantity_available - NEW.quantity
    WHERE stock_item_id = NEW.stock_item_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_prevent_user_delete
BEFORE DELETE ON users
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM orders WHERE user_id = OLD.user_id) > 0
BEGIN
    SELECT RAISE(ABORT, 'Нельзя удалить пользователя с активными заказами');
END;

CREATE TRIGGER IF NOT EXISTS trg_check_negative_quantity
BEFORE INSERT ON stock_items
FOR EACH ROW
WHEN NEW.quantity_available < 0
BEGIN
    SELECT RAISE(ABORT, 'Количество не может быть отрицательным');
END;