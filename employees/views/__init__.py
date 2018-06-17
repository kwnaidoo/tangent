"""
    We import these here so that we can maintain a
    consistent import structure .e.g.
    from employees.views import DashboardView , even
    though these views are seperated into their own files.
"""
from dashboard import DashboardView
from auth import LoginView, LogoutView