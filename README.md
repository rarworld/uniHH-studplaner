# uniHH-studplaner

Stundenplanner für CiS Physik und Physik

Simple Vue UI zum Planen des Semesters.


[GitHubPage](https://rarworld.github.io/uniHH-studplaner/vue/dist/index.html)

## build data
- source .venv/bin/activate
- python data_download.py phy
- python data_download.py cis
- python data_prepare.py
- python data_merge.py
- python nav_prepare.py
- copy to data.json + nav.json -> assets

## build vue 
- npm run build (creates new dist-folder)