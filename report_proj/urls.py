# myproject/urls.py (replace 'myproject' with the name of your project directory)
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('report_proj.myapp.url')),  # Include the app's URLs
]
