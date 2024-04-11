# Project Zero: Smart City Development

<iframe frameborder="0" style="width:100%;height:995px;" src="https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=market_process_flow.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1NdY2A7zdbVWSgDFYVe0Fysj4JK5x_Lr4%26export%3Ddownload"></iframe>

Briefly describe the purpose and goals of your data engineering project.

## Directory Structure

- `config`: Contains information on project setup, business goals and setup
- `data`: Contains project data in raw and processed formates
- `notebooks`: Houses Jupyter notebooks for data exploration and analysis.
- `src`: Contains ETL processing scripts inc pipeline automation
- `tests`: Contains unit and pytest to validate quality code
-

## Data Description

- Raw data is stored in `data-context-and-setup/data/csv/`.
- More details about each data file can be found in the respective CSV files.

## Dependencies

- Python 3.x
- pandas
- (add any other libraries)

## Install dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run:

Data Processing Script
Run the data processing script using:

bash
Copy code
python data-context-and-setup/process_folder/data.py
Jupyter Notebooks
Open Jupyter notebooks using:

bash
Copy code
jupyter notebook notebooks/

## watchdog file monitor

To compile watchdog file monitor into .exe package please follow the following instructions
- cd into watchdog folder
- in comand line run the following code:
`pyinstaller --hidden-import=sklearn --hidden-import=pandas --hidden-import=numpy --hidden-import=etl.utilities --hidden-import=sklearn.pipeline --hidden-import=sklearn.compose --hidden-import=sklearn.preprocessing --hidden-import=sklearn.impute --hidden-import=sklearn.model_selection --hidden-import=sklearn.feature_extraction --hidden-import=sklearn.feature_selection --hidden-import=sklearn.ensemble --hidden-import=sklearn.linear_model --hidden-import=sklearn.metrics watchdog_monitor.py`
-copy `/dist` folder and `pipeline.pkl` into desired location 
- run exe file to initiate the watchdog monitor


## Contact

For questions or feedback, please contact Haaris Ramzan.

## Acknowledgments

We thank [Author Name] for their library [Library Name] that facilitated data processing.
Additional Documentation
