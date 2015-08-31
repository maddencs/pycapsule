import requests


class PyCapsuleObject():
    """
    Data object to be returned by PyCapsuleObjectManager.
    Has functionality to update, delete, retrieve tags,
    add opportunities, and cases.

    Args:
        endpoint (str): Capsule CRM endpoint
    """
    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint
        self.pycapsule = manager.pycapsule
        self.location = pycapsule.location + self.endpoint + '/' + self.capsule_id

    def delete(self):
        """
        Deletes the object from Capsule CRM
        """
        r = requests.delete(self.location, auth=self.pycapsule.auth)
        if r.status_code == 200:
            return "Success"
        else:
            return "There was a problem deleting the object from Capsule CRM."

    def update(self, data=None, headers=None):
        """
        updates the object on capsule crm.
        
        args:
            data (json/xml): data to update capsule object
            data_type(str): the type of data that you're sending
        """
        if headers:
            headers = getattr(self.pycapsule, "%_headers" % headers)
        r = requests.put(self.location, auth=self.pycapsule.auth, data=data, headers=headers)
        if r.status_code != 200:
            return "There was a problem updating the object on Capsule CRM."

    def tags(self, headers=None):
        """
        returns:
            list: list of tags on the object
        """
        if headers:
            headers = getattr(self.pycapsule, "%_headers" % headers)
        r = requests.get(self.location + '/tag', auth=self.pycapsule.auth)
        return None

    def custom_fields(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's custom fields
        """
        return PyCapsuleObjectManager(self)

    
    def opportunities(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's opportunities
        """
        pass

    def cases(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's cases
        """
        pass

    def history(self):
        """
        returns:
            object: pycapsuleobjectmanager for object's history
        """
        pass

    def remove_contact(self, contact_id=None):
        url = self.location + '/contact/' + contact_id
        r = requests.delete(url, auth=self.pycapsule.auth)
        return r.status_code


class PyCapsuleObjectManager():
    """
    object manager for pycapsule objects. can add and retrieve
    capsule crm objects.
    
    args:
        pycapsule (object): pycapsule object to pass on api key and other
            information
        endpoint (str): capsulecrm endpoint ex. party, organisation, person

    """
    
    xml_headers = {'content-type': 'application/xml',
                'accept': 'text/xml'}
    json_headers = {'content-type:': 'application/json',
                'accept': 'text/json'}

    def __init__(self, pycapsule, endpoint, **kwargs):
        if hasattr(pycapsule, 'location'):
            self.endpoint = pycapsule.location + '/' + endpoint
        if hasattr(pycapsule, 'pycapsule'):
            self.pycapsule = pycapsule.pycapsule
        else:
            self.pycapsule = pycapsule

    def add(self, data, data_type=None, return_type=None, capsule_id=None):
        """
        add a new object of this type to capsule crm.

        Args:
            data (xml, json): data to be sent to crm api

        Kwargs:
            data_type (str): format of data being sent ex. json or xml
            return_type (optional[str]): desired format of data to be received
                ex. xml or object. if none is provided, defaults to xml

        Returns:
            object/xml: if xml is specificied in return_type returns xml
                as received from api, otherwise returns a pycapsulerequest
                object

        Example:
            pycapsule.parties.add('filename.xml', 'xml', return_type='object')
        """
        if data_type:
            headers = getattr(self.pycapsule, "%s_headers" % data_type)
        if capsule_id:
            url = self.endpoint + '/' + capsule_id
        else:
            url=self.endpoint
        r = requests.post(url, auth=self.pycapsule.auth, headers=headers)
        return r.location

    def get(self, return_type=None, capsule_id=None):
        """
        get capsule crm object by id.

        Kwargs:
            return_type (optional[str]): desired format of data to be received
            capsule_id (int): capsule crm id of the target object.

        Returns:
            object/xml: returns object with functionality if no return_type
                is specified, otherwise returns the specified data type
        """
        if return_type:
            headers = getattr(self.pycapsule, "%s_headers" % return_type)
        else:
            headers = None
        r.get(self.endpoint + '/%s' % capsule_id, auth=self.pycapsule.auth, headers=headers)
        return """Return data however it's specified"""

    def filter(self, return_type=None, **kwargs):
        """
        get capsule crm objects matching kwargs.

        kwargs:
            return_type (optional[str]): desired format of data to be received
                additional kwargs may be provided to match available filters

        returns:
            list/xml: returns list of pycapsuleobjects if return_type
                not specified
        """
        if return_type:
            headers = getattr(self.pycapsule, "%s_headers" % return_type)
        else:
            headers = None
        r = requests.get(self.endpoint, auth=self.pycapsule.auth, headers=headers, params=kwargs)
        return """Return data however specified"""

    def all(self, return_type=None):
        """
        retrieve all capsule crm objects of the manager's type.

        returns:
            list/xml: returns list of pycapsuleobjects if return_type
                is not specified.
        """
        if return_type:
            headers = getattr(self.pycapsule, "%s_headers" % return_type)
        else:
            headers = None
        r = requests.get(self.endpoint, auth=self.pycapsule.auth, headers=headers)
        return """Return data however specified"""


class PyCapsule():
    """
    pycapsule model handles the adding, updating, and deleting of
    of capsule crm api objects.

    args:
        base_url (str): base for capsulecrm url. ex. name in https://name.capsulecrm.com
        api_key (str): api key received from my preferences on capsule crm
    """

    def __init__(self, base_url, api_key):
        self.location = "https://%s.capsulecrm.com/api/" % base_url
        self.auth = (api_key, "x")
    
    @property
    def parties(self):
        """
        returns:
            object:object manager for all parties. this includes people and 
                organisations.

        """
        return PyCapsuleObjectManager(self, 'party')

    @property
    def opportunities(self):
        """
        returns:
            object: object manager for all opportunities.
        """
        return PyCapsuleObjectManager(self, 'opportunity')

    @property
    def cases(self):
        """
        returns:
            object: object manager for all cases.
        """
        return PyCapsuleObjectManager(self, 'kase')

    @property
    def history(self):
        """
        returns:
            object: object manager for history.
        """
        return PyCapsuleObjectManager(self, 'history')

    @property
    def tasks(self):
        """
        returns:
            object: object manager for tasks.
        """
        return PyCapsuleObjectManager(self, 'task')
    
    @property
    def tracks(self):
        """
        returns:
            object: object manager for tracks.
        """
        return PyCapsuleObjectManager(self, 'tracks')

    @property
    def users(self):
        """
        returns:
            list: list of users on the account
        """
        pass

    @property
    def countries(self):
        """
        returns:
            list: a list of all available countries in capsule crm.
        """
        pass

    @property
    def currencies(self):
        """
        returns:
            list: list of string values of available currencies on capsulecrm
            """
        pass
