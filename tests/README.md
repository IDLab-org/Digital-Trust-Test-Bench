# DTT-Frontend test

### test files organisation / creation
The test files and name it test_functiontestedname and must be located under Test/test_files/

test_utilities contain function that can be used in your files, you can refere to test_githublogin the use of the web driver and test function


### Create Docker image
``` docker build -t testenvironment ./tests ```


### Run the application
``` docker run -p 8000:8000 -it testenvironment ```


### Test report
```allure server url: 127.0.0.1:8000 ```