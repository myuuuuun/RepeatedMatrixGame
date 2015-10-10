# -*- coding: utf-8 -*-
from __future__ import division, print_function
import unittest
from random import randint
import sample

import ikegami
import tsuyoshi
import bocchan
import oyama
import ymagishi_pd
import ogawa_prison
import beelab
import kato
import oyataku


class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.funcs = [ikegami.ikegami, tsuyoshi.allD, bocchan.Iida_tit, oyama.oyama, ymagishi_pd.yamagishi_pd, ogawa_prison.ogaway, beelab.ohno, kato.tit_for_tat, oyataku.random_strategy] # ここに自作の関数を入れる
        self.case1 = [], []
        self.case2 = [0], [1]
        self.case3 = [0, 1, 1], [1, 0, 0]
        self.case4 = [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        self.case5 = [randint(0, 1) for x in range(10001)], [randint(0, 1) for x in range(10001)]


    # case1を引数に渡してテスト
    def test1(self):
        print("testcase:", self.case1)
        for func in self.funcs:
            rst = func(self.case1[0], self.case1[1])
            self.assertIn(rst, (0, 1))


    # case2を引数に渡してテスト
    def test2(self):
        print("testcase:", self.case2)
        for func in self.funcs:
            rst = func(self.case2[0], self.case2[1])
            self.assertIn(rst, (0, 1))


    # case3を引数に渡してテスト
    def test3(self):
        print("testcase:", self.case3)
        for func in self.funcs:
            rst = func(self.case3[0], self.case3[1])
            self.assertIn(rst, (0, 1))


    # case4を引数に渡してテスト
    def test4(self):
        print("testcase:", self.case4)
        for func in self.funcs:
            rst = func(self.case3[0], self.case3[1])
            self.assertIn(rst, (0, 1))


    # case5を引数に渡してテスト
    def test5(self):
        print("testcase: randomint")
        for func in self.funcs:
            rst = func(self.case3[0], self.case3[1])
            self.assertIn(rst, (0, 1))


if __name__ == '__main__':
    import sys
    import nose

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)

