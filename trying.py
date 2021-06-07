from bs4 import BeautifulSoup
from urllib.request import urlopen

link = "https://rhul.buggyrace.net/specs/"

page = urlopen(link)

html_page = page.read().decode("utf-8")
#print(html_page)
soup = BeautifulSoup(html_page,"html.parser")
#mess = soup.get_text()
#print(mess)

cost = {}






def  assign_table(table,classer):
    item = []
    for row in soup.find(table,classer).findAll("tr"):
        for cell in row("td"):
            item.append(cell.get_text().strip())
    return item

main_table = assign_table("table", {"class":"table table-striped table-bordered table-hover table-responsive"})
power_table = assign_table("table", {"class":"table table-striped table-bordered table-hover"})
tyre_table = assign_table("table",{"class":"table table-striped table-bordered table-hover"})

count = 0
costs = []

table = 0


def get_costs(count):
    print(main_table.__getitem__(count))
    if main_table.__getitem__(count) == "Primary motive power":
        for item in range(0,60,6):
            list_costs(item,"power_table")
    if main_table.__getitem__(count + 2).isdigit():
        costs.append([main_table.__getitem__(count + 3),main_table.__getitem__(count + 2)])
    if main_table.__getitem__(count) == "Number of wheels":
        for item in range(0,60,6):
            list_costs(item,"tyre_table")
    #if main_table.__getitem__(count) == "":
    #if items.__getitem__(count + 2) == "—" or items.__getitem__(count + 2) == "—":
        #if table <= 0:
            #print(items[count])
            #print("rawr")


def list_costs(count,item):
    f"print({item}.__getitem__(count))"
    costs.append([item.__getitem__(count+2),[item.__getitem__(count+3),item.__getitem__(count+4),item.__getitem__(count+5)]])



for item in range(0,112,6):
    get_costs(item)
print(costs)
