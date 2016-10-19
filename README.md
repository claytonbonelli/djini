# Djini
A representation object-oriented of sessions of an ini file where the session name will be represented 
by a new Python class and the key/value will be the attributes of this new class.
    
*The current implementation was inspired by the models defined by Django web framework*.
    
### Field
A field is an object that maps to key/value pairs in an ini file.
    
### Model
A model is an object that maps to sessions in an ini file.
A model name is the name of a session formed of key/value pairs defined in a configuration file.
A model consists of one or more fields.
    
### Example    
```bash
*data.ini*

[Data]
name = joe
age = 20

[Names session]
name1 = klaus
name2 = peter
```

```python

# The classes may be mapped as follows:

from djini.models import models, fields
    
class Data (models.Model):
    name = fields.StringField()
    age = fields.IntegerField()


class NamesSession (models.Model):
    first_name = fields.StringField(name = "name1")
    last_name = fields.StringField(name = "name2")

    class Meta:
        session_name = "Names session"

# Use as follows:
    
data = Data.load('file.ini')
print(data.name, data.age)

# Or
    
import os
os.environ[models.Model.ENV_CONFIGURATION] = 'file.ini'
    
names = NamesSession.load()
print(names.first_name, names.last_name)
    
# Or
    
models.ModelsInitializer.set_filename('file.ini')
   
data = Data.load()
print(data.name, data.age)

data.name = "john"
data.save()
```
