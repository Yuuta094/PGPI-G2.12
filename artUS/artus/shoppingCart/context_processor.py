def total_bill(request):
    total = 0
    if request.user.is_authenticated:
        if "shopping_cart" in request.session.keys():
            for key, value in request.session["shopping_cart"].items():
                total += int(value["accum_value"])
    return {"total_bill": total}

def cart_count(request):
    count = 0
    if "shopping_cart" in request.session.keys():
        for key, value in request.session["shopping_cart"].items():
            count += int(value['quantity'])
    return {"cart_count": count}