# Project Title

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.

## Project Directory

```bash
├── app
│   ├── css
│   │   ├── **/*.css
│   ├── favicon.ico
│   ├── images
│   ├── index.html
│   ├── js
│   │   ├── **/*.js
│   └── partials/template
├── dist (or build)
├── node_modules
├── bower_components (if using bower)
├── test
├── Gruntfile.js/gulpfile.js
├── README.md
├── package.json
├── bower.json (if using bower)
└── .gitignore
```

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)

---

# Project Zero: Smart City Development

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
