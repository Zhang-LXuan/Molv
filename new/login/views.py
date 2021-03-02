from django.shortcuts import render
from django.shortcuts import redirect
from . import models
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
# Create your views here.

def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', {'message': message})

            if user.password == password:
                user = models.User.objects.get(name=username)

                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name 
                request.session['user_tel'] = user.tel
                request.session['user_wx'] = user.wx
                request.session['user_zfb'] = user.zfb
                request.session['user_addr1'] = user.addr1
                request.session['user_addr2'] = user.addr2
                return redirect('/login/index/')
                
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', {'message': message})
        else:
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')

def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        tel = request.POST.get('tel')
        wx = request.POST.get('wx')
        zfb = request.POST.get('zfb')
        addr1 = request.POST.get('addr1')
        addr2 = request.POST.get('addr2')
        if password != password2:
            message = "两次密码不一致！"
            return render(request, 'login/register.html',{'message' : message})
        else:
            try:
                same_name_user = models.User.objects.get(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', {'message' : message})
                same_tel_user = models.User.objects.get(tel=tel)
                if same_tel_user:
                    message = '该联系方式已经被注册了！'
                    return render(request, 'login/register.html', {'message' : message})
            except:
                new_user = models.User()
                new_user.name = username
                new_user.password = password
                new_user.tel = tel
                new_user.wx = wx
                new_user.zfb = zfb
                new_user.addr1 = addr1
                new_user.addr2 = addr2
                new_user.save()
                print("注册成功")
                message= "注册成功"
                return redirect('/login/login',{'message' : message})
    else:
        return render(request, 'login/register.html')


################################################################
def buy(request,item_id1):
    try:
        print("商品名称",item_id1)
        username = request.session.get('user_name',None)
        item = models.Itemsss.objects.get(item_id=item_id1)
        value = item.item_value
        try:
            ##########已经存在数据
            car = models.shopcars.objects.get(user_name=username,item_id=item_id1)
            car.item_counter = car.item_counter + 1
            car.item_value = item.item_value
            car.item_money = float(car.item_value) * float(car.item_counter)
            car.save()

            print("更新成功")
            monns = models.shopcars.objects.filter(user_name = username)
            print(9)
            summ = 0.0
            for monn in monns:
                summ = summ + float(monn.item_money)
            print(summ)
            return render(request,'login/shop.html',{"summoney":summ})
        except:
            ###########数据不存在
            print("无购买")
            car1 = models.shopcars.objects.all() 
            car2 = car1.aggregate(Max('car_no'))
            no1 = car2['car_no__max']
            shcar = models.shopcars()
            shcar.item_id = item_id1
            print("item_id = " , shcar.item_id)
            shcar.user_name = username
            print("user_name = " , shcar.user_name)
            shcar.item_counter = 1
            print("item_counter = " , shcar.item_counter)
            shcar.item_value = item.item_value
            print("item_value = " , shcar.item_value)
            shcar.item_money = float(shcar.item_value) * float(shcar.item_counter)
            print("item_money = " , shcar.item_money)
            shcar.car_no = no1 + 1
            print("car_no = " , shcar.car_no)
            
            try:
                shcar.save()
                print("添加成功")
                monns = models.shopcars.objects.filter(user_name = username)
                print(10)
                summ = 0.0
                for monn in monns:
                    summ = summ + float(monn.item_money)
                print(summ)
                return render(request,'login/shop.html',{"summoney":summ})
            except:
                print("添加失败")
                monns = models.shopcars.objects.filter(user_name = username)
                print(11)
                summ = 0.0
                for monn in monns:
                    summ = summ + float(monn.item_money)
                print(summ)
                return render(request,'login/shop.html',{"summoney":summ})

    except:
        return render(request,'login/shop.html')
###############################################################


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/login')
    request.session.flush()

    return redirect("/login/login/")



def shop(request):
    try:
        username = request.session.get('user_name',None)
        monns = models.shopcars.objects.filter(user_name = username)
        print(10)
        summ = 0.0
        for monn in monns:
            summ = summ + float(monn.item_money)
        print(summ)
        return render(request,'login/shop.html',{"summoney":summ})
    except:
        summ = 0.0
        return render(request,'login/shop.html',{"summoney":summ})

def item(request,item_idd):
    try:
        print(item_idd)
        request.session['item_id'] = item_idd


        item = models.Itemsss.objects.get(item_id = item_idd)
        item_src = item.item_src
        item_value = item.item_value
        item_description = item.item_description
        item_name = item.item_name
        return render(request, "login/item.html",{'src':item_src,'value':item_value,'description':item_description,'name':item_name})
    except:
        return render(request,"login/shop.html")

@csrf_exempt
def watch(request):
    #########################苹果
    item = models.itrecord.objects.get(item_name = "苹果")
    d1 = item.item_r1
    d2 = item.item_r2
    d3 = item.item_r3
    d4 = item.item_r4
    d5 = item.item_r5
    d6 = item.item_r6
    d7 = item.item_r7
    d8 = item.item_r8
    d9 = item.item_r9
    d10 = item.item_r10
    list1 = []
    list1.append(d1)
    list1.append(d2)
    list1.append(d3)
    list1.append(d4)
    list1.append(d5)
    list1.append(d6)
    list1.append(d7)
    list1.append(d8)
    list1.append(d9)
    list1.append(d10)
    data1 = {
        "title": "苹果最近销售价格",
        "legend": "价格",
        "x": ["1","2","3","4","5","6","7","8","9","10"],
        "series": list1
    }
    ###############################黄桃
    item = models.itrecord.objects.get(item_name = "黄桃")
    d1 = item.item_r1
    d2 = item.item_r2
    d3 = item.item_r3
    d4 = item.item_r4
    d5 = item.item_r5
    d6 = item.item_r6
    d7 = item.item_r7
    d8 = item.item_r8
    d9 = item.item_r9
    d10 = item.item_r10
    list2 = []
    list2.append(d1)
    list2.append(d2)
    list2.append(d3)
    list2.append(d4)
    list2.append(d5)
    list2.append(d6)
    list2.append(d7)
    list2.append(d8)
    list2.append(d9)
    list2.append(d10)
    data2 = {
        "title": "黄桃最近销售价格",
        "legend": "价格",
        "x": ["1","2","3","4","5","6","7","8","9","10"],
        "series": list1
    }

    infos = models.itrecord.objects.all()
    list3 =[]
    for info in infos:
        data = {
            'value' : info.item_r10,
            'name' : info.item_name
        }
        list3.append(data)
    print(list3)
    return render(request, 'login/watch.html',{'title1':"苹果","legend1": "价格","x1": ["1","2","3","4","5","6","7","8","9","10"],"series1": list1,'title2':"黄桃","legend2": "价格","x2": ["1","2","3","4","5","6","7","8","9","10"],"series2": list2,'list3':list3})

@csrf_exempt
def getcar(request):
    try:
        if request.method == "POST":
            username = request.session.get('user_name',None)
            cardatas = models.shopcars.objects.filter(user_name = username)
            data_info = []
            for cardata in cardatas:
                name = models.Itemsss.objects.get(item_id = cardata.item_id)
                data = {
                    'item_id': int(cardata.item_id),
                    'item_counter': cardata.item_counter,
                    'item_value':cardata.item_value,
                    'item_money':cardata.item_money,
                    'item_name':name.item_name
                }
                data_info.append(data)
            #print(data_info)
            #return render(json.dumps(data_info),content_type="application/json")
            return HttpResponse(json.dumps(data_info))
        else:
            print("请求错误！")
    except Exception as e:
        print("ERROR")
        return HttpResponse(e.args)

def reducar(request,item_id2):
    username = request.session.get('user_name')
    red = models.shopcars.objects.get(user_name = username , item_id = item_id2)
    if int(red.item_counter) == 1:
        red.delete()
    else:
        red.item_counter = int(red.item_counter) - 1
        red.item_money = float(red.item_counter) * float(red.item_value)
        red.save()
    try:
        monns = models.shopcars.objects.filter(user_name = username)
        summ = 0.0
        for monn in monns:
            summ = summ + float(monn.item_money)
        print(summ)
        return render(request,'login/shop.html',{"summoney":summ}) 
    except:
        summ = 0.0
        return render(request,'login/shop.html',{"summoney":summ}) 

def submit(request):
    try:
        username = request.session.get('user_name')
        a = models.shopcars.objects.get(user_name = username)
        monns = models.shopcars.objects.filter(user_name = username)
        summ = 0.0
        for monn in monns:
            summ = summ + float(monn.item_money)
        print(summ)
        message = "提交成功!"
        return render(request,'login/shop.html',{"summoney":summ,"message":message}) 
    except:
        message = "购物车为空，不可提交！"
        summ = 0.0
        return render(request,'login/shop.html',{"summoney":summ,"message":message}) 

#def up_info(request):
    #pass