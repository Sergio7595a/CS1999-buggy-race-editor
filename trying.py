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

def get_item(count,value):
    print(items.__getitem__(count + 5))
    if f'{items.__getitem__(count + 5)}':
        print("yes")
for item in range(10):
    print(items[count])
    integer = 6
    get_item(count,integer)
    count+= 5