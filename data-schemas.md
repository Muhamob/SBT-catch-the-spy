#  Схемы JSON
Схемы json документов, которые получаются после парсинга соответствующих файлов

## TOC (Table of Content):
1. [csv](#csv)
2. [tab](#tab)
3. [xlsx](#xlsx)
4. [xml](#xml)
5. [yaml](#yaml)
6. [json](#json)

### CSV <a name="csv"></a>:
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

### TAB <a name="tab"></a>:
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

### XLSX <a name="xlsx"></a>:
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

### XML <a name="xml"></a>:
```json
[
    {
        "@uid": "613142142",			
        "name": {
            "@first": "IAROMIR",
            "@last": "ZVEREV"
        },
        "cards": {
            "@type": "Airlines"  (все будут Airlines, так как файл называется Airlines),
            "card": {
                "@number": "FB 171388778",
                "bonusprogramm": "Flying Blue",
                "activities": {
                    "@type": "Airlines",
                    "activity": [
                        {
                            "@type": "Flight",
                            "Code": "KE827",
                            "Date": "2017-08-06",
                            "Departure": "rea", (код аэропорта, напрмер как Шереметьево-SVO)
                            "Arrival": "SZX",
                            "Fare": "YGRPZT" (видимо тариф)
                        },
                        {
                            "@type": "Flight",
                            "Code": "MU9706",
                            "Date": "2017-10-26",
                            "Departure": "PEK",
                            "Arrival": "BSD",
                            "Fare": "YSTNYV"
                        }
                    ]
                }
            }
        }
    }
]
```

### YAML <a name="yaml"></a>:
```yaml
'2017-01-01': (Дата, название файла)
  - AF1145: (скорее всего какой-то идентификатор пассажира)
      FF: (frequent flyer)
        FB 520518073: {CLASS: Y, FARE: YRSTFN} (программа лояльности - SU - aeroflot bonus, FB - flying blue : класс, расходы(?))
      FROM: SVO (Откуда)
      STATUS: LANDED (Статус: Приземлился и т.п.)
      TO: CDG (куда)

```

### JSON <a name="json"></a>:
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