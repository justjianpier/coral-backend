from app.models.product_model import Product
from app.models.category_model import Category
from app.schemas.product_schema import ProductSchema
from db import db
import requests

class ProductService:
    def get_all(self) -> list[Product]:
        products = Product.query.filter_by(is_active=True)
        return products

    def get_last(self) -> Product | None:
        product = Product.query.order_by(
            Product.id.desc()
        ).first()
        return product

    def create(
            self,
            data: ProductSchema,
            code: str,
            image: str
    ) -> Product:
        product = Product(
            name=data.name,
            code=code,
            description=data.description,
            image=image,
            brand=data.brand,
            size=data.size,
            price=data.price,
            stock=data.stock,
            category_id=data.category_id
        )
        db.session.add(product)
        db.session.commit()
        return product
    
    def update(
            self,
            product: Product,
            data: ProductSchema,
            image: str | None = None
        ) -> Product:
        if image:
            product.image = image
        product.name = data.name
        product.description = data.description
        product.brand = data.brand
        product.size = data.size
        product.price = data.price
        product.stock = data.stock
        product.category_id = data.category_id
        db.session.commit()
        return product

    def get_by_id(self, id: int) -> Product | None:
        product = Product.query.filter_by(
            id=id,
            is_active=True
        ).first()
        return product

    def delete(self, product: Product) -> None:
        product.is_active = False
        db.session.commit()
        return None
    
    def seed_from_api(self) -> dict:
        try:
            response = requests.get('https://fakestoreapi.com/products')
            if response.status_code != 200:
                return {
                    "error": f"Error al conectar con FakeStoreAPI: Código {response.status_code}"
                }
            
            api_products = response.json()
            counter = 0

            for item in api_products:
                category_name = item['category']
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.commit()

                existing_product = Product.query.filter_by(name=item['title']).first()
                if not existing_product:
                    
                    last_p = self.get_last()
                    next_code = 'P-00001'
                    if last_p:
                        code_num = int(last_p.code.split('-')[1]) + 1
                        next_code = 'P-' + str(code_num).zfill(5)

                    nuevo_producto = Product(
                        name=item['title'],              
                        code=next_code,                  
                        description=item['description'], 
                        image=item['image'],             
                        brand="FakeStore Brand",         
                        size="Estándar",                 
                        price=float(item['price']),      
                        stock=25,                        
                        category_id=category.id          
                    )
                    db.session.add(nuevo_producto)
                    counter += 1            

            db.session.commit()
            return {
                "message": f"Semilla ejecutada con éxito. Se inyectaron {counter} productos nuevos."
            }

        except Exception as e:
            db.session.rollback()
            return {
                "error": f"Fallo en la siembra de datos: {str(e)}"
            }

product_service = ProductService()