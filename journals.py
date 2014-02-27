##########################################################
###               Web scraper 1.0 by Roloyar           ###
##########################################################
###         This scraper is designed for getting       ###
###        data from the Sage Journals library         ###
###              of journalistic articles.             ###
###        Sage website address is listed below        ###
###              in the 'address' variable             ###
##########################################################
###                        USAGE                       ###
##########################################################
###   1. Change the initial year variable as needed.   ###
###   2. Select a range in the next line, for example  ###
###      range(3) and year = 2000 would mean going     ###
###      through years 2000, 2001 and 2002.            ###
###   3. On the bottom of the scraper,                 ###
###      specify the .csv output file name.            ###
###   4. Relax and enjoy the rest of your day!         ###
##########################################################

import csv
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

### Open and read the URL ###

address = 'http://jou.sagepub.com/content/by/year'

br = Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)

### Create a structure of lists that will be nested one in another, except "keywords" list, it is defined later on ###

articles = []
issues = []
years = []

### ### ### On page with all years ### ### ###
### Create a list of all URLs that will be used later ###

full_list =[]

urllist = []
year = 1999
for x in range(1):
    year = year + 1
    address += '/' + str(year)
    urllist.append(address)
    print 'Going through year ' + str(year)

### Open a current (depending on where in loop we are) URL from the list  ###
### ### ### We will thus open a certain year ### ### ###

    html = br.open(urllist[x])
    soup = BeautifulSoup(html)
    table = soup.find('table', {"class" : "proxy-archive-by-year"})
    months = table.findAll('td', {"class" : "proxy-archive-by-year-month"})

### Go through each cell and extract <a> tag, strip URL from each <a> tag. ###
### Append url to a list (container for all URLs on the current page) ###
    
    list_of_a_tags = []
    for a in months:
		links = a.findAll('a')
		for items in links:
			list_of_a_tags.append(items.get('href'))

### Go through each link and open it ###
### ### ### We will thus open certain month's issues, one by one ### ### ###

    for k in range(len(list_of_a_tags)):
		html2 = ''
		html2 = br.open(list_of_a_tags[k])
		soup2 = BeautifulSoup(html2)

### Search through opened page and find all <a> tags that have rel="abstract" attribute, extract URL's from those ###

		abstracts = soup2.findAll('a', attrs={'rel': 'abstract'})
### Save current issue date into a variable (used later) ###
		issue = soup2.find('span', attrs={'class': 'toc-top-pub-date'}).text
		print "... Going through " + issue
		list_of_links_to_abstracts = []
		for item in abstracts:
			list_of_links_to_abstracts.append(item.get('href'))

### Go through each link on this page and open it (yes, another layer down) ###
### ### ### We will thus open all certain issue's abstract pages, one by one ### ### ###

		for x in range(len(list_of_links_to_abstracts)):
			html3 = ''
			html3 = br.open(list_of_links_to_abstracts[x])
			soup3 = BeautifulSoup(html3)

			list_of_keywords = soup3.findAll('ul', {"class" : "kwd-group"})
### Save abstract name (article name) into a variable (used later) ###
			article_name = soup3.find('h1', attrs={'id': 'article-title-1'}).text.encode("utf-8")
			print "... ... Now going through article - " + article_name
			keywords=[]
			for li in list_of_keywords:
				item = li.findAll('a')
				for a in item:
					keyword = a.text.encode('utf-8')
### The most important part, where the actual list for the future CSV is created ###
					full_list.append([year] + [issue] + [article_name] + [keyword])
    address = 'http://jou.sagepub.com/content/by/year'

handle = open('year_2000.csv', 'w')
outfile = csv.writer(handle)

outfile.writerows(full_list)

print ' '
print 'All done successfully!'
