# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:46:57 2023

@author: arnau
"""
import pandas as pd
import Modules.focal_cleaning as clean
data = pd.read_excel(
    'C:/Users/arnau/Desktop/StageImalis/saimiris/Data analysis/time_corrected_final.xls')
data = data.drop(columns=['Unnamed: 0'])
data = data.drop([1629, 1630, 1631])

# correction des problèmes de non-consistence
'''
# on redefinit le numfocal
data2 = data.sort_values(
    ["Observation date", "Start (s)"], ignore_index=True)

# A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
data2.loc[:, 'numfocal'] = (data2.loc[:, ['Observation date', 'Subject']] != data2.loc[:, [
    'Observation date', 'Subject']].shift()).any(axis=1).cumsum() - 1
'''
# ♠localisation des datetime qui foirent à changer manuellement
indiv_list = tuple(dict.fromkeys(data.loc[:, 'Subject']))
data.loc[data['Subject'] == 'Vert-Rose Foncé', 'Subject'] = 'Vert-Rose foncé'
# verifier la liste des comportements.
behav_list = tuple(dict.fromkeys(data.loc[:, 'Behavior']))
data.loc[data['Behavior'] == 'Out of ight', 'Behavior'] = 'Out of sight'


def behavior_table_construction(data, see_table):
    """Builds the behavioral table"""

    # The qualitative version of the behaviorial table is built.
    behavior_table = data.groupby(
        'Behavior')[['Behavioral category']].first()
    # The number of occurence of the behaviors and behavioral categories is added.
    behavior_table.insert(0, 'n', behavior_table.index)
    behavior_table.loc[:, 'n'] = behavior_table.apply(
        lambda row:  str(Counter(data.loc[:, 'Behavior'])[row.n]), axis=1)
    behavior_table.loc[:, 'Behavioral category'] = behavior_table.apply(
        lambda row: row['Behavioral category'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category'])[row['Behavioral category']]), axis=1)
    # Table displaying (optional).
    if see_table == True:
        print(behavior_table)
    return behavior_table


def behavioral_category_check(data):
    l = tuple(dict.fromkeys(data.loc[:, 'Behavior']))
    behavior_cat_list = pd.DataFrame(columns=['Behavior', 'behavior cat list'])
    for i in l:
        a = data.loc[data['Behavior'] == i]
        l2 = tuple(dict.fromkeys(a.loc[:, 'Interaction direction']))
        print(i)
        print(l2)


behavioral_category_check(data)

data.loc[data['Behavior'] == 'Scan', 'Behavioral category'] = 'Scan'
data.loc[data['Behavior'] == 'Proximity',
         'Behavioral category'] = 'Affiliative'
data.loc[data['Behavior'] == 'Stealing', 'Behavioral category'] = 'Agonistic'
data.loc[data['Behavior'] == 'Huddling',
         'Behavioral category'] = 'Affiliative'
data.loc[data['Behavior'] == 'Out of sight',
         'Behavioral category'] = 'Not defined'
data.loc[data['Behavior'] == 'Grab Tail',
         'Behavioral category'] = 'Not defined'
data.loc[data['Behavior'] == 'Displace',
         'Behavioral category'] = 'Agonistic'
data.loc[data['Behavior'] == 'Push-Pull',
         'Behavioral category'] = 'Agonistic'
data.loc[data['Behavior'] == 'Social play',
         'Behavioral category'] = 'Affiliative'
data.loc[data['Behavior'] == 'Mounting',
         'Behavioral category'] = 'Agonistic'
data.loc[data['Behavior'] == 'Fight',
         'Behavioral category'] = 'Agonistic'


# verifier state/points.
# A reprendre ?
data.loc[data['Behavior'] == 'Stealing',
         'Behavior type'] = 'POINT'
data.loc[data['Behavior'] == 'Out of sight',
         'Behavior type'] = 'STATE'
data.loc[data['Behavior'] == 'Push-Pull',
         'Behavior type'] = 'POINT'

# focal_length
data.loc[:, 'focal_length'] = 900

# duration
data.loc[:, 'Duration (s)'] = data.loc[:, 'Stop (s)'] - \
    data.loc[:, 'Start (s)']

data = clean.point_adj(data)

# partie recalcul des colonnes
data = data.drop(columns=['Social behavior category'])

# partie social behavior category
data.loc[data['Behavioral category'] == 'Affiliative',
         'Social behavior category'] = 'Affiliative interaction'
data.loc[data['Behavioral category'] == 'Agonistic',
         'Social behavior category'] = 'Agonistic interaction'
data.loc[:, 'Social behavior category'] = data.loc[:,
                                                   'Social behavior category'].fillna('Non social')


# partie direction
data.loc[data['Modifier #1'] == 'Yes',
         'Interaction direction'] = 'Focal est emetteur'
data.loc[data['Modifier #1'] == 'No',
         'Interaction direction'] = 'Focal est recepteur'
data.loc[:, 'Interaction direction'] = data.loc[:,
                                                'Interaction direction'].fillna('Non-directional')
data = clean.column_reorder(data)


# compte d'observation par focale
x = data.groupby('numfocal')['Subject'].count()
plt.boxplot(x)
plt.show()


# resave, grab tile passe en not defined
data.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/testmanquedirection3005.xlsx')
