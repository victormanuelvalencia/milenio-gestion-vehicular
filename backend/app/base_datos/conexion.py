from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.configuracion.config import configuraciones

motor = create_engine(configuraciones.url_base_datos)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)