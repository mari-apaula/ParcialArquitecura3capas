from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de SQLite
engine = create_engine('sqlite:///trazabilidad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)