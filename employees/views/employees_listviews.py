from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from employees.models import Employee


class EmployeeListsView(View):
    """
    View will display a list of search results if a search
    was performed or just render a list of all employees if
    no search was performed.

    This is accomplished through the HTTP Verbs POST and GET.
    """
    template = 'employees.html'
    token = None
    user_name = None

    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch method is responsible for checking
        if the user is authenticated and setting up
        initial values .
        """
        if 'token' not in request.session:
            return HttpResponseRedirect('/login/')
        self.token = request.session['token']
        self.user_name = request.session['user_name']
        return super(EmployeeListsView, self).dispatch(
            request, *args, **kwargs
        )

    def get(self, request):
        """
        Will only respond to ALL GET requests and
        return a list of all employees.
        """

        try:
            # attempt to create a new user by authenticating against the API
            employee = Employee(token=self.token)
            employees = employee.objects.filter(ordering="user__first_name")
            return render(
                request,
                self.template,
                {
                    'employees': employees,
                    'user_name': self.user_name,
                    'page_title': 'All Employees'
                }
            )
        except Exception as ex:
            return HttpResponseRedirect('/dashboard')

        return HttpResponseRedirect('/dashboard')

    def post(self, request):
        """
        Will only respond to POST requests containing
        an email address to search employees.

        We're checking for q because the users can to this
        endpoint because they've searched for an email address
        stored in q. If no email was sent - go back to dashboard.

        This logic should be improved to provide a validation error
        message to the user.
        """
        if 'q' not in request.POST.keys():
            return Http404()
        try:
            # attempt to create a new user by authenticating against the API
            employee = Employee(token=self.token)
            employees = employee.objects.filter(
                email__contains=request.POST.get('q')
            )
            return render(
                request, self.template,
                {
                    'employees': employees,
                    'user_name': self.user_name,
                    'page_title': 'Employee Search Results'
                }
            )
        except Exception as ex:
            return HttpResponseRedirect('/dashboard')

        return HttpResponseRedirect('/dashboard')
