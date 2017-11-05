from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
import signal

session = Session(server_token='your_token')
client = UberRidesClient(session)

# [lon, lat, name]
origins = [
    [-35.1995, -5.8434, 'ECT'],
    [-35.2054, -5.8323,'IMD']
]

destinations = [[-35.236981800685165, -5.870840666224352, 'Pitimbu'],
 [-35.239511057500785, -5.8623961914886396, 'Pitimbu'],
 [-35.24860515689553, -5.852370621667493, 'Planalto'],
 [-35.24739205909851, -5.8422971531192, 'Planalto'],
 [-35.15596978298069, -5.887973915383883, 'Ponta Negra'],
 [-35.168584855247744, -5.887199968737731, 'Ponta Negra'],
 [-35.20974352004816, -5.866488729132839, 'Neópolis'],
 [-35.216579352759986, -5.865620580955296, 'Neópolis'],
 [-35.20825434639825, -5.844952862777679, 'Capim Macio'],
 [-35.192032562474694, -5.865902667145231, 'Capim Macio'],
 [-35.25667890343955, -5.7640447137790165, 'Potengi'],
 [-35.25103068409885, -5.751524469672768, 'Potengi'],
 [-35.20293156188922, -5.799199687762013, 'Barro Vermelho'],
 [-35.21175595624902, -5.795702059430728, 'Barro Vermelho'],
 [-35.22380104989862, -5.848666799851974, 'Candelária'],
 [-35.2138541432291, -5.859300106086236, 'Candelária'],
 [-35.22215431544492, -5.749424954633537, 'Redinha'],
 [-35.2331018634999, -5.755193450124638, 'Redinha'],
 [-35.285105355750254, -5.741227853201468, 'Nossa Senhora da Apresentação'],
 [-35.263257762701215, -5.749344486262619, 'Nossa Senhora da Apresentação'],
 [-35.20405658674978, -5.774736461859913, 'Ribeira'],
 [-35.20448374240866, -5.7751467508506815, 'Ribeira'],
 [-35.20646534329146, -5.781229934058792, 'Cidade Alta'],
 [-35.20618356547286, -5.784264982577109, 'Cidade Alta'],
 [-35.218644869640706, -5.790558452384586, 'Alecrim'],
 [-35.22044104895825, -5.790315058307776, 'Alecrim'],
 [-35.2353263560941, -5.798918267396442, 'Quintas'],
 [-35.236522332120465, -5.791683775684841, 'Quintas'],
 [-35.23474121280764, -5.813442626757365, 'Nossa Senhora de Nazaré'],
 [-35.232292557638345, -5.816801834175864, 'Nossa Senhora de Nazaré'],
 [-35.219957385550096, -5.828918326434649, 'Lagoa Nova'],
 [-35.20587339928591, -5.813038977663765, 'Lagoa Nova'],
 [-35.19941251638022, -5.8210933802055225, 'Nova Descoberta'],
 [-35.200640402172816, -5.827364323950782, 'Nova Descoberta'],
 [-35.19683237652891, -5.8119112440893455, 'Tirol'],
 [-35.20220670728412, -5.796057712196255, 'Tirol'],
 [-35.19980727338861, -5.781753220028521, 'Petrópolis'],
 [-35.19721630188386, -5.783385852484189, 'Petrópolis'],
 [-35.237040337969404, -5.821493068463147, 'Cidade da Esperança'],
 [-35.23935530014809, -5.829009577179275, 'Cidade da Esperança']]

def handler(signum, frame):
    print("**Timeout**")
    raise Exception("Timeout de resposta da API")

def getPriceEstimates(lat1,long1,lat2,long2):
    return client.get_price_estimates(
        start_latitude=lat1,
        start_longitude=long1,
        end_latitude=lat2,
        end_longitude=long2,
        seat_count=2)

signal.signal(signal.SIGALRM, handler)
writeHeader = True
delta = datetime.now() + timedelta(days=8)

while(datetime.now() < delta):
    delta3min = datetime.now() + timedelta(minutes=3)
    while(datetime.now() < delta3min):
        initial = datetime.now()
        for o in origins:
            for d in destinations:
                
                retries = 1
                while(retries < 4):
                    try:
                        signal.alarm(3)
                        response = getPriceEstimates(o[1],o[0],d[1],d[0])
                        signal.alarm(0)
                        retries = 4;
                    except Exception as inst:
                        retries = retries + 1;
                        print(type(inst))
                        print(str(retries) + ') ')

                try:
                    if response is not None and type(response) != str:
                        json = response.json
                    else:
                        json = None
                        print(str(datetime.now()) + ' response none or str')
                    
                    if json is not None:
                        prices = json.get('prices')

                        if prices is not None:
                            for p in prices:
                                p['date'] = str(datetime.now())
                                p['origin'] = o[2]
                                p['destination'] = d[2]
                        else:
                            print(str(datetime.now()) + ' prices none')
                    else:
                        print(str(datetime.now()) + ' json none')
                    
                    pd.DataFrame(data=prices).to_csv('uberdata.csv', mode='a', header=writeHeader)
                    writeHeader = False 
                except Exception as inst:
                    print(type(inst))
                    print(inst)
        
        final = datetime.now()
        time_to_wait = 180 - divmod((final - initial).seconds, 200)[1] > 0
        if (time_to_wait > 0)
            sleep(time_to_wait)
