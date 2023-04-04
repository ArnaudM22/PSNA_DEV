# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:15:28 2023

@author: arnaud.maupas
"""

data = tonkean_focals.data


undir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(undirected_behaviors)].groupby(['Behavior', 'Subject', 'Modifiers'])[
                         'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
undir_adj = undir_adj.merge(pd.Series(undir_adj.index.get_level_values('Modifiers'), index=undir_adj.index).str.split(
    ',', expand=True), left_index=True, right_index=True)  # The names in the modifiers section are separated.
undir_adj = undir_adj.replace('NaN', np.nan)
undir_adj2 = undir_adj.loc[:, ['Duration (s)', 0]].dropna().rename(
    columns={0: 'Modifiers'})  # undir_adj2 is used for the loop.
# Modifiers correction.
for i in range(1, len(undir_adj.columns) - 1):
    undir_adj2 = pd.concat((undir_adj2, undir_adj.loc[:, [
                           'Duration (s)', i]].dropna().rename(columns={i: 'Modifiers'})))
undir_adj = undir_adj2.set_index(undir_adj2.index.droplevel(2)).groupby(
    ['Behavior', 'Subject', 'Modifiers']).sum(numeric_only = True)  # Summed values for Modifiers.
# Directed case.
dir_adj = pd.DataFrame(data.loc[data['Behavior'].isin(directed_behaviors)].groupby(['Behavior', 'Subject', 'Modifiers'])[
                       'Duration (s)'].sum(numeric_only = True))  # The duration is calculated for each combination of behavior, individual, and modifiers.
dir_adj = dir_adj.merge(pd.Series(dir_adj.index.get_level_values('Modifiers'), index=dir_adj.index).str.split('|', expand=True), left_index=True,
                        right_index=True).rename(columns={0: 'direction', 1: 'Modifiers'}).set_index(dir_adj.index.droplevel(2))  # Modifiers separation.
# A subject column is created.
dir_adj.loc[:, 'Subject'] = dir_adj.index.get_level_values(1)
# Lines with "None" values are deleted.
dir_adj = dir_adj.replace('None', np.nan).dropna(axis=0)
dir_adj.loc[dir_adj['direction'] == 'Focal est recepteur', ['Modifiers', 'Subject']] = dir_adj.loc[dir_adj['direction'] ==
                                                                                                   'Focal est recepteur', ['Subject', 'Modifiers']].values  # Subject and Modifiers are reversed to always have the sender as subject.
# Removal of the Subject index column and replace it with the Subject column
dir_adj = dir_adj.set_index(dir_adj.index.droplevel(1))
# The summed values for each individual in Modifiers are calculated.
dir_adj = dir_adj.groupby(['Behavior', 'Subject', 'Modifiers']).sum(numeric_only = True)








a = data.loc[data['Behavior'].isin(undirected_behaviors)]
b = data.loc[data['Behavior'].isin(directed_behaviors)]

c = data.loc[data.loc[:, 'Behavioral category'] == '5 Proximite']

affiliative_interactions = ['Grooming', 'Etreinte', 'Jeu social', 'Contact passif']
proximity_association = ['0. Debut du scan', '1. Contact passif', '2. Espace peripersonnel', '3. peri<...<2m', '4. Prox. 2-5 m']
directed_interaction = ['Grooming']
undirected_interaction = ['Etreinte', 'Jeu social', 'Contact passif']

def social_category(data, affiliative_interactions = [], agonistic_interactions = [], proximity_association = []):
    data.loc[data['Behavior'].isin(affiliative_interactions), 'Social behavior category'] = 'Affiliative interaction'
    data.loc[data['Behavior'].isin(agonistic_interactions), 'Social behavior category'] = 'Agonistic interaction'
    data.loc[data['Behavior'].isin(proximity_association), 'Social behavior category'] = 'Proximity association'
    data.loc[:, 'Social behavior category'] = data.loc[:,'Social behavior category'].fillna('Non social')
    return data

def interactor_direction(data, directed_interaction = [], undirected_interaction = [], proximity_association = []):
    #directed case
    dir_inter = data.loc[data['Behavior'].isin(directed_interaction), "Modifiers"].str.split('|', expand=True).rename(columns={0: 'Interaction direction', 1: 'Other individual'})
    data = data.merge(dir_inter, how = 'outer', left_index = True, right_index = True)
    #undirected case and proximity
    undir_prox = data.loc[data['Behavior'].isin(undirected_interaction + proximity_association), "Modifiers"]
    data.loc[undir_prox.index, 'Other individual'] = undir_prox
    data.loc[data['Behavior'].isin(undirected_interaction), 'Interaction direction'] = 'Undirected interaction'
    return data
    
    
    dir_inter.loc[:,'Modifiers'].str.split('|', expand=True)
    dir_inter = dir_inter.merge(pd.Series(dir_inter.index.get_level_values('Modifiers'), index=dir_inter.index).str.split('|', expand=True), left_index=True,
                            right_index=True).rename(columns={0: 'direction', 1: 'Modifiers'}).set_index(dir_adj.index.droplevel(2))  # Modifiers separation.
    dir_adj = dir_adj.merge(pd.Series(dir_adj.index.get_level_values('Modifiers'), index=dir_adj.index).str.split('|', expand=True), left_index=True,
                            right_index=True).rename(columns={0: 'direction', 1: 'Modifiers'}).set_index(dir_adj.index.droplevel(2))  # Modifiers separation.
    
    data.loc[data['Behavior'].isin(undirected_interaction), 'Interaction direction'] = 'Undirected interaction'
    
    data.loc[data['Behavior'].isin(agonistic_interactions), 'Social behavior category'] = 'Focal est emetteur'
    data.loc[data['Behavior'].isin(proximity_association), 'Social behavior category'] = 'Focal est recepteur'
    data.loc[:, 'Social behavior category'] = data.loc[:,'Social behavior category'].fillna('NaN')
    return data

def receivers(data, affiliative_interactions = [], agonistic_interactions = [], proximity_association = []):
    data.loc[data['Behavior'].isin(affiliative_interactions), 'Social behavior category'] = 'Affiliative interaction'
    data.loc[data['Behavior'].isin(agonistic_interactions), 'Social behavior category'] = 'Agonistic interaction'
    data.loc[data['Behavior'].isin(proximity_association), 'Social behavior category'] = 'Proximity association'
    data.loc[:, 'Social behavior category'] = data.loc[:,'Social behavior category'].fillna('Non social')
    return data

d = social_category(data, affiliative_interactions = affiliative_interactions, proximity_association= proximity_association)

# New "Self centered" behavioral category.
data.loc[data['Behavior'].isin(
    ['Immobille', 'Se deplace', 'Se gratte', 'Selfgrooming']), 'Behavioral category 2'] = 'Self centered'
# New "Agressive" behavioral category.
data.loc[data['Behavioral category'] == '1 Agression',
         'Behavioral category 2'] = 'Aggressive'
# New "Affiliative" behavioral category.
data.loc[data['Behavioral category'].isin(
    ['2 Grooming', '3 Affiliation', 'Jeu']), 'Behavioral category 2'] = 'Affiliative'
data.loc[:, 'Behavioral category 2'] = data.loc[:,
                                                'Behavioral category 2'].fillna('Else')