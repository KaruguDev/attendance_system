#!/usr/bin/python3

import sys
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from easygui import *
import psycopg2
import time
import csv
import os


usrname = os.environ.get("USERNAME")

try:
	global dbconn
	dbconn = psycopg2.connect(database='AttendanceDemo', user='root', password='root', host='41.76.169.14') 
	print('Connected from outside treasury')


except:
	
	dbconn = psycopg2.connect(database='AttendanceDemo', user='root', password='root', host='10.102.5.70')
	print('Connected from within treasury')	
	
	
def db_reconnect():
	dbconn = psycopg2.connect(database='AttendanceDemo', user='root', password='root', host='10.102.5.70') 
	print('Connected from outside treasury')
		
def InsertToDbSchedule():
	input_values = [mincountyselected,courseselected,desgselected,fnameentry.get(),snameentry.get(),lnameentry.get(),persnumentry.get(),natidentry.get(),mobnumentry.get(),emailidentry.get(),schfromentry.get(),schtoentry.get()]
	schedule_values=[]
	for i in input_values:
		i=i.rstrip()
		schedule_values.append(i)

	cur = dbconn.cursor()

	cur.execute("select max(participant_id)+1 from schedule")
	participant_id_increment = cur.fetchone()
	inc_max_pid=[]
	for x in participant_id_increment:
		inc_max_pid.append(x)

	cur.execute("""insert into schedule(ministry_county_id,course_id,designation_id,participant_id,first_name,middle_name,sur_name,personal_id,national_id,mobile_no,email_id,scheduled_from,scheduled_to)\
	values (%s,%s,%s,%s,'%s','%s','%s','%s',%s,%s,'%s','%s','%s')""" %(schedule_values[0],schedule_values[1],schedule_values[2],inc_max_pid[0],schedule_values[3],schedule_values[4],schedule_values[5],schedule_values[6],schedule_values[7],schedule_values[8],schedule_values[9],schedule_values[10],schedule_values[11]))
	cur.execute("commit;") 
	ClearFieldsSchedule()
	messagebox.showinfo('Notify','Record entered successfully!') 

def ClearFieldsSchedule():
	fnameentry.delete(0,END)
	snameentry.delete(0,END)
	lnameentry.delete(0,END)
	persnumentry.delete(0,END)
	natidentry.delete(0,END)
	mobnumentry.delete(0,END)
	emailidentry.delete(0,END)
	schfromentry.delete(0,END)
	schtoentry.delete(0,END)
		
