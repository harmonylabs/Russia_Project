import csv
import sys
from datetime import datetime
f = sys.argv[1]

start = datetime(2016,11,7)
end   = datetime(2019,4,19)
def str_to_datetime(s):
    return datetime(*[int(x) for x in s.split('-')])

missing = 0
with open(f,'r') as csv_f:
    for row in csv.reader(csv_f):
        if row[0]=='Date':
            continue
        dt = str_to_datetime(row[0])
        if dt.weekday() >4:
            continue
        if start <= dt <= end:
            if not row[5]:
                missing +=1
            if not row[6]:
                missing +=1
            if not row[7]:
                missing +=1
print(missing)
        
        
