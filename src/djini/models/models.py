#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 16 de out de 2016

@author: CLayton Bonelli
@version: 0.1.0
'''

from configparser import ConfigParser
import os


#=======================================================================================================================
# Model
#=======================================================================================================================
class Model(object):
    """
    A model is the name of a session formed of key / value pairs defined in a configuration file, 
    for example in a file named 'data.ini':

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


    And use can be made as follows:
    
    date = Data.load('file.ini')
    print (data.name, data.age)

    or
    
    import os
    os.environ[Model.ENV_CONFIGURATION] = 'file.ini'
    
    names = NamesSession.load()
    print (names.first_name, names.last_name)
    """    

    ENV_CONFIGURATION = "INI_FILENAME"
    
    __META_CLASSNAME = "Meta"
    
    def save(self):
        """
        Saves the current object attributes in the file. 
        """
        raise NotImplemented("Yet")

    @classmethod
    def load(cls, filename=None):
        """
        Read the session which the current class is associated and stores into attributes the information 
        found in the file.
        
        @param filename: The file name that will be used to read the file session. If left empty the file name 
        will be searched in the environment variable Model.ENV_CONFIGURATION. 
        """
        filename = filename or os.environ.get(cls.ENV_CONFIGURATION)
        
        if not filename:
            raise ValueError("filename not found")
        
        return cls.__load_model_attributes(filename, cls(), cls.get_attributes())
    
    @classmethod
    def get_attributes(cls):
        """
        Retrieves all configured attributes for the current class.
        """
        return [
            attribute for attribute in cls.__dict__.keys() if not attribute.startswith('_') and attribute != cls.__META_CLASSNAME
        ]
        
    def to_dict(self, use_attribute_names=True):
        """
        Returns a dictionary with the keys being all configured attributes and their values.
        
        @param use_attribute_names: A True value indicates that the keys are the names of the attributes defined 
        in the current class. A False value indicates that  the keys are the names defined in the file. 
        """
        
        def get_key(attribute):
            return attribute if use_attribute_names else self.__class__.__dict__.get(attribute).name or attribute 
            
        attributes = self.get_attributes()
        return {get_key(attribute): getattr(self, attribute) for attribute in attributes}
        
    @classmethod
    def __load_model_attributes(cls, filename, model, attributes):
        config = cls.__read(filename)
        session_name = cls.__get_session_name()
        
        for attribute in attributes:
            field = getattr(model, attribute)
            value = config.get(session_name, field.name or attribute)
            setattr(model, attribute, field._target_class()(value))
        
        return model
        
    @classmethod
    def __get_session_name(cls):
        if hasattr(cls, cls.__META_CLASSNAME) and hasattr(cls.Meta, "session_name"):
            return cls.Meta.session_name
        else:    
            return cls.__name__

    @classmethod
    def __read(cls, filename):
        config = ConfigParser()
        config.read(filename)
        return config


#=======================================================================================================================
# ModelsInitializer
#=======================================================================================================================
class ModelsInitializer():
    """
    A helper class to set the environment variable to be used by the models.
    """
    
    @classmethod
    def set_filename(cls, filename):
        os.environ[Model.ENV_CONFIGURATION] = filename
