from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from db import db
from app.schemas.product_schema import ProductSchema
from app.utils.helpers import cloudinary_helper
from app.services.product_service import product_service

class ProductResource(Resource):
    def get(self):
        try:
            products = product_service.get_all()
            products_list = []
            for product in products:

                if not product.image.startswith('http'):
                    secure_url = cloudinary_helper.get_secure_url(product.image)
                    product.image = secure_url
                
                products_list.append(product.to_json())

            return products_list, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    def post(self):
        try:
            data = request.form
            image = request.files.get('image')

            cloudinary_helper.validate_image(image)
            
            validated_data = ProductSchema.model_validate(data)
            
            secure_url, public_id = cloudinary_helper.upload_image(
                image,
                'products'
            )

            if not secure_url:
                return {
                    'error': 'Error uploading image'
                }, 400

            next_code = 'P-00001'
            product = product_service.get_last()

            if product:
                code = product.code
                next_code = 'P-' + str(int(code.split('-')[1]) + 1).zfill(5)

            created_product = product_service.create(
                validated_data,
                next_code,
                public_id
            )

            created_product.image = secure_url

            return created_product.to_json(), 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
class ManageProductResource(Resource):
    def get(self, product_id: int):
        try:
            product = product_service.get_by_id(product_id)

            if not product:
                return {
                    'error': 'Product not found'
                }, 404
            
            return product.to_json(), 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    def put(self, product_id: int):
        try:
            data = request.form
            validated_data = ProductSchema.model_validate(data)

            product = product_service.get_by_id(product_id)

            if not product:
                return {
                    'error': 'Product not found'
                }, 404
            
            image = request.files.get('image')

            # Inicia con valores actuales que ya existe en la base de datos
            public_id = getattr(product, 'image_id', None) 
            secure_url = product.image

            if image:
                cloudinary_helper.validate_image(image)
                
                secure_url, public_id = cloudinary_helper.upload_image(
                    image,
                    'products'
                )
                cloudinary_helper.delete_image(product.image)

                if not secure_url:
                    return {
                        'error': 'Error uploading image'
                    }, 400
            
            updated_product = product_service.update(
                product,
                validated_data,
                public_id
            )
            
            updated_product.image = secure_url

            return updated_product.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    def delete(self, product_id: int):
        try:
            product = product_service.get_by_id(product_id)

            if not product:
                return {
                    'error': 'Product not found'
                }, 404
            
            product_service.delete(product)
            
            return None, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400
    

class ProductSyncResource(Resource):
    def post(self):
        try:
            resultado = product_service.seed_from_api()
            
            if "error" in resultado:
                return resultado, 400
                
            return resultado, 200
        except Exception as e:
            return {
                'error': f"Error en el controlador de sincronización: {str(e)}"
            }, 400