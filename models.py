from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, DateTime, Sequence
from sqlalchemy import func
import datetime

Base = declarative_base()

class Pars(Base):

    __tablename__ = 'par'

    par_id = Column(Integer, Sequence('par_id', start=1, increment=1), primary_key=True)
    date = Column(DateTime)
    par_month1 = Column(Float)
    par_month3 = Column(Float)
    par_month6 = Column(Float)
    par_year1 = Column(Float)
    par_year3 = Column(Float)
    par_year5 = Column(Float)
    par_year7 = Column(Float)
    par_year10 = Column(Float)
    par_year20 = Column(Float)
    par_year30 = Column(Float)

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        return "<Par('%s')>" % (self.par_id)


class Spots(Base):

    __tablename__ = 'spot'

    spot_id = Column(Integer, Sequence('spot_id', start=1, increment=1), primary_key=True)
    date = Column(DateTime)
    spot_month1 = Column(Float)
    spot_month3 = Column(Float)
    spot_month6 = Column(Float)
    spot_year1 = Column(Float)
    spot_year3 = Column(Float)
    spot_year5 = Column(Float)
    spot_year7 = Column(Float)
    spot_year10 = Column(Float)
    spot_year20 = Column(Float)
    spot_year30 = Column(Float)

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        return "<Spot('%s')>" % (self.spot_id)
