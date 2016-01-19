#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''
import math
import numpy as np
import pandas as pd
import functools
import matplotlib.pyplot as plt
import scipy.stats as stats
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=400)
#np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 400)
pd.set_option('display.precision', 3)


# Geo(0.03)から抽出した1000個のサンプルの和の分布を求める
"""
seed = 282
np.random.seed(seed=seed)
rs = np.random.RandomState(seed)
parameter = 0.03
size = 1000
sum_max = 100000
ave = 1/parameter
var = (1-parameter)/parameter**2
sum_x = np.arange(100001)

# 「幾何分布から1000個のサンプルを取り出し、和を取る」
#  ことを10万回繰り返し、シミュレーションで分布を求める
sim_size = 100000
sums = np.zeros(sim_size, dtype=float)
for i in range(sim_size):
    sums[i] = rs.geometric(p=parameter, size=1000).sum()

# 負の二項分布 n=1000, p=0.03
nbin = stats.nbinom.pmf(sum_x-1000, 1000, parameter)

# 正規分布 mu=3333.33, sigma^2=107777.78
normal_ave = size * ave
normal_var = size * var
normal = stats.norm.pdf(x=sum_x, loc=normal_ave, scale=pow(normal_var, 0.5))

# プロット
fig, ax = plt.subplots(figsize=(20, 5))
plt.title("Geo(0.03)から抽出した1000個のサンプルの和S(X)の分布")
plt.plot(sum_x, nbin, linewidth=2, color='blue', label="theoretical pmf(負の二項分布)")
plt.plot(sum_x, normal, linewidth=2, color='orange', label="approx pdf(正規分布)")
plt.hist(sums, bins=100, color='#cccccc', normed=True, label="simulation(size=100000)")
ax.set_xlim([25000, 45000])
plt.xlabel("ts_length(X)")
plt.ylabel("density(f)")
plt.legend()
plt.show()

# 統計量
data = np.zeros((11, 3), dtype=float)

ordered_sum = np.sort(sums)
sim_lower_percent = lambda p: (ordered_sum[sim_size*p-1]+ordered_sum[sim_size*p])/2
data[0, 0] = sums.mean()
data[1, 0] = sums.var()
data[2, 0] = sim_lower_percent(0.01)
data[3, 0] = sim_lower_percent(0.025)
data[4, 0] = sim_lower_percent(0.05)
data[5, 0] = sim_lower_percent(0.1)
data[6, 0] = np.median(sums)
data[7, 0] = sim_lower_percent(0.9)
data[8, 0] = sim_lower_percent(0.95)
data[9, 0] = sim_lower_percent(0.975)
data[10, 0] = sim_lower_percent(0.99)

data[0, 1] = stats.nbinom.mean(1000, parameter) + 1000
data[1, 1] = stats.nbinom.var(1000, parameter)
data[2, 1] = stats.nbinom.interval(0.98, 1000, parameter)[0]+1000
data[3, 1] = stats.nbinom.interval(0.95, 1000, parameter)[0]+1000
data[4, 1] = stats.nbinom.interval(0.9, 1000, parameter)[0]+1000
data[5, 1] = stats.nbinom.interval(0.8, 1000, parameter)[0]+1000
data[6, 1] = stats.nbinom.median(1000, parameter) + 1000
data[7, 1] = stats.nbinom.interval(0.8, 1000, parameter)[1]+1000
data[8, 1] = stats.nbinom.interval(0.9, 1000, parameter)[1]+1000
data[9, 1] = stats.nbinom.interval(0.95, 1000, parameter)[1]+1000
data[10, 1] = stats.nbinom.interval(0.98, 1000, parameter)[1]+1000

data[0, 2] = stats.norm.mean(loc=normal_ave, scale=pow(normal_var, 0.5))
data[1, 2] = stats.norm.var(loc=normal_ave, scale=pow(normal_var, 0.5))
data[2, 2] = stats.norm.interval(0.98, loc=normal_ave, scale=pow(normal_var, 0.5))[0]
data[3, 2] = stats.norm.interval(0.95, loc=normal_ave, scale=pow(normal_var, 0.5))[0]
data[4, 2] = stats.norm.interval(0.9, loc=normal_ave, scale=pow(normal_var, 0.5))[0]
data[5, 2] = stats.norm.interval(0.8, loc=normal_ave, scale=pow(normal_var, 0.5))[0]
data[6, 2] = stats.norm.median(loc=normal_ave, scale=pow(normal_var, 0.5))
data[7, 2] = stats.norm.interval(0.8, loc=normal_ave, scale=pow(normal_var, 0.5))[1]
data[8, 2] = stats.norm.interval(0.9, loc=normal_ave, scale=pow(normal_var, 0.5))[1]
data[9, 2] = stats.norm.interval(0.95, loc=normal_ave, scale=pow(normal_var, 0.5))[1]
data[10, 2] = stats.norm.interval(0.98, loc=normal_ave, scale=pow(normal_var, 0.5))[1]

df = pd.DataFrame(data,
    columns=["シミュレーション", "正確分布", "近似分布"],
    index=["平均", "分散", "下側 1%", "下側 2.5%", "下側 5%", "下側 10%", "中央値", "上側 10%", "上側 5%", "上側 2.5%", "上側 1%"])
print(df)
"""


# 総期数の仮説検定
def two_sided_p(x):
    parameter = 0.03
    med = stats.nbinom.median(1000, parameter) + 1000
    if x <= med:
        for p in np.arange(0, 1.005, 0.005):
            point = stats.nbinom.interval(p, 1000, parameter)[0]+1000
            if point <= x:
                return 1-p 
    else:
        for p in np.arange(0, 1.005, 0.005):
            point = stats.nbinom.interval(p, 1000, parameter)[1]+1000
            if x <= point:
                return 1-p

    raise ValueError


def one_sided_p(x):
    parameter = 0.03
    med = stats.nbinom.median(1000, parameter)+1000
    if x <= med:
        p = stats.nbinom.cdf(x-1000, 1000, parameter)
        return p
    else:
        p = stats.nbinom.cdf(x-1000, 1000, parameter)
        return 1-p 

    raise ValueError


print("尾山ゼミの総期数 S=32856")
print("両側検定でのp値:", two_sided_p(32856))
print("片側検定でのp値:", one_sided_p(32856))
print("")
print("神取ゼミの総期数 S=35510")
print("両側検定でのp値:", two_sided_p(35510))
print("片側検定でのp値:", one_sided_p(35510))

