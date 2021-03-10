from django.db import models

class Regular_Pizza(models.Model):
    name = models.CharField(max_length=64)
    topp_num = models.IntegerField(default=0)
    small = models.DecimalField(max_digits = 5, decimal_places = 2)
    large = models.DecimalField(max_digits = 5, decimal_places = 2)  

    def __str__(self):
        return f"{self.name}: small ${self.small}, large ${self.large}"

class Sicilian_Pizza(models.Model):
    name = models.CharField(max_length=64)
    topp_num = models.IntegerField(default=0)
    small = models.DecimalField(max_digits = 5, decimal_places = 2)
    large = models.DecimalField(max_digits = 5, decimal_places = 2) 

    def __str__(self):
        return f"{self.name}: small ${self.small}, large ${self.large}"

class Topping(models.Model):
    topping_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping_name}"

class Subs_Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True, null=True)
    large = models.DecimalField(max_digits = 5, decimal_places = 2) 
    one_size = models.BooleanField(default=False)
    toppings = models.ManyToManyField(Subs_Extra, blank=True)

    def __str__(self):
        if self.small == 0.00:
            return f"{self.name}: large ${self.large}"
        if self.large == 0.00:
            return f"{self.name}: small ${self.small}"
        return f"{self.name}: small ${self.small}, large ${self.large}"

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__(self):
        return f"{self.name} ${self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__(self):
        return f"{self.name} ${self.price}"


class Dinner_Platter(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits = 5, decimal_places = 2)
    large = models.DecimalField(max_digits = 5, decimal_places = 2) 

    def __str__(self):
        return f"{self.name}: small ${self.small}, large ${self.large}"

class Cart(models.Model):
    buyer_name = models.CharField(max_length=64) 
    name = models.CharField(max_length=64) 
    type_p = models.CharField(max_length=64) 
    size = models.CharField(max_length=64, default="") 
    toppings = models.CharField(max_length=64, default="") 
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.name}: {self.type_p} {self.size} {self.toppings}, Price: ${self.price}"

class All_Order(models.Model):
    buyer_name = models.CharField(max_length=64) 
    name = models.CharField(max_length=64) 
    type_p = models.CharField(max_length=64) 
    size = models.CharField(max_length=64, default="") 
    toppings = models.CharField(max_length=64, default="") 
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    total = models.DecimalField(max_digits = 6, decimal_places = 2, default="")
    time = models.DateTimeField()
    status = models.CharField(max_length=16, default="Pending")

    def __str__(self):
        return f"{self.buyer_name} {self.name}: {self.type_p} {self.size} {self.toppings}, Price: ${self.price}, Time: {self.time}"
