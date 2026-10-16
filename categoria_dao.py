
from conexion import obtener_conexion


def listar_categorias():
    """Devuelve todas las categorías, activas e inactivas."""
    conexion = None

    consulta = """
        SELECT
            c.id_categoria,
            c.nombre,
            c.activa,
            COUNT(p.id_producto) AS cantidad_productos
        FROM categorias c
        LEFT JOIN productos p
            ON p.id_categoria = c.id_categoria
        GROUP BY
            c.id_categoria,
            c.nombre,
            c.activa
        ORDER BY c.nombre;
    """

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta)

        return cursor.fetchall()

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def agregar_categoria(nombre):
    """Registra una categoría nueva."""
    conexion = None
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre de la categoría es obligatorio.")

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_categoria, activa
            FROM categorias
            WHERE LOWER(nombre) = LOWER(%s)
            LIMIT 1;
            """,
            (nombre,)
        )

        existente = cursor.fetchone()

        if existente:
            if existente["activa"]:
                raise ValueError(
                    "Ya existe una categoría activa con ese nombre."
                )

            raise ValueError(
                "Ya existe una categoría inactiva con ese nombre. "
                "Podés reactivarla en lugar de crear otra."
            )

        cursor.execute(
            """
            INSERT INTO categorias (nombre, activa)
            VALUES (%s, TRUE);
            """,
            (nombre,)
        )

        id_categoria = cursor.lastrowid
        conexion.commit()

        return id_categoria

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def modificar_categoria(id_categoria, nombre):
    """Modifica el nombre de una categoría."""
    conexion = None
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre de la categoría es obligatorio.")

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id_categoria
            FROM categorias
            WHERE LOWER(nombre) = LOWER(%s)
              AND id_categoria <> %s;
            """,
            (nombre, id_categoria)
        )

        if cursor.fetchone():
            raise ValueError(
                "Ya existe otra categoría con ese nombre."
            )

        cursor.execute(
            """
            UPDATE categorias
            SET nombre = %s
            WHERE id_categoria = %s;
            """,
            (nombre, id_categoria)
        )

        modificada = cursor.rowcount > 0
        conexion.commit()

        return modificada

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def desactivar_categoria(id_categoria):
    """Desactiva una categoría sin borrar sus datos."""
    conexion = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE categorias
            SET activa = FALSE
            WHERE id_categoria = %s
              AND activa = TRUE;
            """,
            (id_categoria,)
        )

        desactivada = cursor.rowcount > 0
        conexion.commit()

        return desactivada

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def activar_categoria(id_categoria):
    """Reactiva una categoría existente."""
    conexion = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_categoria, nombre
            FROM categorias
            WHERE id_categoria = %s;
            """,
            (id_categoria,)
        )

        categoria = cursor.fetchone()

        if categoria is None:
            return False

        cursor.execute(
            """
            SELECT id_categoria
            FROM categorias
            WHERE LOWER(nombre) = LOWER(%s)
              AND id_categoria <> %s
              AND activa = TRUE
            LIMIT 1;
            """,
            (categoria["nombre"], id_categoria)
        )

        if cursor.fetchone():
            raise ValueError(
                "Ya existe una categoría activa con ese nombre."
            )

        cursor.execute(
            """
            UPDATE categorias
            SET activa = TRUE
            WHERE id_categoria = %s
              AND activa = FALSE;
            """,
            (id_categoria,)
        )

        activada = cursor.rowcount > 0
        conexion.commit()

        return activada

    except Exception:
        if conexion is not None and conexion.is_connected():
            conexion.rollback()
        raise

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()
