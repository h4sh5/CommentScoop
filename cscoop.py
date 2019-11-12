#!/usr/bin/env python3

'''
CommentScoop is a python script that crawls through a web page (and any linked pages) source code (including CSS and javascript) and finds comments.

Copyright (C) 2017  Haoxi Tan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

'''

from bs4 import BeautifulSoup
from bs4 import Comment
import datetime, time
import urllib.request
import html
import sys
import re


def parse_url(url):
    '''
    This function parses the URL according to what it starts with.

    '''

    if url.startswith('//'):
        url = "http:"+url

    elif url.startswith("http")==0:
        url = "http://"+url

    
    return url


def get_response(url):
    '''
    Use urllib to get the response of the url requested
    '''
    try:
        opener = urllib.request.build_opener()
        urllib.request.install_opener(opener)
        #set useragent to mozilla
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        print("\nurl: %s\n" % url)
        return opener.open(url)

    except urllib.error.URLError:
            print("Error getting source code at: ",url)




def find_comments(soup):
    '''
    Utilizes the beatifulsoup library to find all HTML comments.
    '''
    for comment in soup.find_all(string=lambda text:isinstance(text,Comment)):
        print('<!--'+comment+'-->')


def get_scripts(soup):
    '''
    Finds JS and CSS scrips attached to the website and return them as a set
    '''

    scripts = []
    for i in soup.find_all('script'):
        if (i.get('src') != None):
            scripts.append(i.get('src'))

    for i in soup.find_all('link'):
        #print(i.get('rel'))
        if i.get('rel') == ['stylesheet']: #finds stylesheets
            scripts.append(i.get('href'))

    return(set(scripts))

def get_internal_links(soup):
    '''
    Loops through all the <a> tags and get all its href attributes to find internal links (that don't start with 'http')
    '''

    links = []
    for i in soup.find_all('a'):
        links.append(i.get('href'))

    for link in set(links):
        if str(link).startswith('http') or link==None:
            links.remove(link)

    return set(links) #returns it as a set to organize and eliminate repeated results


def find_script_comments(soup):
    '''
    loops through the JS and CSS files and finds their comments.
    '''

    #print(soup)
    regex = re.compile('(\/\*[\s\S]*?\*\/)|(\/\/(.*)$)', re.MULTILINE) #adds multiline regex for matching comments
    try:
        for comment in regex.search(str(soup)).groups(): 
            if comment!=None:
                print(comment)

    except AttributeError:
        print("No comments found.")


#main routine
if __name__ == "__main__":

    print('''


 @@@@@@@   @@@@@@   @@@@@@@@@@   @@@@@@@@@@   @@@@@@@@  @@@  @@@  @@@@@@@   @@@@@@    @@@@@@@   @@@@@@    @@@@@@   @@@@@@@   
@@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@  @@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
!@@       @@!  @@@  @@! @@! @@!  @@! @@! @@!  @@!       @@!@!@@@    @@!    !@@       !@@       @@!  @@@  @@!  @@@  @@!  @@@  
!@!       !@!  @!@  !@! !@! !@!  !@! !@! !@!  !@!       !@!!@!@!    !@!    !@!       !@!       !@!  @!@  !@!  @!@  !@!  @!@  
!@!       @!@  !@!  @!! !!@ @!@  @!! !!@ @!@  @!!!:!    @!@ !!@!    @!!    !!@@!!    !@!       @!@  !@!  @!@  !@!  @!@@!@!   
!!!       !@!  !!!  !@!   ! !@!  !@!   ! !@!  !!!!!:    !@!  !!!    !!!     !!@!!!   !!!       !@!  !!!  !@!  !!!  !!@!!!    
:!!       !!:  !!!  !!:     !!:  !!:     !!:  !!:       !!:  !!!    !!:         !:!  :!!       !!:  !!!  !!:  !!!  !!:       
:!:       :!:  !:!  :!:     :!:  :!:     :!:  :!:       :!:  !:!    :!:        !:!   :!:       :!:  !:!  :!:  !:!  :!:       
 ::: :::  ::::: ::  :::     ::   :::     ::    :: ::::   ::   ::     ::    :::: ::    ::: :::  ::::: ::  ::::: ::   ::       
 :: :: :   : :  :    :      :     :      :    : :: ::   ::    :      :     :: : :     :: :: :   : :  :    : :  :    :        
                                                                                                                             
CommentScoop is a Python 3 script that crawls through a web page (and any linked pages) source code (including CSS and javascript) and finds comments.

by Haoxi Tan

''')


    if len(sys.argv) < 2:
        print("usage: ./cscoop.py <url>")
        exit(1)

    url=parse_url(sys.argv[1])
    print("target link: %s\n"%url)

    #get the content of the URL
    response = get_response(url)

    
    #start parsing it with BeautifulSoup
    soup = BeautifulSoup(response, 'html.parser')
    find_comments(soup)

    for link in get_internal_links(soup): #finds comments in all internal links found
        try:
            find_comments(BeautifulSoup(get_response("%s/%s" % (url,link)), 'html.parser'))
        except TypeError:
            pass


    #print(get_scripts(soup))

    for link in get_scripts(soup):
        #print("\n%s\n"%link)

        if link.startswith('http') or link.startswith('//'):
            find_script_comments(BeautifulSoup(get_response(parse_url(link)),'html.parser'))

        else:
            find_script_comments(BeautifulSoup(get_response(parse_url('%s/%s'%(url,link))),'html.parser'))

