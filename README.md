# Weaviate Verba and dlt Sources

This is an experimental project to load data from the [dlt's Verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/) to [Verba](https://github.com/weaviate/Verba).

[zendesk_verba.py](zendesk_verba.py) is a Python script that defines a data pipeline that loads tickets data from Zendesk Support to Verba.

## How to run the data pipeline

1. Clone this repository.
2. Create a Python virtual environment with `python -m venv venv` and activate it with `source venv/bin/activate`.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Set up the credentials for [Weaviate Cloud Services](https://console.weaviate.cloud/) and for Zendesk API in the `.dlt/secrets.toml` file.
5. Run the pipeline script with `python zendesk_verba.py`.

