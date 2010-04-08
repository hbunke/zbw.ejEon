# -*- coding: UTF-8 -*-
# Dr. Hendrik Bunke <h.bunke@zbw.eu>

from zope.interface import Interface
from zope.app.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from Products.CMFCore.utils import getToolByName


KEY = "zbw.eonprize"
USER_KEY = "zbw.EONvoted"

class Vote:
    #implements(IVote)
    #adapts(Interface)

    def __init__(self, context):
         
        self.context = context
        annotations =  IAnnotations(context)
        
        if not annotations.has_key(KEY):
            annotations[KEY] = PersistentList()
        
        self.votes = annotations[KEY]
        
        # getting the voting userobject and its annotations
        self.mtool = getToolByName(self.context, "portal_membership")
        self.user = self.mtool.getAuthenticatedMember()
        userAnnotations = IAnnotations(self.user)
        
        if not userAnnotations.has_key(USER_KEY):
            userAnnotations[USER_KEY] = ''
        
        self.userAnnotations = userAnnotations


    def vote(self):
        """adds reader/vote as annotation
        """
        t = self.votes
        
        if not self.user.getId() in t:
            t.append(self.user.getId())
        else:
            pass
    
    # kann eigentlich auch vote() mit rein. So lässt sich allerdings 
    # erstmal leichter testen
    def setVote(self):
        """set and checks users vote
        """
        #import pdb; pdb.set_trace()
        self.userAnnotations[USER_KEY] = self.context


        
 
