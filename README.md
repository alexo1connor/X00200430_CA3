
# X00200430 (Alex O'Connor) CA 3

## Overview

This project is a simple python calculator function using a Continuous Integration and Delivery pipeline. The repository is setup in GitHub and the Azure runs the pipeline.

## Technologies Used
- GitHub
- Azure Pipelines - Created a pipeline YAML file that runs the pipeline on Azure when code is pushed to the main or development branches.
- Python version 3.13.3 - The language the application was written in.
- Pytest - Used for testing and giving code coverage
- Pylint - Used for creating code quality reports
- Flask - Used to create the web app
- Selenium - Used for UAT Testing
- Locust - Used for Performance Testing
- Gitleaks - Used to find sensitive information in commits
- OWASP - Checks the dependencies of the project

  

## Local Development Setup

### Clone the project

    git clone https://github.com/alexo1connor/X00200430_CA3.git

### Setup a virtual environment

    python -m venv venv

### Install dependencies

    pip install -r requirements.txt

### Run the tests

    pytest

### or for code coverage use below

    pytest --cov

### Run Flask

      flask run

### Run Selenium Tests

    flask run # The applcation needs to be running.
    #Run the command below in a separate terminal instance
    pytest tests/UAT_tests

### Run Locust Tests

    flask run # The applcation needs to be running.
    #Run the command below in a separate terminal instance
    locust -f tests/locustfile.py #This will print a link to a localhost where you can access the lcoust interface.
    #You can run it headless with the command below
    locust -f tests/locustfile.py --headless -u 10 -r 2 --run-time 30s

 

## Pipeline Implementation
The pipeline is run by Azure and uses the azure-pipelines.yml file.

It gets triggered by a push to the main or development branch.

  The pipeline is broken up into four stages.
  

 1. Build -  Builds the application, runs unit tests, checks code coverage, and analysis of the code.
 2. Security Checks - Scans the repo for credential leaks or dependecy security issues.
 3. Deploy Staging - The application is run in a staging environment. UAT and performance tests are then run on it.
 4. Deploy Live - If the branch running the pipeline is the main branch this stage will run and push the application to the live environment. 


## **Build Stage**
1. First the pipeline will create an ubuntu environment and use python version 3.13.3

2. Install Dependencies - The dependencies in the requirements.txt file get installed.

3. Run Tests - The pytest command is run `pytest --cov=./ --cov-report=xml --cov-report=html --cov-fail-under=80` This command will run the tests in the tests directory and generate a report and code coverage score. The step will fail if the coverage is below 80%.

4. Publish Code Coverage Reports - The code coverage report gets published to azure.

5. Run Code Analysis Report - The pylint commands is run to get a report on code quality `pylint src --output-format=text >> pylint_report.txt` the output is redirected to a file for upload later. A second command is run to output the file into the console `cat pylint_report.txt`

6. Publish Code Analysis Report - The report by pylint gets added as an artefact on azure.

7. Build Python App - The python app gets built using `python -m compileall .`

8. The files are then copied and added to azure as an artefact.

![Screenshot build stage](/images/Build.png)

## **Security Checks Stage**

 1. First the pipeline will checkout the repo.
 2. Gitleaks secret scan - Gitleaks runs and checks the repo for any keys or credentials that may cause a security risk. It creates a report and publishes it as an artefact on Azure.
 3. OWASP Dependency Check - This task scans the dependencies of the project for any security issues. It uses a NVD API Key for keeping the database of dependencies up to date.

![Screenshot security checks stage](/images/Security_Tests.png)

## **Deploy to Staging Stage**

 1. First the build artefact from the build stage is downloaded.
 2. Chrome is installed for the Selenium Tests.
 3. Start Web Server - A script runs which goes to the directory of the build artefact creates a virtual environment called "venv". Activates the venv. Then it updates pip and installs all the requirements. It will then start-up the application using guicorn at a localhost with port 5000. Lastly it sleeps (waits) for five seconds to give the application time to start-up.
 4. Run Selenium Tests - Another script runs which goes to the directory again and activates the venv. It then runs the Selenium UAT tests using pytest and creates a report.
 5. Publish UAT Result - The tests are published on Azure.
 6. Run Performance Tests - Another script runs which goes to the directory again and activates the venv. It then runs the performance tests using locust.
 7. Publish Performance Report - The report gets published to Azure.