def schedule_form():
	
	main_frame3.pack_forget()
	frame2.pack_forget()
	frame.pack()
	
	ttk.Label(frame,text='SCHEDULE FORM',font=("Helvetica", 16)).grid(column=2, row=1, sticky=(W,E))
	ttk.Label(frame,text='').grid(column=2, row=2, sticky=(W,E))
	#creating the ministry/county label, combobox 
	ttk.Label(frame,text='Ministry/County: ').grid(column=1, row=3, sticky=(W,E))
	global mincountybox
	mincountybox = ttk.Combobox(frame, state='readonly', width='30', justify='left')
	mincountybox.grid(column=2, row=3, sticky=(W,E))
	mincountybox.current()
	cur = dbconn.cursor()
	cur.execute("select ministry_county_id||' '||ministry_county_name as min_county from ministry_county order by ministry_county_name")
	mincounty = cur.fetchall()
	mincountylist=[]
	for i in mincounty:
		for x in i:
			mincountylist.append(x)
	mincountybox['values'] = mincountylist
	def newselection(event):
		value_of_combo = mincountybox.get()
		global mincountyselected
		mincountyselected=value_of_combo[0:2]    
	mincountybox.bind('<<ComboboxSelected>>',newselection)

	#creating the course label, combobox 
	ttk.Label(frame,text='Course: ').grid(column=1, row=4, sticky=(W,E))
	global coursecombox
	coursecombox = ttk.Combobox(frame, state='readonly', width='30', justify='left')
	coursecombox.grid(column=2, row=4, sticky=(W,E))
	cur = dbconn.cursor()
	cur.execute("select course_id||'  '||course_name from courses")
	course = cur.fetchall()
	courselist=[]
	for i in course:
		for x in i:
			courselist.append(x)
	coursecombox['values'] = courselist
	def newselection(event):
		value_of_combo = coursecombox.get()
		global courseselected
		courseselected=value_of_combo[0:2]    
	coursecomboxselected=coursecombox.bind('<<ComboboxSelected>>',newselection)

	#creating the designation label, combobox 
	ttk.Label(frame,text='Designation: ').grid(column=1, row=5, sticky=(W,E))
	global desgcombox
	desgcombox = ttk.Combobox(frame, state='readonly', width='30', justify='left')
	desgcombox.grid(column=2, row=5, sticky=(W,E))
	cur = dbconn.cursor()
	cur.execute("select designation_code||'    '|| designation_name from designation order by designation_name asc")
	desg = cur.fetchall()
	desglist=[]
	for i in desg:
		for x in i:
			desglist.append(x)
	desgcombox['values'] = desglist
	def newselection(event):
		value_of_combo = desgcombox.get()
		global desgselected
		desgselected=value_of_combo[0:4]
	desgselected=desgcombox.bind('<<ComboboxSelected>>', newselection)

	#creating the first name label, entrybox
	ttk.Label(frame,text='First Name: ').grid(column=1, row=6, sticky=(W,E))
	firstname=StringVar()  
	global fnameentry  
	fnameentry=ttk.Entry(frame,width=15,textvariable=firstname)
	fnameentry.grid(column=2, row=6, sticky=(W,E))

	#creating the second name label, entrybox
	ttk.Label(frame,text='Second Name: ').grid(column=1, row=7, sticky=(W,E))
	secondname=StringVar()   
	global snameentry 
	snameentry=ttk.Entry(frame,width=15,textvariable=secondname)
	snameentry.grid(column=2, row=7, sticky=(W,E))


	#creating the sur name label, entrybox
	ttk.Label(frame,text='Sur Name: ').grid(column=1, row=8, sticky=(W,E))
	lastname=StringVar() 
	global lnameentry   
	lnameentry=ttk.Entry(frame,width=15,textvariable=lastname)
	lnameentry.grid(column=2, row=8, sticky=(W,E))


	#creating the personal number label, entrybox
	ttk.Label(frame,text='Personal Number: ').grid(column=1, row=9, sticky=(W,E))
	persnum=StringVar()   
	global persnumentry 
	persnumentry=ttk.Entry(frame,width=15,textvariable=persnum)
	persnumentry.grid(column=2, row=9, sticky=(W,E))


	#creating the national id label, entrybox
	ttk.Label(frame,text='National ID: ').grid(column=1, row=10, sticky=(W,E))
	natid=IntVar()    
	global natidentry
	natidentry=ttk.Entry(frame,width=15,textvariable=natid)
	natidentry.grid(column=2, row=10, sticky=(W,E))


	#creating the mobile number label, entrybox
	ttk.Label(frame,text='Mobile Number: ').grid(column=1, row=11, sticky=(W,E))
	mobnum=IntVar()   
	global mobnumentry 
	mobnumentry=ttk.Entry(frame,width=15,textvariable=mobnum)
	mobnumentry.grid(column=2, row=11, sticky=(W,E))

	#creating the email id label, entrybox
	ttk.Label(frame,text='Email ID: ').grid(column=1, row=12, sticky=(W,E))
	emailid=StringVar()    
	global emailidentry
	emailidentry=ttk.Entry(frame,width=15,textvariable=emailid)
	emailidentry.grid(column=2, row=12, sticky=(W,E))

	#creating the schedule date from label, entrybox
	ttk.Label(frame,text='Schedule date From: ').grid(column=1, row=13, sticky=(W,E))
	ttk.Label(frame,text='YYYY-MM-DD').grid(column=3, row=13, sticky=(W,E))
	schfrom=StringVar()
	global schfromentry    
	schfromentry=ttk.Entry(frame,width=15,textvariable=schfrom)
	schfromentry.grid(column=2, row=13, sticky=(W,E))

	#creating the schedule date to label, entrybox
	ttk.Label(frame,text='Schedule date To: ').grid(column=1, row=14, sticky=(W,E))
	ttk.Label(frame,text='YYYY-MM-DD').grid(column=3, row=14, sticky=(W,E))
	schto=StringVar()    
	global schtoentry
	schtoentry=ttk.Entry(frame,width=15,textvariable=schto)
	schtoentry.grid(column=2, row=14, sticky=(W,E))

	#submitbutton
	global submitbtn
	submitbtn=ttk.Button(internal_frame, text='Submit', width=10, command=InsertToDbSchedule)
	submitbtn.grid(column=1, row=1,sticky=(W,E))

	#clearbutton
	global clearbtn
	clearbtn=ttk.Button(internal_frame, text='Clear', width=10, command=ClearFieldsSchedule)
	clearbtn.grid(column=1, row=2,sticky=(W,E))

	#exitbutton
	global closebtn
	closebtn=ttk.Button(internal_frame, text='Close', width=10, command=frame.pack_forget)
	closebtn.grid(column=1, row=3,sticky=(W,E))
	
	ttk.Label(frame,text='').grid(column=1, row=18, sticky=(W,E))
	
def ClearFields():
	mincountytext.delete('1.0',END)
	coursetext.delete('1.0',END)
	desgtext.delete('1.0',END)
	fnametext.delete('1.0',END)
	snametext.delete('1.0',END)
	lnametext.delete('1.0',END)
	persnumtext.delete('1.0',END)
	natidtext.delete('1.0',END)
	#phoneentry.delete(0,END)
	emailidtext.delete('1.0',END)
	schfromtext.delete('1.0',END)
	schtotext.delete('1.0',END)
	attfromtext.delete('1.0',END)
	atttotext.delete('1.0',END)

