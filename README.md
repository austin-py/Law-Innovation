# FDA Database Search Engine 
This program is a search platform that allows lawyers (or other interested parties) to easily get descriptive statistics regarding FDA warning letters and inspections. The program stops short of generating a 'risk level', but it is our hope that it can be used by attorneys to have more concrete evidence when presenting information about possible risks to clients. 



## Running The Code
_Note: These instructions currently only pertain to MacOS. Windows Instructions will be added shortly._

### Prereqs [These instructions only need completed once per computer]: 
You must have python3 installed on your computer. MacOS comes with this installed by default. 
Additionally you need the pip package manager. Instructions on how to download this can be found INSERT HERE  
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



## Project Background: 
Details and stuff here... 
