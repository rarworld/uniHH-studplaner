source .venv/bin/activate

python data_download.py phy

python data_download.py cis

python data_prepare.py

python data_merge.py

python nav_prepare.py

copy to data.json + nav.json -> assets