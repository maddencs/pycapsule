import requests
import json


def make_pycobjects(data, manager):
    obj_dict = dict()
    for K, V in data.items():
       try:
           for k, v in list(V.items()):
               obj_dict[k] = list()
               if k != '@size':
                   if isinstance(v, list):
                       for obj in v:
                           obj_dict[k].append(PyCapsuleObject(manager, k, json_response=obj))
                   else:
                        obj_dict[k].append(PyCapsuleObject(manager, k, json_response=v))
       except:
           pass
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
                if k not in ['organisation', 'person']:
                    setattr(self, k, v)
                else:
                    for k2, v2 in v.items():
                        if k2 == 'id':
                            self.location = self.location + '/' +  str(v2)
                        setattr(self, k2, v2)

    def get_headers(self, headers):
        if headers:
            return getattr(self.pycapsule, "%s_headers" % headers)
        else:
            return self.pycapsule.json_headers

    def get_party_url(self):
        import re
        return re.match(r'https://[\w\d]*.capsulecrm.com/api/', self.location).group(0) + 'party/' + self.id

    def delete(self):
        """
        Returns:
            success(bool): True if successfully deleted else False
        """
        url = self.get_party_url()
        r = requests.delete(url, auth=self.pycapsule.auth)
        if r.status_code == 200:
            return True
        else:
            return False

    def update(self, data=None, data_type=None):
        """
        updates the object on capsule crm.
        
        args:
            data (json/xml): data to update capsule object
            data_type(str): the type of data that you're sending
        """
        headers = self.get_headers(data_type) 
        r = requests.put(self.location, auth=self.pycapsule.auth, data=data, headers=headers)
        if r.status_code != 200:
            return "There was a problem updating the object on Capsule CRM."
    
    @property
    def tags(self, headers=None):
        """
        returns:
            list: list of tags on the object
        """
        headers = self.get_headers(headers)
        # url = self.pycapsule.location + 'party/' + str(self.id) + '/tag'
        # r = requests.get(url, auth=self.pycapsule.auth, headers=self.pycapsule.json_headers)
        # tags = dict(json.loads(r.content.decode("utf-8")))
        # tag_list = list()
        # print(tags)
        # if int(tags['tags']['@size']) > 0:
            # for tag in tags['tags']['tag']:
                # tag_list.append(tag['name'])
            # return tag_list
        
        if self.endpoint in ['organisation', 'person']:
            url = 'party/' + self.id + '/tag'
        else:
            url = self.endpoint + '/' + self.id + '/tag'
        return PyCapsuleObjectManager(self, url)

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
        # if hasattr(pycapsule, 'location'):
            # self.location = pycapsule.location + endpoint
        if hasattr(pycapsule, 'location'):
            self.set_location(pycapsule, endpoint)
        if hasattr(pycapsule, 'pycapsule'):
            self.pycapsule = pycapsule.pycapsule
        else:
            self.pycapsule = pycapsule
    
    def set_location(self, pycapsule, endpoint):
        """For setting the API endpoint for tags, cases, etc."""
        end = endpoint.split('/')
        if end[len(end)-1] in ['tag']:
            import re
            self.location = re.match(r'https://[\w\d]*.capsulecrm.com/api/', pycapsule.location).group(0) + endpoint
        else:
            self.location = pycapsule.location + endpoint

    def get_headers(self, headers):
        if headers:
            return getattr(self.pycapsule, "%s_headers" % headers)
        else:
            return self.pycapsule.json_headers

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
        headers = self.get_headers(data_type)
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
        headers = self.get_headers(return_type)
        r = requests.get(self.location + '/%s' % id, auth=self.pycapsule.auth, headers=headers)
        if r.status_code == 404:
            return None
        if return_type == 'json':
            return r.json()
        elif return_type == 'xml':
            return r.text
        else:
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
        if return_type == 'xml':
            return r.content
        if return_type == 'json':
            return r.json()
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
        return PyCapsuleObjectManager(self, 'person')

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
