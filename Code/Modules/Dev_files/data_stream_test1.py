# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:15:28 2023

@author: arnaud.maupas
"""

data = tonkean_focals.data.copy(deep = True)

affiliative_interactions = ['Grooming', 'Etreinte', 'Jeu social', 'Contact passif']
proximity_association = ['0. Debut du scan', '1. Contact passif', '2. Espace peripersonnel', '3. peri<...<2m', '4. Prox. 2-5 m']
directed_interaction = ['Grooming']
undirected_interaction = ['Etreinte', 'Jeu social', 'Contact passif']


                  
data = social_category(data, affiliative_interactions = affiliative_interactions, agonistic_interactions = [], proximity_association = proximity_association)
data = interactor_direction(data, directed_interaction = directed_interaction, undirected_interaction = undirected_interaction, proximity_association = proximity_association)
data = column_reorder(data)
    
    
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