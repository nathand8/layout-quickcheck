
setup:
	pip3 install -r requirements.txt

build:
	(cd web/ui && npm install)
	(cd web/ui && npm run build)
	(cd web/server && pip3 install -r requirements.txt)

nightly:
	bash infra/nightly.sh
