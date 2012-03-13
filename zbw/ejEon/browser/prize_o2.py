from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zbw.ejEon.interfaces import IVoteO2
from zope.app.annotation.interfaces import IAnnotations
from Products.ATContentTypes.utils import DT2dt
from zope.component import getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile



class View(BrowserView):
    """
    """    

    template = ViewPageTemplateFile("prize_o2.pt")

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()


        
    def hasVotedO2(self):
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return False
        user = mtool.getAuthenticatedMember()
        key = 'zbw.O2voted'
        ann = IAnnotations(user)
        if ann.has_key(key):
            return True
        return False
        

    def hasVotedFor(self, context):
        mtool = getToolByName(self, "portal_membership")
        if  mtool.isAnonymousUser():
            return "background:white"
        user = mtool.getAuthenticatedMember()
        key = 'zbw.O2voted'
        ann = IAnnotations(user)
        if self.hasVotedO2():
            votedObj = ann[key]
            if context == votedObj:
                return "background:#FFCE7B;"
        return "background:white"


    
    def getO2PrizeContent(self):
        """content of eon-prize list
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        try:
            obj = portal['o2-text']
            content = obj.EditableBody()
        except:
            content = "No body text yet."
        return content


    def linktitle(self, paper):
        """
        """
        s = "Vote for this article: %s (Journalarticle %s)" %(paper.Title(),
                paper.getId())
        return s

    
    
    def get_nominees(self):
        """
        """
        paperlist = getMultiAdapter((self.context, self.context.REQUEST), 
                name="paperlist")

        catalog = getToolByName(self, "portal_catalog")
        brains = catalog(portal_type="JournalPaper", sort_on="created", 
                sort_order="descending")

        nominees = []
        for brain in brains:
            obj = brain.getObject()
            obj_date = DT2dt(obj.created())
            if obj_date.year < 2012:
                nominees.append(obj)

        return paperlist.filter_objects_by_jel(nominees, 'I')
    
    
    def checkAnonymous(self):
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return True
        return False



class Votes(BrowserView):
    """
    """
    
    def count(self):
        key = 'zbw.o2prize'
        ann = IAnnotations(self.context)
        if ann.has_key(key):
            c = len(ann[key])
            return c
        else:
            return 0


    def voters(self):
        """
        """
        text = ""
        ann = IAnnotations(self.context)
        if ann.has_key('zbw.o2prize'):
            text += "Nominated by: \n\n"
            voters = ann['zbw.o2prize']
            catalog = getToolByName(self.context, 'portal_catalog')
            for voter in voters:
                brains = catalog(portal_type="eJMember", id=voter)
                for brain in brains:
                    text += " - %s\n" %brain.getFullname
        return text

    
    def vote(self):
        """
        """
        obj = self.context
        url = "%s/o2-prize-2012" % obj.portal_url()
        
        if not self.__checkAnonymous() :          
            mtool = getToolByName(self, "portal_membership")
            user = mtool.getAuthenticatedMember()
            #import pdb; pdb.set_trace()
            if not self.__hasVotedO2():
                a = IVoteO2(obj)
                vote = a.vote()
                votinguser = a.setVote()
                msg = "Thank you. Your vote has been registered."

            else:
                msg = "You have already voted!"
        
        else:
            msg = "Please log in as Registered Reader to vote."

        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect("%s/" % url)


    def __checkAnonymous(self):
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return True
        return False

        
    def __hasVotedO2(self):
        mtool = getToolByName(self, "portal_membership")
        if mtool.isAnonymousUser():
            return False
        user = mtool.getAuthenticatedMember()
        key = 'zbw.O2voted'
        ann = IAnnotations(user)
        if ann.has_key(key):
            return True
        return False




 
