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






def  assign_table():
    item = []
    for table in soup.findAll("table"):
        #print(table)
        for row in table("tr"):
            print(row)
            for cell in row("td"):
                item.append(cell.get_text().strip())
    return item

main_table = assign_table()
#print(main_table)
count = 0
costs = {}

table = 0


def get_costs(count):
    return main_table.__getitem__(count)
    #if main_table.__getitem__(count) == "Primary motive power":
        #for item in range(0,60,6):
            #list_costs(item,"power_table")
    #if main_table.__getitem__(count + 2).isdigit():
        #costs.append([main_table.__getitem__(count + 3),main_table.__getitem__(count + 2)])
    #if main_table.__getitem__(count) == "Number of wheels":
        #for item in range(0,60,6):
            #list_costs(item,"tyre_table")
    #if main_table.__getitem__(count) == "":
    #if items.__getitem__(count + 2) == "—" or items.__getitem__(count + 2) == "—":
        #if table <= 0:
            #print(items[count])
            #print("rawr")


def list_costs(count,item):
    #f"print({item}.__getitem__(count))"
    costs[main_table.__getitem__(count)] = main_table.__getitem__(item) #,[item.__getitem__(count+3),item.__getitem__(count+4),item.__getitem__(count+5)]])



for item in range(0,112,6):
    type = get_costs(item+3)
    cost = get_costs(item+2)
    if cost == "varies, per unit":
        costs[type] = []
    elif cost == "varies":
        costs[type] = []
    elif cost == "—":
        print("not wanted")
    else:
        costs[type] = cost

print("")
for item in range(118,178,6):
    if item == 118:
        None
    else:
        power_type = get_costs(item-2)
        power_cost = [get_costs(item-1),get_costs(item),get_costs(item-5)]
        print(power_cost,power_type)
        costs["power_type"] += [power_type,power_cost]


print("")
for item in range(174,238,4):
    offensives = get_costs(item)
print("")
for item in range(238,250,2):
    get_costs(item)

print(costs)
