# akari_sim_unity

## akariをunityで動かすプログラム

![akari Manual](<./images/akari1.png>)

### MODE select

#### チェックボックスOFF　・・・　Manual MODE

こちらはマニュアルでakariのジョイントを動かすことができます。

スライダーを動かすと各関節とLEDの明るさを調整できます。

![alt text](<./images/akari2.png>)
#### チェックボックスON　・・・　TCP MODE
こちらはTCP通信でakariのジョイントを動かすことができます。

ジョイントを動かすスクリプトは別レポジトリに保管してあります。

[こちら](https://github.com/mantues/ros2_for_unity/tree/main/py_pubsub/py_pubsub)

## ROS TCP Connector
[こちら](https://github.com/Unity-Technologies/ROS-TCP-Connector?tab=readme-ov-file#installation)に従ってROS TCP Connectorをインストールしています。

## プログラムの解説
### AKARIController.cs
TCP通信を利用してJson形式でAkariのジョイントとLEDを操作します。（受信のみ、ローカルホストのみ対応）

[AkariData](https://github.com/mantues/akari_sim_unity/blob/master/Assets/Scripts/AKARIController.cs#L14)としてJson形式を定義しています。

Unityを利用したJoint操作は[Unityで学ぶ　ロボットアームの逆運動学](https://amzn.asia/d/cWpOxk2)を参考にしています。

### tcp_basic_unity_akari.py
TCP通信を利用してJson形式でAkariにデータを送信します。

こちらはジョイントの角度のみ送信しています。

### tcp_unity_joint_akari.py
TCP通信を利用してJson形式でAkariにデータを送信します。

こちらはジョイントの角度、テキストをランダムで送信しています。

## ROS2との通信について
詳しくは[別レポジトリ](https://github.com/mantues/ros2_for_unity)参照ください