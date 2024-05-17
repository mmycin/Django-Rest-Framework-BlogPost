# Setting up the Project
### Create a Project

Firstly install some python libraries:
```bash
$ pip install django djangorestframework
```

Now create a Django project and create an API app:
```bash
$ django-admin startproject mysite
$ cd mysite
$ python manage.py startapp api
```

### Folder Structure: 

Now the root folder should look like this:
```
└── 📁mysite
    └── 📁api
        └── admin.py
        └── apps.py
        └── 📁migrations
        └── models.py
        └── tests.py
        └── views.py
    └── manage.py
    └── 📁mysite
        └── asgi.py
        └── settings.py
        └── urls.py
        └── wsgi.py
```
 Now run the server:
 ```bash
 $ python manage.py runserver
```

### Initialize Git Repository

Add this project to a Git Repository:
```git 
$ git init
$ git add .
$ git status
$ git commit -m "Initial commit"
```

Now make a new repository on your GitHub named *Django-Rest-Framework-BlogPost* and push the directory to the repository:
```git
$ git remote add origin https://github.com/$$USERNAME$$/Django-Rest-Framework-BlogPost.git
$ git push -u master
```

### Connect the API to the App

Head over to `mysite/settings.py` and update the`INSTALLED_APPS` list:
```diff 
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
+    "api",
+   "rest_framework"
]
```

Also you can update `ALLOWED_HOSTS` if you want to add frontend to access the API:
```diff
- ALLOWED_HOSTS = []
+ ALLOWED_HOSTS = ["*"]
```

Now create a `urls.py` file into the `api/` directory (`/api/urls.py`) and write the following code:
```python 
from django.urls import path
from . import views

urlpatterns = [
]
```

Now to connect it to the main app, go to the `mysite/urls.py` and update the following block:
``` diff
- from django.contrib import admin
- from django.urls import path
+ from django.urls import path, include

urlpatterns = [
-    path("admin/", admin.site.urls),
+    path("api/", include("api.urls"))
]
```

# Build the App
### Create Models

Head over to `api/models.py` and write the following code to make a database model containing Blog Posts.
```python
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

Now time to migrate the *Sqlite3* database:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create a Serializer

Create a `serializers.py` in the `api/` directory and write the following code: 
```python
from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "created_at"]
```

### Create the Views

Now move to the `views.py` file and add the following code:
```python 
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer

# Create Blog Posts
class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    def delete(self, request, *args, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Update and delete Blog Posts
class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk" # pk means primary key
```

### Set up the Routes

Now update the `api/urls/py` with the following lines: 
```python 
urlpatterns = [
    path(
    "blogs", 
    view=views.BlogPostListCreate.as_view(), 
    name="blog-view-create"
    ),
    path(
        "blogs/<int:pk>",
        view=views.BlogPostRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
]
```

# Testing the App
### Commit and Run

Commit the changes to Git and GitHub 
```git
$ git add .
$ git commit -m "Edited files"
$ git push
```

Now run the server and open *`http://localhost:8000/api/blogs/`* 

Now add some data to the database and test the API.

If you want to see the data in the *JSON* format. Click on `GET > json` and a new URL  *`(http://localhost:8000/api/blogs?format=json)`* will popup:
```json
[
  {
    "id": 7,
    "title": "Test 1",
    "content": "gbedrty,klk",
    "created_at": "2024-05-17T13:57:08.222521Z"
  },
  {
    "id": 8,
    "title": "Test 2",
    "content": "sdfhfgjhkjl",
    "created_at": "2024-05-17T13:57:14.565172Z"
  },
  {
    "id": 9,
    "title": "Test 3",
    "content": "sdfhfgjhkjlsghdfgjh",
    "created_at": "2024-05-17T13:57:19.228084Z"
  },
  {
    "id": 10,
    "title": "Test 4",
    "content": "sdfghj",
    "created_at": "2024-05-17T13:57:28.287965Z"
  }
]
```

To test the API from terminal, we can use *CURL* with the following command:
``` bash 
$ curl http://localhost:8000/api/blogs
[{"id":7,"title":"Test 1","content":"gbedrty,klk","created_at":"2024-05-17T13:57:08.222521Z"},{"id":8,"title":"Test 2","content":"sdfhfgjhkjl","created_at":"2024-05-17T13:57:14.565172Z"},{"id":9,"title":"Test 3","content":"sdfhfgjhkjlsghdfgjh","created_at":"2024-05-17T13:57:19.228084Z"},{"id":10,"title":"Test 4","content":"sdfghj","created_at":"2024-05-17T13:57:28.287965Z"}]
```


***Mycin***
