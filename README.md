# X00200430 (Alex O'Connor) CA 2
## Overview
This project is a simple python calculator function using a Continuous Integration pipeline. The repository is setup in GitHub and the Azure runs the pipeline.  


## Technologies Used

 - GitHub
 - Azure Pipelines - Created a pipeline YAML file that runs the pipeline on Azure when code is pushed to the main or development branches.
 - Python version 3.13.3 - The language the application was written in.
 - Pytest -  Used for testing and giving code coverage
 - Pylint - Used for creating code quality reports

## Local Development Setup


### Clone the project

     git clone https://github.com/alexo1connor/X00200430_CA2.git
     
### Setup a virtual environment

    python -m venv venv
 
 ### Install dependencies

    pip install -r requirements.txt

 
### Run the tests

    pytest
    # or for code coverage use below
    pytest --cov
    

## CI Pipeline Implementation

The CI pipeline is run by Azure and uses the azure-pipelines.yml file.
It gets triggered by a push to the main or development branch.

 1. First the pipeline will create an ubuntu environment and use python version 3.13.3
 2. Install Dependencies - The  dependencies in the requirements.txt file get installed.
 3. Run Tests - The pytest command is run `pytest --cov=./ --cov-report=xml --cov-report=html --cov-fail-under=80` This command will run the tests in the tests directory and generate a report and code coverage score. The step will fail if the coverage is below 80%.
 4. Publish Code Coverage Reports - The code coverage report gets published to azure.
 5. Run Code Analysis Report - The pylint commands is run to get a report on code quality `pylint src --output-format=text >> pylint_report.txt` the output is redirected to a file for upload later.  A second command is run to output the file into the console `cat pylint_report.txt`
 6.  Publish Code Analysis Report - The report by pylint gets added as an artefact on azure. 
 7.  Build Python App -  The python app gets built using `python -m compileall .`
 8. The files are then copied and added to azure as an artefact.

## Branch Policies and Protection
The main branch is protected by rules setup on GitHub.

 1. PR Required - A pull request is required to merge to the main branch.
 2. CI Pass - The CI pipeline on Azure needs to pass before merging.
 3. Review Required - The PR needs to be reviewed before it can be approved. (Since there isn't some else working on this project I have to skip this rule)

## Testing Strategy
I use Pytest for for running the unit tests.

 1. I created a .coveragerc file to setup exclusions so `__init__.py` files aren't included since they can dilute the code coverage score since they always give a 100% score since they are empty.
 2. I enforce a 80% coverage score for the pipeline to pass.
 3. If one test fails the entire pipeline fails.