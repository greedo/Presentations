from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from models import Base
import passwords

engine = create_engine('postgresql+psycopg2://'+passwords.PyGotham.username+':'+passwords.PyGotham.password+'@'+passwords.PyGotham.hostname+':5432/'+passwords.PyGotham.db, echo=True)
Base.metadata.drop_all(engine)
