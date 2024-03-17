run:
	open ./webpage/src/welcome.html
	uvicorn  --app-dir ./src/ main:app --reload
