from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

#######################ADMIN ###################################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)


from django.core.files.storage import FileSystemStorage
from datetime import datetime

from .models import service_master
def admin_service_master_add(request):
    if request.method == 'POST':
        fs = FileSystemStorage()

        uploaded_file = request.FILES['document']

        name = request.POST.get('name')
        qty = '0'
        pic = fs.save(uploaded_file.name, uploaded_file)
        price = request.POST.get('price')
        description = request.POST.get('description')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        status = 'new'


        pp = service_master(name=name,qty=qty,pic=pic,price=price,description=description,dt=dt,tm=tm,status=status)
        pp.save()

        context = {'msg':'Service Details added'}
        return render(request, 'myapp/admin_service_master_add.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/admin_service_master_add.html',context)

def admin_service_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)
    pp = service_master.objects.get(id=int(id))
    pp.delete()

    pp_l = service_master.objects.all()
    context ={'service_list':pp_l,'msg':'Service Details deleted'}
    return render(request,'myapp/admin_service_master_view.html',context)


def admin_service_master_view(request):
    pp_l = service_master.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/admin_service_master_view.html', context)

def admin_service_master_search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        sh_l = service_master.objects.filter(name__contains=query)
        context = {'service_list': sh_l}
        return render(request, 'myapp/admin_service_master_view.html', context)
    else:
        return render(request, 'myapp/admin_service_master_search.html')


from .models import service_offers,service_payment
def admin_service_offers_add(request):
    if request.method == 'POST':
        fs = FileSystemStorage()

        uploaded_file = request.FILES['document']

        pic = fs.save(uploaded_file.name, uploaded_file)
        description = request.POST.get('description')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        status = 'new'


        pp = service_offers(pic=pic,description=description,dt=dt,tm=tm,status=status)
        pp.save()

        context = {'msg':'Service Offers added'}
        return render(request, 'myapp/admin_service_offers_add.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/admin_service_offers_add.html',context)

def admin_service_offers_delete(request):
    id = request.GET.get('id')
    print("id="+id)
    pp = service_offers.objects.get(id=int(id))
    pp.delete()

    pp_l = service_offers.objects.all()
    context ={'service_list':pp_l,'msg':'Service Offers deleted'}
    return render(request,'myapp/admin_service_offers_view.html',context)


def admin_service_offers_view(request):
    pp_l = service_offers.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/admin_service_offers_view.html', context)

def admin_service_payment_view(request):
    sd_l = service_master.objects.all()
    suc_l = service_payment.objects.filter()

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'transaction_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/admin_service_payment_view.html', context)

from .models import service_order
def admin_service_orders_view(request):
    sd_l = service_master.objects.all()
    suc_l = service_order.objects.filter()

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'order_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/admin_service_orders_view.html', context)

def admin_service_orders_view2(request):
    c_id = request.GET.get('c_id')
    sd_l = service_master.objects.all()
    suc_l = service_order.objects.filter(service_id=int(c_id))

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'order_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/admin_service_orders_view.html', context)

def admin_staff_details_add(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        ul = user_login(uname=username, passwd=password, u_type='staff')
        ul.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_staff_details_add.html', context)
    else:
        return render(request, './myapp/admin_staff_details_add.html')


def admin_staff_details_delete(request):
    id = request.GET.get('id')
    print('id = '+id)
    ul = user_login.objects.get(id=int(id))
    ul.delete()
    msg = 'Record Deleted'
    ul_l = user_login.objects.filter(u_type='staff')
    context = {'staff_list': ul_l, 'msg':msg}
    return render(request, './myapp/admin_staff_details_view.html',context)

def admin_staff_details_view(request):
    ul_l = user_login.objects.filter(u_type='staff')
    context = {'staff_list': ul_l}
    return render(request, './myapp/admin_staff_details_view.html',context)

##########################################################################################
#######################STAFF ###################################
def staff_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='staff')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/staff_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/staff_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/staff_login.html',context)


def staff_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/staff_home.html')


def staff_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return staff_login(request)
    else:
        return staff_login(request)

def staff_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='staff')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/staff_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/staff_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/staff_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/staff_changepassword.html', context)


from django.core.files.storage import FileSystemStorage
from datetime import datetime

from .models import service_master
def staff_service_master_add(request):
    if request.method == 'POST':
        fs = FileSystemStorage()

        uploaded_file = request.FILES['document']

        name = request.POST.get('name')
        qty = '0'
        pic = fs.save(uploaded_file.name, uploaded_file)
        price = request.POST.get('price')
        description = request.POST.get('description')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        status = 'new'


        pp = service_master(name=name,qty=qty,pic=pic,price=price,description=description,dt=dt,tm=tm,status=status)
        pp.save()

        context = {'msg':'Service Details added'}
        return render(request, 'myapp/staff_service_master_add.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/staff_service_master_add.html',context)

