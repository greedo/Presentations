from celery import chain
from tasks import file_downloader, parse_doc

# Build URLs
treasury_root = 'http://data.treasury.gov'

years = [2013, 2014, 2015]
urls = []
for year in years:

    urls.append(treasury_root+'/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE) eq '+str(year))

# download docs
downloads = chain(file_downloader.si(urls))()
while downloads.get() == True:
    print "done with downloads"

    # parse them
    files = []
    for url in urls:
        files.append(parse_doc.si(url.split(' ')[2]))
    parsing = chain(files)()
    print "all done"
    break
