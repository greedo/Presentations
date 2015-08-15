import re

file_handler = open("2015")

try:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(file_handler, "lxml")
except ImportError:
    from BeautifulSoup import BeautifulStoneSoup
    soup = BeautifulStoneSoup(file_handler)

dates = soup.findAll(name=re.compile("(d:NEW_DATE)", re.IGNORECASE | re.MULTILINE))
one_months = soup.findAll(name=re.compile("(d:BC_1MONTH)", re.IGNORECASE | re.MULTILINE))

for date, one_month in zip(dates, one_months):
    print date.text, one_month.text

