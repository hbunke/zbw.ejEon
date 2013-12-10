# -*- coding: UTF-8 -*-
# Dr. Hendrik Bunke <h.bunke@zbw.eu>

from zope.interface import Interface
from zope.annotation.interfaces import IAttributeAnnotatable

class IPrizable(IAttributeAnnotatable):
    """
    Marker Interface
    """

class IVote(Interface):
    """
    Interface for storing eon prize votes
    """

    def vote():
        """
        stores vote of registered readers in Article object
        """

    def setVote():
        """stores article object the user has voted for as
        annotation in the user object
        """

class IVoteO2(Interface):
    """
    Interface for storing O2 Prize votes
    """

   
