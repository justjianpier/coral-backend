from flask_restful import Api
from app import app
from app.resources.auth_resource import *
from app.resources.product_resource import *
from app.resources.category_resource import *
from flask_swagger_ui import get_swaggerui_blueprint

api = Api(app, prefix='/api/v1')

# Interfaz de SWAGGER
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Coral Store API"}
)
app.register_blueprint(swaggerui_blueprint)

# Autenticación
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

# Gestión de productos
api.add_resource(ProductResource, '/products')
api.add_resource(ManageProductResource, '/products/<int:product_id>')

api.add_resource(CategoryResource, '/categories')
api.add_resource(ManageCategoryResource, '/categories/<int:category_id>')

# Sincronizar semilla inicial
api.add_resource(ProductSyncResource, '/products/sync')