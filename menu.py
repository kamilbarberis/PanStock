
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date


class MenuPanStock:
    def __init__(self, root):
        self.root = root
        self.root.title("PanStock | Sistema de Control de Stock")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#F3F6FA")

        self.color_fondo = "#F3F6FA"
        self.color_lateral = "#172B4D"
        self.color_acento = "#2F80ED"
        self.color_texto = "#263238"
        self.color_secundario = "#6B778C"
        self.color_blanco = "#FFFFFF"

        self.configurar_estilos()
        self.crear_interfaz()
        self.mostrar_inicio()

    # =========================================================
    # ESTILOS E INTERFAZ GENERAL
    # =========================================================

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Principal.TFrame", background=self.color_fondo)
        estilo.configure("Tarjeta.TFrame", background=self.color_blanco)

        estilo.configure(
            "Titulo.TLabel",
            background=self.color_fondo,
            foreground=self.color_texto,
            font=("Segoe UI", 23, "bold")
        )
        estilo.configure(
            "Subtitulo.TLabel",
            background=self.color_fondo,
            foreground=self.color_secundario,
            font=("Segoe UI", 11)
        )
        estilo.configure(
            "TarjetaTitulo.TLabel",
            background=self.color_blanco,
            foreground=self.color_texto,
            font=("Segoe UI", 14, "bold")
        )
        estilo.configure(
            "TarjetaTexto.TLabel",
            background=self.color_blanco,
            foreground=self.color_secundario,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "Stock.Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background=self.color_blanco,
            fieldbackground=self.color_blanco
        )
        estilo.configure(
            "Stock.Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def crear_interfaz(self):
        self.contenedor = tk.Frame(self.root, bg=self.color_fondo)
        self.contenedor.pack(fill="both", expand=True)

        self.lateral = tk.Frame(
            self.contenedor,
            bg=self.color_lateral,
            width=245
        )
        self.lateral.pack(side="left", fill="y")
        self.lateral.pack_propagate(False)

        tk.Label(
            self.lateral,
            text="PanStock",
            bg=self.color_lateral,
            fg=self.color_blanco,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", padx=25, pady=(30, 0))

        tk.Label(
            self.lateral,
            text="CONTROL DE STOCK",
            bg=self.color_lateral,
            fg="#A9B9D0",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=27, pady=(2, 30))

        tk.Frame(
            self.lateral, bg="#344967", height=1
        ).pack(fill="x", padx=20, pady=(0, 20))

        opciones = [
            ("▦", "Inicio", self.mostrar_inicio),
            ("▤", "Productos", self.mostrar_productos),
            ("▧", "Categorías", self.mostrar_categorias),
            ("↔", "Movimientos", self.mostrar_movimientos),
            ("▣", "Stock actual", self.mostrar_stock),
            ("▥", "Reportes", self.mostrar_reportes),
        ]

        for icono, texto, comando in opciones:
            tk.Button(
                self.lateral,
                text=f"  {icono}     {texto}",
                command=comando,
                bg=self.color_lateral,
                fg="#E8EEF7",
                activebackground=self.color_acento,
                activeforeground=self.color_blanco,
                font=("Segoe UI", 11),
                anchor="w",
                relief="flat",
                bd=0,
                padx=20,
                pady=13,
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=2)

        tk.Frame(
            self.lateral, bg="#344967", height=1
        ).pack(side="bottom", fill="x", padx=20, pady=(0, 15))

        tk.Label(
            self.lateral,
            text="PanStock v1.0",
            bg=self.color_lateral,
            fg="#A9B9D0",
            font=("Segoe UI", 9)
        ).pack(side="bottom", anchor="w", padx=25, pady=(0, 20))

        self.area_principal = tk.Frame(
            self.contenedor, bg=self.color_fondo
        )
        self.area_principal.pack(
            side="left", fill="both", expand=True
        )

    def limpiar_area(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    def crear_encabezado(self, titulo, descripcion):
        encabezado = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(30, 28, 30, 15)
        )
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado, text=titulo, style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            encabezado, text=descripcion, style="Subtitulo.TLabel"
        ).pack(anchor="w", pady=(8, 0))

    # =========================================================
    # INICIO
    # =========================================================

    def mostrar_inicio(self):
        self.limpiar_area()
        self.crear_encabezado(
            "Panel principal",
            "Bienvenido al sistema de control de stock de tu panadería."
        )

        contenido = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(30, 10, 30, 30)
        )
        contenido.pack(fill="both", expand=True)

        tarjetas = [
            (
                "Productos",
                "Administrá productos, precios y categorías.",
                self.mostrar_productos
            ),
            (
                "Categorías",
                "Organizá los productos por tipo.",
                self.mostrar_categorias
            ),
            (
                "Movimientos",
                "Registrá entradas y salidas de mercadería.",
                self.mostrar_movimientos
            ),
            (
                "Stock actual",
                "Consultá existencias y detectá faltantes.",
                self.mostrar_stock
            ),
            (
                "Reportes",
                "Consultá inventario, stock bajo y movimientos.",
                self.mostrar_reportes
            ),
        ]

        for indice, (titulo, descripcion, comando) in enumerate(tarjetas):
            fila, columna = divmod(indice, 2)

            tarjeta = ttk.Frame(
                contenido, style="Tarjeta.TFrame", padding=22
            )
            tarjeta.grid(
                row=fila, column=columna, sticky="nsew",
                padx=8, pady=8
            )

            ttk.Label(
                tarjeta, text=titulo, style="TarjetaTitulo.TLabel"
            ).pack(anchor="w")

            ttk.Label(
                tarjeta,
                text=descripcion,
                style="TarjetaTexto.TLabel",
                wraplength=350
            ).pack(anchor="w", pady=(10, 18))

            tk.Button(
                tarjeta,
                text="Abrir módulo  →",
                command=comando,
                bg=self.color_acento,
                fg=self.color_blanco,
                activebackground="#1D68C5",
                activeforeground=self.color_blanco,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                padx=15,
                pady=9,
                cursor="hand2"
            ).pack(anchor="w")

        contenido.columnconfigure(0, weight=1)
        contenido.columnconfigure(1, weight=1)

        for fila in range(3):
            contenido.rowconfigure(fila, weight=1)

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def mostrar_productos(self):
        self.limpiar_area()
        try:
            from panstock_app import PanStockApp
            PanStockApp(self.root, parent=self.area_principal)
        except Exception as error:
            messagebox.showerror(
                "Error al abrir Productos",
                f"No se pudo abrir el módulo de productos.\n\n{error}"
            )

    # =========================================================
    # CATEGORÍAS
    # =========================================================

    def mostrar_categorias(self):
        self.limpiar_area()
        self.crear_encabezado(
            "Categorías",
            "Administrá las categorías de productos de PanStock."
        )

        contenido = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(30, 10, 30, 25)
        )
        contenido.pack(fill="both", expand=True)

        barra = ttk.Frame(contenido, style="Principal.TFrame")
        barra.pack(fill="x", pady=(0, 15))

        tk.Button(
            barra,
            text="+ Nueva categoría",
            command=self.nueva_categoria,
            bg=self.color_acento,
            fg=self.color_blanco,
            activebackground="#1D68C5",
            activeforeground=self.color_blanco,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=16,
            pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            barra,
            text="Actualizar",
            command=self.cargar_categorias,
            bg=self.color_blanco,
            fg=self.color_texto,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        tarjeta = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=15
        )
        tarjeta.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "estado", "productos")
        self.tabla_categorias = ttk.Treeview(
            tarjeta, columns=columnas, show="headings",
            selectmode="browse"
        )

        configuracion = [
            ("id", "ID", 60, "center"),
            ("nombre", "Nombre de categoría", 300, "w"),
            ("estado", "Estado", 120, "center"),
            ("productos", "Productos asociados", 150, "center"),
        ]

        for columna, titulo, ancho, ancla in configuracion:
            self.tabla_categorias.heading(columna, text=titulo)
            self.tabla_categorias.column(
                columna, width=ancho, anchor=ancla
            )

        scroll = ttk.Scrollbar(
            tarjeta, orient="vertical",
            command=self.tabla_categorias.yview
        )
        self.tabla_categorias.configure(yscrollcommand=scroll.set)
        self.tabla_categorias.pack(
            side="left", fill="both", expand=True
        )
        scroll.pack(side="right", fill="y")

        acciones = ttk.Frame(contenido, style="Principal.TFrame")
        acciones.pack(fill="x", pady=(15, 0))

        tk.Button(
            acciones,
            text="Modificar nombre",
            command=self.editar_categoria,
            bg=self.color_blanco,
            fg=self.color_texto,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            padx=13,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            acciones,
            text="Activar / Desactivar",
            command=self.cambiar_estado_categoria,
            bg=self.color_blanco,
            fg=self.color_texto,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            padx=13,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        self.cargar_categorias()

    def cargar_categorias(self):
        try:
            from categoria_dao import listar_categorias
            categorias = listar_categorias()

            for item in self.tabla_categorias.get_children():
                self.tabla_categorias.delete(item)

            for categoria in categorias:
                estado = "Activa" if categoria["activa"] else "Inactiva"
                self.tabla_categorias.insert(
                    "", "end",
                    values=(
                        categoria["id_categoria"],
                        categoria["nombre"],
                        estado,
                        categoria["cantidad_productos"]
                    )
                )
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las categorías.\n\n{error}"
            )

    def obtener_categoria_seleccionada(self):
        seleccion = self.tabla_categorias.selection()
        if not seleccion:
            messagebox.showwarning(
                "Seleccioná una categoría",
                "Primero seleccioná una categoría de la tabla."
            )
            return None

        valores = self.tabla_categorias.item(seleccion[0], "values")
        return {
            "id": int(valores[0]),
            "nombre": valores[1],
            "estado": valores[2]
        }

    def nueva_categoria(self):
        self.dialogo_categoria()

    def editar_categoria(self):
        categoria = self.obtener_categoria_seleccionada()
        if categoria is not None:
            self.dialogo_categoria(categoria["id"], categoria["nombre"])

    def dialogo_categoria(self, id_categoria=None, nombre_actual=""):
        ventana = tk.Toplevel(self.root)
        ventana.title(
            "Nueva categoría" if id_categoria is None
            else "Modificar categoría"
        )
        ventana.geometry("430x210")
        ventana.resizable(False, False)
        ventana.configure(bg=self.color_fondo)
        ventana.transient(self.root)
        ventana.grab_set()

        marco = tk.Frame(
            ventana, bg=self.color_fondo, padx=25, pady=22
        )
        marco.pack(fill="both", expand=True)

        tk.Label(
            marco,
            text="Nueva categoría" if id_categoria is None
            else "Modificar categoría",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            marco,
            text="Nombre de la categoría",
            bg=self.color_fondo,
            fg=self.color_secundario,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(15, 5))

        entrada = ttk.Entry(marco, font=("Segoe UI", 11))
        entrada.pack(fill="x")
        entrada.insert(0, nombre_actual)
        entrada.focus_set()

        def guardar():
            nombre = entrada.get().strip()
            if not nombre:
                messagebox.showwarning(
                    "Dato obligatorio",
                    "Ingresá el nombre de la categoría.",
                    parent=ventana
                )
                entrada.focus_set()
                return

            try:
                from categoria_dao import (
                    agregar_categoria, modificar_categoria
                )

                if id_categoria is None:
                    agregar_categoria(nombre)
                    mensaje = "Categoría creada correctamente."
                else:
                    modificada = modificar_categoria(id_categoria, nombre)
                    if not modificada:
                        messagebox.showwarning(
                            "Sin cambios",
                            "No se encontró la categoría o el nombre "
                            "no tuvo cambios.",
                            parent=ventana
                        )
                        return
                    mensaje = "Categoría modificada correctamente."

                ventana.destroy()
                self.cargar_categorias()
                messagebox.showinfo(
                    "Operación exitosa", mensaje, parent=self.root
                )
            except Exception as error:
                messagebox.showerror(
                    "No se pudo guardar", str(error), parent=ventana
                )

        botones = tk.Frame(marco, bg=self.color_fondo)
        botones.pack(fill="x", pady=(18, 0))

        tk.Button(
            botones, text="Cancelar", command=ventana.destroy,
            bg=self.color_blanco, fg=self.color_texto,
            relief="solid", bd=1, padx=15, pady=7, cursor="hand2"
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            botones, text="Guardar", command=guardar,
            bg=self.color_acento, fg=self.color_blanco,
            activebackground="#1D68C5",
            activeforeground=self.color_blanco,
            relief="flat", padx=18, pady=8, cursor="hand2"
        ).pack(side="right")

        ventana.bind("<Return>", lambda evento: guardar())
        ventana.bind("<Escape>", lambda evento: ventana.destroy())

    def cambiar_estado_categoria(self):
        categoria = self.obtener_categoria_seleccionada()
        if categoria is None:
            return

        try:
            from categoria_dao import (
                activar_categoria, desactivar_categoria
            )

            if categoria["estado"] == "Activa":
                if not messagebox.askyesno(
                    "Desactivar categoría",
                    f"¿Querés desactivar '{categoria['nombre']}'?\n\n"
                    "Los productos asociados se conservarán, pero "
                    "esta categoría dejará de aparecer en los "
                    "formularios que muestran categorías activas."
                ):
                    return

                resultado = desactivar_categoria(categoria["id"])
                mensaje = (
                    "Categoría desactivada correctamente."
                    if resultado else "La categoría ya estaba inactiva."
                )
            else:
                resultado = activar_categoria(categoria["id"])
                mensaje = (
                    "Categoría reactivada correctamente."
                    if resultado else "La categoría ya estaba activa."
                )

            self.cargar_categorias()
            messagebox.showinfo("Categorías", mensaje)
        except Exception as error:
            messagebox.showerror(
                "No se pudo cambiar el estado", str(error)
            )

    # =========================================================
    # MOVIMIENTOS
    # =========================================================

    def mostrar_movimientos(self):
        self.limpiar_area()
        self.crear_encabezado(
            "Movimientos",
            "Registrá entradas y salidas y consultá el historial."
        )

        contenido = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(25, 5, 25, 20)
        )
        contenido.pack(fill="both", expand=True)

        formulario = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=16
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(
            formulario,
            text="Registrar movimiento",
            style="TarjetaTitulo.TLabel"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        for columna, texto in enumerate(
            ("Producto", "Tipo", "Cantidad", "Observación")
        ):
            ttk.Label(formulario, text=texto).grid(
                row=1, column=columna, sticky="w",
                padx=(0, 8) if columna == 0 else 8
            )

        self.mov_producto_var = tk.StringVar()
        self.mov_tipo_var = tk.StringVar(value="ENTRADA")
        self.mov_cantidad_var = tk.StringVar()
        self.mov_observacion_var = tk.StringVar()
        self.mov_productos = {}

        self.mov_producto_combo = ttk.Combobox(
            formulario, textvariable=self.mov_producto_var,
            state="readonly"
        )
        self.mov_producto_combo.grid(
            row=2, column=0, sticky="ew", padx=(0, 8), pady=(5, 10)
        )

        self.mov_tipo_combo = ttk.Combobox(
            formulario, textvariable=self.mov_tipo_var,
            values=("ENTRADA", "SALIDA"), state="readonly", width=12
        )
        self.mov_tipo_combo.grid(
            row=2, column=1, sticky="ew", padx=8, pady=(5, 10)
        )

        ttk.Entry(
            formulario, textvariable=self.mov_cantidad_var
        ).grid(row=2, column=2, sticky="ew", padx=8, pady=(5, 10))

        ttk.Entry(
            formulario, textvariable=self.mov_observacion_var
        ).grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(5, 10))

        self.mov_stock_label = ttk.Label(
            formulario, text="Stock actual: —",
            style="TarjetaTexto.TLabel"
        )
        self.mov_stock_label.grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        for columna in range(4):
            formulario.columnconfigure(columna, weight=1)

        botones = ttk.Frame(formulario, style="Tarjeta.TFrame")
        botones.grid(row=4, column=0, columnspan=4, sticky="w")

        tk.Button(
            botones, text="Registrar movimiento",
            command=self.registrar_movimiento_ui,
            bg=self.color_acento, fg=self.color_blanco,
            activebackground="#1D68C5",
            activeforeground=self.color_blanco,
            font=("Segoe UI", 10, "bold"), relief="flat",
            padx=15, pady=9, cursor="hand2"
        ).pack(side="left")

        tk.Button(
            botones, text="Actualizar historial",
            command=self.cargar_movimientos_ui,
            bg=self.color_blanco, fg=self.color_texto,
            relief="solid", bd=1, padx=15, pady=8, cursor="hand2"
        ).pack(side="left", padx=(10, 0))

        historial = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=12
        )
        historial.pack(fill="both", expand=True)

        ttk.Label(
            historial,
            text="Historial de movimientos",
            style="TarjetaTitulo.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        columnas = (
            "id", "fecha", "producto", "tipo", "cantidad", "observacion"
        )
        self.tabla_movimientos = ttk.Treeview(
            historial, columns=columnas, show="headings",
            selectmode="browse"
        )

        configuracion = [
            ("id", "ID", 50, "center"),
            ("fecha", "Fecha", 145, "center"),
            ("producto", "Producto", 165, "w"),
            ("tipo", "Tipo", 90, "center"),
            ("cantidad", "Cantidad", 80, "center"),
            ("observacion", "Observación", 230, "w"),
        ]

        for columna, titulo, ancho, ancla in configuracion:
            self.tabla_movimientos.heading(columna, text=titulo)
            self.tabla_movimientos.column(
                columna, width=ancho, anchor=ancla
            )

        scroll_y = ttk.Scrollbar(
            historial, orient="vertical",
            command=self.tabla_movimientos.yview
        )
        scroll_x = ttk.Scrollbar(
            historial, orient="horizontal",
            command=self.tabla_movimientos.xview
        )

        self.tabla_movimientos.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        self.tabla_movimientos.pack(side="top", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.mov_producto_combo.bind(
            "<<ComboboxSelected>>", self.actualizar_stock_movimiento_ui
        )
        self.cargar_productos_movimiento_ui()
        self.cargar_movimientos_ui()

    def cargar_productos_movimiento_ui(self):
        conexion = None
        cursor = None
        try:
            from conexion import obtener_conexion
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_producto, nombre FROM productos ORDER BY nombre"
            )
            productos = cursor.fetchall()

            self.mov_productos = {
                f"{p['id_producto']} - {p['nombre']}": p["id_producto"]
                for p in productos
            }
            self.mov_producto_combo["values"] = list(self.mov_productos)

            if productos:
                self.mov_producto_combo.current(0)
                self.actualizar_stock_movimiento_ui()
            else:
                self.mov_stock_label.config(
                    text="No hay productos registrados."
                )
        except Exception as error:
            messagebox.showerror(
                "Error", f"No se pudieron cargar los productos.\n\n{error}"
            )
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

    def actualizar_stock_movimiento_ui(self, evento=None):
        seleccion = self.mov_producto_var.get()
        if not seleccion or seleccion not in self.mov_productos:
            self.mov_stock_label.config(text="Stock actual: —")
            return

        try:
            from movimiento_dao import obtener_stock
            stock = obtener_stock(self.mov_productos[seleccion])
            self.mov_stock_label.config(
                text=f"Stock actual: {stock} unidades"
            )
        except Exception as error:
            self.mov_stock_label.config(text="Stock actual: no disponible")
            messagebox.showerror("Error de stock", str(error))

    def registrar_movimiento_ui(self):
        seleccion = self.mov_producto_var.get()
        if not seleccion or seleccion not in self.mov_productos:
            messagebox.showwarning(
                "Falta el producto", "Seleccioná un producto."
            )
            return

        cantidad_texto = self.mov_cantidad_var.get().strip()
        if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
            messagebox.showwarning(
                "Cantidad inválida",
                "Ingresá una cantidad entera mayor que cero."
            )
            return

        cantidad = int(cantidad_texto)
        if cantidad > 2147483647:
            messagebox.showwarning(
                "Cantidad inválida",
                "La cantidad ingresada es demasiado grande."
            )
            return

        tipo = self.mov_tipo_var.get()
        observacion = self.mov_observacion_var.get().strip()

        if len(observacion) > 200:
            messagebox.showwarning(
                "Observación demasiado larga",
                "La observación admite hasta 200 caracteres."
            )
            return

        try:
            from movimiento_dao import registrar_movimiento
            resultado = registrar_movimiento(
                self.mov_productos[seleccion], tipo, cantidad, observacion
            )
            self.mov_cantidad_var.set("")
            self.mov_observacion_var.set("")
            self.cargar_movimientos_ui()
            self.actualizar_stock_movimiento_ui()

            messagebox.showinfo(
                "Movimiento registrado",
                f"Producto: {resultado['producto']}\n"
                f"Tipo: {resultado['tipo_movimiento']}\n"
                f"Cantidad: {resultado['cantidad']}\n"
                f"Stock anterior: {resultado['stock_anterior']}\n"
                f"Stock nuevo: {resultado['stock_nuevo']}"
            )
        except Exception as error:
            messagebox.showerror(
                "No se pudo registrar el movimiento", str(error)
            )

    def cargar_movimientos_ui(self):
        try:
            from movimiento_dao import listar_movimientos
            movimientos = listar_movimientos()

            for item in self.tabla_movimientos.get_children():
                self.tabla_movimientos.delete(item)

            for movimiento in movimientos:
                fecha = movimiento["fecha"]
                if fecha:
                    fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")

                self.tabla_movimientos.insert(
                    "", "end",
                    values=(
                        movimiento["id_movimiento"],
                        fecha or "",
                        movimiento["producto"],
                        movimiento["tipo_movimiento"],
                        movimiento["cantidad"],
                        movimiento["observacion"] or ""
                    )
                )
        except Exception as error:
            messagebox.showerror(
                "Error", f"No se pudo cargar el historial.\n\n{error}"
            )

    # =========================================================
    # STOCK ACTUAL
    # =========================================================

    def consultar_datos_stock(self):
        """Devuelve el stock calculado a partir de los movimientos."""
        conexion = None
        cursor = None

        try:
            from conexion import obtener_conexion

            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.nombre,
                    c.nombre AS categoria,
                    p.precio,
                    p.stock_minimo,
                    COALESCE(
                        SUM(
                            CASE
                                WHEN UPPER(m.tipo_movimiento) = 'ENTRADA'
                                    THEN m.cantidad
                                WHEN UPPER(m.tipo_movimiento) = 'SALIDA'
                                    THEN -m.cantidad
                                ELSE 0
                            END
                        ), 0
                    ) AS stock_actual
                FROM productos p
                LEFT JOIN categorias c
                    ON c.id_categoria = p.id_categoria
                LEFT JOIN movimientos m
                    ON m.id_producto = p.id_producto
                GROUP BY
                    p.id_producto,
                    p.nombre,
                    c.nombre,
                    p.precio,
                    p.stock_minimo
                ORDER BY p.nombre
            """)

            return cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

    def mostrar_stock(self):
        self.limpiar_area()
        self.crear_encabezado(
            "Stock actual",
            "Consultá las existencias calculadas a partir de los movimientos."
        )

        contenido = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(25, 5, 25, 20)
        )
        contenido.pack(fill="both", expand=True)

        barra = ttk.Frame(contenido, style="Principal.TFrame")
        barra.pack(fill="x", pady=(0, 12))

        ttk.Label(
            barra, text="Buscar producto:",
            background=self.color_fondo,
            foreground=self.color_texto,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 8))

        self.stock_busqueda_var = tk.StringVar()
        entrada_busqueda = ttk.Entry(
            barra, textvariable=self.stock_busqueda_var, width=28
        )
        entrada_busqueda.pack(side="left", padx=(0, 15))
        entrada_busqueda.bind(
            "<KeyRelease>", lambda evento: self.aplicar_filtro_stock()
        )

        ttk.Label(
            barra, text="Mostrar:",
            background=self.color_fondo,
            foreground=self.color_texto,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 8))

        self.stock_filtro_var = tk.StringVar(value="Todos")
        filtro = ttk.Combobox(
            barra, textvariable=self.stock_filtro_var,
            values=("Todos", "Stock bajo"),
            state="readonly", width=14
        )
        filtro.pack(side="left")
        filtro.bind(
            "<<ComboboxSelected>>",
            lambda evento: self.aplicar_filtro_stock()
        )

        tk.Button(
            barra, text="Actualizar", command=self.cargar_stock_ui,
            bg=self.color_acento, fg=self.color_blanco,
            activebackground="#1D68C5",
            activeforeground=self.color_blanco,
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=15, pady=8, cursor="hand2"
        ).pack(side="right")

        tarjeta = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=12
        )
        tarjeta.pack(fill="both", expand=True)

        columnas = (
            "id", "producto", "categoria", "precio",
            "stock", "minimo", "estado"
        )
        self.tabla_stock = ttk.Treeview(
            tarjeta, columns=columnas, show="headings",
            selectmode="browse", style="Stock.Treeview"
        )

        configuracion = [
            ("id", "ID", 55, "center"),
            ("producto", "Producto", 220, "w"),
            ("categoria", "Categoría", 160, "w"),
            ("precio", "Precio unitario", 120, "e"),
            ("stock", "Stock actual", 110, "center"),
            ("minimo", "Stock mínimo", 110, "center"),
            ("estado", "Estado", 130, "center"),
        ]

        for columna, titulo, ancho, ancla in configuracion:
            self.tabla_stock.heading(columna, text=titulo)
            self.tabla_stock.column(
                columna, width=ancho, anchor=ancla
            )

        self.tabla_stock.tag_configure(
            "bajo", foreground="#B42318", background="#FDECEC"
        )
        self.tabla_stock.tag_configure(
            "normal", foreground="#263238"
        )

        scroll_y = ttk.Scrollbar(
            tarjeta, orient="vertical", command=self.tabla_stock.yview
        )
        scroll_x = ttk.Scrollbar(
            tarjeta, orient="horizontal", command=self.tabla_stock.xview
        )
        self.tabla_stock.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.tabla_stock.pack(side="top", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.stock_estado_label = ttk.Label(
            contenido, text="", style="Subtitulo.TLabel"
        )
        self.stock_estado_label.pack(anchor="w", pady=(10, 0))

        self.cargar_stock_ui()

    def cargar_stock_ui(self):
        try:
            self.stock_datos = self.consultar_datos_stock()
            self.aplicar_filtro_stock()
        except Exception as error:
            messagebox.showerror(
                "Error al consultar stock",
                f"No se pudo cargar el stock actual.\n\n{error}"
            )

    def aplicar_filtro_stock(self):
        if not hasattr(self, "stock_datos"):
            return

        busqueda = self.stock_busqueda_var.get().strip().casefold()
        filtro = self.stock_filtro_var.get()

        for item in self.tabla_stock.get_children():
            self.tabla_stock.delete(item)

        total_productos = 0
        productos_bajos = 0

        for producto in self.stock_datos:
            stock = int(producto["stock_actual"] or 0)
            minimo = int(producto["stock_minimo"] or 0)
            nombre = producto["nombre"] or ""
            categoria = producto["categoria"] or "Sin categoría"
            es_bajo = stock <= minimo

            if busqueda and busqueda not in nombre.casefold():
                continue

            if filtro == "Stock bajo" and not es_bajo:
                continue

            estado = "Stock bajo" if es_bajo else "Normal"
            precio = float(producto["precio"] or 0)

            self.tabla_stock.insert(
                "", "end",
                values=(
                    producto["id_producto"], nombre, categoria,
                    f"$ {precio:,.2f}", stock, minimo, estado
                ),
                tags=("bajo" if es_bajo else "normal",)
            )

            total_productos += 1
            if es_bajo:
                productos_bajos += 1

        if filtro == "Stock bajo":
            texto = (
                f"Productos mostrados: {total_productos} | "
                "Stock actual igual o inferior al mínimo."
            )
        else:
            texto = (
                f"Productos mostrados: {total_productos} | "
                f"Productos con stock bajo en el listado: {productos_bajos}"
            )

        self.stock_estado_label.config(text=texto)

    # =========================================================
    # REPORTES
    # =========================================================

    def mostrar_reportes(self):
        self.limpiar_area()
        self.crear_encabezado(
            "Reportes",
            "Consultá el inventario y el historial de movimientos."
        )

        contenido = ttk.Frame(
            self.area_principal,
            style="Principal.TFrame",
            padding=(25, 5, 25, 20)
        )
        contenido.pack(fill="both", expand=True)

        filtros = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=15
        )
        filtros.pack(fill="x", pady=(0, 12))

        ttk.Label(
            filtros, text="Tipo de reporte",
            style="TarjetaTitulo.TLabel"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(filtros, text="Reporte:").grid(
            row=1, column=0, sticky="w", padx=(0, 8)
        )

        self.reporte_tipo_var = tk.StringVar(value="Stock actual")

        self.reporte_tipo_combo = ttk.Combobox(
            filtros,
            textvariable=self.reporte_tipo_var,
            values=(
                "Stock actual",
                "Stock bajo",
                "Movimientos"
            ),
            state="readonly",
            width=22
        )
        self.reporte_tipo_combo.grid(
            row=1, column=1, sticky="w", padx=(0, 20)
        )
        self.reporte_tipo_combo.bind(
            "<<ComboboxSelected>>", self.cambiar_tipo_reporte
        )

        ttk.Label(filtros, text="Desde (AAAA-MM-DD):").grid(
            row=1, column=2, sticky="w", padx=(0, 8)
        )

        self.reporte_desde_var = tk.StringVar(
            value=date.today().replace(day=1).isoformat()
        )
        self.reporte_desde_entry = ttk.Entry(
            filtros, textvariable=self.reporte_desde_var, width=14
        )
        self.reporte_desde_entry.grid(
            row=1, column=3, sticky="w", padx=(0, 15)
        )

        ttk.Label(filtros, text="Hasta (AAAA-MM-DD):").grid(
            row=2, column=2, sticky="w", padx=(0, 8), pady=(10, 0)
        )

        self.reporte_hasta_var = tk.StringVar(
            value=date.today().isoformat()
        )
        self.reporte_hasta_entry = ttk.Entry(
            filtros, textvariable=self.reporte_hasta_var, width=14
        )
        self.reporte_hasta_entry.grid(
            row=2, column=3, sticky="w", padx=(0, 15), pady=(10, 0)
        )

        ttk.Label(filtros, text="Tipo de movimiento:").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=(10, 0)
        )

        self.reporte_movimiento_var = tk.StringVar(value="Todos")
        self.reporte_movimiento_combo = ttk.Combobox(
            filtros,
            textvariable=self.reporte_movimiento_var,
            values=("Todos", "ENTRADA", "SALIDA"),
            state="readonly",
            width=19
        )
        self.reporte_movimiento_combo.grid(
            row=2, column=1, sticky="w", pady=(10, 0)
        )

        self.reporte_desde_entry.config(state="disabled")
        self.reporte_hasta_entry.config(state="disabled")
        self.reporte_movimiento_combo.config(state="disabled")

        tk.Button(
            filtros,
            text="Consultar reporte",
            command=self.generar_reporte,
            bg=self.color_acento,
            fg=self.color_blanco,
            activebackground="#1D68C5",
            activeforeground=self.color_blanco,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        ).grid(row=3, column=0, sticky="w", pady=(15, 0))

        for columna in range(4):
            filtros.columnconfigure(columna, weight=1)

        resumen = ttk.Frame(
            contenido, style="Principal.TFrame"
        )
        resumen.pack(fill="x", pady=(0, 10))

        self.reporte_resumen_label = ttk.Label(
            resumen,
            text="Seleccioná un reporte y presioná Consultar reporte.",
            style="Subtitulo.TLabel"
        )
        self.reporte_resumen_label.pack(anchor="w")

        tarjeta_tabla = ttk.Frame(
            contenido, style="Tarjeta.TFrame", padding=12
        )
        tarjeta_tabla.pack(fill="both", expand=True)

        self.tabla_reportes = ttk.Treeview(
            tarjeta_tabla,
            show="headings",
            style="Stock.Treeview"
        )

        scroll_y = ttk.Scrollbar(
            tarjeta_tabla,
            orient="vertical",
            command=self.tabla_reportes.yview
        )
        scroll_x = ttk.Scrollbar(
            tarjeta_tabla,
            orient="horizontal",
            command=self.tabla_reportes.xview
        )

        self.tabla_reportes.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        self.tabla_reportes.tag_configure(
            "bajo", foreground="#B42318", background="#FDECEC"
        )
        self.tabla_reportes.tag_configure(
            "normal", foreground="#263238"
        )
        self.tabla_reportes.tag_configure(
            "entrada", foreground="#167647"
        )
        self.tabla_reportes.tag_configure(
            "salida", foreground="#B42318"
        )

        self.tabla_reportes.pack(
            side="top", fill="both", expand=True
        )
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.generar_reporte()

    def cambiar_tipo_reporte(self, evento=None):
        tipo = self.reporte_tipo_var.get()

        es_movimientos = tipo == "Movimientos"

        estado_fechas = "normal" if es_movimientos else "disabled"
        self.reporte_desde_entry.config(state=estado_fechas)
        self.reporte_hasta_entry.config(state=estado_fechas)

        estado_tipo = "readonly" if es_movimientos else "disabled"
        self.reporte_movimiento_combo.config(state=estado_tipo)

        self.generar_reporte()

    def configurar_columnas_reporte(self, configuracion):
        columnas = [elemento[0] for elemento in configuracion]
        self.tabla_reportes["columns"] = columnas

        for columna, titulo, ancho, ancla in configuracion:
            self.tabla_reportes.heading(columna, text=titulo)
            self.tabla_reportes.column(
                columna, width=ancho, anchor=ancla, stretch=True
            )

    def limpiar_tabla_reportes(self):
        for item in self.tabla_reportes.get_children():
            self.tabla_reportes.delete(item)

    def generar_reporte(self):
        tipo = self.reporte_tipo_var.get()
        self.limpiar_tabla_reportes()

        try:
            if tipo == "Stock actual":
                self.reporte_stock(bajo=False)
            elif tipo == "Stock bajo":
                self.reporte_stock(bajo=True)
            elif tipo == "Movimientos":
                self.reporte_movimientos()
        except Exception as error:
            self.reporte_resumen_label.config(
                text="No se pudo generar el reporte."
            )
            messagebox.showerror(
                "Error al generar el reporte",
                f"Ocurrió un problema al consultar los datos.\n\n{error}"
            )

    def reporte_stock(self, bajo=False):
        productos = self.consultar_datos_stock()

        configuracion = [
            ("id", "ID", 55, "center"),
            ("producto", "Producto", 210, "w"),
            ("categoria", "Categoría", 150, "w"),
            ("precio", "Precio unitario", 120, "e"),
            ("stock", "Stock actual", 105, "center"),
            ("minimo", "Stock mínimo", 105, "center"),
            ("estado", "Estado", 120, "center"),
        ]
        self.configurar_columnas_reporte(configuracion)

        mostrados = 0
        cantidad_bajos = 0
        unidades_totales = 0

        for producto in productos:
            stock = int(producto["stock_actual"] or 0)
            minimo = int(producto["stock_minimo"] or 0)
            es_bajo = stock <= minimo

            if es_bajo:
                cantidad_bajos += 1

            if bajo and not es_bajo:
                continue

            precio = float(producto["precio"] or 0)

            self.tabla_reportes.insert(
                "",
                "end",
                values=(
                    producto["id_producto"],
                    producto["nombre"],
                    producto["categoria"] or "Sin categoría",
                    f"$ {precio:,.2f}",
                    stock,
                    minimo,
                    "Stock bajo" if es_bajo else "Normal"
                ),
                tags=("bajo" if es_bajo else "normal",)
            )

            mostrados += 1
            unidades_totales += stock

        if bajo:
            texto = (
                f"Productos con stock bajo: {mostrados} | "
                "Se incluyen productos cuyo stock es igual o inferior "
                "al mínimo."
            )
        else:
            texto = (
                f"Productos: {mostrados} | "
                f"Unidades en inventario: {unidades_totales} | "
                f"Productos con stock bajo: {cantidad_bajos}"
            )

        self.reporte_resumen_label.config(text=texto)

    def reporte_movimientos(self):
        desde_texto = self.reporte_desde_var.get().strip()
        hasta_texto = self.reporte_hasta_var.get().strip()

        try:
            desde = datetime.strptime(desde_texto, "%Y-%m-%d").date()
            hasta = datetime.strptime(hasta_texto, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                "Ingresá las fechas con formato AAAA-MM-DD. "
                "Por ejemplo: 2026-10-01."
            )

        if desde > hasta:
            raise ValueError(
                "La fecha Desde no puede ser posterior a la fecha Hasta."
            )

        tipo_movimiento = self.reporte_movimiento_var.get()

        configuracion = [
            ("id", "ID", 55, "center"),
            ("fecha", "Fecha y hora", 155, "center"),
            ("producto", "Producto", 200, "w"),
            ("tipo", "Tipo", 100, "center"),
            ("cantidad", "Cantidad", 100, "center"),
            ("observacion", "Observación", 280, "w"),
        ]
        self.configurar_columnas_reporte(configuracion)

        conexion = None
        cursor = None

        try:
            from conexion import obtener_conexion

            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    m.id_movimiento,
                    m.fecha,
                    p.nombre AS producto,
                    m.tipo_movimiento,
                    m.cantidad,
                    m.observacion
                FROM movimientos m
                INNER JOIN productos p
                    ON p.id_producto = m.id_producto
                WHERE m.fecha >= %s
                  AND m.fecha < DATE_ADD(%s, INTERVAL 1 DAY)
            """

            parametros = [
                desde.strftime("%Y-%m-%d"),
                hasta.strftime("%Y-%m-%d")
            ]

            if tipo_movimiento != "Todos":
                consulta += " AND UPPER(m.tipo_movimiento) = %s"
                parametros.append(tipo_movimiento)

            consulta += " ORDER BY m.fecha DESC, m.id_movimiento DESC"

            cursor.execute(consulta, tuple(parametros))
            movimientos = cursor.fetchall()

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

        total_entradas = 0
        total_salidas = 0

        for movimiento in movimientos:
            tipo = str(movimiento["tipo_movimiento"]).upper()
            cantidad = int(movimiento["cantidad"] or 0)
            fecha = movimiento["fecha"]

            if fecha:
                fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
            else:
                fecha = ""

            if tipo == "ENTRADA":
                total_entradas += cantidad
            elif tipo == "SALIDA":
                total_salidas += cantidad

            self.tabla_reportes.insert(
                "",
                "end",
                values=(
                    movimiento["id_movimiento"],
                    fecha,
                    movimiento["producto"],
                    tipo,
                    cantidad,
                    movimiento["observacion"] or ""
                ),
                tags=("entrada" if tipo == "ENTRADA" else "salida",)
            )

        self.reporte_resumen_label.config(
            text=(
                f"Movimientos encontrados: {len(movimientos)} | "
                f"Unidades ingresadas: {total_entradas} | "
                f"Unidades retiradas: {total_salidas} | "
                f"Período: {desde.strftime('%d/%m/%Y')} al "
                f"{hasta.strftime('%d/%m/%Y')}"
            )
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPanStock(root)
    root.mainloop()



