# -*- coding: utf8 -*-

"""
Created on 12/10/17 17:28

@author: camille
Part of work coming from the Argumentator project : http://www.argumentator.eu/
"""

import re
from Predicate import Predicate
from Links import CausalLink


class Preprocessor:
    """Preprocessing for converting the textual data to Python objects."""

    @staticmethod
    def __text_init(filename):
        """Reads the textual data and stores it in the returned dictionary."""

        return_dict = {}

        predicates = set()

        with open(filename, "r") as file:
            text = file.read()

        # Find the language and keep the part of the text with the relevant information.
        pattern = "\n\s*language\(\'(\w*)\'\)(.*)$"
        language, text = re.findall(pattern, text, flags=re.DOTALL)[0]
        return_dict['language'] = language
        text = re.sub("(?:^\s*%.*?$)|(?:%+.*?%+)", "", text, flags=re.MULTILINE)

        # Store the logical clauses.
        pattern = "^\s*(-?\w*)\s*<===\s*(.*)\s*$"
        causal_links_text = re.findall(pattern, text, flags=re.MULTILINE)

        causal_links = []

        for conseqs_text, causes_text in causal_links_text:

            conseqs = list(re.findall("([\w-]+)", conseqs_text))
            causes = list(re.findall("([\w-]+)", causes_text))
            causal_links.append((causes, conseqs))

            for cause in causes:
                predicates.add(cause)
            for conseq in conseqs:
                predicates.add(conseq)

        return_dict['causal_links'] = causal_links

        # Store the preferences.
        pattern = "preference\(\s*?(-?\w*)\s*?,\s*?(-?\d*)\s*?\)"
        preferences_text = re.findall(pattern, text, flags=re.MULTILINE)
        preferences = {}
        for predicat, value in preferences_text:
            preferences[predicat] = int(value)

        return_dict['preferences'] = preferences

        # Store the actions.
        pattern = "action\(\s*?(\w*)\s*?\)"
        return_dict['actions'] = re.findall(pattern, text, flags=re.MULTILINE)

        for action in return_dict['actions']:
            predicates.add(action)

        # Store the defaults.
        pattern = "default\(\s*?(-?\w*)\s*?\)"
        return_dict['defaults'] = re.findall(pattern, text, flags=re.MULTILINE)

        # Store the initial situations.
        pattern = "initial_situation\(\s*?(-?\w*)\s*?\)"
        return_dict['initial_situations'] = re.findall(pattern, text, flags=re.MULTILINE)

        # Store the predicate negations.
        for predicate in set(predicates):
            if predicate[0] == "-":
                predicates.add(predicate[1:])
            else:
                predicates.add("-" + predicate)

        return_dict['predicates'] = predicates

        return return_dict

    @staticmethod
    def setup_data(filename):
        """Reads the textual data and converts it into the corresponding
        Predicate objects.
        """

        data_dict = Preprocessor.__text_init(filename)
        predicates = {}
        logical_links = []
        for name in data_dict['predicates']:

            if name[0] != '-':
                negation_name = '-' + name
            else:
                negation_name = name[1:]

            if name in data_dict['preferences']:
                value = data_dict['preferences'][name]
            elif negation_name in data_dict['preferences']:
                value = -data_dict['preferences'][negation_name]
            else:
                value = 0

            actionable = (name in data_dict['actions']) or (negation_name in data_dict['actions'])

            realised = name in data_dict['initial_situations']

            conceived = (name in data_dict['defaults']) or realised

            predicate = Predicate(name, value, actionable, realised, conceived)

            if negation_name in predicates:
                negation_predicate = predicates[negation_name]
                predicate.negation = negation_predicate
                negation_predicate.negation = predicate

            predicates[name] = predicate

        for link in data_dict['causal_links']:
            causes = [predicates[name] for name in link[0]]
            conseqs = [predicates[name] for name in link[1]]
            logical_link = CausalLink(causes, conseqs)
            logical_links.append(logical_link)
            for name in link[0] + link[1]:
                if logical_link not in predicates[name].logical_links:
                    predicates[name].logical_links.append(logical_link)

        for name in predicates:
            if predicates[name].conceived and not predicates[name].negation.realised:
                predicates[name].realised = True

        return predicates, logical_links
