main:
	uvicorn  --app-dir ./src/ main:app --reload 

run:
	python -m http.server -b 127.0.0.1 -d webpage/src/ 8080 &
	uvicorn  --app-dir ./src/ main:app --reload &
	open http://127.0.0.1:8080/welcome.html
