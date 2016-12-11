#!/usr/bin/python
"""Hardcoded library for SusHi tag vs val.

Library written to put in line SusHi tag and value that it's dedicated
to.
For example:
('xs_ggh', 'ggh XS in pb') - shows that value of 'xs_ggh' can be found in
SusHi output file by tag = 'ggh XS in pb'
"""

import collections

__author__ = "Rostyslav Shevchenko"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

tuple_scan = (('tanBeta', 'tan(beta)'),
             ('sinB_A', 'sin(beta-alpha)'))
dict_scan = collections.OrderedDict(tuple_scan)

tuple_h_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('m12', 'm12'),
                ('xs_ggh', 'ggh XS in pb'),
                ('xs_bbh', 'bbh XS in pb'),
                ('width_h', 'h width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_h_sushi = collections.OrderedDict(tuple_h_sushi)

tuple_h_2hdmc = (('br_hZZ', '23    23'),
                ('br_hss', '3    -3'),
                ('br_hcc', '4    -4'),
                ('br_hbb', '5    -5'),
                ('br_hee', '11   -11'),
                ('br_hmumu', '13   -13'),
                ('br_htautau', '15   -15'),
                ('br_hgammagamma', '22    22'),
                ('br_hWW', '24   -24'),
                ('br_hZgamma', '23    22'),
                ('br_hgg', '21    21'))
dict_h_2hdmc = collections.OrderedDict(tuple_h_2hdmc)

tuple_A_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('m12', 'm12'),
                ('xs_ggA', 'ggh XS in pb'),
                ('xs_bbA', 'bbh XS in pb'),
                ('width_A', 'A width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_A_sushi = collections.OrderedDict(tuple_A_sushi)

tuple_A_2hdmc = (('br_Ass', '3    -3'),
                ('br_Acc', '4    -4'),
                ('br_Abb', '5    -5'),
                ('br_Att', '6    -6'),
                ('br_Aee', '11   -11'),
                ('br_Amumu', '13   -13'),
                ('br_Atautau', '15   -15'),
                ('br_Agammagamma', '22    22'),
                ('br_AZgamma', '23    22'),
                ('br_Agg', '21    21'),
                ('br_AZH', '23    35'),
                ('br_AZh', '23    25'))
dict_A_2hdmc = collections.OrderedDict(tuple_A_2hdmc)

tuple_H_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('m12', 'm12'),
                ('xs_ggH', 'ggh XS in pb'),
                ('xs_bbH', 'bbh XS in pb'),
                ('width_H', 'H width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_H_sushi = collections.OrderedDict(tuple_H_sushi)

tuple_H_2hdmc = (('br_HZZ', '23    23'),
                ('br_Hss', '3    -3'),
                ('br_Hcc', '4    -4'),
                ('br_Hbb', '5    -5'),
                ('br_Htt', '6    -6'),
                ('br_Hee', '11   -11'),
                ('br_Hmumu', '13   -13'),
                ('br_Htautau', '15   -15'),
                ('br_Hgammagamma', '22    22'),
                ('br_HWW', '24   -24'),
                ('br_HZgamma', '23    22'),
                ('br_Hgg', '21    21'),
                ('br_HZA', '23    36'),
                ('br_HZh', '23    25'),
                ('br_Hhh', '25    25'),
                ('br_HW+H-', '24   -37'))
dict_H_2hdmc = collections.OrderedDict(tuple_H_2hdmc)

tuple_extra_sushi = (('unitarity', 'Tree-level unitarity'),
                    ('perturbativity', 'Perturbativity'),
                    ('stability', 'Stability'),
                    ('width_Hc', 'Charged Higgs decays'))
dict_extra_sushi = collections.OrderedDict(tuple_extra_sushi)

tuple_extra_2hdmc = (('br_H+sc', '4    -3'),
                    ('br_H+cb', '4    -5'),
                    ('br_H+st', '6    -3'),
                    ('br_H+bt', '6    -5'),
                    ('br_H+munu', '13    14'),
                    ('br_H+taunu', '15    16'),
                    ('br_H+Wh', '24    25'),
                    ('br_H+WH', '24    35'))
dict_extra_2hdmc = collections.OrderedDict(tuple_extra_2hdmc)


dict_higgs = {'h':[dict_h_sushi, dict_h_2hdmc, '25', '35', 'xs11'],
              'H':[dict_H_sushi, dict_H_2hdmc, '35', '36', 'xs12'],
              'A':[dict_A_sushi, dict_A_2hdmc, '36', '37', 'xs21'],
              'extra':[dict_extra_sushi, dict_extra_2hdmc, '37', '#', 'xs11']}
