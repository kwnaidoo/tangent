from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from employees.models import Employee


class ProfileView(View):
    """
    View will fetch and display the current
    users profile data.
    """
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
        return super(ProfileView, self).dispatch(
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
            profile = employee.objects.me()
            return render(
                request,
                'profile.html',
                {
                    'profile': profile,
                    'user_name': self.user_name,
                    'page_title': 'My Profile'
                }
            )
        except Exception as ex:
            return HttpResponseRedirect('/dashboard')

        return HttpResponseRedirect('/dashboard')
