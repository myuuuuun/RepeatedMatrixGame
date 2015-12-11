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
import scipy.stats as stats
EPSIRON = 1.0e-8
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=400)
np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 400)


if __name__ == '__main__':

    seed = 282
    discount_v = 0.97
    ts_length = np.random.RandomState(seed).geometric(p=1-discount_v, size=1000)

    trimmed_ts_length = np.sort(ts_length)[50:950]
    print("基本統計量:")
    print(pd.DataFrame(trimmed_ts_length, columns=["trimmed_ts_length"]).describe())

    print("\n33.33期未満: {0}%".format(trimmed_ts_length[trimmed_ts_length <= 33].size / 10))

    mu = np.mean(trimmed_ts_length)
    sigma = np.var(trimmed_ts_length)

    fig, ax = plt.subplots(figsize=(20, 5))
    plt.title("900セッションの期数の分布")

    # actual histogram
    plt.hist(trimmed_ts_length, bins=np.max(trimmed_ts_length)-1, color='#4488FF')

    # theoretical cdf
    x = np.arange(1, np.max(trimmed_ts_length))
    plt.plot(x, stats.geom.pmf(x, 1-discount_v)*1000, linewidth=2, color='green', label="theoretical cdf(average=33.33)")

    plt.xlabel("trimmed_ts_length")
    plt.ylabel("number of session")
    ax.text(30, 30, r'''$\mu$={0:.3f}, $\sigma^2$={1:.3f}'''.format(mu, sigma), ha = 'left', va = 'bottom', size=14)
    ax.grid(True)
    ax.axvline(x=mu, linewidth=2, color='red')
    plt.legend()
    plt.show()








