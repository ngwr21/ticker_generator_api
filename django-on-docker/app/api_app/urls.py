from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'api_app'

urlpatterns = [
    # path('checks/', views.check_list),
    path('admin/', admin.site.urls),
    path('checks/create/<str:api_key>/', create_check, name='create_check'),
    # path('checks/generate_pdf/<str:api_key>/<int:check_id>/', generate_pdf, name='generate_pdf'),
    path('checks/download_pdf/<str:api_key>/<int:check_id>/', download_pdf, name='download_pdf'),
    path('<str:api_key>/list_checks/', list_checks, name='list_checks'),
]
    # path('api-auth/', include('rest_framework.urls')),


