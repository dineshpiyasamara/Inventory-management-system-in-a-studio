from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import *
from system.forms import *
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def home(request):
    if request.method == 'POST':
        if "login" in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            new_login = authenticate(
                request, username=username, password=password)
            if new_login is None:
                msg = "Login failed. Please use right credentials."
                messages.error(request, msg)
            else:
                login(request, new_login)
                msg = "Welcome {}".format(request.user)
                messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif "logout" in request.POST:
            msg = f"{request.user} logged out..."
            logout(request)
            messages.success(request, msg)

    return render(request, 'home.html')


@login_required(login_url='home')
def inventory(request):
    if request.method == 'POST':
        if 'change_selling_price' in request.POST:
            product_code = request.POST.get('product_code')
            new_price = request.POST.get('price')

            item_obj = Item.objects.get(product_code=product_code)
            selling_price_obj = SellingPrice(
                item=item_obj, selling_price=new_price)
            try:
                selling_price_obj.save()
                msg = "Successfully updated."
                messages.success(request, msg)
            except ValidationError:
                msg = "Input value not valid."
                messages.error(request, msg)
            except:
                msg = "Something went wrong."
                messages.error(request, msg)
            return HttpResponseRedirect(request.path)

        elif "logout" in request.POST:
            msg = f"{request.user} logged out..."
            logout(request)
            messages.success(request, msg)
            return redirect('home')

    item_table = Item.objects.all()
    selling_price_table = SellingPrice.objects.all()

    datalist = []
    for item in item_table:
        data = []
        data.append(item.product_code)
        data.append(item.category)
        data.append(item.color)

        if item.description == None:
            data.append("")
        elif(len(item.description) > 15):
            data.append(item.description[:12]+"...")
        else:
            data.append(item.description)

        data.append(item.purchase_price)

        price = ''
        for sell in selling_price_table:
            if item.product_code == sell.item.product_code:
                price = sell.selling_price
        data.append(price)

        purchases_tot = Purchases.objects.filter(
            product_code=item.product_code).aggregate(Sum('qty'))
        sales_tot = Sales.objects.filter(
            product_code=item.product_code).aggregate(Sum('qty'))

        if purchases_tot['qty__sum'] == None:
            purchases_tot['qty__sum'] = 0
        if sales_tot['qty__sum'] == None:
            sales_tot['qty__sum'] = 0

        data.append(purchases_tot['qty__sum'] - sales_tot['qty__sum'])

        datalist.append(data)

    return render(request, 'inventory.html', {
        'item_table': datalist,
    })


@login_required(login_url='home')
def sell(request):
    if request.method == "POST":
        if 'sell-items' in request.POST:
            name = request.POST.get('name')
            addr = request.POST.get('address')
            phone = request.POST.get('phone_number')
            prod = request.POST.get('item-data')
            qty = request.POST.get('qty')

            purchases_tot = Purchases.objects.filter(
                product_code=prod).aggregate(Sum('qty'))
            sales_tot = Sales.objects.filter(
                product_code=prod).aggregate(Sum('qty'))

            if purchases_tot['qty__sum'] == None:
                purchases_tot['qty__sum'] = 0
            if sales_tot['qty__sum'] == None:
                sales_tot['qty__sum'] = 0

            if ((int(purchases_tot['qty__sum']) - int(sales_tot['qty__sum'])) >= int(qty)):
                customer_obj = Customers(
                    name=name, address=addr, phone_number=phone)
                customer_obj.save()

                items = Item.objects.all()
                for item in items:
                    if item.product_code == prod:
                        sales_obj = Sales(qty=qty, customer_id=customer_obj,
                                          product_code=item, employee_id=request.user)
                        sales_obj.save()
                        messages.success(
                            request, "Sell data successfully added...")
            else:
                messages.error(request, "Not enough items...")

            return HttpResponseRedirect(request.path)

        elif "logout" in request.POST:
            msg = f"{request.user} logged out..."
            logout(request)
            messages.success(request, msg)
            return redirect('home')

    item_list = Item.objects.all().order_by('product_code')

    return render(request, 'sell.html', {
        'item_list': item_list
    })


@login_required(login_url='home')
def json_item_data_others(request, *args, **kwargs):
    selectedProduct = kwargs.get('product')

    obj_data = list(Item.objects.filter(
        product_code=selectedProduct).values()) or None

    if selectedProduct != None:

        obj_price = SellingPrice.objects.raw(
            "SELECT id,selling_price FROM system_sellingprice Where item_id='"+selectedProduct+"' ORDER BY id DESC LIMIT 1")

        return JsonResponse({
            'data': obj_data,
            'price': obj_price[0].selling_price,
        })


