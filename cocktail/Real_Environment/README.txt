著者　小田倉雅人    日付2017/2/17

このフォルダー内のファイルは、実環境下における音声の混合をシミュレーションし、それらの混合データに対して従来の独立成分分析がどのように振る舞うかを検証したものである。
すなわち残響があり、混合音声がもとの音源の線形和ではなく、畳み込みの和として表されるときに
pythonのfastICAを行うとどのような結果が得られるかを見た。

インパルス応答として以下の３パターンを試した。
１）デルタ型＝今まで通りの瞬時混合モデル    delta
２）exp(-t/a)型　ただし時定数aは比較的小さい＝残響は少ない  short_exp
３）exp(-t/b)型　ただし時定数bは比較的大きい＝残響は多い   long_exp

インパルス応答としてexp型を採用したことに深い意味はなく、現実にどれほど則しているかは不明
ただそこまでいい加減な設定ではないと期待する。
他の各種パラメタは適宜適当に設定した。



############
author:M.Odakura    date:2017/2/17

The files in this folder simulate the mixture of sounds in the real environment and show how well fastICA of Python works to these mixed data.
'Real Environment' maeans the mixed data is not linear combination but combination of convolution.

There are three models for the (finite) impulse reactions.
1) delta model = instantaneous mixing model     'delta'
2) exp(-t/a) model, a is relatively small = the effect of reverberation is relatively small 'short_exp'
3) exp(-t/b) model, b is relatively small = the effect of reverberation is relatively big   'long_exp'

Note:
There is no special meaning for adopting exp model, and I don't know how well this model fits actual impulse reactions.
However I expect it is not so divergent from actual situation.
Other parameters are set properly.


Please be patient with my poor English.
#############

