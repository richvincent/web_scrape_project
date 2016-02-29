import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as date
from subprocess import call

call(['clear'])

urlbase = 'https://code.djangoproject.com/ticket/'

rundate = date.now()

filename = "scrape-{}.csv".format(rundate.strftime('%m-%d-%y-%H%M'))

f = open(filename, 'w', newline='')
writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")

response = ''
firstticket = 0
while response != '<Response [404]>':

    firstticket += 1

    r = requests.get("{}{}".format(urlbase, firstticket))

    response = str(r)

    htmldoc = r.text

    soup = BeautifulSoup(htmldoc, 'html.parser')

    title = str(soup.find("title").contents)
    title = title.replace("Django", "")
    title = title.replace("']", "")
    title = title.replace("['", "")
    title = title.replace("\\n", "")

    try:
        ticketId = str(soup.find("a", {"class": "trac-id"}).contents)
    except AttributeError:
        ticketId = 'unknown'

    try:
        user = str(soup.find("td", {"class": "searchable"}).a.contents)
    except AttributeError:
        user = 'unknown'

    try:
        ticketType = str(soup.find("span", {"class": "trac-type"}).a.contents)
    except AttributeError:
        ticketType = 'unknown'

    record = (ticketId, user, ticketType)

    print(record)

    writer.writerow(record)

f.close
del f
