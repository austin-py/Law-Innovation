# FDA Database Search Engine 
This program is a search platform that allows lawyers (or other interested parties) to easily get descriptive statistics regarding FDA warning letters and inspections. The program stops short of generating a 'risk level', but it is our hope that it can be used by attorneys to have more concrete evidence when presenting information about possible risks to clients. 



## Running The Code
_Note: These instructions currently only pertain to MacOS. Windows Instructions will be added shortly._

### Prereqs [These instructions only need completed once per computer]: 
You must have python3 installed on your computer. MacOS comes with this installed by default. 
Additionally you need the pip package manager. Instructions on how to download this can be found [here](https://www.geeksforgeeks.org/how-to-install-pip-in-macos/). 

Run 
```zsh
pip install virtualenv 
```

### Running it [These instructions need completed every time]
1. Navigate to the Law-Innovation parent directory within terminal 
2. In terminal (with zsh activated) type the following to activate the virtual environment: 
```zsh
source virt/bin/activate
```

3. Following that, run the following command: 
``` zsh 
pip install -r requirements.txt 
```

4. Then run the following command: 
``` zsh 
python3 app.py 
```

5. Lastly, once the program is up and running, acccess the website using the [link it provides](https://127.0.0.1:5000/)


_Note if in a different shell such as fish or bash , the command to activvate virtual environemt the might be different_



## Project Background + Future Updates: 

In order to create our search engine, we web-scraped data from the FDA website on warning letters and condensed it into a CSV file. Additionally, we found an excel sheet online with every inspection letter from the FDA over the course of 10+ year. We tried to cross reference between this data, however, not all of it was able to match up. In addition, much of this data from the sheets is not dispaleyd on our website. Therefore, we see it fitting that a future group, continues to work with our data and display more of it when using the search engine. Additionally, the data is not being udpated whereas the FDA website does add new warning letters frequently. Another update to the project could be linking this search engine to the FDA website and it's archives. Lastly, much of our project focused on gathering data, so we also see it fitting that a future group takes our work and improves the CSS/HTML and focus on the user interface interaction with the data. 










