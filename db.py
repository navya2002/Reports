import pymysql
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from sys import argv


con = pymysql.connect('localhost', 'root','Navya.20', 'qwillco', autocommit=True)
cred = credentials.Certificate('/home/navya/Downloads/qwill-c86a9-firebase-adminsdk-80uh9-1d58d1b88c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection('Sales/{}/{}'.format(argv[1],argv[2]))
docs = users_ref.stream()
print(argv[2])
with con:
	cur = con.cursor()
	for doc in docs:
		doc_id=doc.id
		time = doc.get("time")
		volume = doc.get("volume")
		OwnerNumber = doc.get("OwnerNumber")
		brand = doc.get("brand")
		StartSerialNumber = doc.get("StartSerialNumber")
		DistributorID = doc.get("DistributorID")
		StopSerialNumber = doc.get("StopSerialNumber")
		cur.execute("INSERT INTO Sales(ID,brand,start_serial_no,stop_serial_no,volume,sale_ts,distributor_id,user_id,sale_date) \
			values('{}','{}','{}','{}',{},'{}','{}','{}','{}')".format(doc_id,brand,StartSerialNumber,StopSerialNumber,volume,time,DistributorID,OwnerNumber,argv[2]))
		print(u'{} => {}'.format(doc.id, doc.to_dict()))
