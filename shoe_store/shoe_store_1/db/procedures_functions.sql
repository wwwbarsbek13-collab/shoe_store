
CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER) 
RETURNS NUMERIC AS $$
BEGIN
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER, 
    p_stock_item_id INTEGER, 
    p_qty INTEGER
) 
AS $$
DECLARE
    v_price NUMERIC;
    v_order_id INTEGER;
BEGIN
   
    SELECT p.price INTO v_price 
    FROM products p
    JOIN stock_items si ON p.product_id = si.product_id
    WHERE si.stock_item_id = p_stock_item_id;

    INSERT INTO orders (order_date, user_id) 
    VALUES (CURRENT_DATE, p_user_id) 
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items (order_id, stock_item_id, quantity, price)
    VALUES (v_order_id, p_stock_item_id, p_qty, v_price);

    UPDATE stock_items 
    SET quantity_available = quantity_available - p_qty 
    WHERE stock_item_id = p_stock_item_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE safe_update_stock(
    p_stock_item_id INTEGER, 
    p_qty INTEGER
) 
AS $$
DECLARE
    v_current_qty INTEGER;
BEGIN
   
    SELECT quantity_available INTO v_current_qty 
    FROM stock_items 
    WHERE stock_item_id = p_stock_item_id;

   
    IF v_current_qty < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе! Доступно: %, запрошено: %', v_current_qty, p_qty;
    ELSE
        UPDATE stock_items 
        SET quantity_available = quantity_available - p_qty 
        WHERE stock_item_id = p_stock_item_id;
        RAISE NOTICE 'Остаток успешно обновлен.';
    END IF;
    
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Произошла ошибка: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;