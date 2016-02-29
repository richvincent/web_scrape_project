import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as date
from subprocess import call

call(['clear'])

urlbase = 'https://code.djangoproject.com/ticket/'

rundate = date.now()

filename = "data-{}.csv".format(rundate.strftime('%m-%d-%y-%H%M'))

f = open(filename, 'w', newline='')
writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")

response = ''
ticketnumber = 0

if __name__ == '__main__':
    for ticketnumber in range(26295):

        r = requests.get("{}{}".format(urlbase, ticketnumber))

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
            ticketId = ticketnumber

        try:
            user = str(soup.find("td", {"class": "searchable"}).a.contents)
        except AttributeError:
            user = 'unknown'

        try:
            ticketType = str(soup.find("span", {"class":
                                                "trac-type"}).a.contents)
        except AttributeError:
            ticketType = 'unknown'

        record = (ticketId, user, ticketType)

        print("{} | {} | {}".format(ticketId, user, ticketType))
        print(response)

        writer.writerow(record)

f.close
del f
