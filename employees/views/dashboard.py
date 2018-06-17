# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from employees.models import Employee, RACE_GROUPS

"""
    As the name suggests , this view is responsible
    for rendering the apps dashboard.

    NOTE: I noticed when querying the API limiting doesn't
    work as expected so this logic assumes only one page of
    results is returned.
"""
class DashboardView(ListView):

    template_name = 'app.html'
    token = None
    user_name = None

    """
        The dispatch method is responsible for checking 
        if the user is authenticated and setting up
        initial values .
    """
    def dispatch(self, request, *args, **kwargs):
        if 'token' not in request.session:
            return HttpResponseRedirect('/login/')
        self.token = request.session['token']
        self.user_name = request.session['user_name']
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    """
        This is being set to a blank list since we're not using django's
        default ORM models and therefore need to define a custom method
        to set context data.
    """
    def get_queryset(self):
        return []

    """
        Query the rest API and find the relevant stats we need
        to populate the dashboard.
    """
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        EmployeeAPI = Employee(token=self.token)

        context['user_name'] = self.user_name
        context['birthdays'] = EmployeeAPI.objects.filter(ordering="-birth_date")

        # position__sort doesn't seem to work too well
        context['positions'] = EmployeeAPI.objects.filter(ordering="-position")

        # all employees 
        # Generator will discard values after iteracting through them so list this to reuse
        context['employees'] = list(EmployeeAPI.objects.filter(ordering="-user__first_name"))

        # calculate race groups
        race_groups = {} 
        for emp in context['employees']:
            race = RACE_GROUPS[emp.race]
            if race in race_groups.keys():
                race_groups[race] += 1
            else:
                race_groups[race] = 1

        # sort by lowest to highest
        context['race_groups'] =  OrderedDict(
            sorted(race_groups.items(), key=lambda k: k[1])
        )

        # calculate genders
        genders = {'Male' : 0 , 'Female': 0} 

        for emp in context['employees']:
            gender = 'Male' if emp.gender == 'M' else 'Female'
            genders[gender] += 1

        # sort by lowest to highest
        context['genders'] =  OrderedDict(
            sorted(genders.items(), key=lambda k: k[1])
        )
        return context