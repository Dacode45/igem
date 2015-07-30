from bs4 import BeautifulSoup
import json
from pprint import pprint



def initTemplate():
    with open("template.html", "r") as template:
        text = template.read()
        return BeautifulSoup(text)



def parseData(filenames):
    data = dict()
    for filename in filenames:
        with open(filename, "r") as data_file:
            data[filename[:-5]] = json.load(data_file)
    return data

def addScaffold()

def dataToHTML(data, html):
    container = html.find(id="journal_container")
    addScaffold(container)
    for person, journal in data.iteritems():
        personDiv = html.new_tag("div")
        personDiv.string = person
        container.append(personDiv)

def save(html, filename):
    with open(filename, "w") as journal:
        journal.write(html.prettify(formatter="html"))

def main():
    filenames = ["blake.json", "charlotte.json", "laura.json"]
    html = initTemplate()
    data = parseData(filenames)
    dataToHTML(data, html)
    save(html, "journal.html")



if __name__ == "__main__":
    main()
