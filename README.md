#alumnilist.py

This is a small script for searching Georgia State University's scholarworks for dissertations and theses meeting certain criteria.

##Usage
In the file **alumnilist.py**, one can edit *driver* to the desired web browser and *publication_title* to the department name, and *startyear* to give the year to start the search. The user will also need to edit *file_phd* and *file_masters* to give a location to save the .csv files containing the list of phd and masters works submitted to scholarworks.

The program iterates by year because the format of the result page makes it difficult to access results exceeding 25 results, as this is Scholarworks limit on results per page. Note that if a search results in more than 25 results, the script currently only collects those on the first page because accessing additional pages reruns the search submission. 

This program results in csv files with author name, dissertation title, and dissertation date.
