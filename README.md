# Djini
    A representation object-oriented of sessions of an ini file where the session name will be represented 
    by a new Python class and the key/value will be the attributes of this new class.
    
    The current implementation was inspired by the models defined by Django web framework
    
# Model
    A model is an object that maps to sessions in an ini file.
    A model name is the name of a session formed of key/value pairs defined in a configuration file, 
    
# Example    
    data.ini
    ---------

    [Data]
    name = joe
    age = 20

    [Names session]
    name1 = klaus
    name2 = peter
    

    The classes may be mapped as follows:


    class Data (models.Model):
        name = fields.StringField ()
        fields.IntegerField age = ()


    class NamesSession (models.Model):
        first_name = fields.StringField (name = "name1")
        last_name = fields.StringField (name = "name2")

        class Meta:
            session_name = "names session"


    And the use can be made as follows:
    
    date = Data.load('file.ini')
    print (data.name, data.age)

    or
    
    import os
    os.environ[Model.ENV_CONFIGURATION] = 'file.ini'
    
    names = NamesSession.load()
    print (names.first_name, names.last_name)
