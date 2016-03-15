import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as date


class baseURL(object):
    """ Base URLs for Django project """
    text = 'https://code.djangoproject.com/'
    indexurl = 'https://code.djangoproject.com/query?status=assigned&status=closed&status=new&max=10000&desc=1&order=id'


def cleanData(inputstring):
    inputstring = inputstring.replace("']", "")
    inputstring = inputstring.replace("['", "")
    inputstring = inputstring.replace("#", "")
    inputstring = inputstring.replace(")", "")
    inputstring = inputstring.replace("(", "")
    inputstring = inputstring.replace("'", "")
    inputstring = inputstring.replace("\\n", "")
    return inputstring


def findNumberOfTickets():
    base = baseURL()
    indexurl = base.indexurl
    r = requests.get(indexurl)
    htmldoc = r.text
    soup = BeautifulSoup(htmldoc, "html.parser")
    element = soup.find("span", class_="numresults")
    string = cleanData(str(element.contents))
    results = [int(s) for s in string.split() if s.isdigit()]
    results.sort
    numTickets = results[-1]
    return numTickets


def getListOfTickets(url):
    r = requests.get(url)
    htmldoc = r.text
    soup = BeautifulSoup(htmldoc, "html.parser")
    element = soup.find_all("td", class_="id")
    ticketList = []
    for item in element:
        ticketList.append(cleanData(str(item.a.contents)))
    return ticketList


def gatherIndexPages():
    base = baseURL()
    indexurl = base.indexurl
    r = requests.get(indexurl)
    htmldoc = r.text
    soup = BeautifulSoup(htmldoc, "html.parser")
    paging = soup.find("div", class_="paging")
    paginglinks = paging.find_all("a")
    pages = []
    for each in paginglinks:
        pages.append(base.text+each.get("href"))
    pages = pages[:-1]
    pages = [indexurl] + pages
    return pages


def main():

    base = baseURL()

    urlbase = base.text + 'ticket/'

    rundate = date.now()

    urllist = gatherIndexPages()

    filename = "data-{}.csv".format(rundate.strftime('%m-%d-%y-%H%M'))
    f = open(filename, 'a', newline='')
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")
    writer.writerow(['title', 'ticketId', 'user', 'ticketType'])
    for url in urllist:

        tickets = getListOfTickets(url)
        ticketcount = 0

        for ticketnumber in tickets:

            r = requests.get("{}{}".format(urlbase, ticketnumber))

            htmldoc = r.text

            soup = BeautifulSoup(htmldoc, 'html.parser')

            title = str(soup.find("title").contents)
            title = title.replace("Django", "")
            title = cleanData(title)
            title = title.strip()
            title = title[:-1]
            title = title.strip()

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
            user = cleanData(user)
            ticketType = cleanData(ticketType)
            ticketcount += 1

            record = (ticketId, user, ticketType, title, ticketcount)

            print("{} | {} | {} | {} | {}".format(ticketcount,
                                                  ticketId,
                                                  user, ticketType, title))

            writer.writerow(record)
    else:
        f.close
        del f


if __name__ == '__main__':
    main()
