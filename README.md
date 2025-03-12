# FastAPI Setup and Testing Instructions

Follow the steps below to set up and test the FastAPI application with authentication.

### Step 1: Create a `.env` file
Create a `.env` file in the root of your project to store environment variables.

### Step 2: Install Dependencies
Run the following command to install all required dependencies:
run `pip install -r requirements.txt`

### Step 3:  Start the FastAPI Application
Start the FastAPI server with:
run `uvicorn main:app --reload ` to start the project


### Step 4: Test the Application
#### Test the Root Endpoint
navigate to `curl http://127.0.0.1:8000` 

#### Test the Protected Endpoint
if the above is working 
navigate to `curl http://127.0.0.1:8000/protected` 
the above should give you a 403
#### Login and Get an Access Token
navigate to `curl http://127.0.0.1:8000/login`  to get the access token, <your-valid-token>
The username and password are for a user already in the userpool for test

#### Step 6: Access the Protected Endpoint with the Access Token
then `curl -H "Authorization: Bearer <your-valid-token>" http://127.0.0.1:8000/protected`
you should be able to gain access