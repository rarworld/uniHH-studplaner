all: clean download prepare copy build

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