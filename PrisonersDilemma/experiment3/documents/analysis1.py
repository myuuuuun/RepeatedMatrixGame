#-*- encoding: utf-8 -*-
"""
Analysis1 for experiment3-appendix1
compute trim mean

Copyright (c) 2015 @myuuuuun
Released under the MIT license.
"""
import math
import numpy as np
import pandas as pd
import functools
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
EPSIRON = 1.0e-8
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 400)

# 日本語対応
mpl.rcParams['font.family'] = 'Osaka'

def trim_mean(ts_length, aves, width):
    size = ts_length.size
    hist = {}
    for t in ts_length:
        hist[t] = hist.get(t, 0) + 1

    lower_b = size * (1-width) / 2
    upper_b = size * (1 - (1-width)/2)

    s = 0
    total = 0
    for ts, num in sorted(hist.items()):
        old_s = s
        s += num
        if old_s <= lower_b < s:
            total += (s-lower_b) * aves[ts-1]

        elif old_s <= upper_b < s:
            total += (upper_b-old_s+1) * aves[ts-1]

        elif lower_b <= s <= upper_b:
            total += num * aves[ts-1]

        elif s > upper_b:
            break

    return total / (size * width)


if __name__ == '__main__':
    rounds = 1000 * 2
    strategies = 24
    seed = 282
    rs = np.random.RandomState(seed)
    discount_v = 0.97
    repeat = 1000
    ts_length = rs.geometric(p=1-discount_v, size=1000)
    max_ts = ts_length.max()
    
    # 読み込み
    df = pd.read_csv('./contest4/data/set_result.csv', index_col=[0, 1], header=[0, 1])

    # ts_lengthの長い順に並び替え
    ordered_df = df.sortlevel(level="ts_length")

    # 行: プレイヤー, 列: ts_lengthが1〜max期の時の平均利得
    average_matrix = np.zeros((strategies, max_ts), dtype=float)
    for t in range(1, max_ts+1):
        df_t = df.iloc[df.index.get_level_values('ts_length') == t]
        for s in range(1, strategies+1):
            average = df_t[str(s)].mean().mean()
            average_matrix[s-1, t-1] = average

    for i in range(strategies):
        print(trim_mean(ts_length, average_matrix[i], 0.9))

    






