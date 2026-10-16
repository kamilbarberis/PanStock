
#interfaz grafica


import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

from producto_dao import (
    listar_productos,
    obtener_categorias,
    agregar_producto,
    modificar_producto,
    eliminar_producto,
)


class PanStockApp:
    def __init__(self, root, parent=None):
        self.root = root
        self.parent = parent if parent is not None else root

        # Si se abre como ventana independiente, configura la ventana.
        # Si se abre desde el menú, utiliza el área principal existente.
        if parent is None:
            self.root.title("PanStock - Control de stock")
            self.root.geometry("1100x680")
            self.root.minsize(900, 580)

        self.productos = []
        self.categorias = []
        self.id_seleccionado = None

        self.configurar_estilos()
        self.crear_interfaz()
        self.cargar_categorias()
        self.cargar_productos()

    def configurar_estilos(self):
        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 19, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview",
            rowheight=29,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.parent, padding=18)
        contenedor.pack(fill="both", expand=True)

        # Encabezado
        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 18))

        ttk.Label(
            encabezado,
            text="Productos",
            style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            encabezado,
            text="Administración del catálogo y consulta del stock actual.",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", pady=(5, 0))

        # Formulario
        formulario = ttk.LabelFrame(
            contenedor,
            text="Datos del producto",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 15))

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_nombre = ttk.Entry(
            formulario,
            width=35
        )
        self.entrada_nombre.grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(formulario, text="Descripción:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )

        self.entrada_descripcion = ttk.Entry(
            formulario,
            width=40
        )
        self.entrada_descripcion.grid(
            row=0, column=3, sticky="ew", padx=5, pady=5
        )

        ttk.Label(formulario, text="Precio:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_precio = ttk.Entry(
            formulario,
            width=20
        )
        self.entrada_precio.grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )

        ttk.Label(formulario, text="Stock mínimo:").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )

        self.entrada_stock_minimo = ttk.Entry(
            formulario,
            width=20
        )
        self.entrada_stock_minimo.grid(
            row=1, column=3, sticky="w", padx=5, pady=5
        )

        ttk.Label(formulario, text="Categoría:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )

        self.combo_categoria = ttk.Combobox(
            formulario,
            state="readonly",
            width=32
        )
        self.combo_categoria.grid(
            row=2, column=1, sticky="ew", padx=5, pady=5
        )

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        # Botones de operaciones
        botones = ttk.Frame(contenedor)
        botones.pack(fill="x", pady=(0, 15))

        ttk.Button(
            botones,
            text="Agregar",
            command=self.agregar
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Modificar",
            command=self.modificar
        ).pack(side="left", padx=8)

        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).pack(side="left", padx=8)

        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar_formulario
        ).pack(side="left", padx=8)

        ttk.Button(
            botones,
            text="Actualizar listado",
            command=self.cargar_productos
        ).pack(side="right")

        # Tabla de productos
        tabla_marco = ttk.LabelFrame(
            contenedor,
            text="Listado de productos",
            padding=10
        )
        tabla_marco.pack(fill="both", expand=True)

        columnas = (
            "id",
            "nombre",
            "categoria",
            "precio",
            "stock",
            "minimo",
            "estado"
        )

        self.tabla = ttk.Treeview(
            tabla_marco,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        encabezados = {
            "id": "ID",
            "nombre": "Producto",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock actual",
            "minimo": "Stock mínimo",
            "estado": "Estado"
        }

        anchos = {
            "id": 55,
            "nombre": 210,
            "categoria": 150,
            "precio": 100,
            "stock": 95,
            "minimo": 95,
            "estado": 145
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=45,
                anchor="center"
            )

        self.tabla.column("nombre", anchor="w")
        self.tabla.column("categoria", anchor="w")

        scrollbar_vertical = ttk.Scrollbar(
            tabla_marco,
            orient="vertical",
            command=self.tabla.yview
        )

        scrollbar_horizontal = ttk.Scrollbar(
            tabla_marco,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        tabla_marco.rowconfigure(0, weight=1)
        tabla_marco.columnconfigure(0, weight=1)

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_producto
        )

        # Mensaje inferior
        self.etiqueta_estado = ttk.Label(
            contenedor,
            text="Listo.",
            anchor="w"
        )
        self.etiqueta_estado.pack(fill="x", pady=(8, 0))

    def cargar_categorias(self):
        try:
            self.categorias = obtener_categorias()

            nombres = [
                categoria["nombre"]
                for categoria in self.categorias
            ]

            self.combo_categoria["values"] = nombres

            if nombres:
                self.combo_categoria.current(0)
            else:
                self.combo_categoria.set("")

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las categorías.\n\n{error}",
                parent=self.root
            )

    def cargar_productos(self):
        try:
            self.productos = listar_productos()

            for elemento in self.tabla.get_children():
                self.tabla.delete(elemento)

            for producto in self.productos:
                stock = int(producto["stock_actual"])
                minimo = int(producto["stock_minimo"])

                if stock < minimo:
                    estado = "Stock bajo"
                else:
                    estado = "Disponible"

                precio = Decimal(str(producto["precio"]))

                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        producto["id_producto"],
                        producto["nombre"],
                        producto["categoria"],
                        f"${precio:,.2f}",
                        stock,
                        minimo,
                        estado
                    )
                )

            self.etiqueta_estado.config(
                text=f"Productos registrados: {len(self.productos)}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los productos.\n\n{error}",
                parent=self.root
            )

    def validar_formulario(self):
        nombre = self.entrada_nombre.get().strip()
        descripcion = self.entrada_descripcion.get().strip()
        precio_texto = self.entrada_precio.get().strip()
        minimo_texto = self.entrada_stock_minimo.get().strip()
        indice_categoria = self.combo_categoria.current()

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "Ingresá el nombre del producto.",
                parent=self.root
            )
            self.entrada_nombre.focus_set()
            return None

        if len(nombre) > 100:
            messagebox.showwarning(
                "Validación",
                "El nombre no puede superar los 100 caracteres.",
                parent=self.root
            )
            return None

        if len(descripcion) > 200:
            messagebox.showwarning(
                "Validación",
                "La descripción no puede superar los 200 caracteres.",
                parent=self.root
            )
            return None

        try:
            # Acepta tanto 1500.50 como 1500,50.
            precio_texto = precio_texto.replace(",", ".")
            precio = Decimal(precio_texto)

            if not precio.is_finite():
                raise InvalidOperation

            if precio < 0:
                raise ValueError

            if precio.as_tuple().exponent < -2:
                raise InvalidOperation

            if precio >= Decimal("100000000"):
                raise InvalidOperation

        except ValueError:
            messagebox.showwarning(
                "Validación",
                "El precio no puede ser negativo.",
                parent=self.root
            )
            return None

        except (InvalidOperation, ArithmeticError):
            messagebox.showwarning(
                "Validación",
                "Ingresá un precio válido con hasta dos decimales.",
                parent=self.root
            )
            return None

        try:
            stock_minimo = int(minimo_texto)

            if stock_minimo < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Validación",
                "El stock mínimo debe ser un entero mayor o igual a cero.",
                parent=self.root
            )
            return None

        if indice_categoria < 0:
            messagebox.showwarning(
                "Validación",
                "Seleccioná una categoría.",
                parent=self.root
            )
            return None

        id_categoria = self.categorias[indice_categoria][
            "id_categoria"
        ]

        return (
            nombre,
            descripcion or None,
            precio,
            stock_minimo,
            id_categoria
        )

    def agregar(self):
        datos = self.validar_formulario()

        if datos is None:
            return

        try:
            id_nuevo = agregar_producto(*datos)

            self.cargar_productos()
            self.limpiar_formulario()

            self.etiqueta_estado.config(
                text=f"Producto agregado correctamente. ID: {id_nuevo}"
            )

            messagebox.showinfo(
                "Operación exitosa",
                "El producto se agregó correctamente.",
                parent=self.root
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo agregar el producto.\n\n{error}",
                parent=self.root
            )

    def modificar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar producto",
                "Seleccioná un producto de la tabla para modificarlo.",
                parent=self.root
            )
            return

        datos = self.validar_formulario()

        if datos is None:
            return

        try:
            actualizado = modificar_producto(
                self.id_seleccionado,
                *datos
            )

            self.cargar_productos()
            self.limpiar_formulario()

            if actualizado:
                messagebox.showinfo(
                    "Operación exitosa",
                    "El producto se modificó correctamente.",
                    parent=self.root
                )
            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró el producto o no hubo cambios.",
                    parent=self.root
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo modificar el producto.\n\n{error}",
                parent=self.root
            )

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Seleccionar producto",
                "Seleccioná un producto de la tabla para eliminarlo.",
                parent=self.root
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de que querés eliminar el producto seleccionado?\n\n"
            "Si tiene movimientos registrados, MySQL impedirá su eliminación.",
            parent=self.root
        )

        if not confirmar:
            return

        try:
            eliminado = eliminar_producto(self.id_seleccionado)

            self.cargar_productos()
            self.limpiar_formulario()

            if eliminado:
                messagebox.showinfo(
                    "Operación exitosa",
                    "El producto se eliminó correctamente.",
                    parent=self.root
                )
            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró el producto seleccionado.",
                    parent=self.root
                )

        except Exception as error:
            messagebox.showerror(
                "No se pudo eliminar",
                "No se pudo eliminar el producto.\n\n"
                "Verificá si tiene movimientos registrados.\n\n"
                f"Detalle: {error}",
                parent=self.root
            )

    def seleccionar_producto(self, evento=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        self.id_seleccionado = int(valores[0])

        producto = next(
            (
                item
                for item in self.productos
                if item["id_producto"] == self.id_seleccionado
            ),
            None
        )

        if producto is None:
            return

        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, producto["nombre"])

        self.entrada_descripcion.delete(0, tk.END)
        self.entrada_descripcion.insert(
            0,
            producto["descripcion"] or ""
        )

        self.entrada_precio.delete(0, tk.END)
        self.entrada_precio.insert(
            0,
            str(producto["precio"])
        )

        self.entrada_stock_minimo.delete(0, tk.END)
        self.entrada_stock_minimo.insert(
            0,
            str(producto["stock_minimo"])
        )

        for indice, categoria in enumerate(self.categorias):
            if categoria["nombre"] == producto["categoria"]:
                self.combo_categoria.current(indice)
                break

        self.etiqueta_estado.config(
            text=f"Producto seleccionado: {producto['nombre']} (ID {self.id_seleccionado})"
        )

    def limpiar_formulario(self):
        self.id_seleccionado = None

        self.entrada_nombre.delete(0, tk.END)
        self.entrada_descripcion.delete(0, tk.END)
        self.entrada_precio.delete(0, tk.END)
        self.entrada_stock_minimo.delete(0, tk.END)

        if self.categorias:
            self.combo_categoria.current(0)
        else:
            self.combo_categoria.set("")

        seleccion = self.tabla.selection()

        if seleccion:
            self.tabla.selection_remove(*seleccion)

        self.entrada_nombre.focus_set()

        self.etiqueta_estado.config(
            text="Formulario limpio."
        )


def main():
    # El archivo sigue siendo el punto de entrada de la aplicación.
    # El menú importa esta clase para mostrar Productos en su área central.
    from menu import MenuPanStock

    root = tk.Tk()
    MenuPanStock(root)
    root.mainloop()


if __name__ == "__main__":
    main()
