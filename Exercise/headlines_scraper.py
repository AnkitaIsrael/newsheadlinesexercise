import requests
from datetime import datetime
from bs4 import BeautifulSoup
from click._compat import raw_input


# prints the headlines by selecting only the relevant texts of all the 'a' elements, makes lists and joins them
def print_headlines(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    for headlines in soup.find_all('div', class_='grid_24'):  # select the relevant 'div' tag where headlines are
        for a in headlines.findChildren('a', recursive=False):  # find 'a' elements in the 'div' tag
            if a.parent.name == 'div':  # only get the 'a' elements whose immediate parent 'div' tag
                parent_class = a.parent["class"][
                    0] if "class" in a.parent.attrs else ""  # get the class name of the parent
                if parent_class != "tleft":  # skip this class and get rest
                    print(''.join(text for text in a.find_all(text=True)))  # append all headlines


# Fetches headlines by looping over multiple pages till a specific tag is not found
# This missing tag indicates the last page
def fetching_headlines(year):
    page = 1  # start with first page
    url = "https://slashdot.org/archive.pl?op=bytime&keyword=&year={year}&page={page}"
    with requests.Session() as session:
        while True:
            response = session.get(url.format(year=year, page=page))  # substitute the year and page number
            soup = BeautifulSoup(response.content, "lxml")
            nav = soup.find('nav', {'class': 'abdb'})  # find the tag that would indicate the end of the pages
            if nav is None:
                break  # last page
            page += 1  # increment the page number
            print_headlines(response.text)

    print("-------------That's all from {}--------------".format(year))
    print("")


while True:
    current_year = datetime.now().year  # set up current year
    input_year = int(raw_input("Enter Year Here >>") or current_year)  # get user input i.e. year else use current year

    if 1998 <= input_year <= current_year:  # check the range
        print("Perfect! Fetching Slashdot Headlines from {}...".format(input_year))
        fetching_headlines(input_year)  # call the method to fetch headlines for the year specified by user

    else:
        print("Please specify a year between 1998 and {}".format(current_year))  # if user input is out of the range
