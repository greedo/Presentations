from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from marshmallow import Serializer, fields
import psycopg2
import re
import passwords
from models import Pars
import datetime

def soup_maker(fh):
    """ Takes a file handler returns BeautifulSoup"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(fh, "lxml")
        for tag in soup.find_all():
            tag.name = tag.name.lower()
    except ImportError:
        from BeautifulSoup import BeautifulStoneSoup
        soup = BeautifulStoneSoup(fh)
    return soup

class MyParser(object):

    def __init__(self):        
        return

    @classmethod
    def parse(self, file_handle):

        # if no file handle was given create our own
        if not hasattr(file_handle, 'read'):
            file_handler = open(file_handle)
        else:
            file_handler = file_handle

        soup = soup_maker(file_handler)
        file_handler.close()

        return soup

    @classmethod
    def parseData(self, soup):

        par_obj = Par()

        par_obj.date = soup.find_all(name=re.compile("(d:NEW_DATE)", re.IGNORECASE | re.MULTILINE))
        par_obj.month1 = soup.find_all(name=re.compile("(d:BC_1MONTH)", re.IGNORECASE | re.MULTILINE))
        par_obj.month3 = soup.find_all(name=re.compile("(d:BC_3MONTH)", re.IGNORECASE | re.MULTILINE))
        par_obj.month6 = soup.find_all(name=re.compile("(d:BC_6MONTH)", re.IGNORECASE | re.MULTILINE))
        par_obj.year1 = soup.find_all(name=re.compile("(d:BC_1YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year3 = soup.find_all(name=re.compile("(d:BC_3YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year5 = soup.find_all(name=re.compile("(d:BC_5YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year7 = soup.find_all(name=re.compile("(d:BC_7YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year10 = soup.find_all(name=re.compile("(d:BC_10YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year20 = soup.find_all(name=re.compile("(d:BC_20YEAR)", re.IGNORECASE | re.MULTILINE))
        par_obj.year30 = soup.find_all(name=re.compile("(d:BC_30YEAR)", re.IGNORECASE | re.MULTILINE))

        # connect to the db
        engine = create_engine('postgresql+psycopg2://'+passwords.PyGotham.username+':'+passwords.PyGotham.password+'@'+passwords.PyGotham.hostname+':5432/'+passwords.PyGotham.db, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        for date, month1, month3, month6, year1, year3, year5, year7, year10, year20, year30 in zip(par_obj.date, par_obj.month1, par_obj.month3, par_obj.month6, par_obj.year1, par_obj.year3, par_obj.year5, par_obj.year7, par_obj.year10, par_obj.year20, par_obj.year30):
            new_par = Pars(par_id = None,
                           date = datetime.datetime.strptime(date.text.split('T')[0], "%Y-%m-%d"),
                           par_month1 = month1.text,
                           par_month3 = month3.text,
                           par_month6 = month6.text,
                           par_year1 = year1.text,
                           par_year3 = year3.text,
                           par_year5 = year5.text,
                           par_year7 = year7.text,
                           par_year10 = year10.text,
                           par_year20 = year20.text,
                           par_year30 = year30.text)
            session.add(new_par)
            session.commit()
        session.close()

        return par_obj

# Parsed data object
class Par(object):
    def __init__(self,
                 par_month1=0.0,
                 par_month3=0.0,
                 par_month6=0.0,
                 par_year1=0.0,
                 par_year3=0.0,
                 par_year5=0.0,
                 par_year7=0.0,
                 par_year10=0.0,
                 par_year20=0.0,
                 par_year30=0.0):
        self.par_month1 = par_month1
        self.par_month3 = par_month3
        self.par_month6 = par_month6
        self.par_year1 = par_year1
        self.par_year3 = par_year3
        self.par_year5 = par_year5
        self.par_year7 = par_year7
        self.par_year10 = par_year10
        self.par_year20 = par_year20
        self.par_year30 = par_year30

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield value

class ParSerializer(Serializer):
    par_month1 = fields.String()
    par_month3 = fields.String()
    par_month6 = fields.String()
    par_year1 = fields.String()
    par_year3 = fields.String()
    par_year5 = fields.String()
    par_year7 = fields.String()
    par_year10 = fields.String()
    par_year20 = fields.String()
    par_year30 = fields.String()
