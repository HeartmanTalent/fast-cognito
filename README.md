# 🚀 FastAPI Setup & Cognito Test

Get your FastAPI application up and running with authentication in a few easy steps!

## 🛠️ Prerequisites

* Python 3.7+ installed
* `pip` package manager

## ⚙️ Setup

### 1. Create `.env` File

   * In the root directory of your project, create a file named `.env`.

### 2. Install Dependencies

   * Open your terminal and navigate to your project directory.
   * Run the following command to install all required packages:

     ```bash
     pip install -r requirements.txt
     ```

### 3. Start the FastAPI Application

   * Launch the FastAPI server using `uvicorn`:

     ```bash
     uvicorn main:app --reload
     ```

     * This command starts the server and enables automatic reloading for development.

## 🧪 Testing

### 4. Verify Root Endpoint

   * Open your terminal and make a request to the root endpoint:

     ```bash
     curl http://127.0.0.1:8000
     ```

   * You should receive a successful response, confirming the server is running.

### 5. Test Protected Endpoint (Initial Access Denied)

   * Attempt to access the protected endpoint without authentication:

     ```bash
     curl http://127.0.0.1:8000/protected
     ```

   * You should receive a `403 Forbidden` error, indicating that authentication is required.

### 6. Obtain an Access Token (Login)

   * Log in to obtain an access token. Ensure that there is a user in your user pool for testing.

     ```bash
     curl http://127.0.0.1:8000/login
     ```

   * The response will contain your `<access-token>`. Copy this token.

### 7. Access Protected Endpoint with Token

   * Use the obtained access token to access the protected endpoint:

     ```bash
     curl -H "Authorization: Bearer <access-token>" http://127.0.0.1:8000/protected
     ```

   * You should now receive a successful response, confirming that your token is valid and you have access to the protected resource.

## 🎉 Congratulations!

You have successfully set up and tested your FastAPI application with authentication.