
#https://www.youtube.com/watch?v=UJUAazLyu1Q
from binance.client import Client

'''
Pkey = 'c3bf1e536c6f97f2054fd82e2ecec96f865ee86b0ffa281e62d325235670447e'
Skey = 'c73171f62243a90459b3efea9d8aec521562787f4fcacee4eac29f2e2b1bba1a'
client = Client(api_key=Pkey, api_secret=Skey , testnet= True)



#hamansor74@gmail.com
Pkey = 'f1891296f59fc529fb198b91addfbbbac8e3993c8e7d03abf1a7e368921c3834'
Skey = '263cf83cbd196fd108a9f439026b32174bb85a9c613b3ee5daff8f5ab1b2879c'
client = Client(api_key=Pkey, api_secret=Skey , testnet= True)

'''
Pkey = 'sO5Wum9vg6gyL0MrMfJeedYokfv6mrSmefqwCPhc4DcWa1VpleVfxqYiHjmmkMEd'
Skey = 'FXDirUsIGIC7SBfBkl9cCCrBUyqewyO5RdvBjPSnm8IPKHlJjjTa58bJ46Ai89ht'
client = Client(api_key=Pkey, api_secret=Skey ) #لازم تغيرها عند التداول الحقيقي testnet=fales


token='6160408785:AAGu-P60zjpk_Iby14RhZ67kaFL5r_J9SC0'
chat_id= '1041600176'

interval=Client.KLINE_INTERVAL_5MINUTE

'''
json = client.get_account()
#print(json)
freeUSDT = float(json['balances'][11]['free'])  
#print(freeUSDT)
'''
json = client.futures_account_balance()
#print(json)
freeUSDT = float(json[4]['balance'])  
totalUSDT = freeUSDT 



Bol = 2.4

hR = 15
lR = 15


dvr_rsi = 0

h = 10
l = 10


