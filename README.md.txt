# PanStock — Instrucciones de instalación y ejecución

## Requisitos previos

Para ejecutar el proyecto, es necesario tener instalado:

- MySQL 8.0.
- Python 3.

## 1. Importar la base de datos

Desde la carpeta donde se encuentra el archivo `panstock.sql`, abrir una terminal y ejecutar:

```bash
mysql -u root -p < panstock.sql
```

Cuando MySQL solicite la contraseña, ingresar la correspondiente al usuario configurado en la instalación.

Este comando importa la estructura y los datos incluidos en el archivo SQL.

## 2. Configurar la conexión a MySQL

Abrir el archivo `conexion.py` y verificar que los parámetros de conexión correspondan a la instalación local de MySQL.

Si el programa utiliza el usuario `panstock_app`, será necesario crearlo en MySQL y otorgarle los permisos correspondientes sobre la base de datos `panstock`. También se deberá verificar que la contraseña configurada coincida con la utilizada por el programa.

## 3. Instalar la dependencia

Desde la terminal, ejecutar:

```bash
py -m pip install mysql-connector-python
```

## 4. Ejecutar el programa

Desde la carpeta principal del proyecto, ejecutar:

```bash
py menu.py
```

Si se utiliza otro intérprete de Python, puede ser necesario adaptar el comando de ejecución.

## Nota

Los parámetros de conexión y los requisitos adicionales deberán ajustarse según la configuración del entorno local.