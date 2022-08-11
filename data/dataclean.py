import csv
def num_there(s):
    return any(i.isdigit() for i in s)
  



def stripcomma(s):
  if(s[-1]==','):
    return s[:-1];
  else:
    return s;

print(r"{hello}".strip(r"{}"))
# 開啟 CSV 檔案
filename = "result.csv"
filenamewrite = 'dataraw.csv'
with open(filenamewrite,'w',encoding='utf-8') as out:
  with open(filename, newline='',encoding='utf-8') as csvfile:
    writer = csv.writer(out);
    rows = csv.reader(csvfile)

    for row in rows:
      print(row);
      if(row[1]!="skip"):
        row[0]=row[0].strip()
        row[0] = row[0].replace(r'\\' , "\\" )
        row[0] = stripcomma(row[0])
        writer.writerow(row);
        if(row[0].count('x')):
          newrow = row;
          newrow[0] = row[0].replace('x','p');
          newrow[1] = row[1].replace('x','p');
          writer.writerow(newrow);
        if(row[0].count('y')):
          newrow = row;
          newrow[0] = row[0].replace('y','p');
          newrow[1] = row[1].replace('y','p');
          writer.writerow(newrow);

