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

def addScaffold(html, data):
    tabDiv = html.new_tag("div", id="journal_tabs")
    tabList = tabDiv.new_tag("ul", class="nav nav-tabs" role="tablist")
    tabContent = tabDiv.new_tag("div" class="tab-content")

    for person, journal in data.iteritems():
        #Actual tabs
        li = tabList.new_tag("li", role="presentation")
        link = li.new_tag("a", href=person+"_content" aria-controls=person+"_content", role="tab", data-toggle="tab")
        li.append(link)
        tabList.append(li)

        #tab content
        tabPanel = tabContent.new_tag("div", role="tabpanel", class="tab-pane", id=person+"_content")
        tabContent.append(tabPanel)

    tabDiv.append(tabList)
    tabDiv.append(tabContent)
    html.append(tabDiv)


def dataToHTML(data, html):
    container = html.find(id="journal_container")
    addScaffold(container, data)

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
