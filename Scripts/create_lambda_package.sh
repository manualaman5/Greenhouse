#!/bin/bash
set -xv

cd ..
BASEDIR=$(pwd)

rm -rf $BASEDIR/lambda_package.zip

#cd  $BASEDIR/lambda_v2/virtualenv/lib/python3.7/site-packages/
#zip -r9 $BASEDIR/lambda_package.zip *
cd  $BASEDIR/lambda/virtualenv/lib/python3.7/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *

#cd $BASEDIR/lambda_v2/virtualenv/lib64/python3.7/site-packages/
#zip -r9 $BASEDIR/lambda_package.zip *
cd $BASEDIR/lambda/virtualenv/lib64/python3.7/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *

#cd $BASEDIR/lambda_v2
#zip -g $BASEDIR/lambda_package.zip test_lambda.py
#zip -g $BASEDIR/lambda_package.zip language_strings.json
#zip -g $BASEDIR/lambda_package.zip prompts.py
#zip -g $BASEDIR/lambda_package.zip my_functions.py
cd $BASEDIR/lambda
zip -g $BASEDIR/lambda_package.zip *.py
zip -g $BASEDIR/lambda_package.zip language_strings.json
