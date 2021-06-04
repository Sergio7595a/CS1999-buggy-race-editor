from bs4 import BeautifulSoup
from urllib.request import urlopen

link = "https://rhul.buggyrace.net/specs/"

page = urlopen(link)

html_page = page.read().decode("utf-8")
#print(html_page)
soup = BeautifulSoup(html_page,"html.parser")
#mess = soup.get_text()
#print(mess)

def  assign_table(table):
    item = []
    for row in soup.find(table).findAll("tr"):
        for cell in row("td"):
            item.append(cell.get_text().strip())
    return item
items = assign_table("table", {"class":"table table-striped table-bordered table-hover table-responsive"})
items2 = assign_table("table",{"class":"table table-striped table-bordered table-hover"})

count = 0
costs = []
table = 0


def get_costs(count):
    if items.__getitem__(count + 2) == "—":
        if table <= 0:
            print("rawr")


def list_costs():
    print("rawr")


for item in range(19):
    get_costs(count)
    count += 6
print(count)