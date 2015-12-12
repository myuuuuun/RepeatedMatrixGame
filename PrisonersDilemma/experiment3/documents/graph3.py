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
    strategies = 34
    max_ts = 100

    # 読み込み
    df = pd.read_csv('../contest5/data/set_result.csv', index_col=[0, 1], header=[0, 1])

    # ts_lengthの長い順に並び替え
    ordered_df = df.sortlevel(level="ts_length")

    # 行: プレイヤー, 列: ts_lengthが1〜100期の時の平均利得
    average_matrix = np.zeros((strategies, max_ts), dtype=float)

    for t in range(1, max_ts+1):
        df_t = df.iloc[df.index.get_level_values('ts_length') == t]

        for s in range(1, strategies+1):
            average = df_t[str(s)].mean().mean()
            average_matrix[s-1, t-1] = average

    fig, ax = plt.subplots(figsize=(20, 10))
    plt.title("average payoff trend")
    plt.xlabel("ts_length")
    plt.ylabel("average payoff")
    t_list = [i for i in range(1, max_ts+1)]

    for s in range(1, strategies+1):
        if s in [27, 28, 18, 13, 9, 8]:
            pass
        else:
            average_list = average_matrix[s-1]
            plt.plot(t_list, average_list, color='#bbbbbb')

    plt.plot(t_list, average_matrix[27-1], color='red', linewidth=2, label="27 (20%)")
    plt.plot(t_list, average_matrix[28-1], color='blue', linewidth=2, label="28 (2T2FT)")
    plt.plot(t_list, average_matrix[19-1], color='magenta', linewidth=2, label="19 (TFT)")
    plt.plot(t_list, average_matrix[18-1], color='green', linewidth=2, label="18 (WSLS’)")
    plt.plot(t_list, average_matrix[13-1], color='purple', linewidth=2, label="13 (CCDDDD)")
    plt.plot(t_list, average_matrix[9-1], color='brown', linewidth=2, label="9 (STFT)")
    plt.plot(t_list, average_matrix[8-1], color='orange', linewidth=2, label="8 (HIST)")

    plt.legend()
    plt.show()

   



