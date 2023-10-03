import serial


#READコマンド
#メモリーマップ(RAM)のアドレスを指定してデバイスからRAMデータを読み込みます。
def B3M_Read_CMD(servo_id, Data_size, Address):

    #送信コマンドを作成
    txCmd = [0x07,      #SIZE
             0x03,      #CMD
             0x00,      #OPTION
             servo_id,  #ID
             Address,   #ADDRRESS
             Data_size]      #LENGTH

    #チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i
        
    #リストの最後にチェックサムを挿入する
    txCmd.append(checksum & 0xff)
    
    #WRITEコマンドを送信
    b3m.write(txCmd)
    
    #サーボからの返事を受け取る
    rxCmd = b3m.read(5+Data_size)
    
    #もしリスト何になにも入っていなかったら正常に受信できていないと判断    
    if len(rxCmd) == 0:
        return False, 0

    #問題なければデータを返す
    #1Byteの場合
    if Data_size == 1:
        return True, rxCmd[4]

    #2Byteの場合
    elif Data_size == 2:
        Value = [rxCmd[4], rxCmd[5]]
        
        #データの範囲にマイナスが含まれる場合
        if (Address == 0x05     #最小位置制御
            or Address == 0x07  #最大位置制御
            or Address == 0x09  #中央値オフセット
            or Address == 0x0B  #MCU温度リミット
            or Address == 0x0E  #モーター温度リミット
            or Address == 0x2A  #目標位置
            or Address == 0x2C  #現在位置
            or Address == 0x2E  #前回のサンプリングの位置
            or Address == 0x30  #目標速度
            or Address == 0x32  #現在速度
            or Address == 0x34  #前回のサンプリングの速度
            or Address == 0x3C  #目標トルク
            or Address == 0x44  #現在のMCU温度
            or Address == 0x46):#現在のモーター温度
        
            Value = int.from_bytes(Value, 'little', signed=True)

        #データの範囲がプラスのみの場合
        else:
            Value = int.from_bytes(Value, 'little')
        
        return True, Value


    #4Byteの場合    
    elif Data_size == 4:
        Value = [rxCmd[4], rxCmd[5], rxCmd[6], rxCmd[7]]
        Value = int.from_bytes(Value, 'little')
        return True, Value
        
    else:
        return False, 0


#COMポートを開く
b3m = serial.Serial('/dev/ttyUSB0', baudrate=1500000, parity=serial.PARITY_NONE, timeout=0.5)

#ロボットアーム・ハンドのサーボID
idy= [6,7,8,9,10]

for id in range (len(idy)):
    
    #B3M_Read_CMD(servo_id, Data_size, Address)
    #ID番号を読み込む(ID:0,1byte読み込み,アドレス：0x00(ID))
    bl, reData = B3M_Read_CMD(idy[id], 1, 0x00)
    print(bl, reData)

    #現在位置を読み込む(ID:0,2byte読み込み,アドレス：0x2C(現在位置))
    bl, reData = B3M_Read_CMD(idy[id], 2, 0x2C)
    print(bl, reData)

    #通信速度を読み込む(ID:0,4byte読み込み,アドレス：0x01(通信速度))
    bl, reData = B3M_Read_CMD(idy[id], 4, 0x01)
    print(bl, reData)

#ポートを閉じる
b3m.close()
