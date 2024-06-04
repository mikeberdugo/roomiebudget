from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone


# Modelo para Categoría
class Category(models.Model):
    name = models.CharField(max_length=100)  # Nombre de la categoría
    description = models.TextField(blank=True)  # Descripción de la categoría (opcional)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_category_user',blank=True ,null=True)  # Usuario que creó la categoría

    
    def __str__(self):
        return f"{self.name}"
    
    
    @classmethod
    def initial_data(cls):
        initial_data = [
            {'name': 'Comida', 'description': 'Categoría para gastos relacionados con alimentos'},
            {'name': 'Transporte', 'description': 'Categoría para gastos relacionados con transporte'},
            {'name': 'Entretenimiento', 'description': 'Categoría para gastos relacionados con entretenimiento'},
            {'name': 'Facturas', 'description': 'Categoría para gastos relacionados con facturas'},
            {'name': 'Otros', 'description': 'Categoría para otros gastos'},
        ]
        
        for data in initial_data:
            # Verificar si la categoría ya existe
            category, created = cls.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
            # Si es creada, asignarla al usuario "None" para que sea visible para todos los usuarios
            if created:
                category.user = None
                category.save()
                

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'common':
        Category.initial_data()




# Modelo para Tablero
class Board(models.Model):
    name = models.CharField(max_length=100)  # Nombre del tablero
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_boards')  # Usuario creador del tablero AUTOMATICO
    linked_users = models.ManyToManyField(User, related_name='linked_boards' , blank=True)  # Usuarios enlazados al tablero
    description = models.TextField(blank=True)  # Descripción del tablero (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del tablero AUTOMATICO 
    last_updated = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización del tablero AUTOMATICO
    is_active = models.BooleanField(default=True)  # Indica si el tablero está activo AUTOMATICO AL INICIAR - CAMBIO POR USUARIO 
    slug = models.SlugField(unique=True, blank=True) ## AUTOMATICO 

    def save(self, *args, **kwargs):
        if not self.id:  # Si es un nuevo objeto
            self.created_at = timezone.now()  # Asignamos la fecha y hora actual
            self.slug = slugify(self.name)  # Generamos un slug basado en el nombre del tablero
        super().save(*args, **kwargs)  # Guardamos el objeto en la base de datos



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
    


"""  
modelo de pagos basico para generar los pagos que se dieron en el mes y generar un resumen 


"""

class Spent(models.Model):
    name = models.TextField(null=False, blank=False)
    expensedate = models.DateField(auto_now=True , auto_now_add = True)
    category = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)   # Categorías asociadas al pago 
    taxes = models.CharField(max_length=100)
    paid = models.BooleanField(default=False) 
    paymenttype = models.CharField(max_length=100)

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
    


class UserNotification(models.Model):
    message = models.TextField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField(default=0) # 0-NoClasificado, 1-PagoPrestamo
    class Meta:
        ordering = ['-date']