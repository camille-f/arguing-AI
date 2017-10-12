# -*- coding: utf8 -*-

"""
Created on 12/10/17 23:26

@author: camille
"""

from Preprocessor import Preprocessor
from Arguing import Argumentator

predicates, links = Preprocessor().setup_data('doors.pl')
print(predicates)
print(links)

Argumentator().argue(predicates)