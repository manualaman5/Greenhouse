#!/bin/sh
set -xv

cd Scripts/

bash create_lambda_package.sh
bash update_function.sh
