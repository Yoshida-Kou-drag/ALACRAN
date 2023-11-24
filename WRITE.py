# -*- coding: utf-8 -*-
"""
B3M_setPos_Python_Sample
KONDO KAGAKU CO.,LTD.
2021/12/09
"""
import serial
import time


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


#SET POSITIONコマンド
#サーボモータに動作角と目標に到達するまでの時間を指定しポジションを変更します。
def B3M_setPos_CMD(servo_id, pos, MoveTime):

    #送信コマンドを作成
    txCmd = [0x09,                  #SIZE
             0x06,                  #CMD
             0x00,                  #OPTION
             servo_id,              #ID
             pos & 0xff,            #POS_L
             pos >> 8 & 0xff,       #POS_H
             MoveTime & 0xff,       #TIME_L
             MoveTime >> 8 & 0xff]  #TIME_H

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
    else:
        return True
        
        '''
        #現在値を戻り値にする場合は、下記の処理をreturnしてください。
        rePos = [rxCmd[4], rxCmd[5]]
        rePos = int.from_bytes(rePos, 'little')
        
        #サーボからは符号なしでポジションデータが返ってきます。0を中心とした数値に変換するため下記のように処理をします。
        if (rePos > 32765):
                rePos -= 65536

        return rePos
        '''


#COMポートを開く
b3m = serial.Serial('/dev/ttyUSB0', baudrate=1500000, parity=serial.PARITY_NONE, timeout=0.5)

#B3Mサーボが動作するまでの準備
#B3M_Write_CMD(servo_id, TxData, Address)

#動作モード：Free (動作モードと特性を設定するため、設定書き換え中の誤動作を防止するため脱力にしておく)
reData = B3M_Write_CMD(0x00, 0x02, 0x28)
print(reData)

#位置制御モードに設定 (角度を指定して動作するモードです)
reData = B3M_Write_CMD(0x00, 0x02, 0x28)
print(reData)

#軌道生成タイプ：Even (直線補間タイプの位置制御を指定)
reData = B3M_Write_CMD(0x00, 0x01, 0x29)
print(reData)

#ゲインプリセット：No.0 (PIDのプリセットゲインを位置制御モード用に設定)
reData = B3M_Write_CMD(0x00, 0x00, 0x5C)
print(reData)

#動作モード：Normal （Freeの状態からトルクオン）
reData = B3M_Write_CMD(0x00, 0x00, 0x28)
print(reData)


#サーボに目標時間を指定して角度指示
#※軌道生成タイプ：Normal(0x00)の時は目標時間は反映されません。
#B3M_setPos_CMD(servo_id, pos, MoveTime)
#ID0、500msかけて5000(50度)の位置に移動する
reData = B3M_setPos_CMD(6, 5000, 500)
print(reData)
time.sleep(0.5) #サーボが到達するまで次の指示を待つ

reData = B3M_setPos_CMD(6, 13000, 500)
print(reData)
time.sleep(0.5) #サーボが到達するまで次の指示を待つ

reData = B3M_setPos_CMD(6, 9000, 500)
print(reData)
time.sleep(0.5) #サーボが到達するまで次の指示を待つ


#ポートを閉じる
b3m.close()