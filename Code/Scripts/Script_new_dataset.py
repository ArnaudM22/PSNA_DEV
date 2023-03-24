# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:17:46 2023

@author: arnaud.maupas
"""

import pandas as pd
import Modules.net as net
import Modules.neuro as neuro
import Modules.etho as etho
__author__ = " Arnaud Maupas "
__contact__ = "arnaud.maupas@ens.fr"
__date__ = "19/09/22"
__version__ = "1"

"""
For the Tonkean 2021 behavioral category correction:
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
y
None
y
1
None
"""
# Tonkean (shown in the report, Figure 7 and 8ABCD)
tonkean = etho.Focals('../Data/Etho/Raw/Tonkean_2021_2',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
tonkean.data = tonkean.data.replace('Groom.er.ee','Ind', regex=True)

tonkean.filtering(grooming_see=True, non_visible_see=True,
                  short_focal_preprocessing_see=True, save=None, ignore=())

"""
For the Rhesus 2021 behavioral category correction:
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
y
None
y
1
None
"""

rhesus2021 = etho.Focals('../Data/Etho/Raw/Rhesus_2021',
                      open_preprocessed=False, check_empty_col=True, ignore=())

rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

"""
For the Rhesus 2022 behavioral category correction:
0:2 1:4 2:1 3:5 5:3
0:4 1:5 2:6 4:8 5:13 6:25 7:12 8:13 9:14 10:15 11:21 12:22 13:24 14:17 16:23 18:3
1:15 2:12 3:13 4:14 7:3
y
None
y
1
None
"""

rhesus2022 = etho.Focals('../Data/Etho/Raw/Rhesus_2022_xls',
                      open_preprocessed=False, check_empty_col=True, ignore=())

#Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2022.data = rhesus2022.data.drop(np.where(data['Behavior']=='4 Position')[0]).reset_index(drop = True)

rhesus2022.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

for i in grooming.index:
    if (grooming.loc[i, 'Behavior'] == '2 Zone de Grooming') :
        print(re.search("Focal est (.*?)\|", grooming.loc[i, 'Modifiers']).group(1))
    print(i)

grooming = grooming.drop(pd.Series(grooming.loc[grooming['Behavior'] ==
                                                 '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[2]).where(lambda x: x == 'None').dropna().index)

grooming.loc[grooming['Behavior'] == '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[0]
