from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("cancel/<int:pk>", views.cancel, name='cancel'),
    path("", views.index, name='index'),
    path("check", views.checkout, name='checkout'),
    path("payment/<int:pk>/", views.payment, name='payment'),
    path("<int:pk>/", views.detail, name='detail')
]