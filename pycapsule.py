import requests


class PyCapsuleObject():
    """
    Data object to be returned by PyCapsuleObjectManager.
    Has functionality to update, delete, retrieve tags,
    add opportunities, and cases.
    """
    def __init__(self, **kwargs):
        pass

    def delete(self):
        """
        Deletes the object from Capsule CRM
        """
        pass

    def update(self, data):
        """
        Updates the object on Capsule CRM.
        
        Args:
            data (json/xml): data to update Capsule object
            data_type(str): the type of data that you're sending
        """
        pass

    def tags(self):
        """
        Returns:
            list: list of tags on the object
        """
        pass
    
    def opportunities(self):
        """
        Returns:
            object: PyCapsuleObjectManager for this object's opportunities
        """
        pass

    def cases(self):
        """
        Returns:
            object: PyCapsuleObjectManager for this object's opportunities
        """
        pass


class PyCapsuleObjectManager():
    """
    Object Manager for PyCapsule objects. Can add and retrieve
    Capsule CRM objects.
    
    Args:
        pycapsule (object): PyCapsule object to pass on API key and other
            information
        endpoint (str): CapsuleCRM endpoint ex. party, organisation, person

    """
    
    xml_headers = {'Content-Type': 'application/xml',
                'Accept': 'text/xml'}
    json_headers = {'Content-Type:': 'application/json',
                'Accept': 'text/json'}

    def __init__(self, pycapsule, endpoint, **kwargs):
        self.endpoint = endpoint
        if hasattr(pycapsule, 'pycapsule'):
            self.pycapsule = pycapsule.pycapsule
        else:
            self.pycapsule = pycapsule

    def add(self, data, data_type, return_type=None):
        """
        Add a new object of this type to Capsule CRM.

        Args:
            data (xml, json): data to be sent to CRM API
            data_type (str): format of data being sent ex. json or xml

        Kwargs:
            return_type (optional[str]): Desired format of data to be received
                ex. xml or object. If None is provided, defaults to xml

        Returns:
            object/xml: if xml is specificied in return_type returns xml
                as received from API, otherwise returns a PyCapsuleRequest
                object

        Example:
            PyCapsule.parties.add('filename.xml', 'xml', return_type='object')
        """
    def get(self, return_type=None, capsule_id=None):
        """
        Get Capsule CRM object by id.

        Kwargs:
            return_type (optional[str]): Desired format of data to be received
            capsule_id (int): Capsule CRM ID of the target object.

        Returns:
            object/xml: Returns object with functionality if no return_type
                is specified, otherwise returns the specified data type
        """
        pass

    def filter(self, return_type=None, **kwargs):
        """
        Get Capsule CRM objects matching kwargs.

        Kwargs:
            return_type (optional[str]): Desired format of data to be received
            additional kwargs may be provided to match available filters

        Returns:
            list/xml: Returns list of PyCapsuleObjects if return_type
                not specified
        """
        pass

    def all(self, return_type=None):
        """
        Retrieve all Capsule CRM objects of the manager's type.

        Returns:
            list/xml: Returns list of PyCapsuleObjects if return_type
                is not specified.
        """
        pass


class PyCapsule():
    """
    PyCapsule model handles the adding, updating, and deleting of
    of Capsule CRM API objects.

    Args:
        base_url (str): base for capsulecrm url. ex. name in https://name.capsulecrm.com
        api_key (str): API key received from My Preferences on Capsule CRM
    """

    def __init__(self, base_url, api_key):
        self.base_url = "https://%s.capsulecrm.com/api/" % base_url
        self.api_key = (api_key, "x")
    
    @property
    def parties(self):
        """
        Returns:
            object:object manager for all parties. This includes people and 
                organisations.

        """
        return PyCapsuleObjectManager(self,)

    @property
    def opportunities(self):
        """
        Returns:
            object: object manager for all opportunities.
        """
        pass

    @property
    def cases(self):
        """
        Returns:
            object: object manager for all cases.
        """
        pass

    @property
    def history(self):
        """
        Returns:
            object: object manager for history.
        """
        pass

    @property
    def tasks(self):
        """
        Returns:
            object: object manager for tasks.
        """
        pass

    @property
    def tracks(self):
        """
        Returns:
            object: object manager for tracks.
        """

    @property
    def users(self):
        """
        Returns:
            object: object manager for users.
        """
        pass

    @property
    def countries(self):
        """
        Returns:
            list: a list of all available countries in Capsule CRM.
        """
        pass

    @property
    def currencies(self):
        """
        Returns:
            list: list of string values of available currencies on CapsuleCRM
            """
        pass
