all: clean download prepare copy build

v2: v2Clean v2Prepare v2Copy build

v2Prepare:
	( \
		cd data; \
    	source .venv/bin/activate; \
		cd v2; \
		python DataImporter.py; \
		python NaviCreator.py; \
	)

v2Clean:
	rm -f data/v2/data/*.json
	rm -rf vue/dist

v2Copy:
	cp data/v2/data/data_enriched.json vue/src/assets/data.json
	cp data/v2/data/nav.json vue/src/assets


clean:
	rm -f data/linkList*.json data/data*.json
	rm -rf vue/dist


download:
	( \
		cd data; \
    	source .venv/bin/activate; \
		python data_download.py phy; \
		python data_download.py cis; \
	)

prepare:
	( \
		cd data; \
    	source .venv/bin/activate; \
		python data_prepare.py; \
		python data_merge.py; \
		python data_enrich.py; \
		python nav_prepare.py; \
	)
    
build:
	cd vue; npm run build

copy:
	cp data/data_enriched.json vue/src/assets/data.json
	cp data/nav.json vue/src/assets

run:
	cd vue; npm run serve