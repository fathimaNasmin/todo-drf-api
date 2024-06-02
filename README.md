# TODO API - Django Restframework

A simple Todo application built with Django and Django REST Framework. This API allows users to manage their todo tasks by performing CRUD operations (Create, Read, Update, Delete).

##### Try out [On Live](https://tododrfapi-1224185575bf.herokuapp.com/api/docs/).

### Features
- User authentication and registration
- Create, view, update, and delete tasks
- Task completion status
- Swagger API documentation for easy exploration

### Requirements 
- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

### Installation
1. ##### Clone the Repository
    ```git clone https://github.com/fathimaNasmin/todo-drf-api.git```
  
2. ##### Create a virtual environment
   ```python -m venv venv```
   
   ###### For mac/linux
   ```source venv/bin/activate```

   ###### For windows 
    ```venv\Scripts\activate```
   
4. ##### Install the dependencies
   ```pip install -r requirements.txt```
   
6. ##### Run migrations
   ```python manage.py migrate```
   
8. ##### Create a superuser
    ```python manage.py createsuperuser```
   
10. ##### Run the development server
    ```python manage.py runserver```

### API Documentation
The API documentation is available via Swagger. You can access it by navigating to the following URL once the server is running:

```http://localhost:8000/api/docs/```

This interactive documentation allows you to explore the API endpoints and test them directly from the browser.

### Contact
If you have any questions or feedback, feel free to reach out to me at fathimanesmi@gmail.com.
