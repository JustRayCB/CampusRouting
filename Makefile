run:
	open ./webpage/ask_path.html
	uvicorn  --app-dir ./src/ main:app --reload
