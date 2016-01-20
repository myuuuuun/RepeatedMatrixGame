# 繰り返し囚人のジレンマゲームの実験3

実験1と同様に、プログラム同士で繰り返し囚人のジレンマゲームをプレイし、どんな戦略が最も大きな利得を得られるかを実験します。 
今回は

1. perfect monitoring
2. imperfect public monitoring
3. imperfect private monitoring（尾山ゼミの戦略のみ）
4. imperfect private monitoring（神取ゼミの戦略のみ）
5. imperfect private monitoring（神取+尾山ゼミ）

の5パターンの実験を行います。

## 実験結果（1月20日更新）

#### 実験結果まとめ（12月30日更新）
* [実験結果（iPython notebook版）](http://nbviewer.ipython.org/github/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/Experiment-2015-11-30.ipynb)  
* [実験結果（pdf版）](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/%E5%B0%BE%E5%B1%B1%E3%82%BC%E3%83%9F%E5%AE%9F%E9%A8%93%E7%B5%90%E6%9E%9C.pdf)  

#### 資料, Appendix（1月20日追加）
* [対戦別平均利得表（自分との対戦無し）(pdf版)](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/%E5%AF%BE%E6%88%A6%E8%A1%A8%EF%BC%88%E8%87%AA%E5%88%86%E3%81%A8%E3%81%AE%E5%AF%BE%E6%88%A6%E7%84%A1%EF%BC%89.pdf)
, [（xlsx版）](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/documents/match_data.xlsx)
* [対戦別平均利得表（自分との対戦有り）(pdf版)](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/%E5%AF%BE%E6%88%A6%E8%A1%A8%EF%BC%88%E8%87%AA%E5%88%86%E3%81%A8%E3%81%AE%E5%AF%BE%E6%88%A6%E6%9C%89%EF%BC%89.pdf)
, [（xlsx版）](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3-appendix1/documents/match_data.xlsx)
* [Appendix1 期数の分布について](http://nbviewer.jupyter.org/github/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/ts_length.ipynb)
* [Appendix2 自分との対戦の有無による結果の比較（pdf版）](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/Appendix2.pdf)

#### Appendix2の元データ（1月20日追加）
* [自分との対戦を許した場合の実験結果（iPython notebook）](http://nbviewer.jupyter.org/github/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3/Experiment-2015-11-30.ipynb)
* [Summary, 基本統計量, タイプ別利得表の集計結果（xlsx）](https://github.com/myuuuuun/RepeatedMatrixGame/blob/master/PrisonersDilemma/experiment3-appendix1/documents/%E5%AF%BE%E6%88%A6%E6%9C%89%E7%84%A1%E6%AF%94%E8%BC%83.xlsx)

## ルール

### 共通ルール
全ての戦略を総当りで対戦させます。それぞれの戦略同士の対戦は、それぞれ1000回の繰り返しゲームから成ります。  
それぞれの対戦では、以下の利得表のstage gameをN期にわたってプレイします。ただしNはゲーム毎に1000通り用意し、全ての戦略同士の対戦で一定とします。  


<table align="center", style="text-align:center;">
  <tr>
    <th>自分の行動, 相手の行動</th>
    <th>行動0（active）</th>
    <th>行動1（inactive）</th>
  </tr>
  <tr>
    <th>行動0（active）</th>
    <td>4, 4</td>
    <td>0, 5</td>
  </tr>
  <tr>
    <th>行動1（inactive）</th>
    <td>5, 0</td>
    <td>2, 2</td>
  </tr>
</table>
  
ゲームを何期続けるかは、以下のルールによって決めます。

1. 第1期は確率1で到来する
2. 以降は毎期末に抽選を行い、**97%の確率でゲームを継続する**  
（これは、無限回繰り返しゲームにおいて現在割引価値を0.97と取ることを意味します）

平均は33.33期になります（第1期は確率1で来るものとします）。

全ての対戦の後、**利得の総和が最も多かったプログラムが勝ち**です。


### ゲームの履歴について

* **perfect monitoring**の場合、各期の終了時に、自分の行動と相手の行動を正確に知ることが出来ます。この履歴に基づいて、次期以降の行動を決定することが出来ます。  


* **imperfect public monitoring**の場合、プレイヤーは各期の終了時、自分の行動と相手の行動を正確に知ることは出来ず、代わりに2人の行動に基づくシグナルが公開されます。
シグナルとは、「プロジェクトの成功確率」のようなもので、{成功, 失敗}の2種類から成ります。自分と相手が(協調, 協調)をとった時にシグナルが成功になる確率が最も高く、
(攻撃, 攻撃)をとった時に成功する確率が最も低くなるように設定します。具体的には
  

成功が出る確率
<table align="center", style="text-align:center;">
  <tr>
    <th>自分の行動 / 相手の行動</th>
    <th>0</th>
    <th>1</th>
  </tr>
  <tr>
    <th>0</th>
    <td>0.9</td>
    <td>0.5</td>
  </tr>
  <tr>
    <th>1</th>
    <td>0.5</td>
    <td>0.2</td>
  </tr>
</table>

とします。したがって、シグナルから相手の実際の行動を予想し、行動を決定することになります。

* **imperfect private monitoring**の場合、プレイヤーは各期の終了時、**相手の行動に関するシグナル**を受け取ります。
このシグナルは2人の間では共有されず、各プレイヤーは相手に関するシグナルだけを見ることが出来ます。
具体的には、ある行動A = (a1, a2)がプレイされた時に発せられるシグナルは、以下の確率分布に従います。  

行: (自分が受け取る相手の行動のシグナル, 相手が受け取る自分の行動のシグナル) /  
列:(自分の実際の行動, 相手の実際の行動)
<table align="center", style="text-align:center;">
  <tr>
    <th></th>
    <th>(0, 0)</th>
    <th>(0, 1)</th>
    <th>(1, 0)</th>
    <th>(1, 1)</th>
  </tr>
  <tr>
    <th>(G, G)</th>
    <td>0.9</td>
    <td>0.02</td>
    <td>0.02</td>
    <td>0.06</td>
  </tr>
  <tr>
    <th>(G, B)</th>
    <td>0.02</td>
    <td>0.06</td>
    <td>0.9</td>
    <td>0.02</td>
  </tr>
  <tr>
    <th>(B, G)</th>
    <td>0.02</td>
    <td>0.9</td>
    <td>0.06</td>
    <td>0.02</td>
  </tr>
  <tr>
    <th>(B, B)</th>
    <td>0.06</td>
    <td>0.02</td>
    <td>0.02</td>
    <td>0.9</td>
  </tr>
</table>

例えば、実際の行動が(自分, 相手) = (0, 0)であった場合、
* 自分がシグナル0, 相手がシグナル0を正しく受け取る確率は0.9
* 自分がシグナル1, 相手がシグナル0を受け取る確率は0.02
* 自分がシグナル1, 相手がシグナル1を受け取る確率は0.06

となります。自分が相手の行動に関して誤ったシグナルを受け取った場合、相手も自分の行動に関して誤ったシグナルを受け取っている可能性が高いことに注意してください。  
( P[相手のシグナルが誤り | 自分のシグナルが誤り] = 0.06 / (0.02 + 0.06) = 3/4 )


## プログラムの仕様
戦略を表現するクラスを作成してください。  
クラスには、次の2つのメソッドを必ず含めてください（メソッド名も下の通りにしてください）。

* play(self): 各期のstage gameにおいて、行動0または1を返すメソッド
* get_signal(self, signal): 各期のstage game終了後、その期のシグナルを受け取るメソッド

### シグナルについて
* perfect monitoringの場合、シグナルは相手の行動そのもの（相手の行動が0なら0, 1なら1）になります。  
* imperfect public monitoringの場合、シグナルとして、プロジェクトが成功した場合0, 失敗した場合1が与えられます。シグナルは上述の確率分布に従って決定されます。  
* imperfect private monitoringの場合、シグナルとして、相手の行動が0だったか1だったかが与えられます。ただし、その行動にはノイズが含まれており、
双方のシグナルは上述の同時確率分布に従って決定されます。


### クラスのテンプレート

以下のようにクラスを作成してください。例として、「基本的には協調するが、前期のシグナルがBadの場合は20%の確率で攻撃する」
ようなクラスを作成します。


```python
# テンプレート
class MyStrategy(object):
    def __init__(self, random_state=None):
        # RandomStateオブジェクトのインスタンスを受け取る
        # 確率変数を使いたい場合は、このインスタンスを使う
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        
        # 自分の行動の履歴
        self.my_history = []
        
        # 過去の全てのシグナル
        self.signals = []


    # 各ステージゲームの実行時に呼び出されるメソッド
    # その期の行動を0（=協調）, または1（=攻撃）のいずれかから選ぶ
    def play(self):
        # 第1期は協調
        if len(self.signals) < 1:
            self.my_history.append(0)
            return 0

        # 前期のシグナル
        prior_signal = self.signals[-1]

        # 前期のシグナルがBadの時、20%の割合でこちらも攻撃する
        epsilon = self.random_state.uniform()
        if epsilon < 0.2 and prior_signal == 1:
            self.my_history.append(1)
            return 1
        
        else:
            self.my_history.append(0)
            return 0


    # 各期のゲーム終了時に呼び出されるメソッド
    def get_signal(self, signal):
        # 前期のゲームのシグナルを受け取る
        # 受け取ったシグナルをシグナルの履歴に追加
        self.signals.append(signal)
```

* \_\_init\_\_()では、RandomStateクラスのインスタンスを受け取ることができるようにしてください。何らかの確率分布を用いて行動を決定する場合は、
再現性を確保するため、このインスタンスのメソッドを使用してください。RandomStateクラスで使用できる確率変数は
[NumPyのドキュメント](http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html)
を参照してください。


他にもいくつか関数例を用意していますので、参考にしてください。->[関数例](./sample.py)

## テスト
テストを用意しました。->[テスト](./test.py)  
iPython notebook上でテストを行いたい場合はこちら->[テスト](./test.ipynb)






