from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import csv
import time

#Use scholarworks to make a list of recent graduates (those who have shared their dissertations and theses) and related info
driver = webdriver.Firefox()
onlydissauthor=[]
onlydisstitle=[]
onlydissdate=[]
onlythesesauthor=[]
onlythesestitle=[]
onlythesesdate=[]
publication_title="astronomy" #easiest way to limit to one department is the publication title
department="Physics and Astronomy"
file_phd="" #where to save the phd results (.csv)
file_masters="" #where to save the masters results (.csv)
starturl="https://scholarworks.gsu.edu/do/search/advanced/?q=publication_title%3A"+publication_title+"&start=0&start_date="
month=[1]
day=[1]
#we will search by year in order to limit results to less than 25 (at moment this code fails to retrieve results from more than one page)
startyear=2000

while startyear+1 < 2020:
    year=[startyear,startyear+1]
    date="0"+str(month[0])+"%2F0"+str(day[0])+"%2F"+str(year[0])+"&end_date=0"+str(month[0])+"%2F0"+str(day[0])+"%2F"+str(year[1])
    endurl="&context=806485&sort=score&facet="
    url=starturl+date+endurl
    driver.get(url) #navigate to the page
    print("waiting 15 sec to move to new page") #because scholarworks redirects to result page we need to wait for result page
    time.sleep(15)
    print("moving on")
    innerHTLM=driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTLM, 'html.parser')
    results = soup.findAll('span', {"class": "grid_6"})
    found=results[1].text
    if "Showing 0 out of 0 results." not in found:
        print("Results!")
        # Extracting names of results
        author = soup.findAll('span', {"class": "author"})
        title = soup.findAll('span', {"class": "title"})
        publication=soup.findAll('span', {"class": "pub"})
        year= soup.findAll('span', {"class": "year"})
        #now select only results with Physics and Astronomy publication
        auth=[a.text.replace("Author: ","") for a in author]
        print(auth)
        t=[e.text for e in title]
        date=[d.text.replace("Date: ","") for d in year]
        pub=[p.text.replace("Publication: ","") for p in publication]
        finddiss=np.isin(pub,department+" Dissertations") #for PhD alum
        elements=np.where(finddiss)[0][0:len(finddiss)]
        onlydisspub=[pub[e] for e in elements]
        onlydissauthorn=[auth[e] for e in elements]
        onlydisstitlen=[t[e] for e in elements]
        onlydissdaten=[date[e] for e in elements]
        findthesis=np.isin(pub, department+" Theses") #for masters alum
        elements=np.where(findthesis)[0][0:len(findthesis)]
        onlythesespub=[pub[e] for e in elements]
        onlythesesauthorn=[auth[e] for e in elements]
        onlythesestitlen=[t[e] for e in elements]
        onlythesesdaten=[date[e] for e in elements]
        newauthorsdissn=[a.replace(",",".") for a in onlydissauthorn] #helps with csv to replace commas in names and titles with periods
        newtitlesdissn=[a.replace(",",".") for a in onlydisstitlen]
        newauthorsthesesn=[a.replace(",",".") for a in onlythesesauthorn]
        newtitlesthesesn=[a.replace(",",".") for a in onlythesestitlen]
        onlydissauthor=np.concatenate((onlydissauthor, newauthorsdissn), axis=0)
        onlydisstitle=np.concatenate((onlydisstitle, newtitlesdissn), axis=0)
        onlydissdate=np.concatenate((onlydissdate, onlydissdaten), axis=0)
        onlythesesauthor=np.concatenate((onlythesesauthor, newauthorsthesesn), axis=0)
        onlythesestitle=np.concatenate((onlythesestitle, newtitlesthesesn), axis=0)
        onlythesesdate=np.concatenate((onlythesesdate, onlythesesdaten), axis=0)
        startyear=startyear+1
    else:
        print("No results")
        startyear=startyear+1
print("Done")


with open(file_phd,mode="w") as alumni_file:
    for i in range(len(onlydissdate)):
        alumni_writer=csv.writer(alumni_file,delimiter=",")
        alumni_writer.writerow([onlydissauthor[i],onlydisstitle[i],onlydissdate[i]])

with open(file_masters,mode="w") as alumni_file:
    for i in range(len(onlythesesdate)):
        alumni_writer=csv.writer(alumni_file,delimiter=",")
        alumni_writer.writerow([onlythesesauthor[i],onlythesestitle[i],onlythesesdate[i]])
