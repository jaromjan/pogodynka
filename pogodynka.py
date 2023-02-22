# Program do obslugi biblioteki zewnetrznej - sprawdza czy w danym dniu bedzie padac
import os
import datetime
from calendar import monthrange
import csv
import requests
# wskazujemy punkt na mapie
latitude = '50.23'
longitude = '18.66'
opad = None
status = None
dane = None
year = None
month = None
day = None
# obsluga poprawnosci wyboru daty
data_in = input("Podaj date w formacie 'YYYY-MM-DD' lub pusta(zostanie pobrana jutrzejsza): ")
if data_in == '':
    searched_date = datetime.date.today() + datetime.timedelta(days=1)
else:
    data_in = data_in.split(sep='-')
    if len(data_in) < 3:
        print("Błedna data")
        quit()
    for y in data_in[0]:
        if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') or len(data_in[0]) != 4:
            print("Błedny rok")
            quit()
    year = int(data_in[0])
    for m in data_in[1]:
        if m not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') or len(data_in[1]) != 2:
            print("Błedny miesiac")
            quit()
    month = int(data_in[1])
    if month > 12:
        print("Błedny miesiac")
        quit()
    for d in data_in[1]:
        if d not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') or len(data_in[1]) != 2:
            print("Błedny dzien")
            quit()
    day = int(data_in[2])
    if day > monthrange(year, month)[1]:
        print("Dzien poza zakresem podanego miesiaca")
        quit()
    searched_date = datetime.date(year, month, day)
# prametryzujemy url-a
url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&' \
      f'daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}'
# tworzymy plik jesli go niema
if not os.path.exists('opady.csv'):
    fc = open('opady.csv', 'w')
    fc.close()
# odczytujemy plik i sprawdzamy czy niem tam juz danych dla wybranej daty
with open('opady.csv', 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
    zaw = []
    for line in reader:
        zaw.append(line)
    for i in zaw:
        if i[0] == str(searched_date):
            opad = float(i[1])
# jesli niema danych w pliku szukamy w internecie i dopisujemy do pliku, a jesli sa zwracamy dane znalezione w pliku
if opad is None:
    resp = requests.get(url)
    dane = resp.json()
    status = str(resp.status_code)[0]+str(resp.status_code)[1]
    if status != '20':
        print('Brak danych archiwalnych i bledna odpowiedz serwera')
        quit()
    else:
        opad = float(dane['daily']['rain_sum'][0])
        wynik = [str(searched_date), opad]
        with open('opady.csv', 'a', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            writer.writerow(wynik)
print(f'W dniu: {searched_date}')
if opad == 0.0:
    print(f'Nie bedzie padac - przewidywany opad: {opad}')
elif opad > 0.0:
    print(f'Bedzie padac - przewidywany opad: {opad}')
else:
    print('Nie wiem')
