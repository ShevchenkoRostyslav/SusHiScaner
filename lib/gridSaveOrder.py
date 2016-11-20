#!/usr/bin/python

dict_scan = {'mA': 'mA',
             'tanBeta': 'tan(beta)',
             'sinB_A': 'sin(beta-alpha)'}

dict_h_sushi = {'mh': 'mh',
                'xs_ggh': 'ggh XS in pb',
                'xs_bbh': 'bbh XS in pb',
                'width_h': 'h width in GeV'}

#infoTag = ['higgsToZZ_2HDMC', 'higgsToss_2HDMC', 'higgsTocc_2HDMC', 'higgsTobb_2HDMC', 'higgsToee_2HDMC', 'higgsTomumu_2HDMC', 'higgsTotautau_2HDMC', 'higgsTogammagamma_2HDMC', 'higgsToWW_2HDMC', 'higgsToZgamma_2HDMC', 'higgsTogluglu_2HDMC']
dict_h_2hdmc = {'br_hZZ': 'grep "23    23"',
                'br_hss': 'grep "3    -3"',
                'br_hcc': 'grep "4    -4"',
                'br_hbb': 'grep "5    -5"',
                'br_hee': 'grep "11   -11"',
                'br_hmumu': 'grep "13   -13"',
                'br_htautau': 'grep "15   -15"',
                'br_hgammagamma': 'grep "22    22"',
                'br_hWW': 'grep "24   -24"',
                'br_hZgamma': 'grep "23    22"',
                'br_hgg': 'grep "21    21"'}

dict_A_sushi = {'mA': 'mA',
                'xs_ggA': 'ggh XS in pb',
                'xs_bbA': 'bbh XS in pb',
                'width_A': 'A width in GeV'}

#infoTag = ['AiggsToss_2HDMC', 'AiggsTocc_2HDMC', 'AiggsTobb_2HDMC', 'AiggsTott_2HDMC', 'AiggsToee_2HDMC', 'AiggsTomumu_2HDMC', 'AiggsTotautau_2HDMC', 'AiggsTogammagamma_2HDMC', 'AiggsToZgamma_2HDMC', 'AiggsTogluglu_2HDMC', 'AiggsToZH_2HDMC', 'AiggsToZh_2HDMC']
dict_A_2hdmc = {'br_Ass': 'grep "3    -3"',
                'br_Acc': 'grep "4    -4"',
                'br_Abb': 'grep "5    -5"',
                'br_Att': 'grep "6    -6"',
                'br_Aee': 'grep "11   -11"',
                'br_Amumu': 'grep "13   -13"',
                'br_Atautau': 'grep "15   -15"',
                'br_Agammagamma': 'grep "22    22"',
                'br_AZgamma': 'grep "23    22"',
                'br_Agg': 'grep "21    21"',
                'br_AZH': 'grep "23    35"',
                'br_AZh': 'grep "23    25"'}

dict_H_sushi = {'mH': 'mH',
                'xs_ggH': 'ggh XS in pb',
                'xs_bbH': 'bbh XS in pb',
                'width_H': 'H width in GeV'}

#infoTag = ['HiggsToZZ_2HDMC', 'HiggsToss_2HDMC', 'HiggsTocc_2HDMC', 'HiggsTobb_2HDMC', 'HiggsTott_2HDMC', 'HiggsToee_2HDMC', 'HiggsTomumu_2HDMC', 'HiggsTotautau_2HDMC', 'HiggsTogammagamma_2HDMC', 'HiggsToWW_2HDMC', 'HiggsToZgamma_2HDMC', 'HiggsTogluglu_2HDMC', 'HiggsTohh_2HDMC', 'HiggsToZA_2HDMC', 'HiggsToW+H-_2HDMC']
dict_H_2hdmc = {'br_HZZ': 'grep "23    23"',
                'br_Hss': 'grep "3    -3"',
                'br_Hcc': 'grep "4    -4"',
                'br_Hbb': 'grep "5    -5"',
                'br_Htt': 'grep "6    -6"',
                'br_Hee': 'grep "11   -11"',
                'br_Hmumu': 'grep "13   -13"',
                'br_Htautau': 'grep "15   -15"',
                'br_Hgammagamma': 'grep "22    22"',
                'br_HWW': 'grep "24   -24"',
                'br_HZgamma': 'grep "23    22"',
                'br_Hgg': 'grep "21    21"',
                'br_HZA': 'grep "23    36"',
                'br_HZh': 'grep "23    25"',
                'br_Hhh': 'grep "25    25"',
                'br_HW+H-': 'grep "24   -37"'}

dict_extra_sushi = {'unitarity': 'Tree-level unitarity',
                    'perturbativity': 'Perturbativity',
                    'stability': 'Stability',
                    'width_Hc': 'Charged Higgs decays'}

dict_extra_2hdmc = {'br_H+sc': 'grep  "4    -3"',
                    'br_H+cb': 'grep  "4    -5"',
                    'br_H+st': 'grep  "6    -3"',
                    'br_H+bt': 'grep  "6    -5"',
                    'br_H+munu': 'grep "13    14"',
                    'br_H+taunu': 'grep "15    16"',
                    'br_H+Wh': 'grep "24    25"',
                    'br_H+WH': 'grep "24    35"'}


dict_higgs = {'h':[dict_h_sushi, dict_h_2hdmc, '25', '35', 'xs11'],
              'H':[dict_H_sushi, dict_H_2hdmc, '35', '36', 'xs12'],
              'A':[dict_A_sushi, dict_A_2hdmc, '36', '37', 'xs21'],
              'extra':[dict_extra_sushi, dict_extra_2hdmc, '37', '#', 'xs11']}

#infoTag = ['HpggsTosc_2HDMC', 'HpggsTocb_2HDMC', 'HpggsTost_2HDMC', 'HpggsTobt_2HDMC', 'HpggsTomunu_2HDMC', 'HpggsTotaunu_2HDMC', 'HpggsToWh_2HDMC', 'HpggsToWH_2HDMC']
