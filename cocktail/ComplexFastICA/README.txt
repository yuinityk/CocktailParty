今回作成したComplexICAには欠陥がある可能性があります
現在次のような症状が確認されています
    全く同じデータを入力しても、低い確率で
        ①分離がきちんと行われない
        ②下記のようなエラーメッセージが出力される
現在原因は不明ですが、ICAを行う際、内部で乱数を用いて初期値を定めている箇所があり、
この初期値の善し悪しで上手くいくケースといかないケースがあるようです
複素版にする際、いくつかのエラー処理を無効にしたことが原因かもしれません
（ただし初期値の生成部分をいじったことはなく、あくまで入力をfloat型に直す処理を無効にしただけ（のつもり）なので関係ないかもしれません）

追記
2017/2/19   バグは修正したので以上のエラーは起きないはず
2017/2/20   数回に一回分離できないことがあります  まだバグがあるかもしれません
2017/2/21   数回に一回分離できないとのことだったが、
            どうやら今回の入力は、もともとの状態が偶然にも独立性が高く
            初期値によって、そのまま出力されてしまうことがあるようです
            一般のデータでは、このようなことは起こらず
            きちんと成功すると考えていいのではないでしょうか
"""
/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py:58: RuntimeWarning: invalid value encountered in sqrt
  return np.dot(np.dot(u * (1. / np.sqrt(s)), u.T), W)
Traceback (most recent call last):
  File "complex_ica_test.py", line 25, in <module>
    S_ = ica.fit_transform(S)
  File "/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py", line 528, in fit_transform
    return self._fit(X, compute_sources=True)
  File "/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py", line 499, in _fit
    compute_sources=compute_sources, return_n_iter=True)
  File "/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py", line 355, in complexfastica
    W, n_iter = _ica_par(X1, **kwargs)
  File "/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py", line 114, in _ica_par
    - g_wtx[:, np.newaxis] * W)
  File "/Users/odakura/vp_backup/ComplexFastICA/mypackage/complex_fastica_.py", line 55, in _sym_decorrelation
    s, u = linalg.eigh(np.dot(W, W.T))
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/scipy/linalg/decomp.py", line 288, in eigh
    a1 = _asarray_validated(a, check_finite=check_finite)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/scipy/_lib/_util.py", line 228, in _asarray_validated
    a = toarray(a)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy/lib/function_base.py", line 1033, in asarray_chkfinite
    "array must not contain infs or NaNs")
ValueError: array must not contain infs or NaNs
"""