# Esse arquivo é tipo a ponte entre o Python e o banco de dados PostgreSQL.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

# URL de conexão com o PostgreSQL
DATABASE_URL = settings.database_url

# Cria a conexão com o banco
engine = create_engine(DATABASE_URL)

# Sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
