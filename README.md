## App purpose
Multipage Dash app  showing Interactive Charts on .... To COMPLETE<br>

Under development-to join the [Charming Data Community]((https://charming-data.circle.so/c/ai-python-projects/july-project-conflict-and-casualties)) Project initiative <br>
Part of this work is based on:<br>
["UCDP Candidate Events Dataset (UCDP Candidate) version 24.0.X"]((https://ucdp.uu.se/downloads/index.html#candidate))  
<br>

## App structure

```bash
dash-app-structure

|-- .env
|-- .gitignore
|-- data
|-- License
|-- README.md
|-- assets  
|-- components
|   |-- get_components_country.py
|   |-- get_components_home.py
|-- pages
|   |-- Home.py
|   |-- World.py
|   |-- Countries.py
|   |-- Conflictsindex.py
|-- utils
|   |-- settings.py
|-- app.py
|-- requirements.txt

```

<br>

## utils
code to retrieve the environment vars (OPENAI_API_KEY)
## components
support function to build components
## pages
page layout code and callbacks
## python version
python311
