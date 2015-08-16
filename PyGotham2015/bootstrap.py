from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Serializer, fields
import psycopg2
import re
import passwords
from models import Pars, Spots
import datetime
import time
import math

class Bootstrap(object):

    def __init__(self):
        return

    @classmethod
    def bootstrap(self):

        # connect to the db
        engine = create_engine('postgresql+psycopg2://'+passwords.PyGotham.username+':'+passwords.PyGotham.password+'@'+passwords.PyGotham.hostname+':5432/'+passwords.PyGotham.db, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        for p in session.query(Pars).all(): 

            # same as par since they are discount
            spot_month1 = p.par_month1
            spot_month3 = p.par_month3
            spot_month6 = p.par_month6

            # begin bootstrapping
            spot_year1 = ((math.sqrt((1000 + (p.par_year1*100)/2) / (1000 - ((p.par_year1*100)/2 / (1 + p.par_month6/2)))) - 1)*2)*10
            spot_year3 = ((math.sqrt((1000 + p.par_year3*100) / (1000 - (p.par_year3*100 / (1 + (p.par_month6/2)))  - (p.par_year3*100 / ((1 + (p.par_year1/2))**2)))) - 1)*2)*10
            spot_year5 = ((math.sqrt((1000 + p.par_year5*100) / (1000 - (p.par_year5*100 / (1 + (p.par_month6/2))) - (p.par_year5*100 / ((1 + (p.par_year1/2))**2)) - (p.par_year5*100 / ((1 + (p.par_year3/2))**2)))) - 1)*2)*10
            spot_year7 = ((math.sqrt((1000 + p.par_year7*100) / (1000 - (p.par_year7*100 / 1 + (p.par_month6/2)) - (p.par_year7*100 / ((1 + (p.par_year1/2))**2)) - (p.par_year7*100 / ((1 + (p.par_year3/2))**2)) - (p.par_year7*100 / ((1 + (p.par_year5/2))**2)))) -1)*2)*10
            spot_year10 = ((math.sqrt((1000 + p.par_year10*100) / (1000 - (p.par_year10*100 / 1 + (p.par_month6/2)) - (p.par_year10*100 / ((1 + (p.par_year1/2))**2)) - (p.par_year10*100 / ((1 + (p.par_year3/2))**2)) - (p.par_year10*100 / ((1 + (p.par_year5/2))**2)) - (p.par_year10*100 / ((1 + (p.par_year7/2))**2)))) -1)*2)*10
            spot_year20 = ((math.sqrt((1000 + p.par_year20*100) / (1000 - (p.par_year20*100 / 1 + (p.par_month6/2)) - (p.par_year20*100 / ((1 + (p.par_year1/2))**2)) - (p.par_year20*100 / ((1 + (p.par_year3/2))**2)) - (p.par_year20*100 / ((1 + (p.par_year5/2))**2)) - (p.par_year20*100 / ((1 + (p.par_year7/2))**2)) - (p.par_year20*100 / ((1 + (p.par_year10/2))**2)))) -1)*2)*10
            spot_year30 = ((math.sqrt((1000 + p.par_year30*100) / (1000 - (p.par_year30*100 / 1 + (p.par_month6/2)) - (p.par_year30*100 / ((1 + (p.par_year1/2))**2)) - (p.par_year30*100 / ((1 + (p.par_year3/2))**2)) - (p.par_year30*100 / ((1 + (p.par_year5/2))**2)) - (p.par_year30*100 / ((1 + (p.par_year7/2))**2)) - (p.par_year30*100 / ((1 + (p.par_year10/2))**2)) - (p.par_year30*100 / ((1 + (p.par_year20/2))**2)))) -1)*2)*1

            new_spot = Spots(spot_id = None,
                             date = p.date,
                             spot_month1 = spot_month1,
                             spot_month3 = spot_month3,
                             spot_month6 = spot_month6,
                             spot_year1 = spot_year1,
                             spot_year3 = spot_year3,
                             spot_year5 = spot_year5,
                             spot_year7 = spot_year7,
                             spot_year10 = spot_year10,
                             spot_year20 = spot_year20,
                             spot_year30 = spot_year30)
            session.add(new_spot)
            session.commit()
        session.close()

        return None

# Parsed data object
class Bond(object):
    def __init__(self,
                 spot_month1=0.0,
                 spot_month3=0.0,
                 spot_month6=0.0,
                 spot_year1=0.0,
                 spot_year3=0.0,
                 spot_year5=0.0,
                 spot_year7=0.0,
                 spot_year10=0.0,
                 spot_year20=0.0,
                 spot_year30=0.0):
        self.spot_month1 = spot_month1
        self.spot_month3 = spot_month3
        self.spot_month6 = spot_month6
        self.spot_year1 = spot_year1
        self.spot_year3 = spot_year3
        self.spot_year5 = spot_year5
        self.spot_year7 = spot_year7
        self.spot_year10 = spot_year10
        self.spot_year20 = spot_year20
        self.spot_year30 = spot_year30

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield value

class BondSerializer(Serializer):
    spot_month1 = fields.String()
    spot_month3 = fields.String()
    spot_month6 = fields.String()
    spot_year1 = fields.String()
    spot_year3 = fields.String()
    spot_year5 = fields.String()
    spot_year7 = fields.String()
    spot_year10 = fields.String()
    spot_year20 = fields.String()
    spot_year30 = fields.String()
