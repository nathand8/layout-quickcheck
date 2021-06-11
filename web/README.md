# Web UI for Layout QuickCheck

# Running the UI
Quickest way to get the Web UI running. Follow these directions.

### Build the UI

From `web/ui`
```bash
npm install
npm run build
```

### Run the Backend Server

From `web/server`
```bash
pip3 install -r requirements.txt
python main.py
```
### Go

Go to `http://localhost:5000/` to see it running.


# Developing the UI
If you'd like to run the UI to make changes to it, follow these directions.

### Install and Run UI 

From `web/ui`
```bash
npm install
npm start
```

The backend will have to be run on port 5000. If a different port is needed, the proxy in `web/ui/package.json` will need to be updated to that other port.

### Install and Run Backend

From `web/server`
```bash
pip3 install -r requirements.txt
python main.py
```

### Go

Go to `http://localhost:3000/` to see it running.