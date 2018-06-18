from django.conf import settings
from tangent_core import api_logger
import urllib
import requests


class ModelObject(object):
    """
    ModelObject is a simple class we're going to use as a container
    for our JSON data , so everytime we query the API and get JSON
    back we're going to convert that JSON into an object.
    """

    def __init__(self, response_data):
        """
        We'll take the dictionary and set dynamic properties on this
        instance of ModelObject.
        Args:
            response_data (dict) : a dictionary comming
            from response.json()
        """
        try:
            for k, v in response_data.items():
                if type(v) is dict:
                    v = ModelObject(v)
                setattr(self, k, v)
        except Exception as ex:
            api_logger.warning(ex)
            raise('Data provided is not valid JSON.')


class API_Manager(object):
    """
    API Manager Adapter class
    This class will take care of all the interactions with the rest API
    endpoint as per this assignments requirement. The goal is to write
    an adapter to allow for upper level code to consistently interact with
    the API without knowing that it's a JSON API.

    This makes the code more robust and enables for swapping
    out the manager in future.

    I have also made the code adaptable to use any kind of
    HTTP requests library ,I prefer python requests but it's
    possible to easily swap this out for a custom written
    one or something like urllib.
    """

    def __init__(
        self, resource_name,
        token=None, username=None,
        password=None, transport=None
    ):

        """
        Will setup core properties needed by the adapter
        throughout it's processing.
        :param string username: the API username
        :param string password: the unhashed API password
        :param object transport: Specify a different HTTP request handler ,
        defaults to requests

        :raises Exception:
           Will throw and exception if username and password not
           sent to method.Will throw an exception if the
           API authentication fails.
        """
        # will keep track of our authentication headers
        self.token = None
        self.headers = {}

        self.api_endpoint = settings.REST_API_ENDPOINT_URL

        # set the HTTP transportation library to use
        self.transport = transport

        # The name of the API Resource we'll be interacting with.
        self.api_name = resource_name

        # if we already have a token , just set it and don't re-authenticate
        if token is not None:
            self.token = token
            self.headers['Authorization'] = 'Token %s' % self.token

        elif username is None or password is None:
            """
            if no token , username and password present then we can't
            access the API so throw an exception.
            """
            raise("Login credentials provided are invalid.")
        else:
            """
            In a production grade application - we'd probably want to use
            environment vars but for the purposes of this assignment I'm
            not overcomplicating this.
            """
            self.api_username = username
            self.api_password = password
            self.authenticate()  # Authenticate right away and get a token

    def get_token(self):
        """
        Get token - will check return if there's a session token set
        or not. Usefull to test if the user is logged in or not.

        :return: Will return a token or none

        :rtype None | token hash

        """
        return self.token

    def get_transport(self):
        """
        A bit of IOC magic - Will return python request
        as our transport mechanism if no transport object is passed
        to this class.

        This allows for more advanced HTTP querying on the fly
        without just tieing us down to using one library.

        :return: Will return a HTTP transport object
        :rtype: Object
        """
        return self.transport if self.transport else requests

    def authenticate(self):
        """
        Will poll the rest framework backend API to retrieve a token.
        :raises Exception: Will throw an exception if the API
        authentication fails.
        """

        # build the API endpoint URL
        api_endpoint = "%s/api-token-auth/" % (self.api_endpoint)

        # query API to get a token
        try:
            response = self.get_transport().post(
                api_endpoint,
                {
                    'username': self.api_username,
                    'password': self.api_password
                }
            ).json()
            self.token = response['token']
            self.headers['Authorization'] = 'Token %s' % self.token

        except Exception as ex:
            api_logger.warning(ex)
            # provide a more user friendly error
            raise Exception("Login credentials provided are invalid.")

    def me(self):
        """
        Queries API to get current logged in users profile.

        :return: Will return a Instance of ModelObject.
        :rtype: ModelObject
        :raises Exception: User not found or failed to access that user.
        """

        # build api endpoint
        api_endpoint = "%s/api/employee/me/" % (self.api_endpoint)
        headers = self.headers

        # query API to user profile
        try:
            me = self.get_transport().get(
                api_endpoint,
                headers=headers
            ).json()

            # Create instance of ModelObject and fill will JSON data from API
            return ModelObject(me)

        except Exception as ex:
            api_logger.warning(ex)
            raise Exception('User not found or failed to access that user.')

    def filter(self, **kwargs):
        """
        Dynamic querying interface to filter our API results.

        :return: Will return a generator.
        :rtype: Generator
        :raises Exception: will return blank generator.
        """

        try:
            # build API endpoint and GET querystring and grab headers
            query_string = urllib.urlencode(kwargs)
            api_endpoint = "%s/api/employee/?%s" % (
                self.api_endpoint,
                query_string
            )
            headers = self.headers

            # Now query the API for all employees matching filter arguments
            employees = self.get_transport().get(
                api_endpoint,
                headers=headers
            ).json()

            for employee in employees:
                yield ModelObject(employee)

        except Exception as ex:
            api_logger.warning(ex)
            """
            We're within a generator so simply return a blank generator,
            possibly can look at generating an exception but any
            empty collection would indicate that the query failed
            or didn't yield results.
            """
            yield iter(())
