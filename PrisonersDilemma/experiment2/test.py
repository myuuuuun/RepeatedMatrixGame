# -*- coding: utf-8 -*-
from __future__ import division, print_function
import sys
sys.path.append('./user_strategies')
import unittest
import numpy as np
from Iida_perfect_monitoring import Iida_pm
from Iida_imperfect_public import Iida_ipm
from Iida_imperfect_private import Iida_iprm
from kato import KatoStrategy


class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.Strategies = [Iida_pm, Iida_ipm, Iida_iprm, KatoStrategy] # ここに自作のclassを入れる
        self.case1 = "Signal is empty(period 1)"
        self.case2 = [0, 1]
        self.case3 = [1, 0]
        self.case4 = [0, 1, 0, 1, 0, 0, 1]

        self.seed = 11451
        self.RandomState = np.random.RandomState(self.seed)


    # case1を引数に渡してテスト
    def test1(self):
        print("testcase:", self.case1)
        for Strategy in self.Strategies:
            rst = Strategy(self.RandomState).play()
            self.assertIn(rst, (0, 1))


    # case2を引数に渡してテスト
    def test2(self):
        print("testcase:", self.case2)
        for Strategy in self.Strategies:
            S = Strategy(self.RandomState)
            S.get_signal(self.case2)
            rst = S.play()
            self.assertIn(rst, (0, 1))


    # case3を引数に渡してテスト
    def test3(self):
        print("testcase:", self.case3)
        for Strategy in self.Strategies:
            S = Strategy(self.RandomState)
            for signal in self.case3:
                S.get_signal(signal)
            
            rst = S.play()
            self.assertIn(rst, (0, 1))


    # case4を引数に渡してテスト
    def test4(self):
        print("testcase:", self.case4)
        for Strategy in self.Strategies:
            S = Strategy(self.RandomState)
            for signal in self.case4:
                S.get_signal(signal)
                rst = S.play()
            
            self.assertIn(rst, (0, 1))


if __name__ == '__main__':
    import sys
    import nose

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)

