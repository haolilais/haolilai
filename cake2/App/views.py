
import random
from datetime import datetime
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.alipay import ali
from App.forms import RegisterForm
from App.models import *
from cake.settings import SECRET_KEY
from tools.mytoken import Token
from tools.verifycode import VerifyCode


def index(request):

    # bigcategorys = Category.objects.filter(parentid=0)
    # smallcategorys = Category.objects.filter(parentid__gt=0)


    return render(request,'app/index.html',locals())

def all(request):#全部

    # products = Category.objects.get(pk=cid).products_set.filter(isdel=0)
    # product = Category.objects.get(pk=cid).products_set.filter(pk=cid)

    products = Products.objects.filter(isdel=0).filter(cid=1)

    # product = Products.objects.get()

    return render(request, 'app/1.html',locals())

def cake(request):#蛋糕
    return render(request, 'app/cake.html')

def classics(request):#经典
    products = Products.objects.filter(cid=5).filter(isdel=0)
    return render(request, 'app/classcis.html',locals())

def children(request):#儿童
    products = Products.objects.filter(cid=6).filter(isdel=0)
    return render(request, 'app/children.html',locals())

def zunai(request):#尊爱
    products = Products.objects.filter(cid=7).filter(isdel=0)
    return  render(request, 'app/zunai.html',locals())

def snacks(request):#零食
    products = Products.objects.filter(cid=3).filter(isdel=0)
    return  render(request, 'app/snacks.html',locals())

def we(request):#关于我们
    return  render(request, 'app/we.html')


@login_required(login_url='/login/')
def detailed(request,pid):
    product = Products.objects.get(pk=pid)
    c = request.GET.get('c')
    # if request.method == 'GET':
    #     c=request.GET.get('c')
    #     print(c)

    # if c =='1':
    if request.method=='POST':
        # product.iscart = 1
        # # post.delete()
        # product.save()

        user = request.user
        # users = User.objects.get(pk=user.uid)
        carts = Cart.objects.filter(isdel=0).filter(uid=user).filter(name=product.title).first()
        print(carts,'+++++++++++++++')
        if carts:
            print('存在+++++++++++++')
            carts.num += int(request.POST.get('number'))
            carts.total_price = int(request.POST.get('number')) * carts.unit_price
            carts.save()
        else:
            cart = Cart()
            # print(carts)
            # print(carts.only('name'))


            cart.name = product.title
            cart.unit_price = product.price
            cart.num = request.POST.get('number')
            print('------------------',request.POST.get('number'))
            cart.total_price = product.price * int(request.POST.get('number'))
            cart.arrt = request.POST.get('size')
            cart.pid = product
            cart.uid = user
            print(request.POST.get('size'))
            cart.save()

            print('333333333333')
        return redirect(reverse('app:detailed',args=[pid]))

    return render(request,'app/detailed.html',locals())



@login_required(login_url='/login/')
def cart(request):
    # products = Products.objects.filter(isdel=0).filter(iscart=1)

    user = request.user
    carts = Cart.objects.filter(uid=user).filter(isdel=0)
    # print('zouzouzou')
    print(carts,'++++++++')

    #总价
    nums = 0
    for i in carts:
        print(i.total_price)
        nums+=i.total_price
    print(nums)


    #删除
    d = request.GET.get('d')
    print(d,'++++++++++++++++++')
    if d :
        # print('---------->',d)
        pro = Cart.objects.get(pid=int(d))
        pro.isdel =1
        pro.save()
        return redirect(reverse('app:cart'))

    return render(request,'app/cart.html',locals())


#结算生成订单页
def jiesuan(request):
    user = request.user
    carts = Cart.objects.filter(uid=user).filter(isdel=0)
    # print(carts)

    # 总价
    nums = 0
    # 订单产品总积分
    pscores = 0
    for i in carts:
        print("++++++++======")
        print(carts)
        print(i.pid)
        nums += i.total_price
        pscores += i.pid.pscore
    print(pscores)
    # carts = Cart.objects.filter(uid=user).filter(isdel=0)

    # 生成订单
    if request.method == 'POST':
        print("+++++++++++++++++++++++")

        for cart in carts:
            order = Order()
            order.name = cart.name
            # order.ordernumber = str(time.strftime("%b%d%Y%H%M%S",datetime.now()))+ str(random.randint(0,100))
            # order.ordernumber = datetime.now().strftime("%Y%m%d%H%M%S")
            order.ordernumber = str(2019) + str(random.randint(0, 100))
            # print(datetime.now().strftime("%Y%m%d%H%M%S"))
            order.money = cart.total_price
            order.total_price = cart.total_price
            order.create_time = datetime.now()
            print(datetime.date)
            order.paytype = request.POST.get('payment')
            print('-----------------', order.paytype)
            order.num = cart.num
            order.mark = request.POST.get('note')
            order.uid = user
            order.save()
            cart.delete()
        return redirect(reverse("app:order"))
    return render(request,'app/jiesuan.html',locals())




