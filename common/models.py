from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


    

# Modelo para Categoría
class Category(models.Model):
    name = models.CharField(max_length=100)  # Nombre de la categoría
    description = models.TextField(blank=True)  # Descripción de la categoría (opcional)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_category_user')  # Usuario que creó la categoría

# Modelo para Tablero
class Board(models.Model):
    name = models.CharField(max_length=100)  # Nombre del tablero
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_boards')  # Usuario creador del tablero
    linked_users = models.ManyToManyField(User, related_name='linked_boards' , blank=True)  # Usuarios enlazados al tablero
    description = models.TextField(blank=True)  # Descripción del tablero (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del tablero
    last_updated = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización del tablero
    is_active = models.BooleanField(default=True)  # Indica si el tablero está activo
    categories = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)   # Categorías asociadas al tablero
    slug = models.SlugField(unique=True, blank=True)

@receiver(pre_save, sender=Board)
def crear_slug(sender, instance, **kwargs):
    if not instance.slug:
        # Concatenar el nombre del usuario y el título de la issue
        slug_text = f"{instance.usuario.nombre}-{instance.titulo}"
        # Slugificar el texto combinado
        instance.slug = slugify(slug_text)

# Modelo para Cuenta
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario dueño de la cuenta
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo de la cuenta
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la cuenta
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización de la cuenta
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='invoices', default=1)  # Tablero asociado a la cuenta

# Modelo para Factura
class Bill(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Cuenta asociada a la factura
    description = models.CharField(max_length=255)  # Descripción de la factura
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto de la factura
    due_date = models.DateField()  # Fecha de vencimiento de la factura
    is_paid = models.BooleanField(default=False)  # Indica si la factura está pagada o no
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la factura
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización de la factura

# Modelo para Pago
class Payment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Cuenta asociada al pago
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)  # Factura asociada al pago (opcional)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    date = models.DateField()  # Fecha del pago
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del pago
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización del pago
    

class RecurringPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Usuario que crea el pago recurrente
    description  = models.CharField(max_length=255)
    # Descripción breve del pago recurrente
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Monto del pago recurrente
    start_date = models.DateField()
    # Fecha de inicio del pago recurrente
    end_date = models.DateField(null=True, blank=True)
    # Fecha de finalización del pago recurrente (opcional)
    frequency = models.CharField(max_length=20, choices=[('DAILY', 'Diario'), ('WEEKLY', 'Semanal'), ('MONTHLY', 'Mensual')])
    # Frecuencia del pago recurrente (diario, semanal, mensual, etc.)
    interval = models.IntegerField(default=1)
    # Intervalo para el pago recurrente (por ejemplo, cada cuántos días, semanas o meses se realiza el pago)
    created_in = models.DateTimeField(auto_now_add=True)
    # Fecha y hora de creación del registro de pago recurrente
    updated_on = models.DateTimeField(auto_now=True)
    # Fecha y hora de la última actualización del registro de pago recurrente
    
    
    
### modelos de lista de compras 

class ShoppingList(models.Model):
    # Usuario que crea la lista de compras
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Nombre de la lista de compras
    name = models.CharField(max_length=255)
    # Descripción opcional de la lista de compras
    description  = models.TextField(blank=True)
    # Fecha y hora de creación de la lista de compras
    created_at  = models.DateTimeField(auto_now_add=True)
    # Fecha y hora de la última actualización de la lista de compras
    updated_at  = models.DateTimeField(auto_now=True)

class ListItem(models.Model):
    # Lista de compras a la que pertenece el elemento
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    # Nombre del elemento
    name = models.CharField(max_length=255)
    # Cantidad del elemento
    quantity = models.PositiveIntegerField(default=1)
    # Unidad de medida del elemento (opcional)
    unit_of_measure = models.CharField(max_length=50, blank=True)
    # Indicador de si el elemento ha sido comprado
    purchased = models.BooleanField(default=False)
    # precio del items 
    price =models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    