#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 16 de out de 2016

@author: CLayton Bonelli
@version: 1.0.0
'''

from configparser import ConfigParser, RawConfigParser
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
    
    _filename = None

    ENV_CONFIGURATION = "INI_FILENAME"

    __META_CLASSNAME = "Meta"

    def save(self, filename=None, use_attribute_names=True):
        """
        Saves the current object in the file.
         
        @param filename: The file name that will be used to save the session and attributes. 
        If left empty the file name will be searched in the environment variable Model.ENV_CONFIGURATION.
         
        @param use_attribute_names: A True value indicates that the keys are the names of the attributes defined 
        in the current class. A False value indicates that  the keys are the names defined in the file. 
        """
        cls = self.__class__
        
        filename = cls.__get_filename(filename)
        
        # Recreate the session
        config_parser = cls.__read(filename, klass=RawConfigParser)
        session_name = cls.__get_session_name()
        
        config_parser.remove_section(session_name)
        config_parser.add_section(session_name)
        
        self.__insert_attributes(config_parser, session_name, use_attribute_names)
        self.__save_file(filename, config_parser) 

    def delete(self, filename=None):
        """
        Remove the current object from file.
         
        @param filename: The file name that will be used to remove the session. If left empty the file name 
        will be searched in the environment variable Model.ENV_CONFIGURATION.
        """
        cls = self.__class__

        filename = cls.__get_filename(filename)
        
        # Remove the session
        config_parser = cls.__read(filename, klass=RawConfigParser)
        session_name = cls.__get_session_name()
        
        config_parser.remove_section(session_name)
        self.__save_file(filename, config_parser) 
    
    @classmethod
    def load(cls, filename=None):
        """
        Read the session which the current class is associated and stores into attributes the information 
        found in the file.
        
        @param filename: The file name that will be used to read the file session. If left empty the file name 
        will be searched in the environment variable Model.ENV_CONFIGURATION. 
        """
        filename = cls.__get_filename(filename)
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

    def __insert_attributes(self, config_parser, session_name, use_attribute_names=True):
        data = self.to_dict(use_attribute_names)
        for key, value in data.items():
            config_parser.set(session_name, key, value)

    def __save_file(self, filename, config_parser):
        # Save the file    
        with open(filename, 'wt', encoding='utf8') as file:
            config_parser.write(file)    
                
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
    def __read(cls, filename, klass=ConfigParser):
        config = klass()
        config.read(filename)
        return config
    
    @classmethod
    def __get_filename(cls, filename):
        filename = filename or cls._filename or os.environ.get(cls.ENV_CONFIGURATION)
                
        if not filename:
            raise ValueError("filename undefined")

        # Ensures that the file is saved in the class
        cls._filename = filename
        return filename


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