#注册
def register(request):
    if request.method == 'POST':
        # 用POST数据实例化表单，表单对象会验证POST数据
        form = RegisterForm(request.POST)

        # 验证码验证
        yzm1 = request.POST.get('yzm')
        yzm2 = request.session.get('code')
        # 判定验证码是否匹配
        res = (yzm1 == yzm2)
        # 如果验证码不匹配
        if not res:
            form.errors['yzm'] = "验证码不匹配"

        if res and form.is_valid():  # 验证通过
            form.cleaned_data.pop('repassword')
            form.cleaned_data.pop('yzm')
            # form.cleaned_data.pop('phonenumber')
            User.objects.create_user(**form.cleaned_data)

            # 基础写法
            # user = User()
            # print(form.cleaned_data)
            # user.username = form.cleaned_data.get('username')
            # user.password = form.cleaned_data.get('password')
            # user.email = form.cleaned_data.get('email')
            # user.save()
            return redirect(reverse('app:index'))
        return render(request, 'app/register.html', {'form': form }, locals())
    else:
        form = RegisterForm()
        return render(request, 'app/register.html', locals())


def get_yzm(request):
    vc = VerifyCode()
    res = vc.output()
    # 将验证码保存到session
    request.session['code'] = vc.code
    return HttpResponse(res, 'image/png')


def user_login(request):
    if request.method == 'POST':
        if request.POST.get('loginsubmit'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            autologin = request.POST.get('cookietime')
            # print(username)
            # print(password)

            #验证成功返回用户对象，否则返回None
            user = authenticate(request,username=username,password=password)
            # print(user.is_authenticated)
            if user:
                #登陆，写入session,并把user写入request
                #自动登陆处理
                # if autologin:
                #     user.autologin = 1
                user.save()
                login(request,user)
                # request.session.set_expiry(0)
                print('-----------------------------------------')

                return redirect(reverse('app:index'))
            else:
                return redirect(reverse('app:login'))
    return render(request,'app/login.html')

def user_logout(request):
    logout(request)
    # return render(request,'app/index.html')
    return redirect(reverse('app:index'))

#
# def home(request):
#     return render(request,'app/home.html')




def add(request):
    for i in range(35,40):
        pro = Products()
        pro.title = '尊爱'+ str(i)
        # pro.cid = 5
        pro.price = 10*i
        pro.save()
    return HttpResponse('ok')






# 我的账户
def user(request):
    # users=User.objects.all()
    # orders=Order.objects.all()
    # if request.method=='POST':
    #     pass
    return render(request, 'app/user.html',locals())




# 订单列表
def order(request):
    user = request.user
    # carts = Cart.objects.filter(uid=user).filter(isdel=0)
    #
    # print('-------==========-------')
    # # 生成订单
    # # if request.method == 'POST':
    # order = Order()
    # for cart in carts:
    #     order.name = cart.name
    #     # order.ordernumber = str(time.strftime("%b%d%Y%H%M%S",datetime.now()))+ str(random.randint(0,100))
    #     # order.ordernumber = datetime.now().strftime("%Y%m%d%H%M%S")
    #     order.ordernumber = str(2019) + str(random.randint(0,100))
    #     # print(datetime.now().strftime("%Y%m%d%H%M%S"))
    #     order.money = cart.total_price
    #     order.create_time = datetime.now()
    #     print(datetime.date)
    #     order.paytype = request.POST.get('payment')
    #     print('-----------------', order.paytype)
    #     order.num = cart.num
    #     order.mark = request.POST.get('note')
    #     order.uid = user
    #     order.save()


    orders = Order.objects.all()
    if request.method == 'POST':
        if request.POST.get("chaxun") == "查询":
            key = request.POST.get("orderkey")
        if request.POST.get('del') == '删除':
            oid = request.POST.get('oid')
            order1 = Order.objects.get(pk=oid)
            order1.delete()
            return redirect(reverse("app:order"))
        if request.POST.get("pay") == "去支付":
            oid = request.POST.get("oid")
            order = Order.objects.get(pk=oid)
            alipay = ali()
            # 生成支付的url
            query_params = alipay.direct_pay(
                subject=order.name,  # 商品简单描述
                out_trade_no=order.ordernumber,  # 商户订单号
                total_amount=order.total_price,  # 交易金额(单位: 元 保留俩位小数)
            )
            # 支付宝网关,带上订单参数才有意义
            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
            # POST请求重定向到支付宝提供的网关，跳转到支付宝支付界面
            return redirect(pay_url)
    return render(request, 'app/order.html',locals())


def paysucceed(request):
    alipay = ali()

    if request.method == "POST":

        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)

        if status:
            oid = request.POST.get("oid")
            order = Order.objects.get(pk=oid)
            order.status = 1
            order.save()
        return HttpResponse('POST返回')

    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        if status:
            # 获取订单状态，显示给用户
            ordernum = request.GET.get("out_trade_no")
            order = Order.objects.get(ordernumber=ordernum)
            order.status = 1
            order.save()
            return redirect(reverse("app:index"))