![Screenshot deploy staging stage](/images/Deploy_Staging.png)


## **Deploy Production Stage**
This stage only runs if the pipeline was triggered on the main branch.
It does so using the code below:

    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))

This checks if the branch name is "main".

 1. If the branch is main, it downloads the build artefact from the build stage
 2. Deploy Production Web Server - It then runs a script to download the requirements and deploy the web app simulating a live production environment. 

![Screenshot deploy live stage](/images/Deploy_Live.png)

 
## Branch Policies and Protection

The main branch is protected by rules setup on GitHub.

  

1. PR Required - A pull request is required to merge to the main branch.

2. CI Pass - The CI pipeline on Azure needs to pass before merging.

3. Review Required - The PR needs to be reviewed before it can be approved. (Since there isn't some else working on this project I have to skip this rule)
4. Production Approval - Deploying to the production environment requires approval

  

## Testing Strategy

### Unit Tests
I use Pytest for for running the unit tests.
1. I created a .coveragerc file to setup exclusions so `__init__.py` files aren't included since they can dilute the code coverage score since they always give a 100% score since they are empty.

2. I enforce a 80% coverage score for the pipeline to pass.

3. If one test fails the entire pipeline fails.

### UAT Testing

 I use Selenium for the UAT testing. There is a UAT folder in the tests folder that contains the Selenium tests. All tests need to pass for the pipeline to continue.

![Screenshot uats tests](/images/UAT_Tests.png)


### Performance Testing
I use locust for performance testing. There is a locust file in the tests folder. Its a relatively simple setup for performance testing since there is only one route for the application, and one form that can run all the calculator's functions. 

![Screenshot performance tests](/images/Locust_Tests.png)

### Security Testing
I used Gitleaks for checking if there are any key or credentials in the repo.
I use OWASP to scan and check the dependencies of the project for any security risks.

![Screenshot securit tests](/images/Security_Tests.png)


# Flask
There is an app.py file in the root of the project which creates the route for the web app. It links the calculator function with a HTML template in the templates folder. This template maps all the fields and creates a form that the user can submit calculations to. On submit it posts to the route created in the app.py file. This file then run the correct calculator function and returns the result to be displayed on the page.

# Troubleshooting and Extra Points
## Pywin32
For locust to run it downloads a dependency called pywin32. The issue is the azure pipeline runs in ubuntu and does not support this module. The solution is to edit the module line in the requirements.txt file to only be included on windows. This can be achieved using the code below.

    pywin32==311; sys_platform ==  'win32'
    
Adding this to requirements ensures you can test the project locally but it also works in the azure pipeline.
![Screenshot requirements](/images/Requirements.png)


## All Selenium or Locust Tests fail
If all the Selenium or Locust tests fail its probably one of two reasons.

 1. The application isn't running. Unlike unit tests these two tests require the application to be running. In a separate terminal run `flask run`. The in a different terminal then run the tests.
 2. The application is running on a different address to the one Selenium and Locust is looking for. The application should be running on `localhost:5000 or 127.0.0.1:5000`. You can force flask to run on a specific host and port with this ` flask run -h localhost -p 5000`

## Locust Test wont run in pipeline
While testing I noticed an issue where pip installing modules from the requirements.txt file was inconsistent. Sometimes it would log that the module was already installed yet when running the locust tests it would say the module was missing. The solution was to create a virtual environment with python and install all the dependencies there.

     python3 -m venv venv # Creates virtual enviorement
     source venv/bin/activate # Activates the virtual enviorement

![Screenshot venv created](/images/VENV_Created.png)

Its important that the venv is activated or modules wont be installed to it and modules installed to it wont be accessible to the script without the venv running.

 ![Screenshot venv used](/images/VENV_Used.png)




