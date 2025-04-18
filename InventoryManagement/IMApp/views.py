from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Product  , Warehouse, WarehouseAddress
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.core.paginator import Paginator

def index(request):
    return render(request, 'dashboard.html',)

def explain_view(request):
    return render(request, 'explain.html')

@login_required 
def main_view(request):
    user = request.user
    if user.is_superuser:
        products = Product.objects.all()
        total_products = products.count()
    else:
        products = Product.objects.filter(user=user)
    total_products =products.count()
    total_categories = products.values('category').distinct().count()
    total_price= sum(product.price*product.quantity  for product in products)
    low_stock_products=products.filter(quantity__lt=5)
    out_of_stock_products=products.filter(quantity=0)
    return render(request, 'main.html', context={'total_products': total_products, 'total_categories': total_categories, 'total_price': total_price, 'low_stock_products': low_stock_products, 'out_of_stock_products': out_of_stock_products, 'products': products})

  
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        mobile = request.POST.get("mobile")
        terms_accepted = request.POST.get("terms") 

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

       
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

  
        if not terms_accepted:
            messages.error(request, "You must accept the Terms & Conditions!")
            return redirect("register")

        user = User.objects.create_user(
            username=name, 
            email=email,
            mobile=mobile,
            password=password 
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "register.html")

def user_login(request):
    if 'next' in request.GET:
        messages.info(request, "Please login to access this page.")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        selected_role = request.POST.get('role')

        try:
            user = User.objects.get(email=email)  
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

        if user.check_password(password):
      
            if (selected_role == 'admin' and user.is_superuser) or (selected_role == 'user' and not user.is_superuser):
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("main")  
            else:
                messages.error(request, "Role mismatch. Please select the correct role.")
                return redirect("login")
        else:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

