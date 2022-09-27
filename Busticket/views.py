from django.shortcuts import render,redirect
from django . http import HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.auth import logout
from datetime import date
# Create your views here.
def index(request):
    t=date.today()
    print(t)
    return render(request, 'index.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:           
            log=Login.objects.get(username=username,password=password)
            if log.role=='admin':
                return redirect('adminhome')
            elif log.role=='staff':
                staff=Staff.objects.get(login=log)
                request.session['sid']=staff.sid
                request.session['logid']=log.logid
                return redirect('staffhome')
            elif log.role=='user':
                user=User.objects.get(login=log)
                if user.ustatus=='waiting':
                    messages.warning(request, 'waiting for verification')
                    return render(request, 'login.html')
                elif user.ustatus=='approved':
                    request.session['id']=user.uid
                    request.session['logid']=log.logid
                    messages.success(request, 'User login Successfully')
                    return redirect('userhome')
                else:
                    context={
                        'msg':"user Doesnot Exist."
                    }
                    return render(request, 'login.html',context)
        except:
            context={
                'msg':"user Doesnot Exist."
            }
            return render(request, 'login.html',context)
    return render(request, 'login.html')


def userreg(request):
    try: 
        if request.method=='POST':
            fname=request.POST['fname'].capitalize()
            username=request.POST['username'].lower()
            password=request.POST['password']
            password2=request.POST['password2']
            dob=request.POST['dob']
            phone=request.POST['phone']
            email=request.POST['email']
            if password==password2:
                if Login.objects.filter(username=username) and User.objects.filter(email=email) :
                    return render(request, 'userreg.html')
                else:
                    Login.objects.create(username=username,password=password,role='user')
                    log=Login.objects.get(username=username,password=password,role='user')
                    User.objects.create(fname=fname,email=email,dob=dob,phone=phone,ustatus='approved',login=log)
                    return redirect('login')
            return render(request, 'userreg.html')
    except Exception as e:
        print(e)
    return render(request, 'userreg.html')



def adminhome(request):
    return render(request, 'adminhome.html')

def approve_user(request):
    user=User.objects.filter(ustatus='waiting')
    context={
        'user':user
    }
    if request.method=='POST':
        uid=request.POST['uid']
        data=User.objects.get(uid=uid)
        data.ustatus="approved"
        data.save()
        return redirect('approve_user')
    return render(request, 'approve_user.html',context)

def listuser(request):
    user=User.objects.filter(ustatus='approved')
    context={
        'user':user,
    }
    return render(request, 'listuser.html',context)

def add_dist(request):
    dist=District.objects.all()
    if request.method=='POST':
        dname=request.POST.get('distname').capitalize()
        if District.objects.filter(dname=dname):
            return render(request,'add_dist.html')
        else:
            District.objects.create(dname=dname)
            return redirect('add_dist')
    context={
        'dist':dist,
    }
    return render(request, 'add_dist.html',context)




def deletedist(request):
    did=request.POST['did']
    data=District.objects.get(did=did)
    data.delete()
    return redirect('add_dist')



def addlocation(request):
    dist=District.objects.all()
    loc=Location.objects.all()
    if request.method=='POST':
        did=District.objects.get(did=request.POST['dist'])
        lname=request.POST['lname'].capitalize()
        Location.objects.create(lname=lname,district=did)
    context={
        'dist':dist,
        'loc':loc,
    }
    return render(request, 'addlocation.html',context)



def deletelocation(request):
    lid=request.POST['lid']
    loc=Location.objects.get(lid=lid)
    loc.delete()
    return redirect('addlocation')


def addroute(request):
    loc=Location.objects.all()
    rot=Route.objects.all()
    if request.method=='POST':
        floc=request.POST['floc'].capitalize()
        tloc=request.POST['tloc'].capitalize()
        rmap=request.FILES['rmap']
        Route.objects.create(fromlocation=floc,tolocation=tloc,rmap=rmap)
    context={
        'loc':loc,
        'rot':rot,
    }
    return render(request,'addroute.html',context)

def deleteroute(request):
    bid=request.POST['bid']
    bus=Route.objects.get(bid=bid)
    bus.delete()
    return redirect('deletebus')




def addbus(request):
    bus=Bus.objects.all()
    if request.method=='POST':
        btype=request.POST['btype'].capitalize()
        bno=request.POST['bno']
        seats=request.POST['seats']
        Bus.objects.create(btype=btype,bno=bno,seats=seats)
        return redirect('addbus')
    context={
        'bus':bus,
    }
    return render(request, 'addbus.html',context)



def deletebus(request):
    bid=request.POST['bid']
    bus=Bus.objects.get(bid=bid)
    bus.delete()
    return redirect('addbus')



def bus_schedule(request):
    rot=Route.objects.all()
    bus=Bus.objects.all()
    bsch=Bus_Schedule.objects.all()
 
    if request.method=='POST':
        rid=Route.objects.get(rid=request.POST['route'])
        dtime=request.POST['dtime']
        atime=request.POST['atime']
        bid=Bus.objects.get(bid=request.POST['rbus'])
        Bus_Schedule.objects.create(route=rid,deptime=dtime,arrivaltime=atime,bus=bid)
    context={
        'rot':rot,
        'bus':bus,
        'bsch':bsch,
    }
    return render(request, 'bus_schedule.html',context)





def seatschedule(request):
    bus=Bus_Schedule.objects.all()
    data=Seat_Schedule.objects.all()
    if request.method=='POST':
        sdate=request.POST['sdate']
        seat=request.POST['st']
        rbus=Bus_Schedule.objects.get(bsc_id=request.POST['rbus'])
        Seat_Schedule.objects.create(schedule_date=sdate,bus_schedule=rbus,available_seat=seat)
        return redirect('seatschedule')
    context={
        'bus':bus,
        'data':data,
    }
    return render(request, 'seatschedule.html',context)



def ticketmanage(request):
    rot=Route.objects.all()
    bus=Bus.objects.all()
    tic=Ticketrate.objects.all()
    if request.method=='POST':
        rout=Route.objects.get(rid=request.POST['route'])
        adult=request.POST['adult']
        child=request.POST['child']
        btype=Bus.objects.get(bid=request.POST['btype'])
        Ticketrate.objects.create(route=rout,adult=adult,child=child,bustype=btype)
        return redirect('ticketmanage')
    context={
        'rot':rot,
        'bus':bus,
        'tic':tic,
    }
    return render(request, 'ticketmanage.html',context)




def allotstaff(request):
    bus_sc=Bus_Schedule.objects.all()
    seat_sc=Seat_Schedule.objects.all()
    staff_dt=Staff.objects.all()
    allot=Staffallot.objects.all()
    if request.method=='POST':
        bsch=Bus_Schedule.objects.get(bsc_id=request.POST['bsch'])
        scdate=Seat_Schedule.objects.get(seatid=request.POST['scdate'])
        staff=Staff.objects.get(sid=request.POST['staff'])
        Staffallot.objects.create(bus_schedule=bsch,schedule_date=scdate,staff=staff,status='allotted')
        return redirect('allotstaff')
    context={
        'bus':bus_sc,
        'seat':seat_sc,
         'staff':staff_dt,
         'data':allot,
    }
    return render(request, 'allotstaff.html',context)






def staffreg(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        fname=request.POST['fname'].capitalize()
        dob=request.POST['dob']
        phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address'].capitalize()
        gender=request.POST['gender'].capitalize()
        img=request.FILES["img"]
        if Login.objects.filter(username=username) and User.objects.filter(email=email) and Staff.objects.filter(email=email):
            return render(request, 'staffreg.html')
        else:
            Login.objects.create(username=username,password=password,role='staff')
            log=Login.objects.get(username=username,password=password,role='staff')
            Staff.objects.create(fname=fname,email=email,dob=dob,phone=phone,address=address,gender=gender,image=img,login=log)
            return redirect('liststaff')
    return render(request, 'staffreg.html')



def liststaff(request):
    staff=Staff.objects.all()
    context={
        'staff':staff
    }
    return render(request, 'liststaff.html',context)





def staffhome(request):
    sid=request.session['sid']
    staff=Staff.objects.get(sid=sid)
    return render(request, 'staffhome.html',{'staff':staff})



def listlocation(request):
    loc=Location.objects.all()
    context={
        'loc':loc,
    }
    return render(request, 'listlocation.html',context)


def listbus(request):
    bus=Bus.objects.all()
    context={
        'bus':bus,
    }
    return render(request, 'listbus.html',context)



def listroute(request):
    rot=Route.objects.all()
    context={
        'rot':rot,
    }
    return render(request, 'listroute.html',context)



def viewbus_schedule(request):
    bsch=Bus_Schedule.objects.all()
    context={
        'bsch':bsch,
    }
    return render(request, 'viewbus_schedule.html',context)







def viewseat_schedule(request):
    data=Seat_Schedule.objects.all()
    context={
        'data':data,
    }
    return render(request, 'viewseat_schedule.html',context)


def viewstaff_schedule(request):
    staff=request.session['sid']
    data=Staff.objects.get(sid=staff)
    allot=Staffallot.objects.filter(staff=data)
    context={
         'data':allot,
    }
    return render(request, 'viewstaff_schedule.html',context)





def userhome(request):
    user=request.session['id']
    data=User.objects.get(uid=user)
    return render(request, 'userhome.html',{'user':data})



def user_data(request):
    user=request.session['id']
    data=User.objects.get(uid=user)
    context={
        'user':data,
    }
    return render(request, 'userdata.html',context)


def user_update(request,id):
    user=User.objects.get(uid=id)      
    if request.method=='POST':
        user.fname=request.POST['fname'].capitalize()
        user.dob=request.POST['dob']
        user.phone=request.POST['phone']
        user.email=request.POST['email']
        user.save()
        return redirect('userhome')
    return render(request, 'user_update.html',{'user':user})



def bus_search(request):
    
    frm=request.GET['from'].capitalize()
    to=request.GET['to'].capitalize()
    date=request.GET['date']
    data=Seat_Schedule.objects.filter(schedule_date=date,bus_schedule__route__fromlocation=frm,bus_schedule__route__tolocation=to)
    return render(request, 'search.html',{'data':data})

def book_now(request):
    seatid=request.GET['seat_id']
    bus=request.GET['bus']
    data=Ticketrate.objects.get(bustype__btype=bus)
    context={
        'data':data,
    }
    return render(request, 'book_now.html',context)

def booked(request):
    bus_id=request.GET['busid']
    adult=request.GET['ad']
    child=request.GET['ch']
    total=request.GET['tamnt']
    pas=request.GET['pas']
    datas=Seat_Schedule.objects.get(bus_schedule__bus__bid=bus_id)
    udata=User.objects.get(uid=request.GET['uid'])
    context={
        'datas':datas,
        'udata':udata,
        'adult':adult,
        'child':child,
        'total':total,
        'pas':pas,
    }
    return render(request, 'booked.html',context)



def pay(request):
    pas=request.GET['pas']
    seatid=request.GET['seatid']
    tamnt=request.GET['tamnt']
    adult=request.GET['adult']
    child=request.GET['child']

    context={
        'tot':tamnt,
        'pas':pas,
        'seat':seatid,
        'adult':adult,
        'child':child,
    }
    return render(request, 'pay.html',context)
    
def paycomplete(request):
    if request.method=='POST':
        adult=request.POST['adult']
        child=request.POST['child']
        card=request.POST['card']
        expiry=request.POST['expiry']
        cvv=request.POST['cvv']
        seatid=request.POST['seat']
        seat=Seat_Schedule.objects.get(seatid=seatid) 
        tseat=int(seat.available_seat)
        pas=int(request.POST['pas'])
        total=int(request.POST['total'])
        user=User.objects.get(uid=request.session['id'])
        bank=Bank.objects.get(card=card,expiry=expiry,cvv=cvv)
        bln=int(bank.balance)
        if bln>=total or tseat>=pas:
            seat.available_seat=tseat-pas
            seat.save()
            bank.balance=bln-total
            bank.save()
            Ticket.objects.create(uname=user,date=seat,pas=pas,adult=adult,child=child,tot=total)
            context={
                'user':user,
                'seat':seat,
                'pas':pas,
                'adult':adult,
                'child':child,
                'total':total
            }
            return render(request, 'ticket.html',context)
        else:
            return redirect('userhome')
    return HttpResponse('hai')

def booked_history(request):
    uid=request.session['id']
    user=User.objects.get(uid=uid)
    ticket=Ticket.objects.filter(uname=user)
    context={
        'user':user,
        'ticket':ticket,
    }
    return render(request, 'booked_history.html',context)
def privacy(request):
    logid=request.session['logid']
    log=Login.objects.get(logid=logid)
    if request.method=='POST':
        pass2=request.POST['pass2']
        pass3=request.POST['pass3']
        if (log.password==request.POST['pass1']) and (pass2==pass3):
            log.password=pass2
            log.save()      
            return redirect('login')

def log_out(request):
    logout(request)
    return redirect('/')

