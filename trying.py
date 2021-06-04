from bs4 import BeautifulSoup
from urllib.request import urlopen

link = "https://rhul.buggyrace.net/specs/"

page = urlopen(link)

html_page = page.read().decode("utf-8")
#print(html_page)
soup = BeautifulSoup(html_page,"html.parser")
#mess = soup.get_text()
#print(mess)

table = soup.find( "table", {"class":"table table-striped table-bordered table-hover table-responsive"} )
items = []

#print(table)
for row in table.findAll("tr"):
    for cell in row("td"):
        items.append(cell.get_text().strip())
print(items)
count = 0
costs = {}
def get_costs(count):
    print(items.__getitem__(count + 5))
def list_costs():
    print("rawr")
for item in range(10):
    get_item(count)
    count+= 5