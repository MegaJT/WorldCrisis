## App purpose
Multipage Dash app with interactive charts highlighting 2024 civilian casualties in violent conflicts. AI-assisted news summarization and translation are triggered by user interactions with the plots. <br>

Under development-to join the [Charming Data Community](https://charming-data.circle.so/c/ai-python-projects/july-project-conflict-and-casualties) Project initiative <br>

Part of this work is based on:  <br>
["UCDP Candidate Events Dataset (UCDP Candidate) version 24.0.X"](https://ucdp.uu.se/downloads/index.html#candidate)
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

## Subfolders Details
### utils
code to retrieve the environment vars (OPENAI_API_KEY)
### components
support functions to build components instantiated in the pages layout
### pages
pages layout code and callbacks
### python version
python311
