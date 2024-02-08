from django.shortcuts import render, redirect
from detection.models import Signup,Detect
from django.contrib import messages
from django.contrib.auth import login
import uuid
import mysql.connector


mysql=mysql.connector.connect(
    host="localhost",
    user="jithin",
    passwd="jithin",
    database="crime_detect"
) ##

mycursor=mysql.cursor()#

def loginPage(request):

    if request.method=='POST':
        if request.POST['button']:
            un=request.POST['username']
            ps=request.POST['password']
            val=[un,ps]#
            sql="SELECT * FROM login WHERE USERNAME=%s AND PASSWORD=%s"#
            mycursor.execute(sql,val)#
            result=mycursor.fetchone()
            
            if result is not None:
                return redirect('home')
                # return render(request,'detection/dashboard.html',{'user':un})
            else:
                messages.success(request, 'Username or Password is incorrect')
                return render(request,'detection/login.html',{})
        mysql.commit()#
    return render(request,'detection/login.html',{})

def registerPage(request):
    if request.method=='POST':
        if request.POST['button'] and request.POST['password1']==request.POST['password2']:

            sql="insert into login(UNIQUE_ID,USERNAME,EMAIL,PASSWORD) values(%s,%s,%s,%s)"#
            ui= str(uuid.uuid4())
            un=request.POST['username']
            em=request.POST['email']
            ps=request.POST['password1']
            val=[ui,un,em,ps]#
            mycursor.execute(sql,val)#
            mysql.commit()#
            return redirect('login')
        else:
            return render(request,'detection/register.html',{})
    return render(request,'detection/register.html',{})

def home(request):
    un = request.POST.get('username')
    if un is not None:
        obj=Detect.objects.all()
        return render(request,'detection/dashboard.html',{'Detect':obj,'Name':un})
    else:
        return redirect('login')



def show(request,f_id):
    obj=Detect.objects.all()
    ob=obj[f_id-1]
    with open("detection/Images/Detect-"+str(f_id)+".jpg",'wb') as f:
        f.write(bytes(ob.IMAGE))
    return render(request,'detection/show.html',{'Image_src':"detection/Images/Detect-"+str(f_id)+".jpg"})
    
    