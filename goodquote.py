import urllib2
import re,sys
from fake_useragent import UserAgent
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

#let me fake_useragent
ua = UserAgent()
ua.chrome

base_tag_url = "https://www.goodreads.com/quotes/tag/"
if len(sys.argv)<1:
    tag = raw_input("type the tag to mine - ")
else:
    tag = sys.argv[1]
page=1

url = base_tag_url+tag
print (url)

init_html = urllib2.urlopen(url)
init_text = init_html.read()
init_soup = BeautifulSoup(init_text)

for script_tags in init_soup.findAll('script'):
    script_tags.extract()
#count sentences    
def sentence_count(line):
    sentences = line.split('.')
    return len(sentences)

init_quotetext = init_soup.findAll("div","quoteText")    

for i in range(len(init_quotetext)):
    init_clean_text = init_quotetext[i].text.replace("&ldquo;","").split('&')[0]
    init_clean_text = init_clean_text.encode("utf-8")
    print init_clean_text
    print "Indexed : " + str(sentence_count(init_clean_text))
    print "\n"
    
    with open(tag+".txt", "a") as myfile:
        myfile.write(init_clean_text)




#check if next page exists
next_page = init_soup.findAll("a","next_page")


while (next_page):
    page += 1
    newurl = url+"?page="+str(page)
    newtext = urllib2.urlopen(newurl).read()
    print "Indexing page number - " + str(page)


    soup = BeautifulSoup(newtext)
    quotetext = soup.findAll("div","quoteText")

    for script_tags in soup.findAll('script'):
        script_tags.extract()

    for i in range(len(quotetext)):
        clean_text = quotetext[i].text.replace("&ldquo;","").split('&')[0]
        clean_text = clean_text.encode("utf-8")
        print clean_text
        print "Indexed : " + str(sentence_count(clean_text))
        print "\n"
        
        with open(tag+".txt", "a") as myfile:
            myfile.write(clean_text+"\n\n\n")

print "Text Mining for "+tag+ " has completed"
