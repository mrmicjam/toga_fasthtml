# toga_fasthtml
Toga + FastHTML boilerplate app

This uses daphne as a asgi server internally and the default uvicorn has poor mobile support.

## Installation
```
pip install -r requirements.txt
```

## Running local desktop
```
cd helloworld
python -m briefcase dev
```

# Running in android (emulator or device)
```
cd helloworld

# one time initial setup
python -m briefcase create android   

# each time the code is updated
python -m briefcase update android 

python -m briefcase build android

# will prompt for either emulator or connected android device
python -m briefcase run android
```

## Updating the requirements 
```
# one time
pip install pip-tools
python -m piptools compile requirements.in
```

