import requests
import json


def make_pycobjects(data, manager):
    obj_dict = {'organisations': list(),
            'people': list()}
    if 'organisation' in data['parties'].keys():
        for org in data['parties']['organisation']:
            obj_dict['organisations'].append(PyCapsuleObject(manager, 'organisation', json_response=org))
    if 'people' in data['parties'].keys():
        for person in data['parties']['people']:
            obj_dict['people'].append(PyCapsuleObject(manager, 'person', json_response=person))
    return obj_dict

class PyCapsuleObject():
    """
    Data object to be returned by PyCapsuleObjectManager.
    Has functionality to update, delete, retrieve tags,
    add opportunities, and cases.

    Args:
        endpoint (str): Capsule CRM endpoint ex. party, person, kase, etc.

    Kwargs:
        json_response (optional[json]): Used for filling self with capsule data
    """

    def __init__(self, manager, endpoint, location=None, json_response=None, **kwargs):
        self.pycapsule = manager.pycapsule
        self.endpoint = endpoint
        self.location = self.pycapsule.location + endpoint
        if json_response:
            for k, v in json_response.items():
                if k not in ['organisation', 'party']:
                    setattr(self, k, v)
                else:
                    for k2, v2 in v.items():
                        if k2 == 'id':
                            self.location = self.location + '/' +  str(v2)
                        setattr(self, k2, v2)


    def delete(self):
        """Deletes the object from Capsule CRM"""
        r = requests.delete(self.location, auth=self.pycapsule.auth)
        if r.status_code == 200:
            return "Object deleted"
        else:
            return "There was a problem deleting the object from Capsule CRM."

    def update(self, data=None, data_type=None):
        """
        updates the object on capsule crm.
        
        args:
            data (json/xml): data to update capsule object
            data_type(str): the type of data that you're sending
        """
        if data_type:
            headers = getattr(self.pycapsule, "%s_headers" % data_type)
        r = requests.put(self.location, auth=self.pycapsule.auth, data=data, headers=headers)
        if r.status_code != 200:
            return "There was a problem updating the object on Capsule CRM."

    def tags(self, headers=None):
        """
        returns:
            list: list of tags on the object
        """
        if headers:
            headers = getattr(self.pycapsule, "%s_headers" % headers)
        url = self.pycapsule.location + 'party/' + str(self.id) + '/tag'
        r = requests.get(url, auth=self.pycapsule.auth, headers=self.pycapsule.json_headers)
        tags = dict(json.loads(r.content.decode("utf-8")))
        tag_list = list()
        for tag in tags['tags']['tag']:
            tag_list.append(tag['name'])
        return tag_list

    @property
    def custom_fields(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's custom fields
        """
        return PyCapsuleObjectManager(self, self.endpoint)

    @property
    def opportunities(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's opportunities
        """
        pass

    @property
    def cases(self):
        """
        returns:
            object: pycapsuleobjectmanager for this object's cases
        """
        pass

    @property
    def history(self):
        """
        Returns:
            object: pycapsuleobjectmanager for object's history
        """
        pass

    def remove_contact(self, contact_id=None):
        url = self.location + '/contact/' + contact_id
        r = requests.delete(url, auth=self.pycapsule.auth)
        return r.status_code

    @property
    def additional_contacts(self):
        """
        Returns:
            object: PyCapsuleObjectManager for object's contacts
        """
        pass


class PyCapsuleObjectManager():
    """
    object manager for pycapsule objects. can add and retrieve
    capsule crm objects.
    
    args:
        pycapsule (object): pycapsule object to pass on api key and other
            information
        endpoint (str): capsulecrm endpoint ex. party,  person

    """
    
    def __init__(self, pycapsule, endpoint, **kwargs):
        self.endpoint = endpoint
        if hasattr(pycapsule, 'location'):
            self.location = pycapsule.location + endpoint
        if hasattr(pycapsule, 'pycapsule'):
            self.pycapsule = pycapsule.pycapsule
        else:
            self.pycapsule = pycapsule

    def create(self, **kwargs):
        """
        Create new object of type from kwargs

        Kwargs:
            * (optionial[str]): must be existing kwargs for the object
        """
        pass

    def add(self, data, data_type=None, return_type=None):
        """
        add a new object of this type to capsule crm.

        Args:
            data (xml, json): data to be sent to crm api

        Kwargs:
            data_type (str): format of data being sent ex. json or xml
            return_type (optional[str]): desired format of data to be received
                ex. xml or object. if none is provided, defaults to xml

        Returns:
            location (url): Capsule url with new object ID
            
        Example:
            pycapsule.parties.add('filename.xml', 'xml', return_type='object')
        """
        if data_type:
            headers = getattr(self.pycapsule, "%s_headers" % data_type)
        r = requests.post(self.location, data=data, auth=self.pycapsule.auth, headers=headers)
        try:
            return r.headers['Location']
        except:
            return "There was a problem adding the object to Capsule."

    def get(self, id=None, return_type=None):
        """
        get capsule crm object by id.

        Kwargs:
            return_type (optional[str]): desired format of data to be received
            capsule_id (int): capsule crm id of the target object.

        Returns:
            object/xml/json: returns object with functionality if no return_type
                is specified, otherwise returns the specified data type
        """
        if self.endpoint == 'person' or 'organisation':
            self.location = self.pycapsule.location + 'party'
        if return_type == 'json':
            headers = self.pycapsule.json_headers
            r = requests.get(self.location + '/%s' % id, auth=self.pycapsule.auth, headers=headers)
            return r.json()
        elif return_type == 'xml':
            headers = self.pycapsule.xml_headers
            r = requests.get(self.location + '/%s' % id, auth=self.pycapsule.auth, headers=headers)
            return r.text
        elif return_type is None:
            headers = self.pycapsule.json_headers
            url = self.location + '/%s' % id
            r = requests.get(url, auth=self.pycapsule.auth, headers=headers)
            return PyCapsuleObject(self, self.endpoint, json_response=r.json())

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
            headers = self.pycapsule.json_headers
        if self.endpoint == 'person' or 'organisation':
            self.location = self.pycapsule.location + 'party'
        params = {'q': list()} 
        for k, v in kwargs.items():
            if k in ['email', 'lastmodified', 'start', 'tag', 'limit']:
                params[k] = v
            else:
                params['q'].append(v)
        r = requests.get(self.location, auth=self.pycapsule.auth, headers=headers, params=params)
        if return_type:
            return r.content
        data = r.json()
        # return PyCapsuleObject(self, r.content, json_response=r.json())
        return make_pycobjects(data, self)


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
            headers = self.pycapsule.json_headers
        r = requests.get(self.location, auth=self.pycapsule.auth, headers=headers)
        if return_type == 'json':
            return r.json()
        elif return_type == 'xml':
            return r.content
        else:
            data = r.json()
            return make_pycobjects(data, self)


class PyCapsule():
    """
    pycapsule model handles the adding, updating, and deleting of
    of capsule crm api objects.

    args:
        base_url (str): base for capsulecrm url. ex. name in https://name.capsulecrm.com
        api_key (str): api key received from my preferences on capsule crm
    """
    xml_headers = {'content-type': 'application/xml',
                'accept': 'text/xml'}
    json_headers = {'content-type:': 'application/json',
                'accept': 'application/json'}


    def __init__(self, base_url, api_key):
        self.location = "https://%s.capsulecrm.com/api/" % base_url
        self.auth = (api_key, "x")
        
    @property
    def organisations(self):
        """
        returns:
            object:object manager for all parties. this includes people and 
                organisations.

        """
        return PyCapsuleObjectManager(self, 'organisation')
    
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
