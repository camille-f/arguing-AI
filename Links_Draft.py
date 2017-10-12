# -*- coding: utf8 -*-

"""
Created on 12/10/17 17:00

@author: camille
Part of work coming from the Argumentator project : http://www.argumentator.eu/
"""


class CausalLink:
    """Represents a causal link between two lists of predicates"""

    def __init__(self, causes, consequences):
        self.causes = causes
        self.consequences = consequences
        self.link_type = "causal"
        for predicate in causes:
            predicate.forward_links.append(self)
        for predicate in consequences:
            predicate.backward_links.append(self)

    def __repr__(self):
        # Changing the representation of the object for better readability in debugging
        return "Causal_Link_(%s <=== %s)" % (self.consequence, self.causes)

    __str__ = __repr__


class IncompatibilityLink:
    """Represents an incompatibility link between different predicates."""

    def __init__(self, incompatibilities):
        self.incompatibilities = incompatibilities
        self.link_type = "incompatibility"
        for predicate in incompatibilities:
            predicate.forward_links.append(self)
            predicate.negation.backward_links.append(self)

    def __repr__(self):
        # Changing the representation of the object for better readability in debugging
        return "Incompatibility_Link_(%s)" % self.incompatibilities

    __str__ = __repr__


class Logic:
    @staticmethod
    def find_consequences(pred, link):
        """
        :param pred: a predicate
        :param link: a logical link, denoting causality or incompatibility
        :return: list of consequences induced by 'pred' through 'link'
        """

        if link.link_type == "causal" and pred in link.causes:
            return link.consequences
        elif link.link_type == "incompatibility" and pred in link.incompatibilities:
            return [P.negation for P in link.incompatibilities if P != pred]


    @staticmethod
    def find_causes(pred, link):
        """
        :param pred: a predicate
        :param link: a logical link, denoting causality or incompatibility
        :return: list of causes that induced 'pred' through 'link'
        """
        if link.link_type == "causal" and pred in link.consequences:
            return link.causes
        elif link.link_type == "incompatibility" and pred.negation in link.incompatibilities:
            return [P for P in link.incompatibilities if P != pred.negation]


    @staticmethod
    def causal_relations(link):
        """
        :param link: a logical link, denoting causality or incompatibility
        :return: list of relations denoted by 'link'
        """
        if link.link_type == "causal":
            yield (link.causes, link.consequences)
        if link.link_type == "incompatibility":
            incomp = link.incompatibilities
            for i in range(len(incomp)):
                yield (incomp[0:i] + incomp[i + 1:], incomp[i].negation)


