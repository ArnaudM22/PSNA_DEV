# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:36:42 2023

@author: arnaud.maupas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import glob
from collections import Counter

import Modules.focal_cleaning as clean
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
            data = clean.order_data(path, start_end)
            if 'correct_behavioral_cat' not in ignore:
                data, self.behav_cor = clean.correct_behavioral_cat(data, self.reference_behavior_table)
            data = clean.new_behavioral_cat(data)
            if 'empty_col' not in ignore:
                data, self.empty_col_value = clean.empty_col(data, check = True)
                
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
        #create index col that will be useful to keep track of the changes.
        self.data.loc[:,'raw_index'] = self.data.index
        
        # The different functions are applied to the input.
        if 'grooming' not in ignore:
            self.data, self.error_line['grooming'] = clean.grooming(self.data.copy(deep=True), see_error = grooming_see, raw_data = self.raw_data.copy(deep=True))
        if 'non_visible' not in ignore:
            self.data, self.error_line['non-visible'] = clean.non_visible(self.data.copy(deep=True), non_visible_treshold, lag_method, non_visible_method, non_visible_see)
        if 'repetition' not in ignore:
            self.data, self.error_line['repet'] = clean.repetition_preprocessing(self.data.copy(deep=True))
        if 'short_focal' not in ignore:
            self.data, self.error_line['focal_length'] = clean.short_focal_preprocessing(self.data.copy(deep=True), short_focal_threshold, short_focal_preprocessing_see)
                    
        ###
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
            
        
        
            