# R&I Software Server Setup

### Note: You need to have your python editor (vsCode / PyCharm), python3, and postgres installed in your system

****
**[python](https://www.python.org/downloads/)
[postgres](https://www.postgresql.org/download/)
[vscode](https://code.visualstudio.com/download)
[pycharm](https://www.jetbrains.com/pycharm/download/#section=mac)**

****
****
### 1. **Clone R&I server** 
**Create 'risoftware' folder in your desktop. Go to your Editor, and clone the R&I Server.**

Open a new terminal in the editor and run the following commands
```bash
cd desktop
```
```bash
cd risoftware
```
```bash
git clone https://github.com/R-I-Software/server.git
```
****
![img2.png](doc_images%2Fimg2.png)
****
****
### 2. **Create venv**
**Create a python virtual environment in the folder where you have cloned your R&I server.**

Run the following commands.

On macOS / Linux
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

 On Windows
```bash
python -m venv venv
```
```bash
venv/Scripts/activate.bat
```
****
![img5.png](doc_images%2Fimg5.png)
****
****
### 3. **Install Dependencies**
**In the terminal, cd inside the server folder and install the server requirements.**

**Note: Before you run the commands, first, remove line 31, "psycopg2==2.9.5" from requirements.txt.**

Run the following commands afterward

On macOS / Linux
```bash
cd server
```
```bash
pip install -r requirements.txt
```

 On Windows
```bash
cd server
```
```bash
py -m pip install -r requirements.txt
```
****
![img9.png](doc_images%2Fimg9.png)
****
****

### 4. **Create risoftware DB**
**Open pgAdmin and create a database named "risoftware". The password for the database should be 1234, and the port should be 5432.**
****
![img6.png](doc_images%2Fimg6.png)
****
****
5. **Create versions folder** - Go inside server/db/migrations, and create an empty folder named "versions".
****
![img7.png](doc_images%2Fimg7.png)
****
****

### 6. **Populate the DB**
**Go to your editor, and open terminal.**

Run the following command

On macOS / Linux
```bash
python3 fake.py
```

 On Windows
```bash
py fake.py
```
****
![img3.png](doc_images%2Fimg3.png)
****
****

### 7. **Start the server**
**Lastly, start the server.**

Run the following command

On macOS / Linux
```bash
python3 manage.py
```

 On Windows
```bash
py manage.py
```
****
![img8.png](doc_images%2Fimg8.png)