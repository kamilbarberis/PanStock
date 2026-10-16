
from conexion import obtener_conexion


def listar_movimientos():
    """Devuelve el historial de movimientos con el nombre del producto."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """
            SELECT
                m.id_movimiento,
                m.id_producto,
                p.nombre AS producto,
                m.tipo_movimiento,
                m.cantidad,
                m.fecha,
                m.observacion
            FROM movimientos m
            INNER JOIN productos p
                ON p.id_producto = m.id_producto
            ORDER BY m.fecha DESC, m.id_movimiento DESC
        """

        cursor.execute(consulta)
        return cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()


def registrar_movimiento(id_producto, tipo_movimiento, cantidad, observacion=""):
    """
    Registra una ENTRADA o SALIDA y actualiza el stock mediante
    una transacción para evitar inconsistencias.
    """
    tipo_movimiento = tipo_movimiento.strip().upper()

    if tipo_movimiento not in ("ENTRADA", "SALIDA"):
        raise ValueError("El tipo debe ser ENTRADA o SALIDA.")

    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un número entero mayor que cero.")

    observacion = (observacion or "").strip() or None

    if observacion and len(observacion) > 200:
        raise ValueError("La observación no puede superar los 200 caracteres.")

    conexion = obtener_conexion()
    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        # Bloqueamos el producto mientras calculamos y actualizamos su stock.
        cursor.execute(
            """
            SELECT id_producto, nombre
            FROM productos
            WHERE id_producto = %s
            FOR UPDATE
            """,
            (id_producto,)
        )
        producto = cursor.fetchone()

        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        # Calculamos el stock actual a partir de los movimientos registrados.
        cursor.execute(
            """
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN UPPER(tipo_movimiento) = 'ENTRADA'
                            THEN cantidad
                        WHEN UPPER(tipo_movimiento) = 'SALIDA'
                            THEN -cantidad
                        ELSE 0
                    END
                ),
                0
            ) AS stock_actual
            FROM movimientos
            WHERE id_producto = %s
            """,
            (id_producto,)
        )

        resultado = cursor.fetchone()
        stock_actual = int(resultado["stock_actual"])

        if tipo_movimiento == "SALIDA" and cantidad > stock_actual:
            raise ValueError(
                f"Stock insuficiente. Stock actual: {stock_actual} unidades."
            )

        cursor.execute(
            """
            INSERT INTO movimientos
                (id_producto, tipo_movimiento, cantidad, observacion)
            VALUES (%s, %s, %s, %s)
            """,
            (id_producto, tipo_movimiento, cantidad, observacion)
        )

        conexion.commit()

        return {
            "id_movimiento": cursor.lastrowid,
            "producto": producto["nombre"],
            "tipo_movimiento": tipo_movimiento,
            "cantidad": cantidad,
            "stock_anterior": stock_actual,
            "stock_nuevo": (
                stock_actual + cantidad
                if tipo_movimiento == "ENTRADA"
                else stock_actual - cantidad
            ),
        }

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def obtener_stock(id_producto):
    """Calcula el stock actual de un producto desde sus movimientos."""
    conexion = obtener_conexion()
    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN UPPER(tipo_movimiento) = 'ENTRADA'
                            THEN cantidad
                        WHEN UPPER(tipo_movimiento) = 'SALIDA'
                            THEN -cantidad
                        ELSE 0
                    END
                ),
                0
            )
            FROM movimientos
            WHERE id_producto = %s
            """,
            (id_producto,)
        )

        return int(cursor.fetchone()[0])

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
