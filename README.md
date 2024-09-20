# WealthWallet-template 
WealthWallet APP

VERSIONS:

PYTHON 3.11

Prerequisites:
1. Make sure you have postgresql and redis installed on your machine

2. Create a database that you will copy name and user to replace on the .env

How To Run:

1. **Create a virtual environment**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3. **Install all requirements from the `requirements.txt` file**
    ```bash
    pip install -r requirements.txt
    ```

4. **Copy contents of `.env.example` to your `.env` file and replace with the respective details**
    ```bash
    cp .env.example .env
    ```

5. **Run the server locally**
    ```bash
    python manage.py runserver
    ```

6. **Run migrations**
    ```bash
    python manage.py migrate
    ```


To view Api endpoints:
On Your browser enter to view swagger documentation.
 [127.0.0.1:8000/developer/docs](http://127.0.0.1:8000/developer/docs)

![Screenshot 2024-09-20 at 15 04 53](https://github.com/user-attachments/assets/1ea6c221-db84-402f-af18-2dd17836bb38)

To run tests:
    ```python manage.py test```

Or run specific app tests:
    ```python manage.py test app_name```


## How To Test Step-By-Step:

### ADMIN:

1. **Create a Superuser**
   
   Open your terminal in the project’s root folder and create a superuser. This user will have access to view transactions and link accounts to specific users.

   ```bash
   python manage.py createsuperuser
