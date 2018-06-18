
from django.conf.urls import url
from employees.views import DashboardView
from employees.views import LoginView, LogoutView

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'logout/', LogoutView.as_view()),
    url(r'', DashboardView.as_view()),
]
