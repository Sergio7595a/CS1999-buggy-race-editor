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
item = []

#print(table)
for row in table.findAll("tr"):
    for cell in row("td"):
        cell.get_text().strip()
        print(cell.get_text().strip())