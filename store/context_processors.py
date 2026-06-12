from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        return {'cart_item_count': count}
    return {'cart_item_count': 0}