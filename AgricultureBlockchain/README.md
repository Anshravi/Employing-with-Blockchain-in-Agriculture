# Agriculture Blockchain Project

This is a Django web application demonstrating a conceptual integration with a simple blockchain for tracking agricultural products.

## Setup Instructions

**1. Python Version:**
   - **IMPORTANT:** This project requires **Python 3.8, 3.9, 3.10, or 3.11**. 
   - It uses Django 2.1.7, which is **incompatible** with Python 3.12 and newer due to removed standard library modules (`distutils`, `cgi`).
   - Ensure you have a compatible Python version installed and available in your PATH, or use a virtual environment manager (like `venv`, `conda`, `pyenv`) to manage your Python version.

**2. Environment Variables:**
   - Copy the example environment file:
     ```bash
     copy .env.example .env
     ```
   - **Edit the `.env` file:**
     - Set `SECRET_KEY`: Generate a strong random string for Django's security.
     - Set `ENCRYPTION_KEY`: Generate a secure 32-byte (64 hexadecimal characters) AES key. You can use the following command:
       ```bash
       python -c "import secrets; print(secrets.token_hex(32))"
       ```
     - **Do not commit the `.env` file to version control.**

**3. Install Dependencies & Run:**
   - Open your terminal or command prompt in the project's root directory.
   - Run the setup and execution script:
     ```bash
     .\run_project.bat 
     ```
   - This script will:
     - Check your Python version (advisory).
     - Check if `.env` exists.
     - Install required packages from `requirements.txt`.
     - Create `media` and `static` directories if they don't exist.
     - Attempt to collect static files.
     - Run database migrations.
     - Start the Django development server.

**4. Access the Application:**
   - Once the server starts, open your web browser and navigate to:
     [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Important Security Notes

- **Password Handling:** The current implementation stores and compares plaintext passwords within the blockchain transactions. **This is highly insecure.** For any real-world application, password hashing (e.g., using `django.contrib.auth.hashers`) MUST be implemented.
- **Blockchain Simulation:** The blockchain component is a simplified simulation for demonstration purposes. It lacks robust consensus mechanisms and networking found in production blockchains.
- **Encryption:** AES-CTR encryption is used, but ensure the `ENCRYPTION_KEY` in your `.env` file is kept secure. 