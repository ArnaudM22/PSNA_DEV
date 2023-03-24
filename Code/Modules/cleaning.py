# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:18:04 2023

@author: arnaud.maupas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
from collections import Counter
__author__ = " Arnaud Maupas "
__contact__ = "arnaud.maupas@ens.fr"
__date__ = "19/09/22"
__version__ = "1"


class Focals:
    """Contains the methods and attributes allowing to perform operations on ethological data.

    The class attributes are :
        -"affiliative_behaviors", the list of observable affiliative behaviors on any dataset.
        -"reference_behavior_table", a dataframe containing the reference 
        'Behavior'/'Behavioral Category I' pairs.

    The instance attributes are :
        -"data", a dataframe that stores the data that can be successively modified by applying the methods.
        -"raw_data", a dataframe that stores a basic version of 
        the dataset (before the successive modifications).
        -"indiv", a tuple containing the name of the individuals.
        -"path", a string containing the location of the input data.
        -"error_line", a dictionary containing the set of rows 
        deleted if the 'filtering' method has been applied.
        -"behav_cor", a dict of the changes made during the behavioral category 
        correction if this step has been performed ("new_behavioral_cat" during initialization, optional).
        -"empty_col_values", a dictionary with the content of the 
        supposedly empty columns if this step has been performed ("empty_col" at initialization, optional).

    The methods that can be used by the user are :
        -the constructor, Initializes the instance and performs a first 
        cleaning when creating the instance (if specified).
        -"filtering", completes the cleaning.
        -"visualization", provides a set of representations related to the dataset.
        -"affiliative_networks", constructs the adjacency matrices of the 
        different affiliative networks and of the DSI (each time, oriented or not). 
        -"prenet_NM", builds a list of adjacency matrices of random networks 
        according to the pre-network Null Model.    
    """

    # Definition of class attributes.
    affiliative_behaviors = ['Grooming', 'Etreinte',
                             'Jeu social', 'Contact passif']
    #definir ça comme un fichier à part.
    reference_behavior_table = pd.DataFrame(index=pd.MultiIndex.from_arrays([['ref']*31, list(range(31))], names=('table', 'index')),
                                            columns=['Behavior',
                                                     'Behavioral category'],
                                            data=[['Agress. phys.', '1 Agression'],
                                                  ['Deplacement', '1 Agression'],
                                                  ['Menace', '1 Agression'],
                                                  ['Secoue le support',
                                                      '1 Agression'],
                                                  ['0 Presentation', '2 Grooming'],
                                                  ['1 Debut Grooming',
                                                      '2 Grooming'],
                                                  ['2 Zone de Grooming',
                                                      '2 Grooming'],
                                                  ['3 Position', '2 Grooming'],
                                                  ['4 Fin Grooming', '2 Grooming'],
                                                  ['Etreinte', '3 Affiliation'],
                                                  ['Monte', '3 Affiliation'],
                                                  ['Portage', '3 Affiliation'],
                                                  ['Se repose sur',
                                                      '3 Affiliation'],
                                                  ['Sniff', '3 Affiliation'],
                                                  ['0. Debut du scan',
                                                      '5 Proximite'],
                                                  ['1. Contact passif',
                                                      '5 Proximite'],
                                                  ['2. Espace peripersonnel',
                                                      '5 Proximite'],
                                                  ['3. peri<...<2m',
                                                      '5 Proximite'],
                                                  ['4. Prox. 2-5 m',
                                                      '5 Proximite'],
                                                  ['Se gratte', 'Cpt autocentré'],
                                                  ['Selfgrooming',
                                                      'Cpt autocentré'],
                                                  ['Baillement', 'NaN'],
                                                  ['Contact passif', 'NaN'],
                                                  ['Erreur', 'NaN'],
                                                  ['Forage', 'NaN'],
                                                  ['Immobile', 'NaN'],
                                                  ['Non-visible', 'NaN'],
                                                  ['Se deplace', 'NaN'],
                                                  ['Jeu social', 'Jeu'],
                                                  ['Lipsmack', 'Mimique faciale'],
                                                  ['Mimique faciale', 'Mimique faciale']])

    def __init__(self, path, check_empty_col=False, ignore=(), save=None, open_preprocessed=True, start_end = False):
        """Initializes the instance.

        The path to the data is automatically saved in the instance attribute "path".
        The arguments are then passed to the protected function "_preprocessing" 
        which performs the first operations for initialization with the dataset. 
        It is then stored in the attribute "data".
        A copy of this dataset is kept in the attribute "raw_data", 
        and the list of individualsis saved in the attribute "indiv". 
        The "error_line" is initialized to be used with the "filtering" method (optional).

        Parameters
        ----------
        path : str
            Path to the data.
        check_empty_col : bool, optional
            Specifies if the user wants to check the content of suspected 
            empty columns before deleting them. The default is False.
        ignore : tuple of (str,), optional
            Steps that the user wants to skip among {'correct_behavioral_cat', 'empty_col'}. 
            The default is ().
        save : str, optional
            Saving path. The default is None.
        open_preprocessed : bool, optional
            specifies if the data is already clean. The default is True.

        Returns
        -------
        None.
        """

        # Initialization of the instance attributes.
        self.path = path
        self.data = self.__preprocessing(
            path, check_empty_col, ignore, save, open_preprocessed, start_end)
        self.raw_data = self.data.copy(deep=True)
        self.indiv = tuple(dict.fromkeys(self.data.loc[:, 'Subject']))
        self.error_line = {}

    def __preprocessing(self, path, check_empty_col, ignore, save, open_preprocessed, start_end):
        """Performs the first operations for initialization.

        This function is called exclusively by the constructor during initialization, 
        which passes on its arguments.
        If the dataset is already clean, the user can ask to open it without
        cleaning ("open_preprocessed" parameter).
        Otherwise a first part of the cleaning can be done automatically during *
        the construction of the instance, following different steps:
        1. A first import with basic cleaning is done with the internal function "order_data".
        2. The behavioral categories (I) are corrected to match the reference 
        with the internal function "correct_behavioral_cat" (optional step).
        3. A new behavioral category is created with the internal function "new_behavioral_cat".
        4. Empty columns can be deleted with the internal function "empty_col" (optional step).
        5. The table can be saved to be used as input for future analyses ("save" parameter, optional step).

        Parameters
        ----------
        path : str
            Path to the data.
        check_empty_col : bool
            Specifies if the user wants to check the content of some columns before deleting them.
        ignore : tuple of (str,)
            Steps that the user wants to skip among {'correct_behavioral_cat', 'empty_col'}. 
        save : str
            Saving path. 
        open_preprocessed : bool
            specifies if the data is already clean.

        Returns
        -------
        data : dataframe
            The initialized dataframe.
        """

        # The data are directly loaded if they are already preprocessed.
        if open_preprocessed == True:
            data = pd.read_csv(path, index_col=0, keep_default_na=False)

        else:

            def order_data(path, start_end):
                """Import, order the data and perform basic cleaning.

                Imports the data, concatenates them into a single table and 
                orders the rows by observation date and observation starting point.
                Also creates a "numfocal" column containing a numerical 
                identifier for each focal, and a "focal_length" column containing 
                the total focal length for each focal.
                Other small basic changes are made during this step 
                (duration of point behaviors fixed at 1 second, conversion of NaN to str format) 
                to avoid bugs when applying later methods.

                Parameters
                ----------
                path : str
                    Path to the data.

                Returns
                -------
                data : dataframe
                    A first version of the dataset.
                """
                
                # The data is imported, merged and then ordered.
                data = pd.concat(map(pd.read_excel, glob.glob(
                    os.path.join(path, '*.xls'))), ignore_index=True)
                data = data.sort_values(
                    ["Observation id", "Start (s)"], ignore_index=True)
                # A numerical identifier is assigned to each focal length (2 lines are in the same focal length if they are consecutive with the same observation_id and the same subject).
                data.loc[:, 'numfocal'] = (data.loc[:, ['Observation id', 'Subject']] != data.loc[:, [
                                           'Observation id', 'Subject']].shift()).any(axis=1).cumsum() - 1
                if start_end == True :
                    str_end_df = data.loc[data['Behavior'] == 'Debut / Fin']
                    str_end_df.loc[:,'repet'] = (str_end_df.loc[:, 'numfocal'] == str_end_df.loc[:, 'numfocal'].shift(1))
                    index = str_end_df.loc[str_end_df['repet'] == True].index
                    for i in index:
                        data.loc[i:,'numfocal'] = data.loc[i:,'numfocal'] + 1
                    # focal length
                    focal_length = data.loc[data['Behavior'] == 'Debut / Fin', ['Duration (s)', 'numfocal']].rename(columns={"Duration (s)": "focal_length"})
                else:
                    # The focal length is calculated by subtracting the end of the last behavior from the beginning of the first.
                    focal_length = (data.groupby('numfocal').max().loc[:, 'Stop (s)'] - data.groupby(
                        'numfocal').first().loc[:, 'Start (s)']).rename('focal_length', inplace=True)
                data = data.merge(focal_length, on='numfocal')
                # The duration of point behaviors is defined as one second and the 'NaN' are converted to caracter strings.
                data.loc[data['Behavior type'] == 'POINT', 'Duration (s)'] = 1
                data = data.fillna('NaN')
                return data

            def correct_behavioral_cat(data):
                """Corrects behavioral categories to align with the reference.

                This function allows all datasets to be put in the same format 
                despite small variations in the way observers in Strasbourg enter behavioral names/categories.
                It works with a user-friendly command line interface detailed in the report.

                If this step has been performed, a summary of the changes is saved in the attribute "behav_cor".

                Parameters
                ----------
                data : dataframe
                    The dataset of interest.

                Returns
                -------
                data : dataframe
                    The updated dataset.
                """

                if 'correct_behavioral_cat' not in ignore:

                    # The reference is charged in a local variable.
                    reference_behavior_table = self.reference_behavior_table.copy(
                        deep=True)

                    def find_diff(data):
                        """Helper function, returns a table of behavioral category 
                        differences between the dataset and the reference."""

                        # Behaviors and their behavioral categories are retrieved.
                        behavior_table_data = data.groupby('Behavior')[['Behavioral category']].first(
                        ).sort_values(['Behavioral category', 'Behavior'])
                        behavior_table_data.reset_index(inplace=True)
                        behavior_table_data = pd.concat(
                            {'data': behavior_table_data}, names=['origin'])
                        # Rows that are not identical between the reference and the data are recovered.
                        data_ref_diff = pd.concat(
                            [behavior_table_data, reference_behavior_table]).drop_duplicates(keep=False)
                        return data_ref_diff

                    def view_input():
                        """ Helper function, produces the graphical interface and 
                        records the changes to be made."""

                        # Print the differences with an index
                        print('DataIndex : ' + column + '\n'
                              '======================= \n')
                        for i in range(len(cat_data)):
                            print(str(i) + ' : ' + cat_data[i])
                        print('\n \n RefIndex : ' + column + '\n'
                              '======================= \n')
                        for i in range(len(cat_ref)):
                            print(str(i) + ' : ' + cat_ref[i])
                        # The matches entered by the user are retrieved.
                        changes = input('Which DataIndex goes with which RefIndex?  \n'
                                        '(Insert as "DataIndex:RefIndex DataIndex:RefIndex etc.") \n')
                        changes = list(
                            map(lambda x: list(map(int, x.split(':'))), changes.split(' ')))
                        changes = list(
                            map(lambda x: [cat_data[x[0]], cat_ref[x[1]]], changes))
                        return changes

                    behavioralcat_change_list = {}
                    data_ref_diff = find_diff(data)
                    # If the behavioral categories are already like reference
                    if 'data' not in data_ref_diff.index.get_level_values(0):
                        print('\n Behavioral categories already like reference')
                    else:
                        # Changes are made for behaviors/behavioral categories.
                        for column in reversed(list(data_ref_diff.columns)):
                            cat_data = data_ref_diff.loc['data', column].unique(
                            )
                            cat_ref = data_ref_diff.loc['ref', column].unique()
                            changes = view_input()
                            behavioralcat_change_list[column] = changes
                            dictchange = {changes[0]: changes[1]
                                          for changes in changes}
                            data = data.replace(dictchange)
                            data_ref_diff = find_diff(data)
                        # We proceed in the same way for the cases where the behaviors are not associated to the same categories in the two tables.
                        behav_pairs = data_ref_diff['Behavior'] + \
                            ' / ' + data_ref_diff['Behavioral category']
                        cat_data = behav_pairs.loc['data'].unique()
                        cat_ref = behav_pairs.loc['ref'].unique()
                        changes = view_input()
                        behavioralcat_change_list['behav_pairs'] = changes
                        for i in changes:
                            data.loc[(data[['Behavior', 'Behavioral category']] == i[0].split(
                                ' / ')).all(axis='columns'), 'Behavioral category'] = i[1].split(' / ')[1]
                    # The differences remaining at the end of the analysis are also saved.
                    behavioralcat_change_list['Unmatched'] = find_diff(
                        data)
                    self.behav_cor = behavioralcat_change_list
                return data

            def new_behavioral_cat(data):
                """Create the new behavioral categories.

                This function creates a "Behavioral category II" column that associates each behavior
                with a new behavioral category, without overwriting the previous "Behavioral category" column. 
                The "Behavior/New Behavioral Category" mapping table is detailed in the report. 

                Parameters
                ----------
                data : dataframe
                    The dataset of interest.

                Returns
                -------
                data : dataframe
                    The updated dataset.
                """

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
                return data

            def empty_col(data, check=check_empty_col):
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

                if 'empty_col' not in ignore:

                    # The supposed empty columns names are charged in a local variable.
                    empty_col_names = [
                        'Description', 'FPS', 'Comment start', 'Comment stop', 'Media file']
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
                    # The content of the deleted columns is saved separately.
                    self.empty_col_values = empty_col_values
                return data

            # The different functions are applied to the input.
            data = empty_col(new_behavioral_cat(
                correct_behavioral_cat(order_data(path, start_end))))

            # If specified, the dataset is saved.
            if save:
                data.to_csv(path_or_buf=save)

        return data

    def filtering(self, ignore=(), grooming_see=False, non_visible_see=False, short_focal_preprocessing_see=False, non_visible_treshold=400, lag_method='y', non_visible_method=3, short_focal_threshold=20, save=None):
        """Complete the cleaning.

        This method is recommended for the first use of a dataset.
        This additional cleaning is done in several steps, all optional 
        (choice specified by the user with the "ignore" parameter):
        1. A correction of the format of the grooming observations can be done with the internal function "grooming".
        2. The way to handle non-visible durations can be modified with the internal function "non-visible".
        3. Abnormal repetitions can be removed with the internal function "repetition_preprocessing".
        4. Abnormally short focals can be suppressed with the internal function "short_focal_preprocessing".
        5. Abnormal negative duration lines are supressed.
        6. The table can be saved to be used as input for future analyses ("save" parameter).

        The new version of the cleaned dataset is updated directly in the "data" attribute at each step.
        The deleted rows of each step are also successively added in the 'error_line' attribute.

        Parameters
        ----------
        ignore : tuple of (str,), optional
            Steps that the user wants to skip among 
            {'grooming', 'non-visible' , 'repetition', 'short_focal'}. The default is ().
        grooming_see : bool, optional
            Specifies whether to display the grooming lines deleted 
            during the 'grooming' step. The default is False.
        non_visible_see : bool, optional
            Specifies whether to display the 'non-visible' step plots.  The default is False.
        short_focal_preprocessing_see : bool, optional
            Specifies whether to display the 'short_focal_preprocessing' step plots. The default is False.
        non_visible_treshold : int, optional
            Threshold (in seconds) above which lags are considered non-visible. The default is 400.
        lag_method : str, optional
            Method of non-visible duration computation. The default is 'y'.
        non_visible_method : int, optional
            Method of focal length computation. The default is 3.
        short_focal_threshold : int, optional
            Threshold (in seconds) above which focals are considered too short. The default is 20.
        save : str, optional
            Saving path. The default is None.

        Returns
        -------
        None.
        """

        def grooming(see_error):
            """Reformatting and removal of unnecessary grooming lines.

            Because of the possibility of multiple simultaneous observations, 
            the researchers chose a particular format to save the grooming data (see report).
            This function converts the grooming observations into a usable format and deletes the lines that correspond to format errors.
            It also provides the possibility for the user to display the deleted 
            lines ('grooming_see' parameter in filtering).

            The new version of the cleaned dataset is updated directly in the "data" attribute.
            The deleted rows are added in the 'error_line' attribute.

            Parameters
            ----------
            see_error : bool
                Specifies whether to display the deleted lines. 

            Returns
            -------
            None.

            """

            if 'grooming' not in ignore:

                # The data and raw data are charged in local variables.
                data = self.data.copy(deep=True)
                raw_data = self.raw_data.copy(deep=True)

                # Formatting of data in a grooming table (Step1).
                # Columns of interest are maintained.
                grooming = data.drop(columns=data.loc[:, [
                                     'Observation date', 'Observation id', 'Total length', 'Behavioral category', 'Behavior type', 'Duration (s)']])
                # Rows of interest are maintained.
                grooming = grooming.loc[grooming['Behavior'].isin(
                    ['1 Debut Grooming', '2 Zone de Grooming', '4 Fin Grooming'])]
                # Lines with 'None' are deleted.
                grooming = grooming.drop(
                    grooming.loc[grooming['Modifiers'] == 'None'].index)
                # Reformatting the content of the Modifiers column.
                grooming.loc[:, 'autreindiv'] = grooming.apply(lambda row: row.Modifiers if (
                    row.Behavior == '1 Debut Grooming') else np.nan, axis=1)
                # correction des directions = None
                grooming = grooming.drop(pd.Series(grooming.loc[grooming['Behavior'] ==
                                                                '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[0]).where(lambda x: x == 'None').dropna().index)
                grooming.loc[:, 'direction'] = grooming.apply(lambda row:  re.search(
                    "Focal est (.*?)\|", row.Modifiers).group(1) if (row.Behavior == '2 Zone de Grooming') else np.nan, axis=1)
                # Correction des fin grooming multiples
                grooming.loc[(grooming['Behavior'] == '4 Fin Grooming')
                             & (["," in i for i in grooming['Modifiers']]), 'Modifiers'] = grooming.loc[(grooming['Behavior'] == '4 Fin Grooming')
                                                                                                        & (["," in i for i in grooming['Modifiers']]), 'Modifiers'].str.split(",")
                grooming = grooming.explode('Modifiers')
                # correction des ind = None
                grooming = grooming.drop(pd.Series(grooming.loc[grooming['Behavior'] ==
                                                                '2 Zone de Grooming', 'Modifiers'].str.split("|", expand=True)[2]).where(lambda x: x == 'None').dropna().index)
                grooming.loc[:, 'numgroom'] = grooming.apply(lambda row:  int(row.Modifiers.split("Ind ")[1]) if (
                    row.Behavior == '2 Zone de Grooming' or row.Behavior == '4 Fin Grooming') else np.nan, axis=1)
                grooming.drop(columns='Modifiers', inplace=True)
                # Zone changes are not taken into account.
                check = ((grooming.Behavior == '2 Zone de Grooming') &
                         (grooming.shift(-1).Behavior == '2 Zone de Grooming') &
                         (grooming.numgroom == grooming.shift(-1).numgroom) &
                         (grooming.direction == grooming.shift(-1).direction)).shift()
                grooming = grooming.drop(
                    check.dropna()[check.dropna()].index).reset_index()
                # Setting up of the "Start_observation" lines  (Step2)
                check = ((grooming['Behavior'] == '1 Debut Grooming') &
                         (grooming.shift(-1)['Behavior'] == '2 Zone de Grooming') &
                         (grooming['numfocal'] == grooming.shift(-1)['numfocal']))
                grooming.loc[check[check].index, ['direction', 'numgroom']] = grooming.loc[(
                    check[check].index)+1, ['direction', 'numgroom']].values
                grooming.loc[check[check].index,
                             'Behavior'] = 'Start_observation'
                grooming = grooming.drop(
                    (check[check].index)+1).reset_index(drop=True)
                invalid_grooming = list(
                    grooming.loc[grooming['Behavior'] == '1 Debut Grooming', 'index'])
                modifline = pd.DataFrame()
                # Iteratively for each numgroom.
                for a in list(dict.fromkeys(grooming['numgroom'])):
                    grooming_iterate = grooming.loc[grooming['numgroom'] == a].reset_index(
                        drop=True)
                    # Simple case (Step3).
                    check = ((grooming_iterate['Behavior'] == 'Start_observation') &
                             (grooming_iterate.shift(-1)['Behavior'] == '4 Fin Grooming') &
                             (grooming_iterate['numfocal'] == grooming_iterate.shift(-1)['numfocal']))
                    grooming_iterate.loc[check[check].index, 'Stop (s)'] = grooming_iterate.loc[(
                        check[check].index)+1, 'Stop (s)'].values
                    grooming_iterate.loc[check[check].index,
                                         'Behavior'] = 'Finished'
                    grooming_iterate = grooming_iterate.drop(
                        (check[check].index)+1).reset_index(drop=True)
                    # Complex case (Step4).
                    check = grooming_iterate['Behavior'] == 'Start_observation'
                    for i in check[check].index:
                        autreindiv = grooming_iterate.loc[i, 'autreindiv']
                        end = False
                        n = i
                        while end == False:
                            # cas ou start observation est à la fin
                            if n == len(grooming_iterate) - 1:
                                end = True
                            elif grooming_iterate.loc[n+1, 'Behavior'] == '2 Zone de Grooming':
                                grooming_iterate.loc[n+1,
                                                     'autreindiv'] = autreindiv
                                grooming_iterate.loc[n+1,
                                                     'Behavior'] = 'intermediate'
                                grooming_iterate.loc[n,
                                                     'Stop (s)'] = grooming_iterate.loc[n + 1, 'Stop (s)']
                                n += 1
                            elif grooming_iterate.loc[n+1, 'Behavior'] == '4 Fin Grooming':
                                grooming_iterate.loc[n,
                                                     'Stop (s)'] = grooming_iterate.loc[n+1, 'Stop (s)']
                                grooming_iterate.loc[i:n,
                                                     'Behavior'] = 'Finished'
                                grooming_iterate = grooming_iterate.drop(n+1)
                                end = True
                            else:
                                end = True
                    modifline = pd.concat(
                        (modifline, grooming_iterate)).sort_values(by='index')
                invalid_grooming = invalid_grooming + \
                    (list(
                        modifline.loc[modifline['Behavior'] != 'Finished', 'index']))
                # The modfline dataframe is adjusted.
                modifline.loc[:, 'Duration (s)'] = modifline.loc[:,
                                                                 'Stop (s)'] - modifline.loc[:, 'Start (s)']
                modifline.loc[:, 'Modifiers'] = 'Focal est ' + modifline.loc[:,
                                                                             'direction'] + '|' + modifline.loc[:, 'autreindiv']
                modifline = modifline.set_index('index')
                # The original dataset is adjusted (Step5).
                data.loc[modifline.index, ['Start (s)', 'Stop (s)', 'Duration (s)', 'Modifiers']] = modifline.loc[:, [
                    'Start (s)', 'Stop (s)', 'Duration (s)', 'Modifiers']].values
                data.loc[modifline.index, 'Behavior'] = 'Grooming'
                data.loc[modifline.index, 'Behavior type'] = 'STATE'
                # Useless lines are deleted.
                data = data.drop(list(set(
                    data.loc[data['Behavioral category'] == '2 Grooming'].index) - set(modifline.index)))
                data.reset_index(drop=True, inplace=True)
                # Display of error lines (optional)
                if see_error == True:
                    pd.set_option('display.max_columns', None)
                    for i in invalid_grooming:
                        print(
                            raw_data.loc[i:i+20, ['Subject', 'Behavior', 'Modifiers', 'numfocal']])
                        input('Press Enter for next')
                    pd.reset_option('^display.', silent=True)

                # Data and error_line are updated in instance attributes.
                self.data = data.copy(deep=True)
                self.error_line['grooming'] = invalid_grooming

        def non_visible(non_visible_treshold, lag_method, non_visible_method, see_error):
            """Recalculate duration of non-visible observations and focal length if necessary.

            Different types of errors can appear when recording non-visible observations (see report).
            This function allows to:
            1. Consider visible lags that are too long.
            2. Adjust the end of non-visible observations.
            3. Choose whether to remove the non-visible duration from the total duration.

            The new version of the cleaned dataset is updated directly in the "data" attribute.
            The deleted rows are added in the "error_line" attribute.

            Parameters
            ----------
            non_visible_treshold : bool
                Threshold (in seconds) above which lags are considered non-visible. 
            lag_method : str
                Method of non-visible duration computation.
            non_visible_method : int
                Method of focal length computation. 
            see_error : bool
                Specifies whether to display the 'non-visible' step plots. 

            Returns
            -------
            None.
            """

            if 'non_visible' not in ignore:

                # The data are charged in a local variable.
                data = self.data.copy(deep=True)
                # Analysis of lags within a focal.
                # The basic data are retrieved.
                between_lines = data.loc[:, [
                    'numfocal', 'Behavior', 'Start (s)', 'Stop (s)', 'Duration (s)', 'focal_length']]
                between_lines.loc[:, 'debutlignesuivante'] = between_lines.loc[:,
                                                                               'Start (s)'].shift(-1)
                # Lag computation.
                between_lines.loc[:, 'lag'] = between_lines.loc[:,
                                                                'debutlignesuivante'] - between_lines.loc[:, 'Start (s)']
                # We correct the lag and the beginning of the next line in the cases where consecutive lines are not in the same focus.
                between_lines.loc[:, 'index'] = between_lines.index
                between_lines.loc[:, 'last_line'] = between_lines.loc[:, 'index'].isin(
                    between_lines.groupby('numfocal').last().loc[:, 'index'])
                between_lines.loc[between_lines['last_line'], ['lag', 'debutlignesuivante']
                                  ] = between_lines.loc[between_lines['last_line'], ['Duration (s)', 'Stop (s)']].values
                # Graphic representation for visible behaviors (step1).
                if see_error == True:
                    plt.figure()
                    plt.boxplot(
                        between_lines.loc[between_lines['Behavior'] != 'Non-visible', 'lag'].dropna())
                    plt.title('"Visible observation" lags')
                    plt.xticks([])
                    plt.show()
                    non_visible_treshold = input(
                        'what threshold do you want ? ( "None" for no threshold) \n')
                # The visible behavior with a lag above threshold are considered non-visile.
                if non_visible_treshold != 'None':
                    check = ((between_lines.loc[:, 'Behavior'] != "Non-visible") & (
                        between_lines.loc[:, 'lag'] > int(non_visible_treshold)))
                    data.loc[check[check].index, 'Behavior'] = 'Non-visible'
                    between_lines.loc[check[check].index,
                                      'Behavior'] = 'Non-visible'
                    # The indices of the modified lines are saved separately.
                    invalid_non_visible = list(check[check].index)
                # The non-visible are then preprocessed.
                between_nv_lines = between_lines.loc[between_lines['Behavior']
                                                     == 'Non-visible']
                # The difference between the lag and the recorded time is calculated.
                comp = between_nv_lines.loc[:, 'lag'] - \
                    between_nv_lines.loc[:, 'Duration (s)']
                between_nv_lines = between_nv_lines.assign(comp=comp)
                # The table used to choose the method to use is then constructed.
                nv_table = pd.DataFrame()
                # Recorded non-visible time per focal.
                nv_table.loc[:, 'non_visible_length'] = between_nv_lines.groupby('numfocal')[
                    'Duration (s)'].sum()
                nv_table = nv_table.merge(between_nv_lines.groupby('numfocal')[
                                          'focal_length'].last(), on='numfocal')  # Focal length.
                # New focal length without the recorded non-visible lines.
                nv_table.loc[:, 'diff'] = nv_table.loc[:,
                                                       'focal_length'] - nv_table.loc[:, 'non_visible_length']
                # Recalculated non-visible time per focal (with lag).
                nv_table.loc[:, 'non_visible_length2'] = between_nv_lines.groupby('numfocal')[
                    'lag'].sum()
                # New focal length without the recalculated non-visible.
                nv_table.loc[:, 'diff2'] = nv_table.loc[:,
                                                        'focal_length'] - nv_table.loc[:, 'non_visible_length2']
                # Graphical representation (optional).
                if see_error == True:
                    plt.figure()
                    plt.boxplot(between_nv_lines.loc[:, 'comp'].dropna())
                    plt.title('inter-behavior timelength following non-visible')
                    plt.xticks([])
                    plt.show()
                    # Input given by the user.
                    lag_method = input(
                        'Do you want to correct non-visible duration (y/n) \n')
                    # The method comparison plots are drawn.
                    fig, axs = plt.subplots(1, 3)
                    axs[0].hist(nv_table.loc[:, 'focal_length'])
                    axs[0].set_title('Focal lengths', fontdict={'fontsize': 8})
                    axs[1].hist(nv_table.loc[:, 'diff'])
                    axs[1].set_title('After non-visible removal' , fontdict={'fontsize': 8})
                    axs[2].hist(nv_table.loc[:, 'diff2'])
                    axs[2].set_title(
                        'After corrected non-visible removal', fontdict={'fontsize': 8})
                    plt.show()
                    # Input given by the user.
                    non_visible_method = int(input(
                        'What method do you want to use ? ( 1 = no changes, 2 = non-visible removal, 3= corrected non-visible removal) \n'))
                # The data is modified according to the user's choice.
                if lag_method == 'y':
                    # The values of the non visible durations are replaced.
                    data.loc[between_nv_lines.index, ['Duration (s)', 'Stop (s)']] = between_nv_lines.loc[:, [
                        'lag', 'debutlignesuivante']].values
                if non_visible_method == 2:
                    data.loc[:, 'focal_length'] = data.apply(
                        lambda row: nv_table.loc[row.numfocal, 'diff'] if row.numfocal in nv_table.index else row.focal_length, axis=1)
                if non_visible_method == 3:
                    data.loc[:, 'focal_length'] = data.apply(
                        lambda row: nv_table.loc[row.numfocal, 'diff2'] if row.numfocal in nv_table.index else row.focal_length, axis=1)

                # Data and error_line are updated in instance attributes.
                self.data = data.copy(deep=True)
                if non_visible_treshold != 'None':
                    self.error_line['non-visible'] = invalid_non_visible

        def repetition_preprocessing():
            """Supress duplicated "5 Proximite" lines. 

            If there are several consecutive proximity measures, they are considered as misclick and deleted.

            The new version of the cleaned dataset is updated directly in the "data" attribute.
            The deleted rows are added in the "error_line" attribute.

            Returns
            -------
            None.
            """

            if 'repetition' not in ignore:

                # The data are charged in a local variable.
                data = self.data.copy(deep=True)

                # The data are retrieved without time markers.
                repet = data.drop(
                    columns=['Start (s)', 'Stop (s)', 'Duration (s)'])
                # The indices of the duplicated lines are recovered and the lines are supressed.
                repet = ((repet == repet.shift(-1)).all(axis=1)
                         ) & (repet.loc[:, 'Behavioral category'] == '5 Proximite')
                invalid_repet = list(repet[repet].index + 1)
                data = data.drop(invalid_repet)

                # Data and error_line are updated in instance attributes.
                self.data = data.copy(deep=True)
                self.error_line['repet'] = invalid_repet

        def short_focal_preprocessing(short_focal_threshold, see_error):
            """Supress short focals.

            This function allows to observe the number of focals per individual and the 
            distribution of focal lengths, and to remove focals that are too short.

            The new version of the cleaned dataset is updated directly in the "data" attribute.
            The deleted rows are added in the "error_line" attribute.

            Parameters
            ----------
            short_focal_threshold : int
                Threshold (in seconds) under which focals are considered too short.
            see_error : bool
                Specifies whether to display the 'short_focal_preprocessing' step plots.

            Returns
            -------
            None.
            """

            if 'short_focal' not in ignore:

                # The data and are charged in a local variable.
                data = self.data.copy(deep=True)

                # The number of focal per individual is calculated.
                nb_focal_ind = dict.values(
                    Counter(data.groupby('numfocal').first().loc[:, 'Subject']))
                # The individual length is calculated.
                time_indiv = data.groupby('Observation id').first().groupby('Subject').sum(numeric_only = True).loc[:,'focal_length']
                # The focal lengths are retrieved.
                focal_length = data.groupby('numfocal')['focal_length'].first()
                # Graphical representation (optional).
                if see_error == True:
                    fig, axs = plt.subplots(1, 3)
                    axs[0].boxplot(nb_focal_ind)
                    axs[0].set_title('Number of focal per-individual', fontdict={'fontsize': 8})
                    axs[0].set_xticks([])
                    axs[1].boxplot(time_indiv)
                    axs[1].set_title("Observation length per each individual", fontdict={'fontsize': 8})
                    axs[1].set_xticks([])
                    axs[2].boxplot(focal_length)
                    axs[2].set_title('Focal length', fontdict={'fontsize': 8})
                    axs[2].set_xticks([])
                    plt.show()
                    short_focal_threshold = input(
                        'what threshold do you want ? ( "None" for no threshold) \n')
                # Supression of the short focals.
                if short_focal_threshold != 'None':
                    check = data.loc[:, 'focal_length'] < int(
                        short_focal_threshold)
                    invalid_focal_length = list(check[check].index)
                    data = data.drop(check[check].index)

                # Data and error_line are updated in instance attributes.
                self.data = data
                if short_focal_threshold != 'None':
                    self.error_line['focal_length'] = invalid_focal_length

        # The different functions are applied to the input.
        grooming(grooming_see)
        non_visible(non_visible_treshold, lag_method,
                    non_visible_method, non_visible_see)
        repetition_preprocessing()
        short_focal_preprocessing(
            short_focal_threshold, short_focal_preprocessing_see)
        # The abnormal negative duration lines are supressed and saved in error_line.
        neg = self.data['Duration (s)'] < 0
        self.data = self.data.drop(neg[neg].index)
        self.error_line['abnormal_neg'] = list(neg[neg].index)
        # The index is adjusted.
        self.data = self.data.reset_index(drop=True)
        self.data.loc[:, 'numfocal'] = (self.data.loc[:, 'numfocal'] != self.data.loc[:, 'numfocal'].shift(
        )).cumsum() - 1  # on redefinit numfocal suite à supression

        # If specified, the dataset is saved.
        if save:
            self.data.to_csv(path_or_buf=save)