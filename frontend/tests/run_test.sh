#!/bin/bash

# Run pytest and create Allure results
pytest --alluredir=allure_results

# Generate and open Allure report
allure serve -p 8000 allure_results
