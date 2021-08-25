# Grizzly Setup

### Install Python Requirements
```bash
pip3 install -r requirements.txt
pip3 install -e .
```

# Run

```bash
python3 -m grizzly Path/to/firefox lqc
```

# Config

The config file is currently hard coded in the adapter

```python
config = parse_config("./config/preset-firefox.config.json")
```

See more about config files [here](docs/CONFIGURATION.md).