@login_required  
def add_product_view(request):
    warehouse = WarehouseAddress.objects.all() 
  
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        warehouse_id = request.POST.get('warehouse')

      
        if not name or not price or not quantity or not category:
            messages.error(request, 'All fields are required.')
        elif int(price) <= 0:
            messages.error(request, 'Price must be greater than zero.')
        elif int(quantity)<0:
            messages.error(request, 'Quantity must not be negative')
        elif Product.objects.filter(name=name, user=request.user).exists():
            messages.warning(request, 'A product with this name already exists.')
        else:
            warehouse_instance = WarehouseAddress.objects.get(id=warehouse_id) 
            Product.objects.create(
                name=name,
                price=int(price),
                quantity=int(quantity),
                category=category,
                warehouse=warehouse_instance,
                user=request.user  
            )
            messages.success(request, 'Product added successfully!')
            return redirect('product')  
        

    

    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)
    
    paginator = Paginator(products, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product.html', {'products': products, 'warehouse': warehouse, 'page_obj': page_obj})



@login_required
def update_product_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    warehouse = WarehouseAddress.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        warehouse = request.POST.get('warehouse')

        if not name or not price or not quantity or not category:
            messages.error(request, 'All fields are required.')
        elif int(price) <= 0:
            messages.error(request, 'Price must be greater than zero.')
        elif int(quantity) < 0:
            messages.error(request, 'Quantity cannot be negative.')
        elif Product.objects.filter(name=name, user=request.user).exclude(product_id=product_id).exists():
            messages.error(request, 'A product with this name already exists.')

        else:
           
            product.name = name
            product.price = int(price)
            product.quantity = int(quantity)
            product.category = category
            product.warehouse = WarehouseAddress.objects.get(id=warehouse)
            product.save()  
            messages.success(request, 'Product updated successfully!')
            return redirect('product') 

    return render(request, 'update_product.html', {'product': product, 'warehouse': warehouse})



@login_required
def delete_product_view(request, product_id):
    products=Product.objects.get(product_id=product_id)
    products.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        profile_pic = request.FILES.get('profile_pic')

        user.username = name
        user.email = email
        user.mobile = mobile

        if profile_pic:
            user.profile_pic = profile_pic

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

@login_required
def transfer_product_view(request):
    if request.method == 'POST':
        from_warehouse_id = request.POST.get('from_warehouse')
        to_warehouse_id = request.POST.get('to_warehouse')
        quantity_to_transfer = request.POST.get('quantity_to_transfer')
        product_id = request.POST.get('product_id')

        # Check for missing inputs FIRST before using them
        if not from_warehouse_id or not to_warehouse_id or not quantity_to_transfer or not product_id:
            messages.error(request, 'All fields are required.')
            return redirect('transferproduct')
        
        if from_warehouse_id == to_warehouse_id:
            messages.error(request, "Cannot transfer product to the same warehouse.")
            return redirect('transferproduct')


        try:
            product = Product.objects.get(product_id=product_id)
            from_warehouse = WarehouseAddress.objects.get(id=from_warehouse_id)
            to_warehouse = WarehouseAddress.objects.get(id=to_warehouse_id)
        except (Product.DoesNotExist, WarehouseAddress.DoesNotExist):
            messages.error(request, 'Invalid product or warehouse selected.')
            return redirect('transferproduct')

        if int(quantity_to_transfer) > product.quantity:
            messages.error(request, 'Insufficient stock for transfer.')
            return redirect('transferproduct')

       
        Warehouse.objects.create(
            product_id=product,
            from_warehouse=from_warehouse,
            to_warehouse=to_warehouse,
            quantity_to_transfer=quantity_to_transfer,
            transfer_date=timezone.now(),
            user=request.user,  
            status='Pending'

        )

        messages.success(request, 'Product transferred successfully!')
        return redirect('transferproduct')
    
   
    
    products = Product.objects.filter(user=request.user)
    warehouse = WarehouseAddress.objects.all()
    if request.user.is_superuser:
        transfers = Warehouse.objects.select_related('product_id').order_by('-transfer_date')
    else:
        transfers = Warehouse.objects.filter(user=request.user).select_related('product_id').order_by('-transfer_date')
    return render(request, 'transfer.html', {'products': products, 'transfers': transfers, 'warehouse': warehouse})

    

@login_required  
def warehouse_view(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        id=request.POST.get('id')
        if not request.user.is_superuser:
            messages.error(request, 'Access Denied: Only admins can manage warehouses.')
            return render(request, 'warehouse.html', {'addresses': []})

        if not address:
            messages.error(request, 'Address is required.')
            return redirect('warehouse')
        if address:
            if WarehouseAddress.objects.filter(address=address).exists():
                messages.error(request, 'This address already exists.')
                return redirect('warehouse')

        WarehouseAddress.objects.create(address=address)
        messages.success(request, 'Warehouse address added successfully!')
        return redirect('warehouse')  

    addresses = WarehouseAddress.objects.all()
    return render(request, 'warehouse.html', {'addresses': addresses})


@staff_member_required  
def approve_transfers_view(request):
    pending_transfers = Warehouse.objects.filter(status='Pending').select_related('product_id', 'from_warehouse', 'to_warehouse')

    if request.method == 'POST':
        transfer_id = request.POST.get('transfer_id')
        action = request.POST.get('action')

        transfer = get_object_or_404(Warehouse, pk=transfer_id)

        if action == 'approve':
            if transfer.product_id.quantity >= transfer.quantity_to_transfer:
                transfer.product_id.quantity -= transfer.quantity_to_transfer
                transfer.product_id.save()
                transfer.status = 'Approved'
                transfer.save()
                messages.success(request, f"Transfer #{transfer.Warehouse_id} approved!")
            else:
                messages.error(request, f"Insufficient stock for transfer #{transfer.Warehouse_id}.")
        elif action == 'reject':
            transfer.status = 'Rejected'
            transfer.save()
            messages.warning(request, f"Transfer #{transfer.Warehouse_id} rejected.")

        return redirect('approvetransfers')

    return render(request, 'approve_transfers.html', {'transfers': pending_transfers})


@login_required
def warehouse_product_view(request):
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')

    all_warehouses = WarehouseAddress.objects.all()
    all_products = Product.objects.all()
    product_lookup = {p.product_id: p for p in all_products}

   
    warehouse_product_qty = defaultdict(lambda: defaultdict(int))

    
    for product in all_products:
        warehouse_product_qty[product.warehouse.id][product.product_id] += product.quantity

    
    approved_transfers = Warehouse.objects.filter(status='Approved')
    for transfer in approved_transfers:
        to_id = transfer.to_warehouse.id
        pid = transfer.product_id.product_id
        warehouse_product_qty[to_id][pid] += transfer.quantity_to_transfer

    
    for warehouse in all_warehouses:
        _ = warehouse_product_qty[warehouse.id]  

    warehouse_products = {}
    for warehouse in all_warehouses:
        products = []
        for pid, qty in warehouse_product_qty[warehouse.id].items():
            if qty > 0 and pid in product_lookup:
                product_copy = product_lookup[pid]
                product_display = Product(
                    name=product_copy.name,
                    price=product_copy.price,
                    quantity=qty,  
                    category=product_copy.category
                )
                product_display.product_id = pid
                products.append(product_display)

       
        warehouse_products[warehouse] = products

    return render(request, 'warehouse_products.html', {
        'warehouse_products': warehouse_products
    })

@login_required
@staff_member_required
def user_list_view(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@staff_member_required
def make_staff_view(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.is_staff:
        user.is_staff = True
        user.save()
        messages.success(request, f"{user.username} promoted to Staff.")
    else:
        messages.info(request, f"{user.username} is already a Staff.")
    return redirect('user_list')

@login_required
@staff_member_required
def delete_user(request, user_id):
    user_to_delete = User.objects.get(id=user_id)
    if user_to_delete.is_superuser:
        messages.error(request, "You can't delete another admin.")
    else:
        user_to_delete.delete()
        messages.success(request, f"{user_to_delete.username} has been deleted.")
    return redirect('user_list')

@login_required
def user_warehouse_product_view(request):
    user = request.user
    all_warehouses = WarehouseAddress.objects.all()
    user_products = Product.objects.filter(user=user)
    product_lookup = {p.product_id: p for p in user_products}

    warehouse_product_qty = defaultdict(lambda: defaultdict(int))

  
    for product in user_products:
        warehouse_product_qty[product.warehouse.id][product.product_id] += product.quantity

    
    approved_transfers = Warehouse.objects.filter(status='Approved', user=user)
    for transfer in approved_transfers:
        to_id = transfer.to_warehouse.id
        pid = transfer.product_id.product_id
        warehouse_product_qty[to_id][pid] += transfer.quantity_to_transfer

    for warehouse in all_warehouses:
        _ = warehouse_product_qty[warehouse.id]

    
    warehouse_products = {}
    for warehouse in all_warehouses:
        products = []
        for pid, qty in warehouse_product_qty[warehouse.id].items():
            if qty > 0 and pid in product_lookup:
                product_copy = product_lookup[pid]
                product_display = Product(
                    name=product_copy.name,
                    price=product_copy.price,
                    quantity=qty,
                    category=product_copy.category
                )
                product_display.product_id = pid
                products.append(product_display)

        # Include warehouse even if empty
        warehouse_products[warehouse] = products

    return render(request, 'user_warehouse_products.html', {
        'warehouse_products': warehouse_products
    })

def about_us_view(request):
    return render(request, 'aboutus.html')
