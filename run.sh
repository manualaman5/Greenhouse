#!/bin/sh
set -xv

if  [ ! -d lambda/virtualenv ];
then
  cd lambda/
  python3 -m venv virtualenv
  source virtualenv/bin/activate
  pip install requirements.txt
  deactivate
  cd ..
fi

cd Scripts/

bash create_lambda_package.sh
bash update_function.sh
