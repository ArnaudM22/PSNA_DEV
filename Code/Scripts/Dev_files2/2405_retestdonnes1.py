# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:46:57 2023

@author: arnau
"""
import pandas as pd
data = pd.read_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2405_inputretest1.xls')
data = data.drop(columns=['Unnamed: 0'])

# correction des problèmes de non-consistence

other_individual = data.loc[data['Other individual'] != data['Modifier #2']]

data = data.drop(columns=['Modifier #2'])

# on redefinit le numfocal
data = data.sort_values(
    ["Observation date", "Start (s)"], ignore_index=True)

# A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
data.loc[:, 'numfocal'] = (data.loc[:, ['Observation date', 'Subject']] != data.loc[:, [
    'Observation date', 'Subject']].shift()).any(axis=1).cumsum() - 1

# ♠localisation des datetime qui foirent à changer manuellement
indiv_list = tuple(dict.fromkeys(data.loc[:, 'Subject']))

# verifier la liste des comportements.
behav_list = tuple(dict.fromkeys(data.loc[:, 'Behavior']))
data.loc[data['Behavior'] == 'Grab tail', 'Behavior'] = 'Grab Tail'
data.loc[data['Behavior'] == 'Tail grabbing', 'Behavior'] = 'Grab Tail'
data.loc[data['Behavior'] == 'Pull-Push', 'Behavior'] = 'Push-Pull'
data.loc[data['Behavior'] == 'push pull', 'Behavior'] = 'Push-Pull'


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
        l2 = tuple(dict.fromkeys(a.loc[:, 'Behavioral category']))
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


# verifier state/points.
data.loc[data['Behavior'] == 'Huddling', 'Behavior type'] = 'STATE'
data.loc[data['Behavior'] == 'Proximity', 'Behavior type'] = 'STATE'

# focal_length
data.loc[:, 'focal_length'] = 900

# duration
data.loc[:, 'Duration (s)'] = data.loc[:, 'Stop (s)'] - \
    data.loc[:, 'Start (s)']

data = clean.point_adj(data)

# partie recalcul des colonnes
data = data.drop(columns=['Social behavior category', 'Interaction direction'])

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

data.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305premierout_putclean/test_postporcessed2.xls')

# correction manuelle de date sur focale
data = pd.read_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305premierout_putclean/test_postporcessed2.xls')
data = data.drop(columns=['Unnamed: 0'])

# compte d'observation par focale
x = data.groupby('numfocal')['Subject'].count()
plt.boxplot(x)

# correction probleme focale vide
data = data.drop(481)
data.loc[:, 'numfocal'] = (data.loc[:, ['Observation date', 'Subject']] != data.loc[:, [
    'Observation date', 'Subject']].shift()).any(axis=1).cumsum() - 1
data = data.drop(columns=['Proximity'])
hud = data.loc[data['Behavior'] == 'Huddling']

# resave, grab tile passe en not defined
data.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305premierout_putclean/test_postporcessed3.xls')

# resave, après avoir viré les temps négatifs
# duration
data.loc[:, 'Duration (s)'] = data.loc[:, 'Stop (s)'] - \
    data.loc[:, 'Start (s)']
data = clean.point_adj(data)

data.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305premierout_putclean/time_corrected.xls')
