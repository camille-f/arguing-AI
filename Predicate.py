# -*- coding: utf8 -*-

"""
Created on 12/10/17 17:44

@author: camille
Part of work coming from the Argumentator project : http://www.argumentator.eu/
"""


class Predicate:
    """Represents a predicate in the extended sense, with value, causes,
    consequences etc.
    """

    def __init__(self, name, value, actionable, realised, conceived):
        self.name = name
        self.value = value
        self.actionable = actionable
        self.realised = realised
        self._init_situation = realised
        self.conceived = conceived
        self.reconsiderable = (value != 0)
        self.negation = None
        self.logical_links = []

    # -----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Pred_\"" + self.name + "\""

    __str__ = __repr__

    # -----------------------------


    def is_mutable(self, N):
        """Indicates if the predicate is mutable with intensity N."""
        return N * self.value <= 0 and abs(self.value) < abs(N)

    def is_possible(self):
        """Indicates if the predicate is possible."""
        return (not self.negation.realised) or self.actionable

        # def propagate_change(self):
        # """Propagates the update of status forward in the rule set."""
        # for link in self.logical_links:
        # link.propagate_change(self)

    def update(self, changed_cause):
        """Updates the status according to the rules and current status of
        causes.
        """
        being_realised = False
        for link in self.logical_links:
            if link.makes_true(self):
                being_realised = True
                break
        if not self.realised and being_realised:
            print("Inferring %s from %s" % (self.name, changed_cause.name))
            self.make_true()

        elif self.realised and not being_realised and not self._init_situation:
            print("Went back to %s because of %s" % (self.negation.name, changed_cause.negation.name))
            self.negation.make_true()

    def make_action(self):
        """Makes the action corresponding to the predicate if there is one.
        (to be overwritten for particular instances of this class)
        """
        return

    def propagation(self):
        """ implements Wordl argumentation """
        L = self.logical_links
        if self.realised == True:
            for link in L:
                if link.link_type == 'causal' and all(P.realised for P in link.causes):
                    for P in link.consequences:
                        P.realised == True
        else:
            for link in L:
                for P in link.consequences:
                    for link_deux in P.logical_links:
                        if link.makes_true(self):
                            being_realised = True
                            break
                    if not P.realised and being_realised:
                        print("Inferring %s from %s" % (P.name, self.name))
                        make_true(P)

                    elif P.realised and not being_realised and not P._init_situation:
                        print("Went back to %s because of %s" % (P.negation.name, self.negation.name))
                        make_true(P.negation)

    # In[ ]:

    def make_true(self):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        self.realised = True
        self.conceived = True
        self.negation.realised = False
        self.negation.conceived = False
        self.propagation()
        self.negation.propagation()
        self.make_action()

