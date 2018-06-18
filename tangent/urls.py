
from django.conf.urls import url
from employees.views import DashboardView
from employees.views import LoginView, LogoutView
from employees.views import EmployeeListsView
from employees.views import ProfileView

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'logout/', LogoutView.as_view()),
    url(r'employees/', EmployeeListsView.as_view()),
    url(r'employees/search/', EmployeeListsView.as_view()),
    url(r'profile/', ProfileView.as_view()),
    url(r'', DashboardView.as_view())
]
