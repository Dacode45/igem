from bs4 import BeautifulSoup
import json
from pprint import pprint
import dateutil.parser

soup = BeautifulSoup("", "html.parser")

info = {
    "blake":{
        "img":"http://2015.igem.org/wiki/images/5/5c/Blake_actkinson.png",
        "school":"Washington University in St. Louis",
        "major":"Biomedical Engineering",
        "full_name":"Blake Actkinson "
    },
    "david":{
        "img":"http://2015.igem.org/wiki/images/c/c6/David_ayeke.jpg",
        "school":"Washington University in St. Louis",
        "major":"Computer Engineering",
        "full_name":"David Ayeke "
    },
    "charlotte":{
        "img":"http://2015.igem.org/wiki/images/1/1d/Charlotte.JPG",
        "school":"Washington University in St. Louis",
        "major":"Biochemistry and Spanish",
        "full_name":"Charlotte Bourg "
    },
    "mike":{
        "img":"http://2015.igem.org/wiki/images/6/6b/Mike_toomey.png",
        "school":"Washington University in St. Louis",
        "major":"Biomedical Engineering",
        "full_name":"Mike Toomey "
    },
    "laura":{
        "img":"http://2015.igem.org/wiki/images/3/32/Laura.jpg",
        "school":"Pennsylvania State University",
        "major":"Biochemistry and Molecular Biology",
        "full_name":"Laura Beebe "
    },
    "jessica":{
        "img":"http://placehold.it/200x200",
        "school":"Pennsylvania State University",
        "major":"Chemical Engineering",
        "full_name":"Jessica O'Callaghan "
    },
}

def initTemplate():
    with open("template.html", "r") as template:
        text = template.read()
        return BeautifulSoup(text, "html.parser")



def parseData(filenames):
    data = dict()
    for filename in filenames:
        with open(filename, "r") as data_file:
            data[filename[:-5]] = json.load(data_file)
    return data

def addTabularScaffold(data, html):
    tabDiv = soup.new_tag("section", id="journal_tabs")
    tabDiv['class'] = "row bg-white sectionNum1 sectionNum2 sectionNum3 sectionNum4"
    tabList = soup.new_tag("ul",id="journal-sidebar", role="tablist")
    tabList['class'] = "nav nav-tabs"
    tabContent = soup.new_tag("div")
    tabContent['class'] = "tab-content"

    first = True
    for person, journal in data.iteritems():
        #Actual tabs
        li = soup.new_tag("li", role="presentation")
        if first == True:
            li['class'] =  "active"
        link = soup.new_tag("a", href="#"+person+"_content",  role="tab")
        link['data-toggle'] = "tab"
        link['aria-controls'] = person+"_content"
        link.append(person)
        li.append(link)
        tabList.append(li)

        #tab content
        tabPanel = soup.new_tag("div", role="tabpanel", id=person+"_content")
        tabPanel['class'] = "tab-pane"
        if first == True:
            tabPanel['class'] = tabPanel['class'] + " active"
        tabContent.append(tabPanel)
        first = False

    tabDiv.append(tabList)
    tabDiv.append(tabContent)
    html.append(tabDiv)
    return tabContent

