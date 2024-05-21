### job_assignment_pivotroots

#### follow the steps to setup pivot_backend locally (granted git and python is installed on your distro/os)

1. git clone <will add link here later>

2. cd pivot_backend/

3. python3 -m venv venv 

run this if venv isnt installed >> (sudo apt-get install -y python3-venv) as for windows it should come preinstalled

4. source venv/Scripts/activate (if windows system) | source venv/source/activate (if linux system)

5. pip install -r requirements.txt

6. python app.py (depending on what the env variable for python3 is on your system)


#### follow the steps to setup pivot_frontend locally (granted node is installed on your distro/os)

1. cd pivot_frontend

2. npm install (install all necessary packages)

3. npm start

4. npm run build (when deploying)