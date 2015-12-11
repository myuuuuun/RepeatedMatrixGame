#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
Copyright (c) 2015 @myuuuuun
Released under the MIT license.
"""
import math
import numpy as np
import pandas as pd
import functools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
EPSIRON = 1.0e-8
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_columns', 130)
pd.set_option('display.width', 1400)


if __name__ == '__main__':
    rounds = 1000 * 2
    strategies = 24
    max_ts = 100

    # 読み込み
    df = pd.read_csv('./contest4/data/set_result.csv', index_col=[0, 1], header=[0, 1])


    # 行: プレイヤー, 列: 1000*2セッション分の平均利得
    average_matrix = np.zeros((rounds*(strategies-1), strategies), dtype=float)

    for s in range(1, strategies+1):
        for i, opponent in enumerate(df[str(s)].columns.values):
            average_matrix[i*rounds:(i+1)*rounds, s-1] = df[str(s)][str(opponent)]

    
    av_df = pd.DataFrame(average_matrix, columns=list(range(1, strategies+1)))
    print(av_df.describe())

    

    averages = np.zeros(strategies, dtype=float)
    stds = np.zeros(strategies, dtype=float)
    ranking = np.zeros(strategies, dtype=int)
    for i in range(strategies):
        averages[i] = average_matrix[:, i].mean()
        stds[i] = average_matrix[:, i].std()
    ranking = np.argsort(averages)[::-1]+1

    for i in range(strategies):
        print(np.where(ranking == i+1)[0][0]+1)
    
    """
    fig, ax = plt.subplots()
    bp = ax.boxplot(average_matrix, 0, '')
    plt.grid()
    plt.xlabel('戦略番号')
    plt.ylabel('1セッションの平均利得')
    ax.set_xlim([0, strategies+1])
    ax.set_ylim([-0.1, 5.8])
    plt.title('戦略別, 全セッションの平均利得の分布')
    ax.text(0.4, 5.3, "rank\nave\nstd", ha = 'center', va = 'center', color="black")
    for i in range(strategies):
        ax.text(i+1, 5.3, "{0:.0f}\n{1:.3f}\n{2:.3f}".format(np.where(ranking == i+1)[0][0]+1, averages[i], stds[i]), ha = 'center', va = 'center', color="black")
    plt.show()
    """
   