def retrieve_from_schedule_RegisterForm():
	
	ClearFields()
	phoneentry_value=phoneentry.get()
	if phoneentry_value =='':
		messagebox.showinfo('Hint Alert!','Please enter phone number','Notify')
		
	else:
		cur = dbconn.cursor()
		cur.execute('select * from schedule where mobile_no = %s' %(phoneentry_value))
		global output
		output = cur.fetchall()
		
		if cur.rowcount > 0:
			global output_values
			output_values = []
			for i in output:
				for x in i:
					output_values.append(x)
			global output1
			global output2 
			global output3		
			min_county_id = output_values[0]
			course_id = output_values[1]
			desg_id = output_values[2]
			cur.execute('select ministry_county_id, ministry_county_name from ministry_county where ministry_county_id = %s' %(min_county_id))
			output1 = cur.fetchone()
			cur.execute('select course_id, course_name from courses where course_id = %s' %(course_id))
			output2 = cur.fetchone()
			cur.execute('select designation_code, designation_name from designation where designation_code = %s' %(desg_id))
			output3 = cur.fetchone()
			
			mincounty.set(output1[1])
			mincountytext.insert(INSERT, mincounty.get() )
			
			course.set(output2[1])
			coursetext.insert(INSERT, course.get() )
			
			desg.set(output3[1])
			desgtext.insert(INSERT, desg.get() )

			firstname.set(output_values[4])
			fnametext.insert(INSERT, firstname.get() )

			secondname.set(output_values[5])
			snametext.insert(INSERT, secondname.get())

			lastname.set(output_values[6])
			lnametext.insert(INSERT, lastname.get())

			persnum.set(output_values[7]) 
			persnumtext.insert(INSERT, persnum.get())

			if output_values[8] is None:
				natid.set(0)
				natidtext.insert(INSERT, natid.get())

			else:
				natid.set(output_values[8])
				natidtext.insert(INSERT, natid.get())

			emailid.set(output_values[10])
			emailidtext.insert(INSERT, emailid.get())

			schfrom.set(output_values[11])  
			schfromtext.insert(INSERT, schfrom.get())

			schto.set(output_values[12])
			schtotext.insert(INSERT, schto.get())
		else:
			messagebox.showinfo('Hint Alert!','No such phone number found, please retry!')				

def retrieve_from_register():
	
	ClearFields()
	phoneentry_value=phoneentry.get()
	if phoneentry_value =='':
		messagebox.showinfo('Hint Alert!','Please enter phone number','Notify')
	else:
		cur = dbconn.cursor()
		cur.execute('select * from register where mobile_no = %s' %(phoneentry_value))
		global output
		output = cur.fetchall()
		
		if cur.rowcount > 0:
			global output_values
			output_values = []
			for i in output:
				for x in i:
					output_values.append(x)
			global output1
			global output2 
			global output3		
			min_county_id = output_values[0]
			course_id = output_values[1]
			desg_id = output_values[2]
			cur.execute('select ministry_county_id, ministry_county_name from ministry_county where ministry_county_id = %s' %(min_county_id))
			output1 = cur.fetchone()
			cur.execute('select course_id, course_name from courses where course_id = %s' %(course_id))
			output2 = cur.fetchone()
			cur.execute('select designation_code, designation_name from designation where designation_code = %s' %(desg_id))
			output3 = cur.fetchone()
			
			mincounty.set(output1[1])
			mincountytext.insert(INSERT, mincounty.get() )
			
			course.set(output2[1])
			coursetext.insert(INSERT, course.get() )
			
			desg.set(output3[1])
			desgtext.insert(INSERT, desg.get() )

			firstname.set(output_values[4])
			fnametext.insert(INSERT, firstname.get() )

			secondname.set(output_values[5])
			snametext.insert(INSERT, secondname.get())

			lastname.set(output_values[6])
			lnametext.insert(INSERT, lastname.get())
			
			persnum.set(output_values[7]) 
			persnumtext.insert(INSERT, persnum.get())

			if output_values[8] is None:
				natid.set(0)
				natidtext.insert(INSERT, natid.get())

			else:
				natid.set(output_values[8])
				natidtext.insert(INSERT, natid.get())

			emailid.set(output_values[10])
			emailidtext.insert(INSERT, emailid.get())

			schfrom.set(output_values[11])  
			schfromtext.insert(INSERT, schfrom.get())

			schto.set(output_values[12])
			schtotext.insert(INSERT, schto.get())
			
			attfrom.set(output_values[13])  
			attfromtext.insert(INSERT, attfrom.get())

			attto.set(output_values[14])
			atttotext.insert(INSERT, attto.get())
			
			
		else:
			messagebox.showinfo('Hint Alert!','No such phone number found, please retry!')
			#schedule_form()
	
	

