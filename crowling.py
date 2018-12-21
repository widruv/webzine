import requests
from bs4 import BeautifulSoup
from yattag import Doc
from optparse import OptionParser
import sys
import urllib

if(len(sys.argv) <= 1):
	print("crowling.py -h")
	exit()

use = "Usage: %prog [options] word"
parser = OptionParser(usage = use)
parser.add_option("-s", "--search", dest="search", default=False, action="store_true", help="search")
parser.add_option("-o", "--output", dest="output", default=False, action="store_true", help="output")

options, args = parser.parse_args()
file_name = ""
searching_word = "arashi"
if options.search:
	searching_word = urllib.quote(args[0], safe='')

if options.output:
	file_name = args[1]



r = requests.get('http://sitesearch.asahi.com/sitesearch/index.php?Keywords='+searching_word+'&sort=1&iref=pc_ss_score')
bs = BeautifulSoup(r.text, 'html.parser')
ul = bs.find('ul', {'id':'SiteSearchResult'})
data = []
for item in ul:
    a = item.find('a')
    if a == -1:
        continue

    link = a['href']
    image_span = a.find('span', {'class':'Image'})
    image = ""
    if image_span != None:
        image = "http:" + image_span.find('img')['src']

    headline = a.find('span', {'class': 'SearchResult_Headline'}).find('em')
    data.append({'head': headline.get_text(), 'image': image, 'link': link})


doc, tag, text = Doc().tagtext()

with tag('html', lang='ja'):
    with tag('head'):
        doc.asis('<meta charset="utf-8">')
        doc.asis('<meta http-equiv="Content-Type", content="text/html; charset=euc-jp">')
        doc.asis('<link rel="stylesheet" type="text/css" href="article.css">')
    with tag('body'):
        with tag('ul', id='item-list'):
            for item in data:
                with tag('li'):
                    with tag('article'):
                        with tag('a', href=item['link'].encode('utf-8')):
                            doc.stag('img', src=item['image'].encode('utf-8'), height='300', width='275')
                        with tag('p'):
                            with tag('a', href=item['link'].encode('utf-8')):
                                text(item['head'].encode('utf-8'))




result = doc.getvalue()
f = open(file_name, 'w')
f.write(result)
f.close()
