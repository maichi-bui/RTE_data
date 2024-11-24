# RTE_data
Temporary script to get data from RTE API
## Setting up before running the packages

1. Create virtual environment, activate it and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
Note that Python version used is 3.9

2. Repository (temp) structure
    .
    ├── notebooks               # POC code in Jupyter notebooks
    │   ├── fetch_data.ipynb    # script to get data of 11 months
    ├── output_data             # exported data in csv form
    ├── utils               
    │   ├── common_func.py      # some reusable functions 
    │   ├── config.py           # environment variables
    ├── .env.sample             # example to set up `.env` file
    ├── .gitignore              
    ├── main.py                 # script to call API periodically
    ├── requirement.txt         # all packages required for scripts to run 
    ├── README.md               # instructions to run script
    └── ...

3. Configure client ID and secret

- Create a `.env` file at the root of your project and input the BASE64_CLIENT (following the file `.env.sample`), 
- By click to "Copy to base 64" in the UI following [this instruction](https://data.rte-france.org/documents/20182/22648/EN_GuideOauth2_v5.1.pdf/54d3d183-f20f-4290-9417-bcae122b9e46), we can obtain value to fill in `.env` file

4. Run `main.py`
Example:
```bash
python main.py --end_date "2024-11-11 00:00:00" --interval 5
```