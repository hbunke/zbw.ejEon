# Zope imports 
from zope.interface import Interface, providedBy

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import WorkflowException

# Five imports
from Products.Five.browser import BrowserView

from zbw.ejEon.interfaces import IVote
from zope.app.annotation.interfaces import IAnnotations
from Products.ATContentTypes.utils import DT2dt
from zope.component import getMultiAdapter


class IPrizeEon(Interface):
    """Interface, which provides methods for an article.
    """
       
    def voteEON():
        """vote for this paper for EON Prize
        """

    def hasVotedEON():
        """checks for annotation
        """
    def hasVotedFor():
        """compares objects
        """
    def checkAnonymous():
        """exactly"""

    def countVotes():
        """counts votes
        """

    def linktitle():
        """returns a string for <a title=...
        """

    def eonvoters():
        """lists voters for article
        """

    def get_nominees():
        """
        this whole package is an ugly hack :-(
        """


class PrizeEon(BrowserView):
    """
    """    
    def voteEON(self):
        """
        """
        obj = self.context
        url = "%s/eon-prize-2010" % obj.portal_url()
        
        if not self.checkAnonymous() :          
            mtool = getToolByName(self, "portal_membership")
            user = mtool.getAuthenticatedMember()
            #import pdb; pdb.set_trace()
            if not self.hasVotedEON():
                a = IVote(obj)
                vote = a.vote()
                votinguser = a.setVote()
                obj.REQUEST.RESPONSE.redirect("%s?portal_status_message=Thank you. Your vote has been registered." % url)

            else:
                obj.REQUEST.RESPONSE.redirect("%s?portal_status_message=You have already voted!" % url)
        
        else:
            obj.REQUEST.RESPONSE.redirect("%s?portal_status_message=Please log in as Registered Reader to vote." % url)

    
    def hasVotedEON(self):
        
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return False
        user = mtool.getAuthenticatedMember()
        key = 'zbw.EONvoted'
        ann = IAnnotations(user)
        if ann.has_key(key):
            return True
        return False
        

    def hasVotedFor(self, context):
        mtool = getToolByName(self, "portal_membership")
        if  mtool.isAnonymousUser():
            return "background:white"
        user = mtool.getAuthenticatedMember()
        key = 'zbw.EONvoted'
        ann = IAnnotations(user)
        if self.hasVotedEON():
            votedObj = ann[key]
            if context == votedObj:
                return "background:#FFCE7B;"
        return "background:white"

    def checkAnonymous(self):
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return True
        return False

    def countVotes(self, context):
        key = 'zbw.eonprize'
        ann = IAnnotations(context)
        if ann.has_key(key):
            c = len(ann[key])
            return c
        else:
            return 0

    def getEonPrizeContent(self):
        """content of eon-prize list
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        obj = portal['eon2010-text']
        content = obj.EditableBody()
        return content

    def linktitle(self, paper):
        """
        """
        s = "Vote for this article: %s (Journalarticle %s)" %(paper.Title(),
                paper.getId())
        return s

    def eonvoters(self):
        """
        """
        text = ""
        ann = IAnnotations(self.context)
        if ann.has_key('zbw.eonprize'):
            text += "Nominated by: \n\n"
            voters = ann['zbw.eonprize']
            catalog = getToolByName(self.context, 'portal_catalog')
            for voter in voters:
                brains = catalog(portal_type="eJMember", id=voter)
                for brain in brains:
                    text += " - %s\n" %brain.getFullname

        return text

    
    
    def get_nominees(self):
        """
        """
        paperlist = getMultiAdapter((self.context, self.context.REQUEST), name="paperlist")

        catalog = getToolByName(self, "portal_catalog")
        brains = catalog(portal_type="JournalPaper", sort_on="created", 
                sort_order="descending")

        nominees = []
        for brain in brains:
            obj = brain.getObject()
            obj_date = DT2dt(obj.created())
            if obj_date.year < 2011:
                nominees.append(obj)

        return paperlist.filter_objects_by_jel(nominees, 'Q')
        
        




 
