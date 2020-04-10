import webbrowser
import pymysql
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore,storage
from sys import argv
import pdfkit 
import datetime
options = {
    'page-size': 'A4',
    'margin-top': '0.50in',
    'margin-right': '0.50in',
    'margin-bottom': '0.50in',
    'margin-left': '0.50in',
}



con = pymysql.connect('localhost', 'root','Navya.20', 'qwillco', autocommit=True)
cred = credentials.Certificate('/home/navya/Downloads/qwill-c86a9-firebase-adminsdk-80uh9-1d58d1b88c.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'qwill-c86a9.appspot.com'
})

db = firestore.client()
users_ref = db.collection('Sales/{}/{}'.format(argv[1],argv[2]))
docs = users_ref.stream()
date=argv[2]
dd=date[0:2]+" "
mm=date[2:5]+ " "
yy=date[5:9]
m2=dd+mm+yy
print(m2)

f1=list()
m1="<tbody>"
t1="""<br><table class="container">
	<thead>
		<tr>
			<th><h1>Brand</h1></th>
			<th><h1>Start Serial Number</h1></th>
			<th><h1>Stop Serial Number</h1></th>
			<th><h1>Volume</h1></th>
			<th><h1>Timestamp</h1></th>
			<th><h1>Distributor ID</h1></th>
			<th><h1>User ID</h1></th>
		</tr>
	</thead>
	"""
with con: 

    cur = con.cursor()
    cur.execute("SELECT * FROM Sales")
    
    h=1
    row = cur.fetchall()
    i=0
    g=len(row)
    for i in range(i,len(row)):
    	# if argv[2]==row[8]:
	    	m1=m1+"""
	    	<tr>
				<td>"""+row[i][1]+"""</td>
	 			<td>"""+row[i][2]+"""</td>
	 			
	 			<td>"""+row[i][3]+"""</td>
	 			<td>"""+str(row[i][4])+"""</td>

	 			<td>"""+row[i][5]+"""</td>
	 			<td>"""+row[i][6]+"""</td>

	 			<td>"""+str(row[i][7])+"""</td>


	 		</tr>
	    	"""
	    	i=i+1
	    	if i%18==0:
	    		h=h+1
	    		m1=m1+"</tbody></table>"
	    		f1.append(m1)
	    		f1.append(t1)
	    		m1="<tbody>"+"""<p style="page-break-after: always;"></p>"""

	
if h>=(g/18):
	f1.append(m1+"</table>")
	    		

o1=""
for i in range(0,len(f1)):
	o1=o1+f1[i]	

print(o1)

f = open('helloworld.html','wb')
a=2
# message = """<html>
# <h1>SALES REPORT</h1>
# <title>QWILLCO</title>
# <body><p>Hello World!""" +str(a)+"""</p></body>
# </html>"""
message="""<head><link rel="stylesheet" href="/home/navya/report.css"></head>
<title>QWILLCO</title>
<h1><b><span class="blue"></span>SALES  REPORT<span class="blue"></b></span></h1>

<table class="container">
	<thead>
		<tr>
			<th><h1>Brand</h1></th>
			<th><h1>Start Serial Number</h1></th>
			<th><h1>Stop Serial Number</h1></th>
			<th><h1>Volume</h1></th>
			<th><h1>Timestamp</h1></th>
			<th><h1>Distributor ID</h1></th>
			<th><h1>User ID</h1></th>
		</tr>
	</thead>""" + o1 + """</tbody>
	</table>"""

f.write(message.encode())
f.close()



#Change path to reflect file location
filename = '/home/navya/' + 'helloworld.html'
webbrowser.open_new_tab(filename)
pdfkit.from_file('/home/navya/helloworld.html', 'out.pdf',options=options) 
bucket = storage.bucket()
blob = bucket.blob('outfinal.pdf')
outfile='/home/navya/out.pdf'
blob.upload_from_filename(outfile)
print(blob.generate_signed_url(datetime.timedelta(seconds=200), method='GET'))



