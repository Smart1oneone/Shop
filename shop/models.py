import string
import random

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def rand_slug():
    """
        Generate a random slug consisting of 3 characters from lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
class Category(models.Model):
    """
    Class representing a Category model with fields for name, parent category, slug, and creation date.
    Defines Meta options for uniqueness constraints and verbose names.
    """
    name = models.CharField(max_length=250, db_index=True, verbose_name='Категория')
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name='Родительcкий класс'
    )
    slug = models.SlugField(max_length=250, null=False, unique=True, editable=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = (['parent', 'slug'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return  '>'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the Category instance.

        If the slug field is not set, generate a slug using a random 3-character string and the category name.
        The generated slug is created by combining the random string, '-pickBetter', and the category name.
        Finally, call the parent class's save method to save the Category instance.

        """
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', kwargs={'slug': self.slug})

class Product(models.Model):
    """
    Class representing a Product model with fields for category, title, brand, description, slug, image, availability, creation date, and last update date.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название', max_length=250)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField(max_length=250, verbose_name='URL')
    image = models.ImageField(upload_to='products/products/%Y/%m/%d', verbose_name='Изображение')
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2, default=99.99)

    class Meta:
        verbose_name='Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_details', kwargs={'slug': self.slug})

class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Custom manager for the Product model that filters the queryset to only include available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)
class ProductProxy(Product):
    """
    Proxy model for the Product model that allows customization of querysets and model methods without changing the original Product model.
    """

    objects = ProductManager()

    class Meta:
        proxy = True



