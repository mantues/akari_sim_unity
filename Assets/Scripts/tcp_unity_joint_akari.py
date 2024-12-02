#python送信側
import socket
import random
import time
import json
import random
import math

HOST = '127.0.0.1'
PORT = 50007
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

akari_pan = 0
akari_tilt = 0
pan_VMAX = 0.08
tilt_VMAX = 0.08
pan_ACC = 0.002
tilt_ACC = 0.002
akari_text = "TEXT"
text = ["akari", "AKARI", "Hello, akari"]
##############################################
# 経路生成プログラム　詳細はGoogleスプレッドシート参照
def path_plotter(VMAX, ACC, D1, D2):
  path_first = []
  path_latter = []
  path_all = [D1]

  # 始点と終点を設定。同じ場合はD1のみを返す。
  # 始点と終点が逆転している場合はFlag1にして最後にpathをひっくり返す
  FLAG = 0
  if (D1 < D2):
    FLAG = 0
  elif D1 == D2:
    # 始点と終点が一致している場合はエラー文と始点を返す
    print("Please set D1=!D2")
    print("PATH: {}".format(path_all))
    return path_all
  else:
    FLAG = 1

  # ここから経路作成
  # 始点と終点の設定、小さいほうを始点、大きいほうを終点とする
  startpoint = min(D1, D2)
  endpoint = max(D1, D2)
  distance = endpoint - startpoint
  # 最大速度、最小速度の設定。速度は0にならない小さい値、最大値は距離の10分の1（適当に決めてる）
  VMAXmin = 0.0001
  VMAXmax = distance / 10

  VMAXset = max(VMAXmin, min(VMAXmax, VMAX))

  # 最大加速度、最小加速度の設定。加速度は0にならない小さい値、最大値は速度の2分の1（適当に決めてる）
  ACCmin = 0.0001
  ACCmax = VMAX/2
  ACCset = max(ACCmin, min(ACCmax, ACC))
  #print("VMAXset: {}, ACCset: {}".format(VMAXset, ACCset))

  # 中間地点の計算
  mid = (distance)/2
  # 速度、加速度から計算される最大速度まで到達する距離
  delta = VMAXset*VMAXset/ACCset/2
  # 最大速度まで到達するステップ数
  Nmid = int(0.5*(1+(4*distance/ACCset)**0.5))
  Ndel = int(VMAXset/ACCset)

  # 中間地点までに最大速度に達する場合のステップ数
  if(delta < mid):
    N1 = int(Ndel)
    Nm = int((mid - delta)/VMAXset)
  # 中間地点までに最大速度まで到達しない場合は加速の途中でステップ数が止まる
  else:
    N1 = int(Nmid)
    Nm = 0

  # 経路の計算、単純化のために0を始点に経路作成
  # path_firstは前半経路（0からスタート）
  # path_latterは後半経路（終点からpath_firstを引いた点をあとでひっくり返す）
  Pos = 0
  Vel = 0
  acc = ACCset
  for i in range(Nm+N1):
    if(i <= N1):
      Pos += Vel
      Vel += ACCset
      path_first.append(Pos)
      path_latter.append(distance - Pos)
    else:
      Pos += VMAXset
      path_first.append(Pos)
      path_latter.append(distance - Pos)
  # 不連続な部位の調整
  if(delta < mid):
      path_latter.append(0.5*distance)
  # 後半経路を逆転させる
  path_latter_l = path_latter[::-1]
  # 後半経路の距離分だけ足してつじつま合わせ
  delta_value = distance - path_latter[0]
  path_latter_a = [x + delta_value for x in path_latter_l]
  # 経路の結合
  path_all = path_first + path_latter_a
  # 始点と終点が逆転していたらひっくり返す
  if FLAG == 1:
    path_all = path_all[::-1]
  # 経路の始点を与えられた始点にするため足し算する
  delta_value_all =  D1-path_all[0]
  path_all=[x+delta_value_all for x in path_all]
  # 始点と終点を与えられたものに合わせる
  path_all[0] = D1
  path_all[-1] = D2

  #print("start: {}, endpoint: {}, mid: {}, delta: {}".format(startpoint, endpoint, mid, delta))
  #print("N1: {}, Nm: {}".format(N1, Nm))
  #print("Flag: {}".format(FLAG))
  #print("PATH_F: {}\nPATH_L: {}\nPATH_A: {}".format(path_first, path_latter, path_all))
  return path_all
##############################################
# 2種類のパスを比較して長いリストに長さを合わせる関数。
def conpare_list(listA, listB):
  numA = len(listA)
  numB = len(listB)
  length = max(numA, numB)
  if numA < numB:
    addlist = [listA[-1]]*(numB - numA)
    listA += addlist
    return listA, listB
  elif numA == numB:
    return listA, listB
  else:
    addlist = [listB[-1]]*(numA - numB)
    listB += addlist
    return listA, listB
##############################################

def send_TCPdata(pan = akari_pan, tilt = akari_tilt, text = akari_text):
    global HOST, PORT, CLIENT, akari_pan, akari_tilt, akari_text
    data = {
        "message": "Hello, from server!",
        "timestamp": time.time(),
        "pan": akari_pan*180/math.pi,
        "tilt": akari_tilt*180/math.pi,
        "text": akari_text
    }
    print("Send data:\n{}".format(data))
    json_data = json.dumps(data).encode('utf-8')
    CLIENT.sendto(json_data,(HOST,PORT))

def move_joint(pan_target, tilt_target):
    global akari_pan, akari_tilt, pan_VMAX, tilt_VMAX, pan_ACC, tilt_ACC
    road_path_pan = path_plotter(VMAX=pan_VMAX, ACC=pan_ACC, D1=akari_pan,  D2=pan_target)
    road_path_tilt = path_plotter(VMAX=tilt_VMAX, ACC=tilt_ACC, D1=akari_tilt,  D2=tilt_target)
    pan_path_list, tilt_path_list = conpare_list(road_path_pan, road_path_tilt)
    print("!!!!START!!!!")
    for i in range(len(pan_path_list)):
        akari_pan = pan_path_list[i]
        akari_tilt = tilt_path_list[i]
        send_TCPdata(pan = akari_pan, tilt = akari_tilt)
        time.sleep(0.1)
    akari_pan = pan_target
    akari_tilt = tilt_target
    
def send_text(send_text):
    global akari_pan, akari_tilt, akari_text
    send_TCPdata(text = send_text)
    time.sleep(0.1)
    print("!!TEXT!!{}".format(send_text))
    akari_text = send_text
    
def main():
    tcp_text = random.choice(text)
    send_text(tcp_text)
    time.sleep(0.5)
    
    move_joint(0.25, -0.5)
    tcp_text = random.choice(text)
    send_text(tcp_text)
    time.sleep(0.5)

    move_joint(1.25, -0.5)
    tcp_text = random.choice(text)
    send_text(tcp_text)
    time.sleep(0.5)

    move_joint(-1.5, -0.5)
    tcp_text = random.choice(text)
    send_text(tcp_text)
    time.sleep(0.5)
    
    move_joint(-0.5, 0.5)
    tcp_text = random.choice(text)
    send_text(tcp_text)
    time.sleep(0.5)
    
    move_joint(0.0, 0.0)
    tcp_text = random.choice(text)
    send_text(tcp_text)
    print("finish")
if __name__ == '__main__':
    main()
