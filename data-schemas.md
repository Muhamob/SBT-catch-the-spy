#  Схемы JSON
Схемы json документов, которые получаются после парсинга соответствующих файлов

## TOC (Table of Content):
1. [Raw data schemas](#raw)
    1. [csv](#csv)
    2. [tab](#tab)
    3. [xlsx](#xlsx)
    4. [xml](#xml)
    5. [yaml](#yaml)
    6. [json](#json)
2. [Mongo data schemas](#mongo)
    1. [csv](#csv-mongo)
    2. [tab](#tab-mongo)
    3. [xlsx](#xlsx-mongo)
    4. [xml](#xml-mongo)
    5. [yaml](#yaml-mongo)
    6. [json](#json-mongo)

### Raw data schemas <a name="raw"></a>
#### CSV <a name="csv"></a>:
```yaml
PassengerFirstName : SAVELII
PassengerSecondName : VIKTOROVICH
PassengerLastName : RUSANOV
PassengerSex : Male
PassengerBirthDate : 03/10/1983
PassengerDocument : 2879 096860
BookingCode : FRNINO
TicketNumber : 6625956945991971
Baggage : Transit
FlightDate : 2017-03-22
FlightTime : 06:05
FlightNumber : SU1369
CodeShare : Own
Destination : Moscow
```

#### TAB <a name="tab"></a>:
```yaml
PaxName : ОЗЕРОВ ИЛЬДАР ДАНИИЛОВИЧ
PaxBirthDate : 1999-05-15
DepartDate : 2017-05-30
DepartTime : 00:05
ArrivalDate : 2017-05-30
ArrivalTime : 08:05
FlightCodeSh : SU1306NO
From : SVO
Dest : OVB
Code : ZBQSPY
e_Ticket : 7360415302044672
TravelDoc : 9375 053270
Seat : N/A
Meal : N/A
TrvCls : J
Fare : JGRPGN
Baggage : 0PC
PaxAdditionalInfo : S
FF : SU 38116280
AgentInfo : Go2See
```

#### XLSX <a name="xlsx"></a>:
```yaml
sequence: 76,  # хз что
name_prefix: "MR",  # префикс перед именем, например мистер или миссис
name_surname: "ZUEV ANTON G",  #  фамилия имя о.
unk1: "J",  #  вроде статус
flight: "MU5361",  #  рейс
departure: "SHANGHAI",  # пункт отправления
arrival: "SHENZHEN",  # пункт прибытия
gate: "N/A",  # посадочный гейт
dep_short: "PVG",  # сокращённое название аэропорта отправления
arr_short: "SZX",  # то же самое, прибытия
dep_date: "2017-09-09",  # дата отправления
dep_time: "20:25",  # вермя отправления
airlines_comment: "Operated by Some Other Airline",  # комментарий от авиаперевозчика
appendix_info: "Boarding is ended 20 minutes before departure time",  # дополнительная информация по рейсу
seat: "N/A",  # место
pnr: "GHMYPI",  # passenger name record
ticket_type: "E-TICKET",  # тип билета
ticket_num: "6964101325081258" # id билета
```

#### XML <a name="xml"></a>:
```yaml
- "@uid": '613142142'
  name:
    "@first": IAROMIR
    "@last": ZVEREV
  cards:
    "@type": Airlines  # (все будут Airlines, так как файл называется Airlines)
    card:
      "@number": FB 171388778
      bonusprogramm: Flying Blue
      activities:
        "@type": Airlines
        activity:
        - "@type": Flight
          Code: KE827
          Date: '2017-08-06'
          Departure: rea  # (код аэропорта, напрмер как Шереметьево-SVO)
          Arrival: SZX
          Fare: YGRPZT  # (видимо тариф)
        - "@type": Flight
          Code: MU9706
          Date: '2017-10-26'
          Departure: PEK
          Arrival: BSD
          Fare: YSTNYV

```

#### YAML <a name="yaml"></a>:
```yaml
FLIGHT: "AF1145" 
DATA: "2017-01-01"
FF: 
  - CARD: "FB 520518073"
    CLASS: "Y"
    FARE: "YRSTFN"
FROM: "SVO"
STATUS: "LANDED"
TO: "CDG"
```

#### JSON <a name="json"></a>:
```
Forum Profiles[
    Registered Flights[  Зарегистрированные рейсы
        {
            Date,
            Codeshare,  bool что значит хз возможно полетел не полетел 
            Arrival:
                {
                    City,
                    Airport,
                    Country
                },
            Flight,
            Departure:
                {
                    City,
                    Airport,
                    Country
                }
        }
    ],
    NickName,
    Travel Documents:[
    Passports
    ],
    Sex,
    Loyality Programm[
        {
          Status,
          programm,
          Number
        }
    ],
    Real Name:
        {
            Last Name,
            First Name
        }
]


```

### Mongo data schemas <a name="mongo"></a>

#### CSV <a name="csv-mongo"></a>:
```json
{
    "PassengerFirstName": "SAVELII",
    "PassengerSecondName": "VIKTOROVICH",
    "PassengerLastName": "RUSANOV",
    "gender": "Male",
    "birth_date": "03/10/1983",
    "documents": "2879 096860",
    "BookingCode": "FRNINO",
    "ticket": "6625956945991971",
    "Baggage": "Transit",
    "dep_date": "2017-03-22",
    "dep_time": "06:05",
    "flight": "SU1369",
    "CodeShare": "Own",
    "arr_long": "Moscow",
    "full_name": "SAVELII VIKTOROVICH RUSANOV"
}
```

#### JSON <a name="json-mongo"></a>:
```json
{
    "documents": [],
    "gender": "Male",
    "flights": [
        {
            "dep_date": "2017-03-04",
            "arr_long": "Pittsburgh PA",
            "arr_short": "PIT",
            "dep_long": "Boston MA",
            "dep_short": "BOS",
            "flight": "DL3377"
        },
        ...,
        {
            "dep_date": "2017-07-21",
            "arr_long": "Detroit MI",
            "arr_short": "DTW",
            "dep_long": "Green Bay WI",
            "dep_short": "GRB",
            "flight": "DL3630"
        }
    ],
    "full_name": "",
    "ff": [
        "KE 889215424",
        "DT 484697244"
    ]
}
```

#### TAB <a name="tab-mongo"></a>:
```json
{
    "full_name": "ОЗЕРОВ ИЛЬДАР ДАНИИЛОВИЧ",
    "birth_date": "1999-05-15",
    "dep_date": "2017-05-30",
    "dep_time": "00:05",
    "arr_date": "2017-05-30",
    "arr_time": "08:05",
    "FlightCodeSh": "SU1306NO",
    "dep_short": "SVO",
    "arr_short": "OVB",
    "Code": "ZBQSPY",
    "ticket": "7360415302044672",
    "documents": "9375 053270",
    "Seat": "N/A",
    "Meal": "N/A",
    "TrvCls": "J",
    "Fare": "JGRPGN",
    "Baggage": "0PC",
    "PaxAdditionalInfo": "S",
    "ff": "SU 38116280",
    "AgentInfo": "Go2See"
}
```

#### XLSX <a name="xlsx-mongo"></a>:
```json
{
    "sequence": 1,
    "name_prefix": "MR",
    "full_name": "SPIRIDONOV ARSEN",
    "unk1": "A",
    "flight": "MF8008",
    "dep_long": "HONG KONG",
    "arr_long": "WUYISHAN",
    "gate": "N/A",
    "dep_short": "SAR",
    "arr_short": "WUS",
    "dep_date": "2017-12-07",
    "dep_time": "18:25",
    "airlines_comment": "Operated by Some Other Airline",
    "appendix_info": "Boarding is ended 20 minutes before departure time",
    "seat": "N/A",
    "pnr": "QPOMZL",
    "ticket_type": "E-TICKET",
    "ticket": "8341755097926283"
}
```

#### XML <a name="xml-mongo"></a>:
```json
{
    "flight": "KE827",
    "dep_date": "2017-08-06",
    "dep_short": "rea",
    "arr_short": "SZX",
    "ff": "FB 171388778",
    "full_name": "ZVEREV IAROMIR"
}
```

#### YAML <a name="yaml-mongo"></a>:
```json
{
    "CLASS": "Y",
    "FARE": "YFLXZQ",
    "ff": "FB 542659498",
    "flight": "AF1144",
    "dep_data": "2017-01-07",
    "dep_short": "SVO",
    "STATUS": "LANDED",
    "arr_short": "CDG"
}
```