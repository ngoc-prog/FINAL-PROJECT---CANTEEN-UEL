from django.shortcuts import render,redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    
    id = request.GET.get('id', '')
    product = Product.objects.filter(id=id).first()
    products = Product.objects.filter(id=id)
    feedbacks = Feedback.objects.filter(product=product).order_by('-created_at')
    related_products = []
    if product:
        # Get the categories of this product
        product_categories = product.category.all()
        if product_categories.exists():
            # Get related products that share any of the same categories
            related_products = Product.objects.filter(
                category__in=product_categories
            ).exclude(id=product.id).distinct()[:4]
    
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    
    context = {
        'products': products,
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'related_products': related_products,
        'feedbacks':feedbacks,
        
    }
    
    return render(request, 'app/detail.html', context)
    
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
    context= {'categories':categories,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/category.html',context)

# Create your views here.
def search(request):
    searched = request.GET.get('searched', '').strip()
    keys = []
    
    # Get search results if there's a search term
    if searched:
        keys = Product.objects.filter(name__icontains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    products = Product.objects.all()
    
    context = {
        'active_category': active_category,
        'searched': searched,
        'keys': keys,
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'items': items,
        'order': order
    }
    
    return render(request, 'app/search.html', context)
def register(request):
    form = CreateUserForm()
    context = {'form':form}
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request,'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'User name or password is incorrect')

    context = {}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    is_bestseller = Product.objects.filter(is_bestseller=True)[:8]
    products = Product.objects.all()
    
    context= {'is_bestseller':is_bestseller,'categories':categories,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # Gọi đúng cách
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']  # Sửa lại để lấy giá trị từ dict
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login

    }
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context= {'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/checkout.html',context)
import json
from django.http import JsonResponse

@csrf_exempt  # Dùng tạm để debug nếu bị lỗi CSRF
def updateItem(request): 
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')

    print(f"Received: Product={productId}, Action={action}")  # Debug

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    response_data = {
        'message': 'Item was updated',
        'cart_total': order.get_cart_total,
        'cart_items': order.get_cart_items
    }

    print("Response Data:", response_data)  # Debug

    return JsonResponse(response_data, safe=False)

def profile(request):
    # Logic để lấy thông tin người dùng
    return render(request, 'app/profile.html')


def contact(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context= {'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/contact.html',context )

def clear_cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            order.orderitem_set.all().delete()  # Xóa tất cả các mục trong giỏ hàng
    return redirect('cart')  # Chuyển hướng về trang giỏ hàng

def fullmenu(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login= "show"
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all().order_by('category')

    # Group products by category
    categorized_products = {}
    for category in categories:
        categorized_products[category] = Product.objects.filter(category=category)

    context = {
        'categories': categories,
        'categorized_products': categorized_products,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'order': order,
        'items': items,
        'products':products
    }
    
    return render(request, 'app/fullmenu.html', context)
def get_user_context(request):
    """Helper function to get common user context"""
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        return {
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'user_not_login': "hidden",
            'user_login': "show"
        }
    return {
        'items': [],
        'order': {'get_cart_items': 0, 'get_cart_total': 0},
        'cartItems': 0,
        'user_not_login': "show",
        'user_login': "hidden"
    }
from django.http import HttpResponseRedirect
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        # Get form data with print statements for debugging
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        print(f"Debug - Form Data: product_id={product_id}, rating={rating}, comment={comment}")

        # Individual field validation with specific messages
        if not product_id:
            messages.error(request, 'Không tìm thấy thông tin sản phẩm.')
            return redirect('home')
        if not rating:
            messages.error(request, 'Vui lòng chọn số sao đánh giá.')
            return HttpResponseRedirect(f'/detail/?id={product_id}')
        if not comment:
            messages.error(request, 'Vui lòng nhập nội dung đánh giá.')
            return HttpResponseRedirect(f'/detail/?id={product_id}')

        try:
            product = get_object_or_404(Product, id=product_id)
            print(f"Debug - Found product: {product.name}")
            
            # Create or update feedback
            feedback = Feedback.objects.filter(
                user=request.user,
                product=product
            ).first()

            if feedback:
                # Update existing feedback
                feedback.rating = rating
                feedback.comment = comment
                feedback.save()
                print(f"Debug - Updated existing feedback for product {product.id}")
            else:
                # Create new feedback
                Feedback.objects.create(
                    user=request.user,
                    product=product,
                    rating=rating,
                    comment=comment
                )
                print(f"Debug - Created new feedback for product {product.id}")

            messages.success(request, 'Cảm ơn bạn đã đánh giá sản phẩm!')
            return HttpResponseRedirect(f'/detail/?id={product_id}')

        except Product.DoesNotExist:
            print("Debug - Product not found")
            messages.error(request, 'Không tìm thấy sản phẩm.')
            return redirect('home')
        except Exception as e:
            print(f"Debug - Error occurred: {str(e)}")
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            return redirect('home')

    return redirect('home')