def addJournalContent(person, journal, contentDiv):
    header, main, aside = addJournalScaffold(person, contentDiv)

    #add picture and description to header
    profilePicWrapper = soup.new_tag("div", id=person+"_profile_pic_wrapper")
    profilePicWrapper['class'] = "col-md-3"
    profilePic = soup.new_tag("img", src=info[person]["img"])
    profilePic['class'] = "img-responsive img-thumbnail"
    profilePicWrapper.append(profilePic)
    header.append(profilePicWrapper)

    infoWrapper = soup.new_tag("div", id=person+"infoWrapper")
    infoWrapper['class'] = "col-md-9"
    school = soup.new_tag("p")
    school['class'] = "text-muted"
    infoWrapper.append(info[person]['full_name'])
    infoWrapper.append(info[person]['school'])
    header.append(infoWrapper)

    nav = soup.new_tag("div")
    nav['class'] = "list-group journal_nav"
    nav['data-spy'] = "affix"
    nav['data-offset-top'] = "1500"
    aside.append(nav)

    #process journals.
    for day in journal:
        journalSection = soup.new_tag('div')
        journalSection['class'] = "journal-section list-group"
        date = dateutil.parser.parse(day['when'])
        dateID = date.strftime('%b_%d')
        h1 = soup.new_tag('h1', id="person_"+dateID)
        anchorStyle = "font-family: anchorjs-icons; font-style: normal; font-variant: normal; font-weight: normal; position: absolute; margin-left: -1em; padding-right: 0.5em;"
        anchor = soup.new_tag('a', href="#person_"+dateID,  style=anchorStyle)
        anchor['aria-label'] = "Anchor link for: "+dateID
        anchor['data-anchorjs-icon'] = "[]"
        anchor['class'] = "anchorjs-link"
        journalSection.append(anchor)
        h1.append(date.strftime('- Experiments From %b %d'))
        h1['class'] = "page-header"
        journalSection.append(h1)

        #Add this Day to the sidebar.
        dayList = soup.new_tag('div')
        dayList['class'] = "list-group-item"
        anchor = soup.new_tag('a', href="#person_"+dateID)
        anchor.append(dateID)
        dayList.append(anchor)
        dayList.append(soup.new_tag('hr'))

        dayListList = soup.new_tag('ul')
        dayListList['class'] = "nav"

        #Create list of exp


        for exp in day['what']:
            #Create Lead for Experiment
            #print person, day['when']
            journalEntry = soup.new_tag('div', id=exp['id'])
            journalEntry['class'] = 'list-group-item journal-entry'

            h2 = soup.new_tag('h2')
            anchor = soup.new_tag('a', href=exp['id'], style=anchorStyle)
            anchor['aria-label'] = "Anchor link for: "+person+exp['id'][-3:]
            anchor['data-anchorjs-icon'] = "[]"
            anchor['class'] = "anchorjs-link"
            h2.append(anchor)
            h2.append(exp['lead'])
            journalEntry.append(h2)
            expID = soup.new_tag('p')
            expID['class'] = "text-muted"
            expID.append(exp['id'])
            journalEntry.append(expID)

            #Add link to Experiment to sidebar
            dayListListItem = soup.new_tag('li')
            anchor = soup.new_tag('a', href="#"+exp['id'])
            anchor.append(exp['id'])
            dayListListItem.append(anchor)
            dayListList.append(dayListListItem)

            why = soup.new_tag('p')
            why['class'] = "text-primary"
            why.append(exp.get("why", ""))
            journalEntry.append(why)

            #add actual content to experiment
            description = soup.new_tag('p')
            description.append(exp.get("description", ""))
            journalEntry.append(description)




        dayList.append(dayListList)
        nav.append(dayList)
        journalSection.append(journalEntry)
        main.append(journalSection)

def addJournalScaffold(person, contentDiv):
    header = soup.new_tag("div", id=person+"_content_header")
    header['class']= "row"

    mainRow = soup.new_tag("div")
    mainRow['class'] = "row"

    main = soup.new_tag("div", id=person+"_journal_main", role="main")
    main['class'] = "col-md-9"

    aside = soup.new_tag("aside", id=person+"_journal_aside", role="complementary")
    aside['class'] = "col-md-3 scrollspy journal_asside"

    mainRow.append(main)
    mainRow.append(aside)

    contentDiv.append(header)
    contentDiv.append(mainRow)

    return (header, main, aside)



def dataToHTML(data, html):
    container = html.find(id="journal_container")
    tabContent = addTabularScaffold(data, container)

    for person, journal in data.iteritems():
        contentDiv = tabContent.find(id=person+"_content")
        addJournalContent(person, journal, contentDiv)

def save(html, filename):
    with open(filename, "w") as journal:
        journal.write(html.prettify(formatter="html").encode('utf-8'))

def main():
    filenames = ["blake.json", "charlotte.json", "laura.json"]
    html = initTemplate()
    data = parseData(filenames)
    dataToHTML(data, html)
    save(html, "../new_version/journal.html")



if __name__ == "__main__":
    main()
