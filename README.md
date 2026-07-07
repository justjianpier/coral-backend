# Coral Backend

Este es un proyecto backend desarrollado con **Flask** cuyo propósito principal es servir como API de conexión, procesando los datos y reglas de negocio para ser consumidos de manera dinámica por una interfaz frontend en **React (Vite)**. 

El sistema se integra con **FakeStoreAPI** como proveedor de datos externo, consumiendo su API para obtener un catálogo inicial de productos y realizar un proceso de siembra (*seeding*) automatizado hacia la base de datos local.



##  Características del Proyecto

* **Catálogo de Productos**: Listado dinámico consumido desde el backend en tiempo real.
* **Operaciones CRUD**: Gestión completa de productos (Crear, Leer, Actualizar, Eliminar).
* **Persistencia de Datos**: Conexión e integración con base de datos a través de SQLAlchemy.
* **Sincronización Automática**: Endpoint integrado para sembrar e inicializar la base de datos con la semilla de productos externos.
* **Documentación Interactiva**: API totalmente documentada y testeable mediante **Swagger UI**.


##  Tecnologías Utilizadas

### Backend
* **Python** & **Flask** (Flask-RESTful)
* **SQLAlchemy** (ORM para persistencia)
* **Cloudinary** (Almacenamiento en la nube para las imágenes)
* **Flask-Swagger-UI** (Documentación de la API)


##  Estructura del Repositorio

```text
├── backend/               # Código fuente del servidor Flask
│   ├── app/
│   │   ├── resources/     # Controladores que manejan las peticiones HTTP (Resources de Flask-RESTful)
│   │   ├── schemas/       # Esquemas de validación de datos (Pydantic / Marshmallow)
│   │   ├── services/      # Lógica de negocio y comunicación con la base de datos
│   │   ├── static/        # Archivos estáticos del servidor (Contiene swagger.json)
│   │   ├── utils/         # Funciones utilitarias o helpers (Cloudinary, validaciones extra)
│   │   ├── router.py      # Controlador central de rutas (Registra los recursos en la API)
│   │   └── __init__.py    # Inicialización y configuración de la aplicación Flask
│   └── requirements.txt   # Dependencias de Python requeridas para el backend

```


## Instalación y Ejecución del Proyecto
### Requisitos Previos
- Python 3.10 o superior
- Un gestor de base de datos compatible o SQLite por defecto


### Clonar el Repositorio
- git clone https://github.com/justjianpier/coral-backend.git


### Configurar el entorno virtual (Windows)
```bash
# Crear el entorno virtual
python -m venv entorno_flask

# Activar el entorno virtual
venv\Scripts\activate
```

## Instalar Dependencias del proyecto
```bash
pip install -r requirements.txt
```

## Levantar el Servidor de Flask
```bash
flask run
```
Al ejecutarlo correctamente, la terminal se quedará escuchando e indicará que la API está disponible en: http://localhost:5000

## Documentación de la API (Swagger UI)
La API cuenta con una interfaz gráfica interactiva utilizando Swagger UI para probar y visualizar todos los recursos CRUD en tiempo real sin necesidad de un cliente externo como Bruno o Postman.

Para acceder, asegúrate de que el backend esté corriendo (flask run) e ingresa desde tu navegador a la siguiente dirección: http://localhost:5000/docs

Endpoints Principales Disponibles:
- **GET** /api/v1/products - Obtener el inventario completo de productos.

- **POST** /api/v1/products - Crear un producto cargando una imagen física a Cloudinary.

- **PUT** /api/v1/products/<product_id> - Actualizar información o stock de un producto específico.

- **DELETE** /api/v1/products/<product_id> - Eliminación o desactivación lógica de un recurso.

- **POST** /api/v1/products/sync - Ejecución de la siembra inicial del catálogo.