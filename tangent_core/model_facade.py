from tangent_core.api_manager import API_Manager
import json


class ModelFacade(object):
    """
    To provide a consisten API for our models to work similar
    to Django's built in ORM This Facade will manage all classes
    to achieve this and provide.

    :param string username: the API username
    :param string password: the unhashed API password
    """
    """
    We now bind the objects property to our API model
    so that we can perform queries like :
    self.objects.filter(*kwargs)
    """
    def __init__(
        self,
        token=None,
        username=None,
        password=None,
        transport=None
    ):
        self.objects = API_Manager(
            self.__class__.__name__.lower(),
            token=token,
            username=username,
            password=password,
            transport=transport
        )

    def rebuild_manager(
        self,
        token=None,
        username=None,
        password=None,
        transport=None
    ):
        """
        Future proofing - at some point we may need to re-use
        an existing model object after the token as expired
        or something to that effect - so use this method to
        recreate the model manager.
        """
        self.objects = API_Manager(
            self.__class__.__name__.lower(),
            token=token,
            username=username,
            password=password,
            transport=transport
        )
