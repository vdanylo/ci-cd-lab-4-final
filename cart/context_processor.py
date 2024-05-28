from cart.service import CartService


#це нада, шоб на base сторінці відображати к-сть товарів з корзини
def cart_size(request):
    current_user = request.user

    if current_user.is_authenticated:
        cart_size = len(CartService.get_or_create_cart(current_user).items.all())
    else:
        cart_size = 0
    return {'cart_size': cart_size}