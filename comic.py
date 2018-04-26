import sys
import requests
import bs4
import os
import pyperclip
#import time


print('enter the Folder name:')
line = sys.stdin.readline()
line = line.strip(' \t\n\r')

print('paste the first page URL:')
url = pyperclip.paste().strip(' \t\n\r')

#url = 'http://comic.ck101.com/vols/28137105/1' for example
os.makedirs(line, mode=0o777)
count = 0

while not url.endswith('#'):
	#download page(HTML)
	print('Downloading the page %s...' % url)
	res = requests.get(url)
	res.raise_for_status()

	#content in text
	soup = bs4.BeautifulSoup(res.text)
	
	#translation HTML tag
	imgeElem = soup.select('#defualtPagePic')
	#print(soup.select('#mangaFile'))
	
	if imgeElem ==[]:
		print('Could not find imge')
	else:
		try:
			#get picture link and download
			imgeUrl = imgeElem[0].get('src')
			print('Downloading imge %s...' % (imgeUrl))
			res = requests.get(imgeUrl)
			res.raise_for_status()
		except requests.exceptions.MissingSchema:
			#if error deal with next page
			prevLink = soup.select('.nextPageButton')[0]
			url = 'http://comic.ck101.com'+prevLink.get('href')
			continue
		
		#save picture 
		imgeFile = open(os.path.join(line, os.path.basename(str(count))),'wb')
		for chunk in res.iter_content(1000000):
			imgeFile.write(chunk)
		imgeFile.close()

	#deal with next page
	prevLink = soup.select('.nextPageButton')[0]
	url = 'http://comic.ck101.com'+prevLink.get('href')
	
	
	#count number of picture
	count = count+1
	#if count==2:
	#	break

print('Done.')








