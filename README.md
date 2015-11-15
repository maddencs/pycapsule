# PyCapsule
Python library for consuming the <a href="https://developer.capsulecrm.com">Capsule CRM API.</a>

The goal of this project is to make interacting with Capsule CRM's API very simple in Python.

### Installation
To install the PyCapsule library simply clone the repository into your project directory like this:
`
cd path/to/project
git clone https://github.com/maddencs/pycapsule.git
`


### Configuration
To configure the library for use in your project just initialize a new PyCapsule object with your Capsule CRM username and API Key that you can retrieve from your Capsule My Preferences page under API Authentication Token.

```
from pycapsule import PyCapsule

pc = PyCapsule('pycapsule', '234jdfas8f2jrfasdvm8234jf')
```

## Queries
When querying the Capsule CRM API you can get your results back in one of three ways. This is specified by using the keyword `return_type` in your query.
`pc.organisations.all(return_type='json')`

#### Organisations
The following code snippets show how you can interact with the Organisations API

##### To get a list of all organisations:

```
orgs = pc.organisations.all() # Returns a list of PyCapsuleObjects

orgs = pc.organisations.all(return_type='json') # Returns the raw json from your query

orgs = pc.organisations.all(return_type='xml') # Returns raw XML from query
```
*return_type can be used in any query

##### To get a filtered list of organisations
When filtering organisations specifiy the parameters you would like to filter by in the `filter()` method. If your keyword isn't in the following list it will be converted into a basic query that will search name, phone number, and custom fields: `email, tag, lastmodified, limit, start`. More info on the parameters can be found <a href='http://developer.capsulecrm.com/v1/resources/parties/'>here</a>.

Examples:

```
orgs = pc.organisations.filter(name='Google') // Returns a list of PyCapsuleObjects with Google in the name
orgs = pc.organisations.filter(name='Google', limit=100) // Returns a maximum of 100 matching organisiations
```

##### To get an organisation by its ID
Use the `get()` method to grab a specific Capsule object from Capsule

Example:
```
pc.organisations.get(id=1234567890) // Returns PyCapsuleObject for the org with this ID
pc.organisations.get(id=1234567890, return_type='json') // Returns the json version of your query
```

#### People
People share the same query methods as Organisations. The way the Capsule CRM handles people and organisations is under the same API endpoint, so querying parties and organisations will give you the same objects as a result. There is no benefit of querying either way.

Example:

```
parties = pc.parties.all() // Returns a list of PyCapsuleObjects for the Party endpoint
first_person = parties['person'][0]
print(first_person.firstName) // Prints the firstName of the Capsule CRM person

person = pc.parties.get(id=1234567890) // Gets you the "Person" object from Capsule CRM
```
