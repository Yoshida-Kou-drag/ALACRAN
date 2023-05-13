import b3mCtrl                                      #これはオリジナルのライブラリなので同じフォルダにb3mCtrl.pyを入れておかないとエラーになる
import time

if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()

    #ポート設定: B3Mがつながっているポート番号を調べて
    # aaa.begin("/dev/ttyUSB0",1500000)             #linux OS /raspi OS
    aaa.begin("COM3",1500000)                       #windows OS

    id = 1                                          #一つのIDを動かしたいとき
    #idx = [1,2,3,4,5,6,7,8,9]                      #複数のIDを動かしたいとき

    # print (aaa.setTrajectoryType(255,"EVEN"))
    # time.sleep(0.01)
    print("start")
    print (aaa.setMode(255,"FREE"))                 #setMode(id,mode) 今回の場合はIDが255なのでブロードキャスト
    time.sleep(0.01)                                #コマンド送信後はちょっと間をあける
    print (aaa.setMode(id,"POSITION"))              #id=1をposistionモードに変更(このコマンドを送った時にID1のモータに力が入っていればOK)
    time.sleep(0.01)                

    time.sleep(5)                                   #5秒間待機
    print (aaa.positionCmd(id,0,1))                 #ID1にposition0を送信
    time.sleep(1)                                   #5秒間待機
    print (aaa.positionCmd(id,3000,1))              #ID１にposition3000を送信(この時角度は30°動く)
    time.sleep(1)                                   #5秒間待機


    print("enterを押すと FREE MODE")
    input()
    print (aaa.setMode(255,"FREE"))                 #ブロードキャストでモーター全体をFree Modeに変更

    print("End")
    
    
    
    