@login_required(login_url='home')
def purchase(request):
    if request.method == 'POST':
        if 'purchase-items' in request.POST:
            prod = request.POST.get('product_code', "error")
            cat = request.POST.get('category')
            col = request.POST.get('color')
            des = request.POST.get('description')
            purch = request.POST.get('purchase_price')
            sell = request.POST.get('selling_price')
            qty = request.POST.get('qty')
            org = request.POST.get('organization')
            address = request.POST.get('address')
            phone = request.POST.get('phone_number')

            print(prod)

            item_obj = Item(product_code=prod, category=cat,
                            color=col, description=des, purchase_price=purch)
            item_obj.save()

            items = Item.objects.all()
            for item in items:
                if item.product_code == prod:
                    sell_obj = SellingPrice(item=item, selling_price=sell)
                    sell_obj.save()

            supplier_obj = Suppliers(
                organization=org, address=address, phone_number=phone)
            supplier_obj.save()

            purchase_obj = Purchases(
                qty=qty, product_code=item_obj, supplier_id=supplier_obj, employee_id=request.user)
            purchase_obj.save()

            messages.success(request, "Purchase Successful.")
            return HttpResponseRedirect(request.path)

        elif "logout" in request.POST:
            msg = f"{request.user} logged out..."
            logout(request)
            messages.success(request, msg)
            return redirect('home')

    item_list = Item.objects.all().order_by('product_code')

    return render(request, 'purchase.html', {
        "item_list": item_list,
    })


@login_required(login_url='home')
def employees(request):
    if request.method == 'POST':
        if 'edit_user' in request.POST:
            userdata = User.objects.get(id=request.user.id)
            accountdata = Account.objects.get(user=request.user.id)

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address = request.POST.get("address")
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")
            gender = request.POST.get("gender")

            userdata.first_name = first_name
            userdata.last_name = last_name
            userdata.email = email
            userdata.save()

            accountdata.phone_number = phone_number
            accountdata.address = address
            accountdata.gender = gender
            accountdata.save()

            messages.success(request, "Your bios save successful")
            return HttpResponseRedirect(request.path)

        elif 'register_user' in request.POST:
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()

                emp_obj = Account(user=User.objects.all().last())
                emp_obj.save()
                messages.success(request, "User successfully registered")

            else:
                name = form.cleaned_data.get('username')
                users = User.objects.filter(username=str(name)).count()

                if users != 0 or name == None:
                    messages.error(request, "User Already exist")
                else:
                    messages.error(request, "Password invalid or mismatch")
            return HttpResponseRedirect(request.path)

        elif 'remove_user' in request.POST:

            username = request.POST.get('label-to-remove-user')

            user_obj = User.objects.get(username=username)
            user_obj.is_active = False
            user_obj.save()

            messages.success(request, 'User removed successful')
            return HttpResponseRedirect(request.path)

        elif 'change_password' in request.POST:
            old_password = request.POST.get("old_password")
            new_password1 = request.POST.get("new_password1")
            user = authenticate(username=request.user, password=old_password)
            if user:
                user.set_password(new_password1)
                user.save()
                new_login = authenticate(username=user, password=new_password1)
                login(request, new_login)
                messages.success(request, "Password updated...")
            else:
                messages.error(request, "Incorrect old password.")
            return HttpResponseRedirect(request.path)

        elif "logout" in request.POST:
            msg = f"{request.user} logged out..."
            logout(request)
            messages.success(request, msg)
            return redirect('home')

    me = dict()
    my_detail1 = User.objects.all().filter(username=request.user)
    for detail1 in my_detail1:
        me['username'] = detail1.username
        me['first_name'] = detail1.first_name
        me['last_name'] = detail1.last_name
        me['email'] = detail1.email
        my_detail2 = Account.objects.all().filter(user=detail1)

        for detail2 in my_detail2:
            me['address'] = detail2.address
            me['phone_number'] = detail2.phone_number
            me['gender'] = detail2.gender

    employee_table = User.objects.all()
    account_table = Account.objects.all()

    datalist = []
    for employee in employee_table:
        if employee.is_superuser == False and employee.is_active == True:
            data = []
            data.append(employee.username)
            data.append('{} {}'.format(
                employee.first_name, employee.last_name))
            data.append(employee.email)

            address = ''
            phone_number = ''
            gender = ''

            for account in account_table:
                if employee.username == account.user.username:
                    address = account.address
                    phone_number = account.phone_number
                    gender = account.gender

            if address == None:
                data.append("")
            elif(len(address) > 15):
                data.append(address[:12]+"...")
            else:
                data.append(address)

            data.append(phone_number)
            data.append(gender)

            datalist.append(data)

    newdatalist = []
    for y in datalist:
        data = [x if x != None else "" for x in y]
        newdatalist.append(data)

    form = NewUserForm()

    return render(request, 'employees.html', {
        'me': me,
        'employee_table': newdatalist,
        'control': request.user.is_staff,
        'form': form,
    })
