# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:28:01 2023

@author: arnau
"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.colors as mcolors
import random
import math
from matplotlib.patches import Rectangle



def plot_colortable(colors, *, ncols=4, sort_colors=True):

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        names = sorted(
            colors, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
    else:
        names = list(colors)

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7')
        )

    return fig

def datastream_viz(data, n_line, n_column, behav_col='Behavior', col_list=None):
    # liste de comportements d'interet
    behav_li = sorted(list(dict.fromkeys(data.loc[:, behav_col])))
    if col_list == None:
        # random choice of colors
        col_list = list(mcolors.CSS4_COLORS.values())
        random.shuffle(col_list)
        col_list[:len(behav_li)]
    col_dict = {behav_li[i]: col_list[i] for i in range(len(behav_li))}
    # plot legend
    plot_colortable(col_dict, ncols=3, sort_colors=False)
    plt.show()
    # The data and individual list are charged in local variables to facilitate debugging.
    indiv = sorted(tuple(dict.fromkeys(data.loc[:, 'Subject'])))

    # A "plot_data" table is initialized.
    iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
        dict.fromkeys(data.loc[:, behav_col]))]  # Index content.
    # Index initialization.
    index = pd.MultiIndex.from_product(
        iterables, names=['numfocal', behav_col])
    plot_data = pd.DataFrame(index=index)  # initialiser dataframe
    # The data to plot are calculated.
    # Number of occurence.
    nbr_occur = data.groupby(
        ['numfocal', behav_col]).size().rename('nbr_occur')
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
        ['Subject', behav_col]).sum()  # on somme
    # For pei charts
    plt.rcParams.update({'font.size': 8,
                         'axes.titlepad': 0})
    plot_indiv_data = plot_indiv_data.unstack(level=0)
    plot_indiv_data.plot(kind='pie', subplots=True, layout=(
        n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='', colors=col_list)  # plot pour indiv
    plt.rcParams.update(plt.rcParamsDefault)
    # For stacked bar plots.
    fig, axs = plt.subplots(n_line, n_column)
    l = 0
    for a in range(n_line):
        for b in range(n_column):
            if l < (len(indiv)):
                plot_data2 = plot_data.loc[plot_data.index.get_level_values(
                    'Subject') == indiv[l]].unstack(level=1)
                plot_data2.plot(
                    ax=axs[a, b], kind='bar', stacked=True, legend=False, xlabel='', fontsize=2, color=col_list)  # Plot construction.
                # xticks Parameters.
                axs[a, b].tick_params(
                    axis='both', labelbottom=False, bottom=False, which='major', pad=0)
                # Title parameters.
                axs[a, b].set_title(indiv[l], pad=0, fontsize=10)
                l += 1
            else:
                axs[a, b].axis('off')
    plt.show()

def behavior_table_construction(data, see_table):
    """Builds the behavioral table"""

    # The qualitative version of the behaviorial table is built.
    behavior_table = data.groupby(
        'Behavior')[['Behavioral category', 'Behavioral category 2']].first()
    # The number of occurence of the behaviors and behavioral categories is added.
    behavior_table.insert(0, 'n', behavior_table.index)
    behavior_table.loc[:, 'n'] = behavior_table.apply(
        lambda row:  str(Counter(data.loc[:, 'Behavior'])[row.n]), axis=1)
    behavior_table.loc[:, 'Behavioral category'] = behavior_table.apply(
        lambda row: row['Behavioral category'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category'])[row['Behavioral category']]), axis=1)
    behavior_table.loc[:, 'Behavioral category 2'] = behavior_table.apply(
        lambda row: row['Behavioral category 2'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category 2'])[row['Behavioral category 2']]), axis=1)
    # Table displaying (optional).
    if see_table == True:
        print(behavior_table)
    return behavior_table

'''dev tests
def time_budg_construction(data, n_line, n_column):
    """"Builds the set of pie charts and stacked bar plot"""

    # The data and individual list are charged in local variables to facilitate debugging.
    indiv = tuple(dict.fromkeys(data.loc[:, 'Subject']))

    # A "plot_data" table is initialized.
    iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
        dict.fromkeys(data.loc[:, 'Behavioral category 2']))]  # Index content.
    # Index initialization.
    index = pd.MultiIndex.from_product(
        iterables, names=['numfocal', 'Behavioral category 2'])
    plot_data = pd.DataFrame(index=index)  # initialiser dataframe
    # The data to plot are calculated.
    # Number of occurence.
    nbr_occur = data.groupby(
        ['numfocal', 'Behavioral category 2']).size().rename('nbr_occur')
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
        ['Subject', 'Behavioral category 2']).sum()  # on somme
    # For pei charts
    plt.rcParams.update({'font.size': 8,
                         'axes.titlepad': 0})
    plot_indiv_data.unstack(level=0).plot(kind='pie', subplots=True, layout=(
        n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='')  # plot pour indiv
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


def visualisation(data, n_line, n_column, see_table=False):
    """Performs basic exploratory visualizations.

    This function allows to build :
    1. A table of behaviors with all the behaviors, their number of occurrences, 
    their behavioral categories (type I and II, with each time the corresponding number of occurrences).
    2. A set of piecharts showing the proportion of the number of occurrence of 
    each behavioral category (type II) for each individual.
    3. A set of stacked bar plots for each individual showing the proportion of 
    the number of occurrences of each behavioral category (type II), where each bar represents a focal.   

    Parameters
    ----------
    n_line : int
        Number of lines on the plot.
    n_column : int
        Number of columns on the plot.
    see_table : bool, optional
        Specifies whether to display the behavioral table. The default is False.

    Returns
    -------
    None.
    """

    def behavior_table_construction(data, see_table):
        """Builds the behavioral table"""

        # The qualitative version of the behaviorial table is built.
        behavior_table = data.groupby(
            'Behavior')[['Behavioral category', 'Behavioral category 2']].first()
        # The number of occurence of the behaviors and behavioral categories is added.
        behavior_table.insert(0, 'n', behavior_table.index)
        behavior_table.loc[:, 'n'] = behavior_table.apply(
            lambda row:  str(Counter(data.loc[:, 'Behavior'])[row.n]), axis=1)
        behavior_table.loc[:, 'Behavioral category'] = behavior_table.apply(
            lambda row: row['Behavioral category'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category'])[row['Behavioral category']]), axis=1)
        behavior_table.loc[:, 'Behavioral category 2'] = behavior_table.apply(
            lambda row: row['Behavioral category 2'] + ': n=' + str(Counter(data.loc[:, 'Behavioral category 2'])[row['Behavioral category 2']]), axis=1)
        # Table displaying (optional).
        if see_table == True:
            print(behavior_table)

    def time_budg_construction(data, indiv, n_line, n_column):
        """"Builds the set of pie charts and stacked bar plot"""

        # The data and individual list are charged in local variables to facilitate debugging.
        indiv = etho_obj.indiv
        data = etho_obj.data

        # A "plot_data" table is initialized.
        iterables = [list(dict.fromkeys(data.loc[:, 'numfocal'])), list(
            dict.fromkeys(data.loc[:, 'Behavioral category 2']))]  # Index content.
        # Index initialization.
        index = pd.MultiIndex.from_product(
            iterables, names=['numfocal', 'Behavioral category 2'])
        plot_data = pd.DataFrame(index=index)  # initialiser dataframe
        # The data to plot are calculated.
        # Number of occurence.
        nbr_occur = data.groupby(
            ['numfocal', 'Behavioral category 2']).size().rename('nbr_occur')
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
            ['Subject', 'Behavioral category 2']).sum()  # on somme
        # For pei charts
        plt.rcParams.update({'font.size': 8,
                             'axes.titlepad': 0})
        plot_indiv_data.unstack(level=0).plot(kind='pie', subplots=True, layout=(
            n_line, n_column), legend=False, sharex=False, labels=None, title=indiv, ylabel='')  # plot pour indiv
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

    indiv = tuple(dict.fromkeys(data.loc[:, 'Subject']))

    behavior_table_construction(data, see_table)
    time_budg_construction(data, indiv, n_line, n_column)
'''
'''cleaning visualisation test
def visible_lags(data):
    # Analysis of lags within a focal.
    invalid_non_visible = None
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
    # plot a proprement parler
    plt.figure()
    plt.boxplot(
        between_lines.loc[between_lines['Behavior'] != 'Non-visible', 'lag'].dropna())
    plt.title('"Visible observation" lags')
    plt.xticks([])
    plt.show()'''
