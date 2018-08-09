from lxml import html
import requests

#Thanks to Alex for this script :)
# Fill this in with the cookie from the Shibboleth authenticiation
cookies = dict(_shibsession_xxxxxxxxx = '_xxxxxxx')

page = requests.get('https://gophergold.umn.edu/balance.php', cookies=cookies)
tree = html.fromstring(page.content)
data = tree.xpath('//td[@style="text-align:right"]/text()')

print("You currently have " + data[0] + " meal(s) left. ")
print("You currently have $" + data[1] + " in FlexDine. ")
print("You currently have $" + data[2] + " in GopherGold. ")

if len(data) > 3: # If you don't have a meal plan, this data will be missing
    print("You currently have " + data[3] + " guest meals. ")
