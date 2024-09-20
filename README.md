# WealthWallet-template 
WealthWallet APP

VERSIONS:

PYTHON 3.11

Prerequisites:
1. Make sure you have PostgreSQL and Redis installed on your machine

2. Create a database that you will copy the name and user to replace on the .env

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

4. **Copy contents of `.env.example` to your `.env` file and replace them with the respective details**
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


To view API endpoints:
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
   
   Open your terminal in the project’s root folder and create a superuser. This user can view transactions and link accounts to specific users.

   ```bash
   python manage.py createsuperuser

2. **Obtain Token as SuperUSer**
   
   Open Postman, and use the login credentials entered above to obtain the token. Just so you know, all logins would only work on Postman since Swagger is currently blocked by the Authentication library currently being used.

   <img width="908" alt="Screenshot 2024-09-20 at 15 24 37" src="https://github.com/user-attachments/assets/9c3fc7b6-fbe3-4d52-a693-e315c5c12396">

3. **Attach Token to continue using swagger**
   
   Go to the swagger docs and paste the token with the prefix "token XXXXXXXXXXXXXXX".

  ![Screenshot 2024-09-20 at 15 27 27](https://github.com/user-attachments/assets/bee7b8a6-c3de-4732-9344-747aa5a4d89d)



