from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

from employees.models import Employee


"""
    Will be responsible for reading the post form data 
    and attempting to authenticate this user via the REST
    API.
"""

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # attempt to create a new user by authenticating against the API
            employee = Employee(username=username, password=password)

            # if the API failed for whatever reason get_token will be blank
            token = employee.objects.get_token()
            if token:
                request.session['token'] = token
                me = employee.objects.me()
                request.session['user_name'] = "%s %s" % (me.user.first_name , me.user.last_name)
        except Exception as ex:
            return HttpResponseRedirect('/login')

        return HttpResponseRedirect('/')

"""
    Will be responsible for clearing out the logged In
    user's session.
"""
class LogoutView(View):
    def get(self, request):
        if 'token' in request.session:
            del request.session['token']
            del request.session['user_name']
        return HttpResponseRedirect('/login')