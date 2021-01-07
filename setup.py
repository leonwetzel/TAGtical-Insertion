#!/usr/bin/env python3
from distutils.core import setup

# FIXME naam van applicatie aanpassen
setup(name='Distutils',
      version='1.0',
      description='Python Distribution Utilities',
      author="Leon Wetzel, Marjolein Spijkerman, Nik van 't Slot",
      author_email='l.f.a.wetzel@student.rug.nl,'
                   ' m.spijkerman.1@student.rug.nl,'
                   ' n.g.van.t.slot@student.rug.nl',
      url='https://github.com/leonwetzel/Computational-Semantics',
      packages=['tagtical_insertion', 'tagtical_insertion.pipeline', 'tagtical_insertion.preprocessing'],
     )