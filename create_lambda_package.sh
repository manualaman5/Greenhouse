#!/bin/bash
BASEDIR=$(pwd)

rm -rf $BASEDIR/lambda_package.zip
cd  $BASEDIR/lambda/testenv/lib/python3.6/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *
cd $BASEDIR/lambda/testenv/lib64/python3.6/site-packages/
zip -r9 $BASEDIR/lambda_package.zip *
cd $BASEDIR/lambda

zip -r9 $BASEDIR/lambda_package.zip test_lambda.py
