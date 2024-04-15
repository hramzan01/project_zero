# Project Zero: Smart City Development

## Description
Project Zero is a cutting-edge data analytics tool designed to streamline and enhance the management of evolving city projects. By centralizing and facilitating dynamic data tracking, Project Zero empowers project stakeholders to adapt and optimize their designs effectively.

### Key Features:
- Centralized Data Management: Project Zero provides a centralized platform to consolidate various types of data related to city projects, including early concept data such as areas and building types.

*Dynamic Tracking: With Project Zero, users can seamlessly track changes in project design over time, ensuring that the most up-to-date information is always available.

*Specialist Data Integration: The tool integrates specialist data to enhance analysis and decision-making processes. This includes data related to expected energy demand, predicted population trends, and embodied carbon.

*Comprehensive Outputs: Project Zero generates comprehensive outputs based on the integrated data, offering insights into various aspects of the project, such as expected energy demand, predicted population growth, and embodied carbon emissions.


## Project Directory
```bash
+---app
|   |   00_home.py
|   |   home.py
|   |   README.md
|   |
|   +---assets
|   |       logo.png
|   |       pzero_code.mp4
|   |       pzer_t2.mp4
|   |       pz_vid.mp4
|   |       pz_what.png
|   |
|   \---pages
|           01_utilities.py
|           02_carbon.py
|           03_population.py
|
+---config
|       file_renamer.py
|       pipeline.drawio
|       timeline.html
|
+---etl
|   |   carbon.py
|   |   extract.py
|   |   load.py
|   |   population.py
|   |   typologies.py
|   |   utilities.py
|   |   utils.py
|   |   __init__.py
|
+---notebooks
|       nb_carbon.ipynb
|       nb_data_merge.ipynb
|       nb_openai.ipynb
|       nb_population.ipynb
|       nb_sklearn_setup.ipynb
|       nb_sklearn_test_train.ipynb
|       nb_sus_coefficient.ipynb
|       nb_sus_targets.ipynb
|       nb_timeline.ipynb
|       nb_typologies.ipynb
|       nb_utilities_01.ipynb
|       nb_utilities_02.ipynb
|       nb_utilities_03.ipynb
|       nb_utilities_04.ipynb
|       nb_utilities_pipe.ipynb
|
+---pipeline
|       pipeline.pkl
|       pipeline.py
|       __init__.py
|
+---tests
|   |   test_pipeline.py
|   |   __init__.py
|
\---watchdog
        data_coefficients.csv
        data_demmand.csv
        data_design.csv
        data_population.csv
        energy_demmand.csv
        pipeline.pkl
        watchdog_monitor.py
```

## Getting Started

### Dependencies
```bash
pip install -r requirements.txt
```

### Installing
```bash
pip install project_zero
```

### Executing program

* How to run the program
* Step-by-step bullets
```bash
code blocks for commands
```

## Authors
Haaris Ramzan
Riccardo Pellizon

## License
This project is licensed under Proprietary License - see the LICENSE.md file for details

## Acknowledgments
* The Project Technology Team and Leadership at RSHP who helped support and facilitate this development

---


