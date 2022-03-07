# ====================
# 学習サイクルの実行
# ====================

# パッケージのインポート
from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network

# デュアルネットワークの作成
dual_network()

for i in range(1):
    print('Train',i,'====================')
    # セルフプレイ部
    self_play()

    # パラメータ更新部
    train_network()

    # evaluation of new network
    evaluate_network()
