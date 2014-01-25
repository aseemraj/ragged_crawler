## A simple web crawler that builds up the keyword-url index


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def splitstring(source, splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] += char 
    return output

def union(a, b):                    #modifies 'a' as 'a' union 'b'
    for e in b:
        if e not in a:
            a.append(e)

def get_next_target(pagestring):    #finds the next url in the page string
    start_link = pagestring.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = pagestring.find('"', start_link)
    end_quote = pagestring.find('"', start_quote + 1)
    url = pagestring[start_quote + 1: end_quote]
    return url, end_quote

def record_user_click(index, keyword, url):
    for e in index:
        if keyword == e[0]:
            for ucpair in e[1]:
                if url in ucpair:
                    ucpair[1] += 1

def add_to_index(index, keyword, url):    #adds the keyword and url to the index
    for e in index:
        if keyword == e[0]:
            for ucpair in e[1]:
                if url == ucpair[0]:
                    return
            e[1].append([url, 0])
            return
    index.append([keyword, [[url, 0]]])

def add_page_to_index(index, url, content): #adds words found on the url to the index as keywords and the respective url in the url list for that keyword
    word_list = splitstring(content, ' !@#$%^&*()-_+=;:"/?.>,<`~')
    for word in word_list:
        add_to_index(index, word, url)

def lookup(index, keyword):         #returns url list for a keyword in an index
    for e in index:
        if keyword == e[0]:
            return e[1]
    return []

def get_all_links(pagestring):      #returns list of all urls in page string
    url_list = []
    while True:
        url, endpos = get_next_target(pagestring)
        if url:
            url_list.append(url)
            pagestring = pagestring[endpos:]
        else:
            break
    return url_list

def crawl_web(seed, max_depth):     #returns list of crawled links
    tocrawl = [seed]
    crawled = []
    index = []
    next_depth = []
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(next_depth, get_all_links(content))
            crawled.append(page)
        if not tocrawl:
                  tocrawl, next_depth = next_depth, []
                  depth += 1
    return index
##
##seed = raw_input('Enter the seed url (e.g. http://www.google.com): ')
##depth = input('Enter the depth of crawl for building the index: ')
##index_list = crawl_web(seed, depth)
##for e in index_list:
##    print e
