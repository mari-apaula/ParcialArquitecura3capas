# data/repositories.py
from .db_config import Session, Base, engine
from sqlalchemy import Column, Integer, String, Float

# --- Entidades ---
class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    lote = Column(String)
    variedad = Column(String)       # NUEVO: Tipo de producto
    finca = Column(String)          # NUEVO: Origen exacto
    fecha_cosecha = Column(String)
    fecha_empaquetado = Column(String)
    calidad_ok = Column(String)
    temperatura_transporte = Column(Float)
    fecha_entrega = Column(String)

class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)

# --- Repositorios ---
class TraceabilityRepository:
    def save(self, product_data):
        session = Session()
        new_product = ProductEntity(**product_data)
        session.add(new_product)
        session.commit()
        session.close()

    def get_all(self):
        session = Session()
        products = session.query(ProductEntity).all()
        session.close()
        return products

    # NUEVOS MÉTODOS CRUD
    def get_by_id(self, id):
        session = Session()
        product = session.query(ProductEntity).filter_by(id=id).first()
        session.close()
        return product

    def update(self, id, data):
        session = Session()
        product = session.query(ProductEntity).filter_by(id=id).first()
        if product:
            for key, value in data.items():
                setattr(product, key, value)
            session.commit()
        session.close()

    def delete(self, id):
        session = Session()
        product = session.query(ProductEntity).filter_by(id=id).first()
        if product:
            session.delete(product)
            session.commit()
        session.close()

class UserRepository:
    def get_by_username(self, username):
        session = Session()
        user = session.query(UserEntity).filter_by(username=username).first()
        session.close()
        return user

    def create_admin_if_not_exists(self):
        session = Session()
        if not session.query(UserEntity).filter_by(username='admin').first():
            admin = UserEntity(username='admin', password='123')
            session.add(admin)
            session.commit()
        session.close()