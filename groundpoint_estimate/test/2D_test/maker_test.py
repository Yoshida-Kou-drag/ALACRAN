import matplotlib.pyplot as plt
# 左上から順番にplotしている。

plt.plot(0.1, 1.5, marker='.', markersize=20) #　点
plt.plot(0.2, 1.5, marker=',')                #　ピクセル（絵を描くときなどに使える？？？？）
plt.plot(0.3, 1.5, marker='o', markersize=20) #　円
plt.plot(0.4, 1.5, marker='v', markersize=20) #　下向き三角形
plt.plot(0.5, 1.5, marker='^', markersize=20) #　上向き三角形
plt.plot(0.1, 1.4, marker='<', markersize=20) #　左向き三角形
plt.plot(0.2, 1.4, marker='>', markersize=20) #　右向き三角形
plt.plot(0.3, 1.4, marker='1', markersize=20) #　下向き棒三角形
plt.plot(0.4, 1.4, marker='2', markersize=20) #　上向き棒三角形
plt.plot(0.5, 1.4, marker='3', markersize=20) #　左向き棒三角形
plt.plot(0.1, 1.3, marker='4', markersize=20) #　右向き棒三角形
plt.plot(0.2, 1.3, marker='8', markersize=20) #　八角形
plt.plot(0.3, 1.3, marker='s', markersize=20) #　四角形
plt.plot(0.4, 1.3, marker='p', markersize=20) #　五角形
plt.plot(0.5, 1.3, marker='P', markersize=20) #　プラス
plt.plot(0.1, 1.2, marker='*', markersize=20) #　星型
plt.plot(0.2, 1.2, marker='h', markersize=20) #　縦向き六角形
plt.plot(0.3, 1.2, marker='H', markersize=20) #　横向き六角形
plt.plot(0.4, 1.2, marker='+', markersize=20) #　細いプラス
plt.plot(0.5, 1.2, marker='x', markersize=20) #　バツ
plt.plot(0.1, 1.1, marker='X', markersize=20) #　太いバツ
plt.plot(0.2, 1.1, marker='D', markersize=20) #　ダイヤ
plt.plot(0.3, 1.1, marker='d', markersize=20) #　細長いダイヤ
plt.plot(0.4, 1.1, marker='|', markersize=20) #　縦ライン
plt.plot(0.5, 1.1, marker='_', markersize=20) #　横ライン

plt.show()