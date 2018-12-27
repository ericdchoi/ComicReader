#! python3
# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.

import webbrowser, sys, pyperclip, requests, bs4, os, threading

maxthreads = 5
sema = threading.Semaphore(value=maxthreads)

def download(link, filelocation):
	sema.acquire()
	res = requests.get(link)
	res.raise_for_status()
	imageFile = open(os.path.join(filelocation, os.path.basename(link)), 'wb')
	for chunk in res.iter_content(100000):
		imageFile.write(chunk)
	sema.release()
	imageFile.close()
def downloadThread(link, filelocation):
	download_thread = threading.Thread(target=download, args = (link, filelocation))
	download_thread.start()

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
print('https://mangapark.me' + list_Manga[int(selection_Number) - 1]['href'])
res = requests.get('https://mangapark.me' + list_Manga[int(selection_Number) - 1]['href'])
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
search_Manga = bs4.BeautifulSoup(res.text, features="html.parser")
list_Chapters = search_Manga.select('.chapter > li > div > a.ml-1')

for i in range(len(list_Chapters)):
	print(str(i+1) + '. ' + list_Chapters[i].text)

chapter_Begin = input('Please select starting chapter ')
chapter_End = input('Please select ending chapter ')

chapters = list()
for i in range(int(chapter_Begin) - 1, int(chapter_End)):
	chapters.append('https://mangapark.me' + list_Chapters[i]['href'][:-2])
	print(str(i+1) + '. ' + list_Chapters[i].text)
print(chapters)
chapter_Title = input('Please input directory name ')
os.makedirs(chapter_Title, exist_ok=True)
chapter_Images = list()
for i in range(len(chapters)):
	res = requests.get(chapters[i])
	try:
	    res.raise_for_status()
	except Exception as exc:
	    print('There was a problem: %s' % (exc))
	search_Page = bs4.BeautifulSoup(res.text, features="html.parser")
	for j in range(len(search_Page.select('.img-num'))):
		print(search_Page.select('#canvas-' + str(j+1) + ' .img-num')[0]['href'])
		temp = search_Page.select('#canvas-' + str(j+1) + ' .img-num')[0]['href']
		if 'https:' in temp:
			chapter_Images.append(search_Page.select('#canvas-' + str(j+1) + ' .img-num')[0]['href'])
		else:
			chapter_Images.append('https:' + search_Page.select('#canvas-' + str(j+1) + ' .img-num')[0]['href'])
print(chapter_Images)

for i in range(len(chapter_Images)):
	comicUrl = chapter_Images[i]
	print('Downloading image %s...' % (comicUrl))
	downloadThread(comicUrl, chapter_Title)
print('Done.')