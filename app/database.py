from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# esto es por la base de datos local con la contraseña para poder ingresar por el momento 
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/api_tienda" 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()