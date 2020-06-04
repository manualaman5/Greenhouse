#!/bin/bash
BASEDIR=$(pwd)

rm -rf $BASEDIR/lambda_package.zip

cd  $BASEDIR/lambda_v2/virtualenv/lib/python3.7/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *

cd $BASEDIR/lambda_v2/virtualenv/lib64/python3.7/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *

cd $BASEDIR/lambda_v2
zip -g $BASEDIR/lambda_package.zip test_lambda.py

#Update lambda function
cd $BASEDIR
aws lambda update-function-code --function-name pythontest --zip-file fileb://lambda_package.zip
