import pandas as pd
import json
import gzip
import create_and_write_to_queue
from flatten_json import flatten
from sklearn import preprocessing
import psycopg2
import os

os.chdir('../')

url = './data/sample_data.json.gz'
with open(url,'rb') as f:
    gzip_fd = gzip.GzipFile(fileobj=f)
    d = json.loads(gzip_fd.read())

df = pd.json_normalize(d)



# Import label encoder

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()

# Encode labels in column 'species'.
df['masked_device_id']= label_encoder.fit_transform(df['device_id'])
df['masked_ip']= label_encoder.fit_transform(df['ip'])

df = df.drop(columns=['foo','bar'])
df['create_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
df = df[['user_id', 'device_type', 'masked_ip','masked_device_id','locale','app_version','create_date']]
print(df)

#establishing the connection
conn = psycopg2.connect(
    database="postgres", user='postgres', password='postgrespw', host='host.docker.internal', port= '49156'
)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS user_logins(user_id  varchar(128), device_type varchar(32),masked_ip varchar(256),masked_device_id varchar(256),locale varchar(32),app_version integer,create_date date)')
print('Creation of table succeeded')


for i in df.index:
    cols  = ','.join(list(df.columns))
    vals  = [df.at[i,col] for col in list(df.columns)]
    query = "INSERT INTO user_logins VALUES('%s','%s','%s','%s','%s','%s','%s')" % (vals[0], vals[1], vals[2],vals[3],vals[4],vals[5],vals[6])
    cursor.execute(query)

# fetching all rows
sql1='''select * from user_logins'''
cursor.execute(sql1)
for i in cursor.fetchall():
    print(i)