#! python3
# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.

import webbrowser, sys, pyperclip, requests, bs4
if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

res = requests.get('https://mangapark.me/search?q=' + address)
print('https://mangapark.me/search?q=' + address)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
search_Manga = bs4.BeautifulSoup(res.text, features="html.parser")
check_Exists = search_Manga.select('.no-match')
if len(check_Exists):
	print('Nothing was found')
	sys.exit()
else:
	print('Found ' + address + '!')

list_Manga = search_Manga.select('.item > table > tr > td > h2 > a')
for i in range(len(list_Manga)):
	print(str(i+1) + '. ' + list_Manga[i]['title'])

selection_Number = input('Please select the number you would like to download ')
if int(selection_Number) > 0 and int(selection_Number) < 9 and selection_Number.isdigit():
	print('Nice')
else:
	print('Not nice')
print('https://mangapark.me/' + list_Manga[int(selection_Number) - 1]['href'])
res = requests.get('https://mangapark.me' + list_Manga[int(selection_Number) - 1]['href'])