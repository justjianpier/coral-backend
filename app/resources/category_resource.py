from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from db import db
from app.services.category_service import category_service
from app.schemas.category_schema import CategorySchema

class CategoryResource(Resource):
    def get(self):
        try:
            categories = category_service.get_all()

            categories_list = [category.to_json() for category in categories]

            return categories_list, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400
    
    def post(self):
        try:
            data = request.get_json()
            validated_data = CategorySchema.model_validate(data)

            category = category_service.create(validated_data)

            return category.to_json(), 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400
    

class ManageCategoryResource(Resource):
    def get(self, category_id: int):
        try:
            category = category_service.get_by_id(category_id)

            if not category:
                return {
                    'error': 'Category not found'
                }, 404
            
            return category.to_json(), 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400
    
    def put(self, category_id: int):
        try:
            data = request.get_json()
            validated_data = CategorySchema.model_validate(data)

            category = category_service.get_by_id(category_id)

            if not category:
                return {
                    'error': 'Category not found'
                }, 404
            
            updated_category = category_service.update(
                category,
                validated_data
            )

            return updated_category.to_json(), 200
        except ValidationError as e:
            return {
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400
    
    def delete(self, category_id: int):
        try:
            category = category_service.get_by_id(category_id)

            if not category:
                return {
                    'error': 'Category not found'
                }, 404
            
            category_service.delete(category)

            return None, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400