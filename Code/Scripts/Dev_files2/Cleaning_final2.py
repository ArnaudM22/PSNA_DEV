# -*- coding: utf-8 -*-
"""
Created on Wed May 17 12:23:05 2023

@author: arnau
"""
import Modules.focal_cleaning as clean
import Modules.class_definition as class_def
import Modules.datastream_viz as viz
import numpy as np

affiliative_interactions = ['Grooming',
                            'Etreinte', 'Jeu social', 'Contact passif']
proximity_association = ['0. Debut du scan', '1. Contact passif',
                         '2. Espace peripersonnel', '3. peri<...<2m', '4. Prox. 2-5 m']
agonistic_interactions = []
directed_interaction = ['Grooming']
undirected_interaction = ['Etreinte', 'Jeu social', 'Contact passif']
social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association


behaviors = affiliative_interactions

'''Tonkean 2021'''


"""
First step : data cleaning. 
Enter : 
0:2 1:0 2:4 3:1 4:3
0:5 1:0 2:1 3:2 4:3 5:4 6:6
0:0
y
None
y
1
None
"""

tonkean_focals = class_def.Focals('../Data/Raw/Tonkean_2021',
                                  open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
tonkean_focals.data = tonkean_focals.data.replace(
    'Groom.er.ee', 'Ind', regex=True)

tonkean_focals.filtering(grooming_see=True, non_visible_see=True,
                         short_focal_preprocessing_see=True, save=None, ignore=())

tonkean_focals.data = clean.social_category(tonkean_focals.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
tonkean_focals.data = clean.interactor_direction(tonkean_focals.data, directed_interaction=directed_interaction,
                                                 undirected_interaction=undirected_interaction, proximity_association=proximity_association)
tonkean_focals.data = clean.column_reorder(tonkean_focals.data)

tonkean_focals.data.to_excel(
    '../Data/Cleaned_data_input_format/tonkean_2021.xls')


'''Rhesus 2021'''


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

rhesus2021 = class_def.Focals('../Data/Raw/Rhesus_2021',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2021.data = rhesus2021.data.replace('Groom.er.ee', 'Ind', regex=True)


rhesus2021.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

# Partie column reorga
rhesus2021.data = clean.social_category(rhesus2021.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
rhesus2021.data = clean.interactor_direction(rhesus2021.data, directed_interaction=directed_interaction,
                                             undirected_interaction=undirected_interaction, proximity_association=proximity_association)
rhesus2021.data = clean.column_reorder(rhesus2021.data)

rhesus2021.data.to_excel(
    '../Data/Cleaned_data_input_format/rhesus_2021.xls')


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

rhesus2022 = class_def.Focals('../Data/Raw/Rhesus_2022',
                              open_preprocessed=False, check_empty_col=True, ignore=())

# Manual adjustment : renommer Groom.er.ee -> Ind
rhesus2022.data = rhesus2022.data.drop(np.where(
    rhesus2022.data['Behavior'] == '4 Position')[0]).reset_index(drop=True)

rhesus2022.filtering(grooming_see=True, non_visible_see=True,
                     short_focal_preprocessing_see=True, save=None, ignore=())  # filtering

# Partie column reorga
rhesus2022.data = clean.social_category(rhesus2022.data, affiliative_interactions=affiliative_interactions, agonistic_interactions=[
], proximity_association=proximity_association)
rhesus2022.data = clean.interactor_direction(rhesus2022.data, directed_interaction=directed_interaction,
                                             undirected_interaction=undirected_interaction, proximity_association=proximity_association)
rhesus2022.data = clean.column_reorder(rhesus2022.data)

rhesus2022.data.to_excel(
    '../Data/Cleaned_data_input_format/rhesus_2022.xls')


"""Saimiris 2023"""

path = 'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/full0.xls'


# import and merge
sai2023 = pd.read_excel(path)
sai2023 = sai2023.drop(columns=['Unnamed: 0'])

sai2023 = sai2023.sort_values(
    ["Observation date", "Start (s)"], ignore_index=True)

# A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
sai2023.loc[:, 'numfocal'] = (sai2023.loc[:, ['Observation date', 'Subject']] != sai2023.loc[:, [
    'Observation date', 'Subject']].shift()).any(axis=1).cumsum() - 1

# focal_length
sai2023.loc[:, 'focal_length'] = sai2023.loc[:, 'Total duration']

#sai2023 = clean.nan_char(sai2023)


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


behavior_table_construction(sai2023, see_table=True)

# partie social behavior category
sai2023.loc[sai2023['Behavioral category'] == 'Affiliative',
            'Social behavior category'] = 'Affiliative interaction'
sai2023.loc[sai2023['Behavioral category'] == 'Agonistic',
            'Social behavior category'] = 'Agonistic interaction'
sai2023.loc[:, 'Social behavior category'] = sai2023.loc[:,
                                                         'Social behavior category'].fillna('Non social')

# partie other individual
sai2023.loc[:, 'Other individual'] = sai2023.loc[:, 'Modifier #2']
sai2023.loc[:, 'Other individual'] = sai2023.loc[:,
                                                 'Other individual'].fillna('No other individual')

# partie direction
sai2023.loc[sai2023['Modifier #1'] == 'Yes',
            'Interaction direction'] = 'Focal est recepteur'
sai2023.loc[sai2023['Modifier #1'] == 'No',
            'Interaction direction'] = 'Focal est emetteur'
sai2023.loc[:, 'Interaction direction'] = sai2023.loc[:,
                                                      'Interaction direction'].fillna('Non-directional')
sai2023 = clean.column_reorder(sai2023)

sai2023.loc[sai2023['Subject'] == 'Vert-Rose Foncé',
            'Subject'] = 'Vert-Rose foncé'

sai2023.to_excel(
    '../Data/Cleaned_data_input_format/sai2023_test2.xls')

sai2023
sai2023.loc[:, 'Duration (s)'] = sai2023.loc[:,
                                             'Stop (s)'] - sai2023.loc[:, 'Start (s)']

sai2023.to_excel(
    '../Data/Cleaned_data_input_format/sai2023_test3.xls')


"""Saimiris 2023, reprise avec donnees completes"""

path = 'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305_nouveau_input_cleaning'


# import and merge
sai2023 = clean.import_merge(path)
sai2023 = sai2023.drop(columns=['Unnamed: 0'])

sai2023 = sai2023.sort_values(
    ["Observation date", "Start (s)"], ignore_index=True)

# A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
sai2023.loc[:, 'numfocal'] = (sai2023.loc[:, ['Observation date', 'Subject']] != sai2023.loc[:, [
    'Observation date', 'Subject']].shift()).any(axis=1).cumsum() - 1

# focal_length
sai2023.loc[:, 'focal_length'] = sai2023.loc[:, 'Total duration']

#sai2023 = clean.nan_char(sai2023)


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


behavior_table_construction(sai2023, see_table=True)

# partie social behavior category
sai2023.loc[sai2023['Behavioral category'] == 'Affiliative',
            'Social behavior category'] = 'Affiliative interaction'
sai2023.loc[sai2023['Behavioral category'] == 'Agonistic',
            'Social behavior category'] = 'Agonistic interaction'
sai2023.loc[:, 'Social behavior category'] = sai2023.loc[:,
                                                         'Social behavior category'].fillna('Non social')

# partie other individual
sai2023.loc[:, 'Other individual'] = sai2023.loc[:, 'Modifier #2']
sai2023.loc[:, 'Other individual'] = sai2023.loc[:,
                                                 'Other individual'].fillna('No other individual')

# partie direction
sai2023.loc[sai2023['Modifier #1'] == 'Yes',
            'Interaction direction'] = 'Focal est recepteur'
sai2023.loc[sai2023['Modifier #1'] == 'No',
            'Interaction direction'] = 'Focal est emetteur'
sai2023.loc[:, 'Interaction direction'] = sai2023.loc[:,
                                                      'Interaction direction'].fillna('Non-directional')
sai2023 = clean.column_reorder(sai2023)

sai2023.loc[sai2023['Subject'] == 'Vert-Rose Foncé',
            'Subject'] = 'Vert-Rose foncé'


sai2023
sai2023.loc[:, 'Duration (s)'] = sai2023.loc[:,
                                             'Stop (s)'] - sai2023.loc[:, 'Start (s)']

sai2023.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305premierout_putclean/sai2023_test4.xls')

# ♦precedent test2 est biaisé il faut essayer de remonter pour comprendre tout ça mais on peut le  retrouver en relançant premiere version


def time_budg_construction(data, n_line, n_column):
    """"Builds the set of pie charts and stacked bar plot"""

    # The data and individual list are charged in local variables to facilitate debugging.
    indiv = tuple(dict.fromkeys(data.loc[:, 'Subject']))

    # A "plot_data" table is initialized.
    iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
        dict.fromkeys(data.loc[:, 'Behavior']))]  # Index content.
    # Index initialization.
    index = pd.MultiIndex.from_product(
        iterables, names=['numfocal', 'Behavior'])
    plot_data = pd.DataFrame(index=index)  # initialiser dataframe
    # The data to plot are calculated.
    # Number of occurence.
    nbr_occur = data.groupby(
        ['numfocal', 'Behavior']).size().rename('nbr_occur')
    # Table filling.
    plot_data = plot_data.merge(
        nbr_occur, right_index=True, left_index=True, how='left')
    plot_data = plot_data.merge(data.groupby('numfocal')['Subject'].first(
    ), on='numfocal', how='left').set_axis(plot_data.index)  # Individual ID is added.
    plot_data = plot_data.fillna(0)  # Nan are replaced by 0.
    # Individual ID is set as an index level.
    plot_data = plot_data.set_index('Subject', append=True)
    # The data for the stacked bar plot are calculated.
    plot_indiv_data = plot_data.groupby(
        ['Subject', 'Behavior']).sum()  # on somme
    # For pei charts
    plt.rcParams.update({'font.size': 8,
                         'axes.titlepad': 0})
    plot_indiv_data.unstack(level=0).plot(kind='pie', subplots=True, layout=(
        n_line, n_column), legend=True, sharex=False, labels=None, title=indiv, ylabel='')  # plot pour indiv
    plt.rcParams.update(plt.rcParamsDefault)
    # For stacked bar plots.
    fig, axs = plt.subplots(n_line, n_column)
    l = 0
    for a in range(n_line):
        for b in range(n_column):
            if l < (len(indiv)):
                plot_data.loc[plot_data.index.get_level_values('Subject') == indiv[l]].unstack(level=1).plot(
                    ax=axs[a, b], kind='bar', stacked=True, legend=False, xlabel='', fontsize=2)  # Plot construction.
                # xticks Parameters.
                axs[a, b].tick_params(
                    axis='both', labelbottom=False, bottom=False, which='major', pad=0)
                # Title parameters.
                axs[a, b].set_title(indiv[l], pad=0, fontsize=10)
                l += 1
            else:
                axs[a, b].axis('off')
    plt.show()


time_budg_construction(data, 5, 3)

plot_indiv_data = plot_indiv_data.unstack(level=0)

plot_indiv_data.unstack(level=0).plot(kind='pie', subplots=True, layout=(
    n_line, n_column), legend=True, sharex=False, labels=None, title=indiv, ylabel='')
