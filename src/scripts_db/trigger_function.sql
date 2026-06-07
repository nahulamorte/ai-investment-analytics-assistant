CREATE OR REPLACE FUNCTION fn_actualizar_cartera()
    RETURNS TRIGGER AS
$$
DECLARE
    v_cantidad_actual DECIMAL(18, 6);
    v_ppp_actual      DECIMAL(18, 4);
    v_nueva_cantidad  DECIMAL(18, 6);
    v_nuevo_ppp       DECIMAL(18, 4);
BEGIN
    SELECT cantidad_neta, precio_promedio_compra
    INTO v_cantidad_actual, v_ppp_actual
    FROM cartera
    WHERE id_usuario = NEW.id_usuario
      AND id_activo = NEW.id_activo;

    IF v_cantidad_actual IS NULL THEN
        v_cantidad_actual := 0;
        v_ppp_actual := 0;
    END IF;

    IF (NEW.tipo_operacion = 'COMPRA') THEN
        --Guardo en variable, la nueva cantidad.
        v_nueva_cantidad := v_cantidad_actual + NEW.cantidad;

        --Guardo en variable, el nuevo Precio Ponderado Promedio (PPP).
        v_nuevo_ppp := ((v_cantidad_actual * v_ppp_actual) + (NEW.cantidad * NEW.precio_ejecucion)) / v_nueva_cantidad;

    ELSIF (NEW.tipo_operacion = 'VENTA') THEN
        IF (NEW.cantidad > v_cantidad_actual) THEN
            RAISE EXCEPTION 'No puede vender mas de lo que tiene en cartera. Cantidad actual: %', v_cantidad_actual;
            RETURN NEW;
        end if;

        v_nueva_cantidad := v_cantidad_actual - NEW.cantidad;
        v_nuevo_ppp := v_ppp_actual; -- El PPP no cambia con una venta, solo con compras.


    END IF;

    --UPSERT:
    IF (v_nueva_cantidad = 0) THEN
        DELETE FROM cartera WHERE id_usuario = NEW.id_usuario AND id_activo = NEW.id_activo;

    ELSIF (v_cantidad_actual > 0) THEN
        UPDATE cartera SET cantidad_neta = v_nueva_cantidad, precio_promedio_compra = v_nuevo_ppp
                       WHERE id_usuario = NEW.id_usuario AND id_activo = NEW.id_activo;
    ELSE -- Si entra en este bloque es porque es un activo nuevo, por lo tanto: inserto.
        INSERT INTO cartera (cantidad_neta, id_activo, id_usuario) VALUES (v_nueva_cantidad, NEW.id_activo, NEW.id_usuario);
    end if;


    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER tr_act_cartera
AFTER INSERT ON operaciones
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_cartera();


CREATE OR REPLACE FUNCTION fn_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'No se pueden borrar registros';
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_delete
BEFORE DELETE ON operaciones
FOR EACH ROW
EXECUTE FUNCTION fn_delete();