def InsertToDb():	#insert to register

	min_county_id = output_values[0]
	course_id = output_values[1]
	desg_id = output_values[2]
	participant_id = output_values[3]
	
	mincountytext.delete('1.0',END)
	coursetext.delete('1.0',END)
	desgtext.delete('1.0',END)
	
	mincounty.set(output_values[0])
	mincountytext.insert(INSERT, mincounty.get() )
	
	course.set(output_values[1])
	coursetext.insert(INSERT, course.get() )
	
	desg.set(output_values[2])
	desgtext.insert(INSERT, desg.get() )
	
	input_values = [mincountytext.get('1.0',END),coursetext.get('1.0',END),desgtext.get('1.0',END),fnametext.get('1.0',END), snametext.get('1.0',END), lnametext.get('1.0',END), persnumtext.get('1.0',END), natidtext.get('1.0',END), phoneentry.get(), emailidtext.get('1.0',END), schfromtext.get('1.0',END), schtotext.get('1.0',END),attfromtext.get('1.0',END),atttotext.get('1.0',END)]
	
	schedule_values=[]
	for i in input_values:
		i=i.rstrip('\n')
		schedule_values.append(i)
		cur = dbconn.cursor()

	#insert_register	
	cur.execute("""insert into register(ministry_county_id,course_id,designation_id,participant_id,first_name,middle_name,sur_name,personal_id,national_id,mobile_no,email_id,scheduled_from,scheduled_to,attended_from,attended_to)\
	values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')\
	""" %(schedule_values[0],schedule_values[1],schedule_values[2],participant_id,schedule_values[3],schedule_values[4],schedule_values[5],schedule_values[6],schedule_values[7],schedule_values[8],schedule_values[9],schedule_values[10],schedule_values[11],schedule_values[12],schedule_values[13]))
	cur.execute("commit;") 
	messagebox.showinfo('Notify','Record entered successfully! in register') 

def update_schedule_register():
	min_county_id = output_values[0]
	course_id = output_values[1]
	desg_id = output_values[2]
	participant_id = output_values[3]
	
	mincountytext.delete('1.0',END)
	coursetext.delete('1.0',END)
	desgtext.delete('1.0',END)
	
	mincounty.set(output_values[0])
	mincountytext.insert(INSERT, mincounty.get() )
	
	course.set(output_values[1])
	coursetext.insert(INSERT, course.get() )
	
	desg.set(output_values[2])
	desgtext.insert(INSERT, desg.get() )
	
	input_values = [mincountytext.get('1.0',END),coursetext.get('1.0',END),desgtext.get('1.0',END),fnametext.get('1.0',END), snametext.get('1.0',END), lnametext.get('1.0',END), persnumtext.get('1.0',END), natidtext.get('1.0',END), phoneentry.get(), emailidtext.get('1.0',END), schfromtext.get('1.0',END), schtotext.get('1.0',END),attfromtext.get('1.0',END),atttotext.get('1.0',END)]
	
	schedule_values=[]
	for i in input_values:
		i=i.rstrip('\n')
		schedule_values.append(i)
		cur = dbconn.cursor()
	
	if schedule_values[12]=='' and schedule_values[13]=='':
		#update_schedule
		cur.execute("update schedule set ministry_county_id='%s',course_id='%s',designation_id='%s',first_name='%s',middle_name='%s',sur_name='%s',personal_id='%s',national_id=%s,email_id='%s',scheduled_from='%s',scheduled_to='%s' where mobile_no = %s" %(schedule_values[0],schedule_values[1],schedule_values[2],schedule_values[3],schedule_values[4],schedule_values[5],schedule_values[6],schedule_values[7],schedule_values[9],schedule_values[10],schedule_values[11],schedule_values[8]))
		cur.execute("commit;") 
		messagebox.showinfo('Notify','Record updated successfully! in schedule') 
	
	else:
		#update_schedule
		cur.execute("update schedule set ministry_county_id='%s',course_id='%s',designation_id='%s',first_name='%s',middle_name='%s',sur_name='%s',personal_id='%s',national_id=%s,email_id='%s',scheduled_from='%s',scheduled_to='%s' where mobile_no = %s" %(schedule_values[0],schedule_values[1],schedule_values[2],schedule_values[3],schedule_values[4],schedule_values[5],schedule_values[6],schedule_values[7],schedule_values[9],schedule_values[10],schedule_values[11],schedule_values[8]))
		cur.execute("commit;") 
		messagebox.showinfo('Notify','Record updated successfully! in schedule') 
		
		#update_register
		cur.execute("update register set ministry_county_id='%s',course_id='%s',designation_id='%s',first_name='%s',middle_name='%s',sur_name='%s',personal_id='%s',national_id=%s,email_id='%s',scheduled_from='%s',scheduled_to='%s',attended_from='%s',attended_to='%s' where mobile_no = %s" %(schedule_values[0],schedule_values[1],schedule_values[2],schedule_values[3],schedule_values[4],schedule_values[5],schedule_values[6],schedule_values[7],schedule_values[9],schedule_values[10],schedule_values[11],schedule_values[12],schedule_values[13],schedule_values[8]))
		cur.execute("commit;") 
		messagebox.showinfo('Notify','Record entered successfully! in register') 


