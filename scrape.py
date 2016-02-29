import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as date
import click
from subprocess import call


def cleanData(inputstring):
    inputstring = inputstring.replace("']", "")
    inputstring = inputstring.replace("['", "")
    return inputstring


@click.command()
@click.option('--start', default=1, help='Starting ticket of scrape')
@click.option('--stop', default=30000, help='Ending ticket of the scrape')
def main(start, stop):
    call(['clear'])

    urlbase = 'https://code.djangoproject.com/ticket/'

    rundate = date.now()

    ticketnumber = 0

    filename = "data-{}-{}-{}.csv".format(rundate.strftime('%m-%d-%y-%H%M'),
                                          str(start), str(stop))
    f = open(filename, 'w', newline='')
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")

    for ticketnumber in range(start, stop):

        r = requests.get("{}{}".format(urlbase, ticketnumber))

        htmldoc = r.text

        soup = BeautifulSoup(htmldoc, 'html.parser')

        title = str(soup.find("title").contents)
        title = title.replace("Django", "")
        title = title.replace("']", "")
        title = title.replace("['", "")
        title = title.replace("\\n", "")
        title = title.strip()
        title = title[:-1]
        title = title.strip()

        try:
            ticketId = str(soup.find("a", {"class": "trac-id"}).contents)
        except AttributeError:
            ticketId = str(ticketnumber)

        try:
            user = str(soup.find("td", {"class": "searchable"}).a.contents)
        except AttributeError:
            user = 'unknown'

        try:
            ticketType = str(soup.find("span", {"class":
                                                "trac-type"}).a.contents)
        except AttributeError:
            ticketType = 'unknown'

        title = cleanData(title)
        ticketId = cleanData(ticketId)
        ticketId = ticketId.replace("#", "")
        user = cleanData(user)
        ticketType = cleanData(ticketType)

        record = (ticketId, user, ticketType, title)

        print("{} | {} | {} | {}".format(ticketId, user, ticketType, title))

        writer.writerow(record)
    else:
        f.close
        del f


if __name__ == '__main__':
    call('clear')
    main()
