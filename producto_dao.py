
#aca concentro las operaciones sobre los datos (alta, consulta, baja y modificacion) de ahi el DAO significa Data Access Object:


from conexion import obtener_conexion


def listar_productos():
    """Devuelve todos los productos con su categoría y stock actual."""
    conexion = None

    consulta = """
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock_minimo,
            c.nombre AS categoria,
            COALESCE(
                SUM(
                    CASE
                        WHEN m.tipo_movimiento = 'ENTRADA'
                            THEN m.cantidad
                        WHEN m.tipo_movimiento = 'SALIDA'
                            THEN -m.cantidad
                        ELSE 0
                    END
                ),
                0
            ) AS stock_actual
        FROM productos p
        INNER JOIN categorias c
            ON c.id_categoria = p.id_categoria
        LEFT JOIN movimientos m
            ON m.id_producto = p.id_producto
        GROUP BY
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock_minimo,
            c.nombre
        ORDER BY p.nombre;
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta)
        productos = cursor.fetchall()

        return productos

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def obtener_categorias():
    """Devuelve las categorías activas para los formularios."""
    conexion = None

    consulta = """
        SELECT id_categoria, nombre
        FROM categorias
        WHERE activa = TRUE
        ORDER BY nombre;
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta)
        categorias = cursor.fetchall()

        return categorias

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def agregar_producto(
    nombre,
    descripcion,
    precio,
    stock_minimo,
    id_categoria
):
    """Registra un producto nuevo."""
    conexion = None

    consulta = """
        INSERT INTO productos (
            nombre,
            descripcion,
            precio,
            stock_minimo,
            id_categoria
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            consulta,
            (
                nombre,
                descripcion,
                precio,
                stock_minimo,
                id_categoria
            )
        )

        conexion.commit()
        return cursor.lastrowid

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def modificar_producto(
    id_producto,
    nombre,
    descripcion,
    precio,
    stock_minimo,
    id_categoria
):
    """Actualiza los datos de un producto existente."""
    conexion = None

    consulta = """
        UPDATE productos
        SET
            nombre = %s,
            descripcion = %s,
            precio = %s,
            stock_minimo = %s,
            id_categoria = %s
        WHERE id_producto = %s;
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            consulta,
            (
                nombre,
                descripcion,
                precio,
                stock_minimo,
                id_categoria,
                id_producto
            )
        )

        conexion.commit()
        return cursor.rowcount > 0

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def eliminar_producto(id_producto):
    """Elimina un producto si no tiene movimientos asociados."""
    conexion = None

    consulta = """
        DELETE FROM productos
        WHERE id_producto = %s;
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(consulta, (id_producto,))
        conexion.commit()

        return cursor.rowcount > 0

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()
