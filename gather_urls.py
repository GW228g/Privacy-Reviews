#!/usr/bin/env python3

import csv, re, tldextract, requests, time, os, pdfkit
from urllib.parse import urljoin
from bs4 import BeautifulSoup

user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

header = ("date", "domain", "privacy", "terms")
outputFile = open('summary.csv', 'a', newline='')
outputWriter = csv.writer(outputFile, delimiter=',')
outputWriter.writerows([header])

input_file = csv.DictReader(open('urls.csv'))
for row in input_file:
#    url = input("Enter full url: ")
    url = str(row["URL"])
    ext = tldextract.extract(url)
    filename = ext.domain
    print('Searching... '+ filename)

    date = time.strftime("%Y%m%d")
    datestamp = time.strftime("%Y/%m/%d")
    timestr = time.strftime("%Y%m%d")

    r = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(r.text, "lxml")

    print('Checking for Privacy Policies...')
    for tag in soup.find_all("a", href=re.compile("rivacy")):
        Full_url1 = urljoin(url, tag['href'])
        print(Full_url1)

    print('Checking for Terms...')
    for tag in soup.find_all("a", href=re.compile("erms")):
        Full_url2 = urljoin(url, tag['href'])
        print(Full_url2)

    rows = (datestamp, filename, Full_url1, Full_url2)
    header = ("date", "domain", "privacy", "terms")
    print('Adding to CSV file...summary.csv')
    outputFile = open('summary.csv', 'a', newline='')
    outputWriter = csv.writer(outputFile, delimiter=',')
    outputWriter.writerows([rows])

    outputFile.close()
print('Checked for Privacy Policies and Terms complete')


#Step two create PDFs
print('Now creating PDFs...')
options = {
    'quiet': ''
    }

input_file = csv.DictReader(open('summary.csv'))
for row in input_file:
    domain = str(row["domain"])
    privacy = str(row["privacy"])
    terms = str(row["terms"])
    filename1 = domain + ' privacy ' + timestr + ".pdf"
    filename2 = domain + ' Terms ' + timestr + ".pdf"
    pdfkit.from_url([privacy], filename1, options=options)
    pdfkit.from_url([privacy], filename2, options=options)
    print('PDFs Generated')
os.rename('summary.csv','Privacy_Summary_' + date + '.csv')
