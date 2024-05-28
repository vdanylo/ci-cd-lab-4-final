from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.contrib.auth import views as auth_views

from core.forms import LoginForm
from core.views import contact, index, signup

urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("admin/", admin.site.urls),
    path("items/", include("item.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("orders/", include("order.urls")),
    path("cart/", include("cart.urls"), name="cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
