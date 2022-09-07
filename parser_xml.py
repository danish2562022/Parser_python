"""
@author: Danwer
Date: 06:09:2022
"""

import bs4
import os
import lxml
import pandas as pd
from tqdm import tqdm

from bs4 import BeautifulSoup as bs
file_name = []
value = []
data = pd.DataFrame(columns = ["file_name","Isolation_source"])
for i in tqdm(os.listdir("./xml")):
    
    path = "./xml/" + str(i)
    with open(path, "r") as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        bs_content = bs(content, "lxml")
    

    result  = bs_content.find_all("sample_attribute")
    result_2= str(bs_content.find("primary_id"))
    result_2 = result_2.split("<")[1].split(">")
    file_name.append(result_2[1])
    for i in result:
        i = str(i)
    
        if "tag>isolation_source" in i.split("<"):
            x = i.split(">")[4].split("<")[0]
    value.append(x)
data["file_name"] = file_name
data["Isolation_source"] = value
data.to_excel("output.xlsx")
    
