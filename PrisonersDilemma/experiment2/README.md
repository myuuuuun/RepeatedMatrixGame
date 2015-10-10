# 繰り返し囚人のジレンマゲームの実験2

実験1と同様に、プログラム同士で繰り返し囚人のジレンマゲームをプレイし、どんな戦略が最も大きな利得を得られるかを実験します。 
今回はperfect monitoring, imperfect public monitoring, imperfect private monitoringの3パターンの実験を行います。

## ルール

### 共通ルール
全てのプログラムを総当りで、それぞれ1000回ずつ対戦させます。それぞれの対戦では、以下の利得表のstage gameをN期にわたってプレイします。ただし、Nは全ゲームで一定とします。

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

* 現在n期とすると、**n+1期が来る確率は97%**（n=0, 1, 2,...）  
（これは、無限回繰り返しゲームにおいて現在割引価値を0.97と取ることを意味します）

平均は97期になります（第1期は確率1で来るものとします）。

全ての対戦の後、**利得の総和が最も多かったプログラムが勝ち**です。


### ゲームの履歴について

**perfect monitoring**の場合、各期の終了時に、自分の行動と相手の行動を正確に知ることが出来ます。この履歴に基づいて、次期以降の行動を決定することが出来ます。  

**imperfect public monitoring**の場合、プレイヤーは各期の終了時、自分の行動と相手の行動を正確に知ることは出来ず、後述の確率でノイズが入ります。この情報を行動の**シグナル**と言います。
public monitoringの場合、シグナルは自分と相手とで共通のものになります。例えばある期の行動が(協力, 協力)であった場合、一定確率で(協力, 攻撃)という誤ったシグナルが発せられますが、
自分と相手の受け取るシグナルは同一のものになります。  

**imperfect private monitoring**の場合、プレイヤーが受け取るシグナルは**自分と相手で異なります。**例えばある期の行動が(協力, 協力)であった場合、自分は正しく(協力, 協力)という
シグナルを受け取る一方、相手は(攻撃, 協力)という誤ったシグナルを受け取る事が起こります。  

imperfect monitoringの場合は、受け取ったシグナルにノイズが入っていることを考慮して行動計画を決める必要があります。


## プログラムの仕様
戦略を表現するクラスを作成してください。  
クラスには、次の2つのメソッドを必ず含めてください（メソッド名も下の通りにしてください）。

* play(self): 各期のstage gameにおいて、行動0または1を返すメソッド
* get_signal(self, signal): 各期のstage game終了後、その期の自分と相手の行動のシグナルの配列[自分の行動のシグナル, 相手の行動のシグナル]を受け取るメソッド


### クラスのテンプレート

以下のようにクラスを作成してください。

```python
# テンプレート
class MyStrategy():
    def __init__(self, RandomState):
        # RandomStateオブジェクトのインスタンスを受け取る
        # 確率変数を使いたい場合は、このインスタンスを使う
        self.RandomState = RandomState

        # 過去の全てのシグナルを（必要があれば）保存しておく
        self.my_signals = []
        self.opponent_signals = []


    # 各ステージゲームの実行時に呼び出されるメソッド
    # その期の行動を0（=協調）, または1（=攻撃）のいずれかから選ぶ
    # ここでは、ランダムに行動を決める戦略の例を使用している
    def play(self):
        return self.RandomState.randint(0, 1)


    # 各期のゲーム終了時に呼び出されるメソッド
    def get_signal(self, signal):
        # 前期のゲームのシグナルを配列形式で受け取る
        # signal = [前期の自分の行動のシグナル, 相手の行動のシグナル]
        my_signal = signal[0]
        opponent_signal = signal[1]

        # 受け取ったシグナルをシグナルの履歴に追加
        self.my_signals.append(my_signal)
        self.opponent_signals.append(opponent_signal)
```

* __init__は、RandomStateクラスのインスタンスを受け取ることができるようにしてください。何らかの確率分布を用いて戦略を決定する場合は、
再現性を確保するため、このインスタンスのメソッドを使用してください。RandomStateクラスで使用できる確率変数は
[NumPyのドキュメント](http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html)
を参照してください。




たとえばtit for tatは以下のように書けます。
```python
# しっぺ返し
class TitForTat():
    def __init__(self, RandomState):
        # 相手の1期前のシグナル
        self.opponent_signal = 0

    def play(self):
        return self.opponent_signal

    def get_signal(self, signal):
        # シグナルを更新
        self.opponent_signal = signal[1]
```

他にもいくつか関数例を用意していますので、参考にしてください。->[関数例](./sample.py)

## テスト
テストを用意しました。->[テスト](./test.py)






