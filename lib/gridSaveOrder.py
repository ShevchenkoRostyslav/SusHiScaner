#!/usr/bin/python
import collections

tuple_scan = (('tanBeta', 'tan(beta)'),
             ('sinB_A', 'sin(beta-alpha)'))
dict_scan = collections.OrderedDict(tuple_scan)

tuple_h_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('xs_ggh', 'ggh XS in pb'),
                ('xs_bbh', 'bbh XS in pb'),
                ('width_h', 'h width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_h_sushi = collections.OrderedDict(tuple_h_sushi)

tuple_h_2hdmc = (('br_hZZ', 'grep "23    23"'),
                ('br_hss', 'grep "3    -3"'),
                ('br_hcc', 'grep "4    -4"'),
                ('br_hbb', 'grep "5    -5"'),
                ('br_hee', 'grep "11   -11"'),
                ('br_hmumu', 'grep "13   -13"'),
                ('br_htautau', 'grep "15   -15"'),
                ('br_hgammagamma', 'grep "22    22"'),
                ('br_hWW', 'grep "24   -24"'),
                ('br_hZgamma', 'grep "23    22"'),
                ('br_hgg', 'grep "21    21"'))
dict_h_2hdmc = collections.OrderedDict(tuple_h_2hdmc)

tuple_A_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('xs_ggA', 'ggh XS in pb'),
                ('xs_bbA', 'bbh XS in pb'),
                ('width_A', 'A width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_A_sushi = collections.OrderedDict(tuple_A_sushi)

tuple_A_2hdmc = (('br_Ass', 'grep "3    -3"'),
                ('br_Acc', 'grep "4    -4"'),
                ('br_Abb', 'grep "5    -5"'),
                ('br_Att', 'grep "6    -6"'),
                ('br_Aee', 'grep "11   -11"'),
                ('br_Amumu', 'grep "13   -13"'),
                ('br_Atautau', 'grep "15   -15"'),
                ('br_Agammagamma', 'grep "22    22"'),
                ('br_AZgamma', 'grep "23    22"'),
                ('br_Agg', 'grep "21    21"'),
                ('br_AZH', 'grep "23    35"'),
                ('br_AZh', 'grep "23    25"'))
dict_A_2hdmc = collections.OrderedDict(tuple_A_2hdmc)

tuple_H_sushi = (('mh', 'mh'),
                ('mH', 'mH'),
                ('mA', 'mA'),
                ('xs_ggH', 'ggh XS in pb'),
                ('xs_bbH', 'bbh XS in pb'),
                ('width_H', 'H width in GeV'),
                ('unitarity', 'Tree-level unitarity'),
                ('perturbativity', 'Perturbativity'),
                ('stability', 'Stability'),
                ('width_Hc', 'Charged Higgs decays'))
dict_H_sushi = collections.OrderedDict(tuple_H_sushi)

tuple_H_2hdmc = (('br_HZZ', 'grep "23    23"'),
                ('br_Hss', 'grep "3    -3"'),
                ('br_Hcc', 'grep "4    -4"'),
                ('br_Hbb', 'grep "5    -5"'),
                ('br_Htt', 'grep "6    -6"'),
                ('br_Hee', 'grep "11   -11"'),
                ('br_Hmumu', 'grep "13   -13"'),
                ('br_Htautau', 'grep "15   -15"'),
                ('br_Hgammagamma', 'grep "22    22"'),
                ('br_HWW', 'grep "24   -24"'),
                ('br_HZgamma', 'grep "23    22"'),
                ('br_Hgg', 'grep "21    21"'),
                ('br_HZA', 'grep "23    36"'),
                ('br_HZh', 'grep "23    25"'),
                ('br_Hhh', 'grep "25    25"'),
                ('br_HW+H-', 'grep "24   -37"'))
dict_H_2hdmc = collections.OrderedDict(tuple_H_2hdmc)

tuple_extra_sushi = (('unitarity', 'Tree-level unitarity'),
                    ('perturbativity', 'Perturbativity'),
                    ('stability', 'Stability'),
                    ('width_Hc', 'Charged Higgs decays'))
dict_extra_sushi = collections.OrderedDict(tuple_extra_sushi)

tuple_extra_2hdmc = (('br_H+sc', 'grep  "4    -3"'),
                    ('br_H+cb', 'grep  "4    -5"'),
                    ('br_H+st', 'grep  "6    -3"'),
                    ('br_H+bt', 'grep  "6    -5"'),
                    ('br_H+munu', 'grep "13    14"'),
                    ('br_H+taunu', 'grep "15    16"'),
                    ('br_H+Wh', 'grep "24    25"'),
                    ('br_H+WH', 'grep "24    35"'))
dict_extra_2hdmc = collections.OrderedDict(tuple_extra_2hdmc)

dict_higgs = {'h':[dict_h_sushi, dict_h_2hdmc, '25', '35', 'xs11'],
              'H':[dict_H_sushi, dict_H_2hdmc, '35', '36', 'xs12'],
              'A':[dict_A_sushi, dict_A_2hdmc, '36', '37', 'xs21'],
              'extra':[dict_extra_sushi, dict_extra_2hdmc, '37', '#', 'xs11']}
