"""
    We import these here so that we can maintain a
    consistent import structure .e.g.
    from employees.views import DashboardView , even
    though these views are seperated into their own files.

    I decided to sperated views because it makes them extendible
    for future we can easily add on features or adjust current features.
"""
from dashboard import DashboardView
from auth import LoginView, LogoutView
from employees_listviews import EmployeeListsView
from profile import ProfileView