def generate_by_date():
	
	global gui
	gui = Tk()
	gui.title('Enter From & To Dates')
	gui.geometry("350x200+30+30")

	frame = ttk.Frame(gui,padding='10 10 10 10')
	frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
	
	
	ttk.Label(frame,text='From: ').grid(column=1, row=1, sticky=(W,E))
	ttk.Label(frame,text='YYYY-MM-DD').grid(column=3, row=1, sticky=(W,E))
	getfrom=StringVar()
	global fromentry    
	fromentry=ttk.Entry(frame,width=15,textvariable=getfrom)
	fromentry.grid(column=2, row=1, sticky=(W,E))

	
	ttk.Label(frame,text='To: ').grid(column=1, row=2, sticky=(W,E))
	ttk.Label(frame,text='YYYY-MM-DD').grid(column=3, row=2, sticky=(W,E))
	getto=StringVar()    
	global toentry
	toentry=ttk.Entry(frame,width=15,textvariable=getto)
	toentry.grid(column=2, row=2, sticky=(W,E))


	global okbtn
	okbtn=ttk.Button(frame, text='OK', width=8, command=generate_by_date_2)
	okbtn.grid(column=4, row=3,sticky=(W,E))
	gui.mainloop()
	
	
def generate_by_date_2():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where scheduled_from between  '%s' and '%s' order by scheduled_from;"%(fromentry.get(),toentry.get()))
		get_sch_report=cur.fetchall()
		
		if get_sch_report ==[]:
			messagebox.showwarning('Warning', "No data found from period '%s' to '%s'" %(fromentry.get(),toentry.get()))
		else: 
			file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
			all_trained_mdac_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='Generate by date All Trained MDAC Report', defaultextension=".csv", filetypes= file_format)
			outfile = open(all_trained_mdac_report, "w")
			writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			writer.writerow( ['ministry_county_name','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
			
			for i in get_sch_report:
				writer.writerows([i])
			outfile.close()
			gui.destroy()
			
	except psycopg2.InternalError:
		messagebox.showerror('Error', 'You need to input dates')
		messagebox.showerror('Error', 'Fatal Error occured')
		sys.exit(0)
			
	except:
		pass
		
def mdac_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute('select distinct mc.ministry_county_name,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id order by mc.ministry_county_name;')
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_trained_mdac_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All Trained MDAC Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_trained_mdac_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministry_county_name','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()
	except:
		pass 

def counties_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where mc.ministry_county_name like '%County' order by counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_counties_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All Counties Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_counties_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()
		
	except:
		pass
		
def mdas_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as mdas,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where mc.ministry_county_name not like '%County' order by mdas;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All MDAs Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['mdas','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()
		
	except:
		pass

def p2p_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like '%Procure To Pay' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All P2P Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
	
	except:
		pass
		
def iproc_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like '%Procurement' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All IPROC Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
		
	except:
		pass
def r2c_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like '%Revenue To Cash' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All R2C Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
	
	except:
		pass
		
def r2r_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like '%Record To Report' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All R2R Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
		
	except:
		pass
		
def p2b_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like '%Plan To Budget' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All P2B Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
	
	except:
		pass
		
def ict_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like 'ICT%' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All ICT Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
	
	except:
		pass
		
def c2c_trained():
	
	try:
		cur=dbconn.cursor()
		cur.execute("select distinct mc.ministry_county_name as ministries_and_counties,c.course_name, r.first_name, r.middle_name, r.sur_name, r.personal_id, r.national_id, r.mobile_no, r.email_id,r.scheduled_from,r.scheduled_to,r.attended_from,r.attended_to from register r join ministry_county mc on mc.ministry_county_id = r.ministry_county_id join courses c on c.course_id = r.course_id where c.course_name like 'Communicate To Change' order by ministries_and_counties;")
		get_sch_report=cur.fetchall() 
		file_format = [("CSV files","*.csv"),("Text files","*.txt"),("All files","*.*")] 
		all_mdas_trained_report = asksaveasfilename( title ="Save As='.csv'", initialdir="C:\\Users\\usrname", initialfile ='All C2C Trained Report', defaultextension=".csv", filetypes= file_format)
		outfile = open(all_mdas_trained_report, "w")
		writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow( ['ministries_and_counties','course_name','first_name','middle_name','sur_name','personal_id','national_id','mobile_no','email_id','scheduled_from','scheduled_to','attended_from','attended_to'])
		
		for i in get_sch_report:
			writer.writerows([i])
		outfile.close()	
		
	except:
		pass

def get_num_changemgt():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Communicate To Change' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Communicate To Change' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Communicate To Change'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
					
	messagebox.showinfo('Get Numbers','Total participants trained on Change Management = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_p2p():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Procure To Pay' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Procure To Pay' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Procure To Pay'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
	
	messagebox.showinfo('Get Numbers','Total participants trained on Procure to Pay = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_p2b():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Plan To Budget' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Plan To Budget' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Plan To Budget'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
	
	messagebox.showinfo('Get Numbers','Total participants trained on Plan to Budget = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_r2c():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Revenue To Cash' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Revenue To Cash' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Revenue To Cash'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
			
	
	messagebox.showinfo('Get Numbers','Total participants trained on Revenue to cash = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_r2r():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Record To Report' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Record To Report' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Record To Report'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
			
	messagebox.showinfo('Get Numbers','Total participants trained on Record to Report = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_iproc():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'I-Procurement' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'I-Procurement' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'I-Procurement'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
			
	messagebox.showinfo('Get Numbers','Total participants trained on I-Procurement = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
			
def get_num_su():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Super Users' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'Super Users' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'Super Users'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
			
			
	messagebox.showinfo('Get Numbers','Total participants trained on Super Users = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))
	
def get_num_ict():
	cur = dbconn.cursor()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'ICT To Support' and ministry_county_name like '%County';")
	output1 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id join ministry_county mc on mc.ministry_county_id = r.ministry_county_id where course_name = 'ICT To Support' and ministry_county_name not like '%County';")
	output2 = cur.fetchall()
	cur.execute("select count(*) from register r join courses c on c.course_id=r.course_id where course_name = 'ICT To Support'")
	output3 = cur.fetchall()
	
	for i in output1:
		for x in i:
			output1=x
			
	for i in output2:
		for y in i:
			output2=y
			
	for i in output3:
		for z in i:
			output3=z
			
			
	messagebox.showinfo('Get Numbers','Total participants trained on ICT To Support = %s \n MDAs = %s \n Counties = %s'%(output3,output2,output1))

def get_num_mdas():
	cur = dbconn.cursor()
	cur.execute("select count(distinct mobile_no) from register join ministry_county on ministry_county.ministry_county_id = register.ministry_county_id where ministry_county_name not like '%County';")
	output = cur.fetchall()
	for i in output:
		for x in i:
			messagebox.showinfo('Get Numbers','Total MDAs trained = '+str(x))

def get_num_counties():
	cur = dbconn.cursor()
	cur.execute("select count(distinct mobile_no) from register join ministry_county on ministry_county.ministry_county_id = register.ministry_county_id where ministry_county_name like '%County';")
	output = cur.fetchall()
	for i in output:
		for x in i:
			messagebox.showinfo('Get Numbers','Total Participants trained from the counties = '+str(x))

def get_num_all():
	cur = dbconn.cursor()
	cur.execute("select count(distinct mobile_no) from register join ministry_county on ministry_county.ministry_county_id = register.ministry_county_id;")
	output = cur.fetchall()
	for i in output:
		for x in i:
			messagebox.showinfo('Get Numbers','Total participants trained = '+str(x))
   
def register_form():
	
	main_frame3.pack_forget()
	frame.pack_forget()
	frame2.pack()
	
	ttk.Label(frame2,text='REGISTER FORM',font=("Helvetica", 16)).grid(column=2, row=1, sticky=(W,E))
	ttk.Label(frame2,text='').grid(column=1, row=2, sticky=(W,E))
	
	#creating the mobile number label, entrybox
	phoneentrylabel=Label(frame2,text='Enter Phone Number: ',fg="red")
	phoneentrylabel.grid(column=1, row=3, sticky=(W,E))
	searchphonelabel=Label(frame2,text="*Search*",fg="red")
	searchphonelabel.grid(column=3, row=3, sticky=(W,E))
	global mobnum
	mobnum=IntVar()
	global phoneentry    
	phoneentry=Entry(frame2,width=15,textvariable=mobnum)
	phoneentry.grid(column=2, row=3, sticky=(W,E))

	#creating the Ministry/County label, entrybox
	ttk.Label(frame2,text='Ministry/County: ').grid(column=1, row=4, sticky=(W,E))
	global mincounty
	mincounty=StringVar()
	global mincountytext
	mincountytext=Text(frame2,width=30,height=1,bg='white')
	mincountytext.grid(column=2, row=4, sticky=(W,E))

	#creating the course label, entrybox
	ttk.Label(frame2,text='Course: ').grid(column=1, row=5, sticky=(W,E))
	global course
	course=StringVar()
	global coursetext
	coursetext=Text(frame2,width=30,height=1,bg='white')
	coursetext.grid(column=2, row=5, sticky=(W,E))

	#creating the designation label, entrybox
	ttk.Label(frame2,text='Designation: ').grid(column=1, row=6, sticky=(W,E))
	global desg
	desg=StringVar()
	global desgtext
	desgtext=Text(frame2,width=30,height=1,bg='white')
	desgtext.grid(column=2, row=6, sticky=(W,E))

	#creating the first name label, entrybox
	ttk.Label(frame2,text='First Name: ').grid(column=1, row=7, sticky=(W,E))
	global firstname
	firstname=StringVar()
	global fnametext
	fnametext=Text(frame2,width=30,height=1,bg='white')
	fnametext.grid(column=2, row=7, sticky=(W,E))

	#creating the second name label, entrybox
	ttk.Label(frame2,text='Second Name: ').grid(column=1, row=8, sticky=(W,E))
	global secondname
	secondname=StringVar() 
	global snametext 
	snametext=Text(frame2,width=30,height=1,bg='white')
	snametext.grid(column=2, row=8, sticky=(W,E))

	#creating the sur name label, entrybox
	ttk.Label(frame2,text='Sur Name: ').grid(column=1, row=9, sticky=(W,E))
	global lastname
	lastname=StringVar()  
	global lnametext
	lnametext=Text(frame2,width=30,height=1,bg='white')
	lnametext.grid(column=2, row=9, sticky=(W,E))

	#creating the personal number label, entrybox
	ttk.Label(frame2,text='Personal Number: ').grid(column=1, row=10, sticky=(W,E))
	global persnum
	persnum=StringVar() 
	global persnumtext
	persnumtext=Text(frame2,width=30,height=1,bg='white')
	persnumtext.grid(column=2, row=10, sticky=(W,E))

	#creating the national id label, entrybox
	ttk.Label(frame2,text='National ID: ').grid(column=1, row=11, sticky=(W,E))
	global natid
	natid=IntVar() 
	global natidtext
	natidtext=Text(frame2,width=30,height=1,bg='white')
	natidtext.grid(column=2, row=11, sticky=(W,E))

	#creating the email id label, entrybox
	ttk.Label(frame2,text='Email ID: ').grid(column=1, row=12, sticky=(W,E))
	global emailid
	emailid=StringVar() 
	global emailidtext 
	emailidtext=Text(frame2,width=30,height=1)
	emailidtext.grid(column=2, row=12, sticky=(W,E))

	#creating the schedule date from label, entrybox
	ttk.Label(frame2,text='Schedule date From: ').grid(column=1, row=13, sticky=(W,E))
	ttk.Label(frame2,text='YYYY-MM-DD').grid(column=3, row=13, sticky=(W,E))
	global schfrom
	schfrom=StringVar() 
	global schfromtext
	schfromtext=Text(frame2,width=30,height=1)
	schfromtext.grid(column=2, row=13, sticky=(W,E))

	#creating the schedule date to label, entrybox
	ttk.Label(frame2,text='Schedule date To: ').grid(column=1, row=14, sticky=(W,E))
	ttk.Label(frame2,text='YYYY-MM-DD').grid(column=3, row=14, sticky=(W,E))
	global schto
	schto=StringVar() 
	global schtotext
	schtotext=Text(frame2,width=30,height=1)
	schtotext.grid(column=2, row=14, sticky=(W,E))

	#creating the schedule date from label, entrybox
	ttk.Label(frame2,text='Attended From: ').grid(column=1, row=15, sticky=(W,E))
	ttk.Label(frame2,text='YYYY-MM-DD').grid(column=3, row=15, sticky=(W,E))
	global attfrom
	attfrom=StringVar()   
	global attfromtext
	attfromtext=Text(frame2,width=30,height=1)
	attfromtext.grid(column=2, row=15, sticky=(W,E))

	#creating the schedule date to label, entrybox
	ttk.Label(frame2,text='Attended To: ').grid(column=1, row=16, sticky=(W,E))
	ttk.Label(frame2,text='YYYY-MM-DD').grid(column=3, row=16, sticky=(W,E))
	global attto
	attto=StringVar()    
	global atttotext
	atttotext=Text(frame2,width=30,height=1)
	atttotext.grid(column=2, row=16, sticky=(W,E))
	
	ttk.Label(frame2,text='').grid(column=1, row=17, sticky=(W,E))
	 
	#checkschedulebutton
	global fndbtn
	fndbtn=ttk.Button(internal_frame2, text='Check schedule', width=12, command=retrieve_from_schedule_RegisterForm)
	fndbtn.grid(column=1, row=1, sticky=(W,E))

	#clearbutton
	clearbtn=ttk.Button(internal_frame2, text='Clear', width=12, command=ClearFields)
	clearbtn.grid(column=1, row=2, sticky=(W,E))

	#checkregisterbutton
	global check_reg_btn
	check_reg_btn=ttk.Button(internal_frame2, text='Check register', width=12, command=retrieve_from_register)
	check_reg_btn.grid(column=1, row=3, sticky=(W,E))
	
	#savebutton
	global savebtn
	savebtn=ttk.Button(internal_frame2, text='Save', width=12, command=InsertToDb)
	savebtn.grid(column=1, row=4, sticky=(W,E))
	
	#updatebutton
	global updatebtn
	updatebtn=ttk.Button(internal_frame2, text='Update', width=12, command=update_schedule_register)
	updatebtn.grid(column=1, row=5, sticky=(W,E))

	#closebutton
	closebtn=ttk.Button(internal_frame2, text='Close', width=12, command=frame2.pack_forget)
	closebtn.grid(column=1, row=6, sticky=(W,E))
	

main_gui = Tk()
main_gui.title('IFMIS ATTENDANCE SYSTEM')
main_gui.geometry("1200x640+30+30")

main_frame = ttk.Frame(main_gui,padding='10 10 10 10')
main_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

main_frame2 = ttk.Frame(main_gui,padding='10 10 10 10')
main_frame2.pack(side=RIGHT, fill=BOTH, padx=5, pady=5)

main_frame3 = ttk.Frame(main_gui,padding='10 10 10 10')
main_frame3.pack(side=BOTTOM,fill=BOTH,padx=5, pady=5)

frame = ttk.Frame(main_frame, relief=GROOVE)
frame.pack(side=LEFT, fill=BOTH,)

ttk.Label(main_frame3,text='VERSION 2.0',font=("Helvetica", 7)).grid(column=2, row=2, sticky=(W,E))
ttk.Label(main_frame3,text='AUTHOR: PAUL',font=("Helvetica", 7)).grid(column=2, row=3, sticky=(W,E))
ttk.Label(main_frame3,text='EMAIL: paul.k.karugu@gmail.com',font=("Helvetica", 7)).grid(column=2, row=4, sticky=(W,E))
ttk.Label(main_frame3,text="COPYRIGHT \u00A9 2014",font=("Helvetica", 7)).grid(column=2, row=5, sticky=(W,E))

frame2=ttk.Frame(main_frame2, relief=GROOVE)
frame2.pack(side=RIGHT, fill=BOTH)

internal_frame=ttk.Frame(frame,padding ='5 5 5 5', relief=GROOVE)
internal_frame.grid(column=4,row=19, sticky=(W,E))
internal_frame2=ttk.Frame(frame2, padding ='5 5 5 5', relief=GROOVE)
internal_frame2.grid(column=4,row=18, sticky=(W,E))

#menubar
menubar = Menu(main_gui)
# create a pulldown menu, and add it to the menu bar
connect = Menu(menubar, tearoff=0)
connect.add_command(label="Schedule", command=schedule_form)
connect.add_command(label="Register", command=register_form)
connect.add_separator()
connect.add_command(label="Exit", command=main_gui.destroy)
menubar.add_cascade(label="Connect To", menu=connect)

reports = Menu(menubar, tearoff=0)
reports.add_command(label="All Trained Partcipants [MDA&C]", command=mdac_trained)
reports.add_command(label="All MDAs Trained Partcipants", command=mdas_trained)
reports.add_command(label="All Counties Trained Partcipants", command=counties_trained)
reports.add_command(label="All Change Mgt Trained", command= c2c_trained)
reports.add_command(label="All P2P Trained", command= p2p_trained)
reports.add_command(label="All I-Proc Trained", command= iproc_trained)
reports.add_command(label="All P2B Trained", command= p2b_trained)
reports.add_command(label="All R2C Trained", command= r2c_trained)
reports.add_command(label="All R2R Trained", command= r2r_trained)
reports.add_command(label="All ICT Trained", command= ict_trained)
reports.add_command(label="Generate by date", command=generate_by_date)
menubar.add_cascade(label="Reports", menu=reports)

getnum = Menu(menubar, tearoff=0)
getnum.add_command(label="Change Mgt", command=get_num_changemgt)
getnum.add_command(label="Procure to Pay", command=get_num_p2p )
getnum.add_command(label="Plan to Budget", command=get_num_p2b)
getnum.add_command(label="Revenue to Cash", command=get_num_r2c )
getnum.add_command(label="Record to Report", command=get_num_r2r )
getnum.add_command(label="I-Procurement", command=get_num_iproc)
getnum.add_command(label="ICT", command= get_num_ict)
getnum.add_command(label="Super Users", command= get_num_su)
getnum.add_command(label="MDAs", command= get_num_mdas)
getnum.add_command(label="Counties", command= get_num_counties)
getnum.add_command(label="All Trained", command= get_num_all)
menubar.add_cascade(label="Get Numbers", menu=getnum)
main_gui.config(menu=menubar)


main_gui.mainloop()


	



