serve:
	sudo FLASK_APP=app.py flask run --port 80 --host 0.0.0.0
.PHONY: serve

purge:
	python3 app.py --purge; python3 app.py --import-data import.json
.PHONY: purge
