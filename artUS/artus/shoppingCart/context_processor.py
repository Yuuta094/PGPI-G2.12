def total_bill(request):
    total = 0
    if request.user.is_authenticated:
        if "shoppingCart" in request.session.keys():
            for key, value in request.session["shoppingCart"].items():
                total += int(value["accum_value"])
    return {"total_bill": total}