#Update the lambda function
aws lambda update-function-code --function-name pythontest --zip-file fileb://../lambda_package.zip
