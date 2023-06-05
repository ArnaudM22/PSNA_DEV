# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:50:16 2023

@author: arnau
"""
import pandas as pd
"""Saimiris 2023"""

path = '../Data/Raw/Sai_xls_2'

# import and merge
data = clean.import_merge(path)

data_vic = data.sort_values(
    ["Observation id", "Start (s)"], ignore_index=True)


"""donnees Arnaud"""
path = 'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale'

# import and merge
data_arnaud = clean.import_merge(path)

# supprimer empty columns :


def empty_col(data, empty_col_names, check=False):
    """Supress uninformative empty columns.

    Allows the user to delete columns often left empty by Strasbourg observers 
    ("Description", "FPS", "Comment start", "Comment stop", "Media file"). 
    The user can check the content of these columns before deleting them 
    ("check_empty_col" parameter during initialization).

    If this step has been performed, a summary of the content of the supposedly empty columns is saved in the attribute "empty_col_values".

    Parameters
    ----------
    data : dataframe
        The dataset of interest.
    check : bool, optional
        Specifies if the user wants to check the content of some columns before 
        deleting them. The default is check_empty_col.

    Returns
    -------
    data : dataframe
        The updated dataset.
    """

    # The supposed empty columns names are charged in a local variable.
    # Their content is retrieved.
    empty_col_values = dict((col_name, tuple(dict.fromkeys(
        data.loc[:, col_name].fillna('NaN')))) for col_name in empty_col_names)
    # The user can see and decide to delete the empty columns or not.
    if check == True:
        print('\n Suspected empty col values : \n')
        for col in empty_col_values:
            print(col, ':', empty_col_values[col])
        choice = input(
            'Do you want to supress suspected empty cols? (y to delete them all) \n')
        if choice == 'y':
            data = data.drop(columns=empty_col_names)
            print('\n Supressed !')
        else:
            data = data.drop(columns=choice)
    # By default, they are all deleted.
    else:
        data = data.drop(columns=empty_col_names)

    return data, empty_col_values


empty_col_names_sai = ['Description', 'Observation type', 'Source', 'Media duration (s)', 'FPS (frame/s)',
                       'Image index stop', 'Image file path start', 'Image file path stop', 'Comment start', 'Comment stop', 'Media file name']
data_arnaud, empty_col_values = empty_col(
    data_arnaud, empty_col_names_sai, check=True)

# add observer and assistant columns
data_arnaud = data_arnaud.assign(Observer='Arnaud')
data_arnaud = data_arnaud.assign(Assistant='Victoire')

# reorder columns
data_arnaud.columns.tolist()

new_col = ['Observation id',
           'Observation date',
           'Observer',
           'Assistant',
           'Total duration',
           'Subject',
           'Observation duration by subject by observation',
           'Behavior',
           'Behavioral category',
           'Modifier #1',
           'Modifier #2',
           'Modifier #3',
           'Behavior type',
           'Start (s)',
           'Stop (s)',
           'Duration (s)',
           'Image index start',
           'Start (m)',
           'Stop (m)',
           'Comments',
           'Notes']

data_arnaud = data_arnaud[new_col]

# premiere sauvegarde
data_arnaud.to_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/test0.xls')


# test2 = version avec les trucs de note et de durée changer, encore quelques modifs à apporter mais globalement bien
data_arnaud2 = pd.read_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/test2.xls')
empty_col_names_sai = ['Comments', 'Notes']
data_arnaud, empty_col_values = empty_col(
    data_arnaud2, empty_col_names_sai, check=True)

data_arnaud = data_arnaud.drop(columns=['Start (m)', 'Stop (m)'])

# deuxieme sauvegarde clean
data_arnaud.to_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/test3.xls')

# maintenant on termine la prise de données de vic, d'abord on git pull et on refait le pipeline pour avoir ensemble de fichier basique.
path = '../Data/Raw/Sai_xls_2'

# import and merge
data_vic = clean.import_merge(path)

data_vic.to_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/data_vic0.xls')

# post_cleaning secondes
data_vic2 = pd.read_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/data_vic1.xls')
data_vic2 = data_vic2.drop(columns=['Unnamed: 0'])

# merge both data frame
data_arnaud = data_arnaud.drop(columns=['Unnamed: 0'])

test_full = pd.concat([data_arnaud, data_vic2])
test_full.to_excel(
    'C:/Users/arnau/Desktop/StageImalis/Projet_Saimiri/premiere_version_finale/premier_merge/full0.xls')

"""Correction de la derniere paire de focales"""
# on sauve à part les deux dernieres
data_arnaud3 = data_arnaud.copy(deep=True)
data_arnaud = pd.read_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305_2dernieresfocales/2dernieres_corr.xls')

empty_col_names_sai = ['Description', 'Observation type', 'Source', 'Media duration (s)', 'FPS (frame/s)',
                       'Image index stop', 'Image file path start', 'Image file path stop', 'Comment start', 'Comment stop', 'Media file name']
data_arnaud, empty_col_values = empty_col(
    data_arnaud, empty_col_names_sai, check=True)

# add observer and assistant columns
data_arnaud = data_arnaud.assign(Observer='Arnaud')
data_arnaud = data_arnaud.assign(Assistant='Victoire')


new_col = ['Observation id',
           'Observation date',
           'Observer',
           'Assistant',
           'Total duration',
           'Subject',
           'Observation duration by subject by observation',
           'Behavior',
           'Behavioral category',
           'Modifier #1',
           'Modifier #2',
           'Modifier #3',
           'Behavior type',
           'Start (s)',
           'Stop (s)',
           'Duration (s)',
           'Image index start']

data_arnaud = data_arnaud[new_col]

data_arnaud = data_arnaud.rename(columns={"Image index start": "Note"})

data_arnaud.to_excel(
    'C:/Users/arnau/Desktop/Projet_samimiris_correction/2305_2dernieresfocales/2dernieres_corr_withscript.xls')
