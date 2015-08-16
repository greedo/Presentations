from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from models import Pars, Spots, Base
import passwords

engine = create_engine('postgresql+psycopg2://'+passwords.PyGotham.username+':'+passwords.PyGotham.password+'@'+passwords.PyGotham.hostname+':5432/'+passwords.PyGotham.db, echo=True)
#Base.metadata.tables['par'].create(bind=engine)
Base.metadata.tables['spot'].create(bind=engine)
