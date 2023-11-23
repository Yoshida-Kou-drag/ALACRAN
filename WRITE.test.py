import serial
import time
 
 
#COMポートを開く
b3m = serial.Serial('/dev/ttyUSB0', baudrate=1500000, parity=serial.PARITY_NONE, timeout=0.5)

#WRITEコマンド
#メモリーマップ(RAM)のアドレス指定でデバイスのRAM上に書き込みます。
def B3M_Write_CMD(servo_id, TxData, Address):
 
    #送信コマンドを作成
    txCmd = [0x08,      #SIZE
             0x04,      #CMD
             0x00,      #OPTION
             servo_id,  #ID
             TxData,    #DATA
             Address,   #ADDRRESS
             0x01]      #COUNT
 
    #チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i
 
    #リストの最後にチェックサムを挿入する
        txCmd.append(checksum & 0xff)
 
    #WRITEコマンドを送信
        b3m.write(txCmd)
 
    #サーボからの返事を受け取る
        rxCmd = b3m.read(5)
 
    #もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        return False
 
    #問題なければ返事を返す
    return True

def B3M_setPos_CMD(servo_id, pos, MoveTime):
 
    #送信コマンドを作成
    txCmd = [0x09, #SIZE
                   0x06, #CMD
                   0x00, #OPTION
                   servo_id, #ID
                   pos & 0xff, #POS_L
                   pos >> 8 & 0xff, #POS_H
                   MoveTime & 0xff, #TIME_L
                   MoveTime >> 8 & 0xff] #TIME_H
 
    #チェックサムを作成
    checksum = 0
    for i in txCmd:
        checksum += i
 
      #リストの最後にチェックサムを挿入する
        txCmd.append(checksum & 0xff)
 
      #コマンドを送信
        b3m.write(txCmd)
 
      #サーボからの返事を受け取る
        rxCmd = b3m.read(7)
 
    #もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        return False
 
    #問題なければ返事を返す
    return True

#B3M_Write_CMD(servo_id, TxData, Address)
 
#動作モード：Free (動作モードと特性を設定するため、設定書き換え中の誤動作を防止するため脱力にしておく)
reData = B3M_Write_CMD(0x00, 0x02, 0x28)
 
#位置制御モードに設定 (角度を指定して動作するモードです)
reData = B3M_Write_CMD(0x00, 0x02, 0x28)
 
#軌道生成タイプ：Even (直線補間タイプの位置制御を指定)
reData = B3M_Write_CMD(0x00, 0x01, 0x29)
 
#ゲインプリセット：No.0 (PIDのプリセットゲインを位置制御モード用に設定)
reData = B3M_Write_CMD(0x00, 0x00, 0x5C)
 
#動作モード：Normal （Freeの状態からトルクオン）
reData = B3M_Write_CMD(0x00, 0x00, 0x28)

#B3M用角度への変換
angle6 = 8000
angle7 = -5000
angle8 = 5000
angle9 = 5000

#ID0、500msかけて5000(50度)の位置に移動する
reData = B3M_setPos_CMD(6, angle6, 500)
time.sleep(0.5) 
reData = B3M_setPos_CMD(7, angle7, 500)
time.sleep(0.5) 
reData = B3M_setPos_CMD(8, angle8, 500)
time.sleep(0.5) 
reData = B3M_setPos_CMD(9, angle9, 500)
time.sleep(0.5) 

#ポートを閉じる
b3m.close()
