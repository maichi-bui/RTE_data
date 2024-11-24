# RTE_data
Temporary script to get data from RTE API
## Setting up before running the packages

1. Create virtual environment, activate it and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

2. Configure client ID and secret

Create a `.env` file at the root of your project and input the BASE64_CLIENT (following the file `.env.sample`), by click to "Copy to base 64" in the UI following [this instruction](https://data.rte-france.org/documents/20182/22648/EN_GuideOauth2_v5.1.pdf/54d3d183-f20f-4290-9417-bcae122b9e46)

3. Run `main.py`

```bash
python main.py --end_date "2024-11-11 00:00:00"
```