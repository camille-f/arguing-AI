# -*- coding: utf8 -*-

"""
Created on 12/10/17 17:44

@author: camille
Part of work coming from the Argumentator project : http://www.argumentator.eu/
"""


class LogicalLink:
    """Represents a logical link of any kind between different predicates."""

    def __init__(self, link_type):
        self.link_type = None

    def find_causes(self, T, N):
        """Find a cause for T if the link provides one, or None."""
        raise NotImplementedError("Please Implement this method")

    def propagate_change(self, T):
        """Propagates a change on T through the logical link."""
        raise NotImplementedError("Please Implement this method")

    def makes_true(self, T):
        """Checks if the logical link has predicate T as a consequence."""
        raise NotImplementedError("Please Implement this method")


class CausalLink(LogicalLink):
    """Represents a causal link between two lists of predicates."""

    def __init__(self, causes, consequences):
        self.causes = causes
        self.consequences = consequences
        self.link_type = "causal"

    # -----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Logic_(%s --> %s)" % (self.causes, self.consequences)

    __str__ = __repr__

    # -----------------------------

    def find_causes(self, T):
        if T in self.consequences:
            return self.causes
        return None

    def propagate_change(self, T):
        if T in self.causes:
            for P in self.consequences:
                P.update(T)

    def makes_true(self, T):
        if T in self.consequences:
            if all(P.realised for P in self.causes):
                return True
        return False
