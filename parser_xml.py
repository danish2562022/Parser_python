import bs4

import lxml

from bs4 import BeautifulSoup as bs
with open("SraExperimentPackage.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")
    

result  = bs_content.find_all("sample_attribute")
for i in result:
    i = str(i)
    
    if "tag>isolation_source" in i.split("<"):
        print(i)