# 我的收藏夹
def favorite(request):
    shous=Collections.objects.all()
    # pid = int('pid')

    if request.method=='POST':
        coid = request.POST.get('coid')
        shou1 = Collections.objects.get(pk=coid)
        if request.POST.get("del"):
            shou1.delete()
            return redirect(reverse('app:favorite'))
        if request.POST.get("tianjia"):
            name = shou1.name
            unit_prict = shou1.price
            cart = Cart()
            cart.name = name
            cart.unit_prict = unit_prict
            cart.total_price = unit_prict
            cart.num = 1
            uid = request.user.pk
            user = User.objects.get(pk=uid)
            cart.uid = user
            cart.save()
            return redirect(reverse('app:favorite'))
    return render(request, 'app/favorite.html',locals())

# 我的亲友团
def friend(request):
    return render(request, 'app/friend.html')

# 我的收货地址簿
def address(request):
    uid = request.user.pk
    user = User.objects.get(pk=uid)
    addresses = user.addressdetail_set.all()
    if request.method == "POST":
        if request.POST.get("add"):
            province = request.POST.get("province")
            city = request.POST.get("city")
            district = request.POST.get("district")
            address = request.POST.get("address")
            phone = request.POST.get("phone")
            addressdetail = Addressdetail()
            addressdetail.receivename = province + city + district + address
            addressdetail.content = address
            addressdetail.uid = user
            addressdetail.phone = phone
            addressdetail.save()
            return redirect(reverse("app:address"))
        if request.POST.get("del"):
            rid = request.POST.get("rid")
            address = Addressdetail.objects.get(pk=rid)
            address.delete()
            return redirect(reverse("app:address"))
        if request.POST.get("default"):
            isdefaultadd = Addressdetail.objects.get(isdefault=1)
            isdefaultadd.isdefault = 0
            isdefaultadd.save()
            rid = request.POST.get("rid")
            address = Addressdetail.objects.get(pk=rid)
            address.isdefault = 1
            address.save()


    return render(request, 'app/address.html', locals())

# 我的积分
def integral(request):
    return render(request, 'app/integral.html')

# 我的优惠劵
def bonus(request):
    return render(request, 'app/bonus.html')

# 留言板
def message(request):
    return render(request, 'app/message.html')

# 更换手机号
def changem(request):
    return render(request, 'app/changem.html')

# 修改密码
def editpwd(request):
    # 用户id
    uid = Token(SECRET_KEY).confirm_validate_token(request.GET.get('token'))
    # print(res)
    # password = request.GET.get('password')
    # print('uid:',res,"password:",password)
    return render(request, 'app/editpwd.html',locals())




# 编辑用户信息
def profile(request):
    if request.method == 'POST':
        user = request.user
        # print(user)
        users = User.objects.get(pk=user.uid)
        users.gender = request.POST.get('sex')
        users.userdetail_set.update(signature=request.POST.get('nickname'))
        users.userdetail_set.update(birthday=request.POST.get('birthday'))
        users.save()
    return render(request, 'app/profile.html')

