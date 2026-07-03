from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Product, CartItem, Category
from .forms import ProductForm

def product_list(request):
    # Lógica para manejar la subida de un nuevo producto
    if request.method == 'POST' and request.user.is_staff: # Solo el staff puede subir productos
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Al guardar, django-storages sube la imagen a Azure automáticamente
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    products = Product.objects.all().select_related('category')
    return render(request, 'product_list.html', {
        'products': products,
        'form': form,
    })
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # Vuelve a la página en la que estabas en lugar de ir al carrito
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def cart_detail(request):
    # Usamos select_related('product') para traer los productos relacionados
    # en una sola consulta SQL, evitando N+1 queries.
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.total_price() for item in items)
    return render(request, 'cart_detail.html', {'items': items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def delete_product(request, product_id):
    # Solo los administradores pueden eliminar productos
    if not request.user.is_staff:
        return redirect('product_list')
        
    product = get_object_or_404(Product, id=product_id)
    product.delete() # Gracias a django-storages, esto también elimina el blob de Azure.
    return redirect('product_list')
