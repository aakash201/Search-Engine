import urllib
import requests
from bs4 import BeautifulSoup

depth=7
getrank={}
def getpage(url):
    src_code=requests.get(url)
    plain_text=src_code.text
    return plain_text
def getnexturl(page):
    start_link=page.find('a href')
    if start_link==-1:
        return None,0
    start_quote=page.find("'",start_link)
    end_quote=page.find("'",start_quote+1)
    url=page[start_quote+1:end_quote]
    return url,end_quote
def get_all_links(url):
    links=[]
    src_code=requests.get(url)
    plain_text=src_code.text
    soup=BeautifulSoup(plain_text)
    #print 'links\n'
    for link in soup.find_all('a',href=True):
        href=link.get('href')
        #print href
        if href.startswith('http'):
            links.append(href)
    return links
def union(a,b,visit):
    for e in b :
        if e not in a:
            if e not in visit:
                a.append(e)

def addtoindex(index,url,keyword):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword]=[url]
def addpagetoindex(index,url,page):
    for i in page.split():
        addtoindex(index,url,i)
def crawl(src):
    global depth
    q=[src]
    index={}
    visit=[]
    visit.append(src)
    graph={}
    while q:
        p=q[0]
        q.pop(0)
        print "\np= "
        print p
        print "\n"
        depth-=1
        print depth
        if depth<=0:
            break;
        c=getpage(p)
        f=get_all_links(p)
        addpagetoindex(index,p,c)
        graph[p]=[]
        for i in f :
            if i not in visit:
                q.append(i)
                visit.append(i)
                graph[p].append(i)
    return visit,index,graph

def compute_rank(graph):
    d=0.8
    rank={}
    newranks={}
    npages=6.0
    time=6
    for url in graph:
        rank[url]=1.0/npages
    while(time>0):
        for url in graph:
            newrank=(1-d)/npages
            for temp in graph:
                if url in temp:
                    if len(graph[temp]) != 0:
                        newrank=newrank+(d*rank[temp]/len(graph[temp]))
                    else :
                        newrank=newrank+(d*rank[temp])
            newranks[url]=newrank
        rank=newranks
        time=time-1;
    return rank
def compare(a,b):
    if getrank[b]<getrank[a]:
        return -1
    elif getrank[b]>getrank[a]:
        return 1
    else:
        return 0


#url="http://pthonproject201.blogspot.in/"
#url="http://udacity.com/cs101x/urank/index.html"
url = raw_input("\nEnter url of seed page : ")
p=getpage(url)
l=get_all_links(url)
l=list(set(l))
visit,index,graph=crawl(url)
global getrank
rank=compute_rank(graph)
getrank=rank
for keyword in index:
    index[keyword].sort(compare)
value = raw_input("\nEnter keyword to be searched : ")
if value not in index :
    print ("\nKeyword not found\n")
else :
    b=index[value]
    print ("\nProcessing finished ... Required pages follow in order of popularity\n")
    print b


