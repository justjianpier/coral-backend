from db import db
from sqlalchemy import Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
# 👇 IMPORTAMOS EL HELPER (Asumiendo que está en utils.py, si está en otro archivo ajusta el nombre)
from app.utils.helpers import cloudinary_helper 

class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(7), nullable=False) # P-00001
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    def to_json(self):
        url_imagen = self.image
        if self.image and not self.image.startswith('http'):
            url_imagen = cloudinary_helper.get_secure_url(self.image)

        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'image': url_imagen,
            'brand': self.brand,
            'size': self.size,
            'price': float(self.price),
            'stock': self.stock,
            'is_active': self.is_active,
            'category_id': self.category_id
        }