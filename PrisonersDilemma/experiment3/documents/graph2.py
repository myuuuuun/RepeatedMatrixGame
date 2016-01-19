#-*- encoding: utf-8 -*-
"""
Graph func for experiment3
ts_length distribution

Copyright (c) 2015 @myuuuuun
Released under the MIT license.
"""
import math
import numpy as np
import pandas as pd
import functools
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as stats
EPSIRON = 1.0e-8
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 400)
plt.rcParams['font.size'] = 14

# 日本語対応
mpl.rcParams['font.family'] = 'Osaka'


if __name__ == '__main__':

    seed = 282
    discount_v = 0.97
    ts_length = np.random.RandomState(seed).geometric(p=1-discount_v, size=1000)

    print("基本統計量:")
    print(pd.DataFrame(ts_length, columns=["ts_length"]).describe())

    print("\n33.33期未満: {0}%".format(ts_length[ts_length <= 33].size / 10))

    mu = np.mean(ts_length)
    sigma = np.var(ts_length)

    fig, ax = plt.subplots(figsize=(20, 5))
    plt.title("1000セッションの期数の分布")

    # actual histogram
    plt.hist(ts_length, bins=np.max(ts_length)-1, color='#4488FF')

    # theoretical cdf
    x = np.arange(1, np.max(ts_length))
    plt.plot(x, stats.geom.pmf(x, 1-discount_v)*1000, linewidth=2, color='green', label="theoretical cdf(average=33.33)")

    plt.xlabel("ts_length")
    plt.ylabel("number of session")
    ax.text(30, 30, r'''$\mu$={0:.3f}, $\sigma^2$={1:.3f}'''.format(mu, sigma), ha = 'left', va = 'bottom', size=14)
    ax.grid(True)
    ax.axvline(x=mu, linewidth=2, color='red', label="average")
    plt.legend()
    plt.show()
    








