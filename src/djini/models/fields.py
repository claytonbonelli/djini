#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 16 de out de 2016

@author: CLayton Bonelli
@version: 0.1
'''

from abc import ABC, abstractmethod


#=======================================================================================================================
# Field
#=======================================================================================================================
class Field(ABC):
    """
    Base class for all field values.
    """
    
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        
    @abstractmethod
    def _target_class(self):
        pass


#=======================================================================================================================
# StringField
#=======================================================================================================================
class StringField(Field):
    """
    Represent a string field value.
    """
    
    def _target_class(self):
        return str


#=======================================================================================================================
# IntegerField
#=======================================================================================================================
class IntegerField(Field):
    """
    Represent an int field value.
    """
    
    def _target_class(self):
        return int
