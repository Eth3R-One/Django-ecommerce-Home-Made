from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
from django.utils.text import slugify
from io import BytesIO
from PIL import Image
import uuid
from user.models import Userprofile


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        allow_unicode=True,
        max_length=50,
        editable=True,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = self.title.replace(" ", "-").replace(",", "")
            self.slug = slugify(self.title, allow_unicode=True)
        # return super(Category, self).save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey(
        User, related_name="products", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        allow_unicode=True,
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        editable=True,
    )
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="uploads/product_images", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="uploads/product_images/thumbnail", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return "https://placehold.co/600x400"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            # self.slug = self.title.replace(" ", "-").replace(",", "")
            self.slug = slugify(self.title, allow_unicode=True)
        # return super(Product, self).save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(917, 1000)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)
        name = image.name.replace("uploads/product_images/", "")
        thumbnail = File(thumb_io, name=name)

        return thumbnail


class Order(models.Model):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    ON_THE_WAY = "On the way"
    DELIVERED = "Delivered"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
        (ON_THE_WAY, "On the way"),
        (DELIVERED, "Delivered"),
    )
    CASH = "cash"
    CARD = "card"
    Online = "Online"
    PAYMENT_CHOICES = (
        (CASH, "Cash"),
        (CARD, "Card"),
        (Online, "Online"),
    )
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    user = models.ForeignKey(
        User, related_name="order", on_delete=models.SET_NULL, null=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True, default=0)
    is_paid = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_CHOICES, default=CASH
    )

    def __str__(self) -> str:
        return f"{self.uid}-{self.first_name} {self.last_name} {self.status}"

    def get_total_quantity(self):
        orders = OrderItem.objects.filter(order=self)
        # sum = 0
        # for item in orders:
        #     sum += item.quantity
        # return sum
        return sum(int(item.quantity) for item in orders)

        # return sum(int(item.quantity) for item in self.items.all())

    def get_total_price(self):
        order = OrderItem.objects.filter(order=self)
        return sum(int(item.quantity * item.product.price) for item in order)
        # return sum(int(item.quantity * item.product.price) for item in self.items.all())

    def get_order_count(self):
        return OrderItem.objects.filter(order=self).count()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            str(self.id)
            + " "
            + self.product.title
            + " "
            + self.order.first_name
            + " "
            + self.order.last_name
            + " "
            + self.order.status
        )

    def get_total_price(self):
        return self.quantity * self.product.price
