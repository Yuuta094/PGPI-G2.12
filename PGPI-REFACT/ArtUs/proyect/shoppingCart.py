class ShoppingCart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        shoppingCart = self.session.get("shoppingCart")
        if not shoppingCart:
            self.session["shoppingCart"] = {}
            self.shoppingCart = self.session["shoppingCart"]
        else:
            self.shoppingCart = shoppingCart

    def add(self, artwork):
        id = str(artwork.id)
        if id not in self.shoppingCart.keys():
            self.shoppingCart[id]={
                "artwork_id": artwork.id,
                "name": artwork.name,
                "accum_value": float(artwork.price),  # Convertir a float
                "quantity": 1,
            }
        else:
            self.shoppingCart[id]["quantity"] += 1
            self.shoppingCart[id]["accum_value"] += float(artwork.price)  # Convertir a float
        self.save_shoppingCart()

    def save_shoppingCart(self):
        self.session["shoppingCart"] = self.shoppingCart
        self.session.modified = True

    def delete(self, artwork):
        id = str(artwork.id)
        if id in self.shoppingCart:
            del self.shoppingCart[id]
            self.guardar_shoppingCart()

    def substract(self, artwork):
        id = str(artwork.id)
        if id in self.shoppingCart.keys():
            self.shoppingCart[id]["quantity"] -= 1
            self.shoppingCart[id]["accum_value"] -= float(artwork.price)  # Convertir a float
            if self.shoppingCart[id]["quantity"] <= 0: self.delete(artwork)
            self.guardar_shoppingCart()
    def clean(self):
        self.session["shoppingCart"] = {}
        self.session.modified = True