import csv
import os
import typing

from src.base.parsers import BaseParser


class TABParser(BaseParser):
    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        with open(path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        rows_for_json = []
        for i in range(len(rows)):
            d = dict(
                PaxName=list(rows[i].values())[0][0:60].rstrip(),
                PaxBirthDate=list(rows[i].values())[0][60:72].rstrip(),
                DepartDate=list(rows[i].values())[0][72:84].rstrip(),
                DepartTime=list(rows[i].values())[0][84:96].rstrip(),
                ArrivalDate=list(rows[i].values())[0][96:108].rstrip(),
                ArrivalTime=list(rows[i].values())[0][108:120].rstrip(),
                FlightCodeSh=list(rows[i].values())[0][120:132].rstrip(),
                From=list(rows[i].values())[0][132:138].rstrip(),
                Dest=list(rows[i].values())[0][138:144].rstrip(),
                Code=list(rows[i].values())[0][144:150].rstrip(),
                e_Ticket=list(rows[i].values())[0][150:168].rstrip(),
                TravelDoc=list(rows[i].values())[0][168:180].rstrip(),
                Seat=list(rows[i].values())[0][180:186].rstrip(),
                Meal=list(rows[i].values())[0][186:192].rstrip(),
                TrvCls=list(rows[i].values())[0][192:198].rstrip(),
                Fare=list(rows[i].values())[0][198:204].rstrip(),
                Baggage=list(rows[i].values())[0][204:216].rstrip(),
                PaxAdditionalInfo=list(rows[i].values())[0][216:240].rstrip(),
                FF=list(rows[i].values())[0][243:276].rstrip(),
                AgentInfo=list(rows[i].values())[0][276:].rstrip())

            for key, value in d.items():
                if len(value) == 0:
                    d[key] = 'N/A'

            rows_for_json.append(d)
        
        output_path = kwargs.get('output_path', '../../data/tab-parsed/Sirena-export-fixed.json')
        self.to_json(rows_for_json, output_path=output_path)

if __name__ == '__main__':
    a = TABParser()
    a.parse('/Users/dmitrij/Downloads/Sirena-export-fixed.tab')

