from django.conf import settings
from django.test import TestCase
from tangent_core.model_facade import ModelFacade
from tangent_core.api_manager import ModelObject


"""
    MockedHttpTransport will mock the requests library so we can test in isolation
"""
class MockedHttpTransport(object):
    def __init__(self, mocked_routes):
        self.mocked_routes = mocked_routes

    def get_mocked_json(route):
        return self.mocked_routes[route]

    def get(self, *args, **kwargs):
        self.mocked_data = self.mocked_routes[args[0]]
        return self

    def post(self, *args, **kwargs):
        self.mocked_data = self.mocked_routes[args[0]]
        return self

    def json(self):
        return self.mocked_data


class MockedModel(ModelFacade):
    pass


class APITestCase(TestCase):

    # instatiate model with fake http transporter
    def setUp(self):
        self.api_endpoint = settings.REST_API_ENDPOINT_URL

        """ 
            we'll fake the actual HTTP trip as we're not testing the network
            but rather just testing that our API manager's query interface.
        """
        mocked_routes = {
            "%s/api-token-auth/" % (self.api_endpoint) : {'token' :  '1234'},
            "%s/api/employee/me/" % (self.api_endpoint) : {'username': 'kevin'},
            "%s/api/employee/?department=2" % self.api_endpoint : [
                {'username': 'kevin'},
                {'username': 'kevin'}
            ]
        }

        # create our Mocked model
        self.model = MockedModel(
            username='kevin',
            password='kevin',
            transport=MockedHttpTransport(mocked_routes)
        )
        
    # test get my profile
    def test_api_get_me(self):
        me = self.model.objects.me()
        self.assertEqual(me.username , 'kevin')

    # test get token
    def test_api_get_token(self):
        self.assertEqual(self.model.objects.get_token() , '1234')

    # test getting a collection of objects 
    def test_api_get_collection(self):
        employees = self.model.objects.filter(department=2)
        for emp in employees:
            self.assertEqual(emp.username, 'kevin')

    # testing that model object converts a dict to object correctly
    def test_model_object(self):
        test_data = {'name': 'kevin', 'surname': 'naidoo'}

        m = ModelObject(test_data)
        self.assertEqual(m.name , 'kevin')
        self.assertEqual(m.surname, 'naidoo')

        # test more complex dict
        test_data = {'user': {'name': 'kevin', 'surname': 'naidoo'} }
        m = ModelObject(test_data)
        self.assertEqual(m.user.name , 'kevin')
        self.assertEqual(m.user.surname, 'naidoo')
