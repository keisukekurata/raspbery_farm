# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sqlite3
import dht11
import time
import datetime
 
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
 
# read data using pin 14
instance = dht11.DHT11(pin=14)
 
while True:
    result = instance.read()
    if result.is_valid():
        TIME = str(datetime.datetime.now())
        TEMP = result.temperature
        HUMID =  result.humidity
        #以下のプリントは無くても良い。
        print("Last valid input: " + TIME)
        print("Temperature: %d C" % TEMP)
        print("Humidity: %d %%" % HUMID)
        #データが取れたのでブレイクしてSQLiteに保存
        break;
 
# SQLiteのデータベースの名前と保管場所を指定。
#このコードはdht11.pyと同じ場所に置く必要があります。DBも同じ場所にしてみました。
dbname = '/home/pi/DHT11_Python/dht11_1.db'
# データベース内のテーブルの名前
dbtable = 'sensor1'
# SQLiteへの接続
conn = sqlite3.connect(dbname)
c = conn.cursor()
 
# SQLiteにテーブルがあるかどうか確認するクエリ
checkdb = conn.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % dbtable)
# もしテーブルがなかったら新規でテーブルを作成する
if checkdb.fetchone() == None:
    # ID、タイムスタンプ、温度、湿度の4列のテーブルを作成するクエリを作成。IDは自動附番。
    create_table = '''create table ''' + dbtable + '''(id integer primary key autoincrement, timestamp varchar(20),
                  temp real, humid real)'''
    # クエリを実行
    c.execute(create_table)
    # 変更を保存する
    conn.commit()
 
# SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
# セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
# タプルで渡す．
# 温度、湿度、タイムスタンプを保存。
sql = 'insert into sensor1 (timestamp, temp, humid) values (?,?,?)'
data= (TIME, TEMP, HUMID)
c.execute(sql, data)
conn.commit()
 
#接続を切る
conn.close()
