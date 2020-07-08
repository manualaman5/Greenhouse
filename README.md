Hi!

In order to have a own-hosted Alexa skill, you will need to set up the front end [Named Link](https://developer.amazon.com/es-ES/alexa "here"). The back end is going to be hosted in AWS Lambda. 

Make sure that you have:

Correct intents in your front end.
The front end and the back end are connected using ARN AWS.
Configured your account in the AWS CLI.
Updated the Scipts/Update_function.sh so it updates your Lambda function.


Follow the steps to get your code up and running:

1.Create the package:
  mkdir lambda cd lambda
  #Create the virtual env
  python3 -m venv testenv
  source testenv/bin/activate
  pip install requirements.txt
  deactivate
  touch test_lambda.py
  cd ..
  touch create_lambda_package.sh
  bash -x create_lambda_package.sh

2.Use the script Update_function.sh to update the function in your lambda:
  bash Update_function.sh

3.Make the connection between your front end and the lambda function
4.Make sure that you build the model in the front end