def staff_service_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)
    pp = service_master.objects.get(id=int(id))
    pp.delete()

    pp_l = service_master.objects.all()
    context ={'service_list':pp_l,'msg':'Service Details deleted'}
    return render(request,'myapp/staff_service_master_view.html',context)


def staff_service_master_view(request):
    pp_l = service_master.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/staff_service_master_view.html', context)

def staff_service_master_search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        sh_l = service_master.objects.filter(name__contains=query)
        context = {'service_list': sh_l}
        return render(request, 'myapp/staff_service_master_view.html', context)
    else:
        return render(request, 'myapp/staff_service_master_search.html')


from .models import service_offers,service_payment
def staff_service_offers_add(request):
    if request.method == 'POST':
        fs = FileSystemStorage()

        uploaded_file = request.FILES['document']

        pic = fs.save(uploaded_file.name, uploaded_file)
        description = request.POST.get('description')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        status = 'new'


        pp = service_offers(pic=pic,description=description,dt=dt,tm=tm,status=status)
        pp.save()

        context = {'msg':'Service Offers added'}
        return render(request, 'myapp/staff_service_offers_add.html',context)

    else:

        context = {'msg':''}
        return render(request, 'myapp/staff_service_offers_add.html',context)

def staff_service_offers_delete(request):
    id = request.GET.get('id')
    print("id="+id)
    pp = service_offers.objects.get(id=int(id))
    pp.delete()

    pp_l = service_offers.objects.all()
    context ={'service_list':pp_l,'msg':'Service Offers deleted'}
    return render(request,'myapp/staff_service_offers_view.html',context)


def staff_service_offers_view(request):
    pp_l = service_offers.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/staff_service_offers_view.html', context)

def staff_service_payment_view(request):
    sd_l = service_master.objects.all()
    suc_l = service_payment.objects.filter()

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'transaction_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/staff_service_payment_view.html', context)

from .models import service_order
def staff_service_orders_view(request):
    sd_l = service_master.objects.all()
    suc_l = service_order.objects.filter()

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'order_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/staff_service_orders_view.html', context)

def staff_service_orders_view2(request):
    c_id = request.GET.get('c_id')
    sd_l = service_master.objects.all()
    suc_l = service_order.objects.filter(service_id=int(c_id))

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'order_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/staff_service_orders_view.html', context)




############################ USER ################################################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        gender = request.POST.get('gender')
        age = request.POST.get('age')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        #status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, age=age,addr=addr, pin=pin, contact=contact, email=email )
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)


def user_service_master_view(request):
    pp_l = service_master.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/user_service_master_view.html', context)

def user_service_master_search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        sh_l = service_master.objects.filter(name__contains=query)
        context = {'service_list': sh_l}
        return render(request, 'myapp/user_service_master_view.html', context)
    else:
        return render(request, 'myapp/user_service_master_search.html')

def user_service_offers_view(request):
    pp_l = service_offers.objects.all()
    context = {'service_list': pp_l, 'msg': ''}
    return render(request, 'myapp/user_service_offers_view.html', context)

from .models import service_payment,service_order

def user_service_payment_add(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        cake_id = int(request.POST.get('cake_id'))
        amt = request.POST.get('amt')
        card_no = request.POST.get('card_no')
        cvv = request.POST.get('cvv')
        remarks = request.POST.get('remarks')
        bdt = request.POST.get('bdt')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'

        suc = service_payment(amt=amt,service_id=cake_id,user_id=int(user_id),
                                   card_no=card_no,cvv=cvv,dt=dt,tm=tm,status=status)
        suc.save()
        brh = service_order(cake_id=cake_id,user_id=int(user_id),dt=dt,tm=tm,bdt=bdt,
                                  remarks=remarks,status=status)
        brh.save()
        context = {'msg': 'Item Booked'}
        return render(request, './myapp/user_home.html', context)
    else:
        service_id = int(request.GET.get('service_id'))
        l_l = service_master.objects.get(id=service_id)
        context = { 'service_id': service_id, 'msg': '','amt':l_l.price}
        return render(request, './myapp/user_service_payment_add.html', context)

def user_service_payment_view(request):
    user_id = request.session['user_id']
    sd_l = service_master.objects.all()
    suc_l = service_payment.objects.filter(user_id=int(user_id))

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'transaction_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/user_service_payment_view.html', context)

def user_service_orders_view(request):
    user_id = request.session['user_id']
    sd_l = service_master.objects.all()
    suc_l = service_order.objects.filter(user_id=int(user_id))

    ud_l = user_details.objects.all()
    context = {'service_list': sd_l, 'order_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/user_service_orders_view.html', context)

