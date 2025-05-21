# toga_fasthtml
Toga + FastHTML boilerplate app

This uses daphne as a asgi server internally and the default uvicorn has poor mobile support.

## Installation
```
pip install -r requirements.txt
```

## Running
```
python app.py
```

## Updating the requirements 
```
# one time
pip install pip-tools
python -m piptools compile requirements.in
```

## TODO
- [ ] example briefcase android and ios builds

