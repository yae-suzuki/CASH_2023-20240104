##GPTの点数回答を抽出
#変数定義
joy,anger,sad,fun = 0,0,0,0
target_emottion = []

#GPTの回答を変数に格納
for n_char in range(4):
    char="こんにちはにゃあ！楽しい: 5, 悲しい: 0, 怒り: 0, 喜び: 5 にゃあ！今日の天気が良くて嬉しいにゃあ！"
    char_num = ["喜び","怒り","悲しい","楽しい"]
    print(char_num[n_char])
    target = char_num[n_char]+':'
    idx_1 = char.find(target)
    r1 = char[idx_1+len(target):]
    target = ','
    idx_2 = r1.find(target)
    r2 = r1[:idx_2]
    print(r2)
    target_emottion.append(r2)

print(target_emottion)
joy,anger,sad,fun = target_emottion
joy,anger,sad,fun = int(joy),int(anger),int(sad),int(fun)
print(type(joy))
print(joy)

#変数をリストに格納、最大値の抽出→display_emottionに格納
values_emottion = [joy,anger,sad,fun]
max_values_emottion = max(values_emottion)
if joy == max_values_emottion:
    display_emottion="joy"
elif anger == max_values_emottion:
    display_emottion="anger"
elif sad == max_values_emottion:
    display_emottion="sad"
elif fun == max_values_emottion:
    display_emottion="fun"


#todo 各ノードの役割の記述 
"""
#岡本さんに伝える
sub_gpt:録音された音声のテキストをgptに送信し回答生成、音声による回答の読み上げ、回答の表情の決定
sub_face:sub_gpt によって決定された回答の表情をcv_bridgeを用いてdisplayに表示させる。（ラズパイに入れる）
sub_motor:sub_gpt によって決定された回答の表情から耳の動作を行う（ラズパイに入れる）
"""

#todo 27-36に動画のファイル名を入れて再生する動画の情報を入れる。
#todo2 完成したらメインのGPTのプログラムに組み込む
#todo3 12/30までの岡本さんがやったプログラムを追加し、動作ができるかどうか確認する。