from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
import random
import string

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser #, Group , Permission
from django.db import models

class AstradUser(AbstractUser):
    
    ROLES_CHOICES = [
        ('Usuario Estándar', 'Usuario Estándar'),
        ('Usuario Premium', 'Usuario Premium'),
    ]

    GENDER_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Viudo/a', 'Viudo/a'),
    ]
    
    OCCUPATION_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Profesional', 'Profesional'),
        ('Empleado', 'Empleado'),
        ('Empresario', 'Empresario'),
        ('Desempleado', 'Desempleado'),
        ('Otro', 'Otro'),
    ]
    
    
    # menbresia 
    
    membership_paid = models.BooleanField(default=False)
    membership_expiry_date = models.DateField(null=True, blank=True)
    
    ## general 
    role = models.CharField(max_length=50, choices=ROLES_CHOICES, default='Usuario Estándar')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    financial_goals = models.TextField(null=True, blank=True)
    
    # Añade related_name a las relaciones groups y user_permissions
    # groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='astraduser_set', related_query_name='user')
    # user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='astraduser_set', related_query_name='user')
    

    def number_of_boards(self):
        return self.board_set.count()



# Modelo para Categoría
class Category(models.Model):
    name = models.CharField(max_length=100)  # Nombre de la categoría
    description = models.TextField(blank=True)  # Descripción de la categoría (opcional)
    user = models.ForeignKey(AstradUser, on_delete=models.CASCADE, related_name='created_category_user',blank=True ,null=True)  # Usuario que creó la categoría

    
    def __str__(self):
        return f"{self.name}"
    
    
    @classmethod
    def initial_data(cls):
        initial_data = [
            {'name': 'Ahorros e Inversiones', 'description': 'Ahorros e inversiones financieras'},
            {'name': 'Alquiler o Hipoteca', 'description': 'Pago de alquiler o hipoteca'},
            {'name': 'Pago de Deuda', 'description': 'Pago de deudas pendientes'},
            {'name': 'Sueldo o Salario', 'description': 'Ingresos por sueldo o salario'},
            {'name': 'Retiro de Monto', 'description': 'Retiro de dinero'},
            {'name': 'Compras', 'description': 'Compras de bienes'},
            {'name': 'Facturas de Servicios', 'description': 'Pago de facturas de servicios'},
            {'name': 'Transporte', 'description': 'Gastos relacionados con transporte'},
            {'name': 'Ocio y Entretenimiento', 'description': 'Gastos relacionados con ocio y entretenimiento'},
            {'name': 'Educación', 'description': 'Gastos relacionados con educación'},
            {'name': 'Salud', 'description': 'Gastos relacionados con salud'},
            {'name': 'Impuestos', 'description': 'Pago de impuestos'},
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
    creator_user = models.ForeignKey(AstradUser, on_delete=models.CASCADE, related_name='created_boards')  # Usuario creador del tablero AUTOMATICO
    linked_users = models.ManyToManyField(AstradUser, related_name='linked_boards' , blank=True)  # Usuarios enlazados al tablero
    description = models.TextField(blank=True)  # Descripción del tablero (opcional)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del tablero AUTOMATICO 
    last_updated = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización del tablero AUTOMATICO
    is_active = models.BooleanField(default=True)  # Indica si el tablero está activo AUTOMATICO AL INICIAR - CAMBIO POR USUARIO 
    slug = models.SlugField(unique=True, blank=True) ## AUTOMATICO 

    def save(self, *args, **kwargs):
        if not self.id:  # Si es un nuevo objeto
            self.created_at = timezone.now()  # Asignamos la fecha y hora actual
            # Generamos un valor aleatorio basado en el usuario y la hora
            random_value = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            # Combinamos el nombre del tablero, el valor aleatorio y el ID del usuario
            combined_string = f"{self.name}-{random_value}-{self.creator_user.id}"
            # Calculamos el slug a partir de la cadena combinada
            self.slug = slugify(combined_string)
        super().save(*args, **kwargs)  # Guardamos el objeto en la base de datos
        
    def __str__(self):
        return self.name



# Modelo para Cuenta
class Account(models.Model):
    user = models.ForeignKey(AstradUser, on_delete=models.CASCADE)  # Usuario dueño de la cuenta
    name = models.CharField(max_length=100)  # Nombre de la cuenta
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo de la cuenta
    currency = models.CharField(max_length=3)  # Moneda de la cuenta (ejemplo: USD, EUR, MXN, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la cuenta
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización de la cuenta
    account_type = models.CharField(max_length=50)  # Tipo de cuenta (ejemplo: Cuenta Corriente, Cuenta de Ahorros, Tarjeta de Crédito, etc.)
    status = models.CharField(max_length=20)  # Estado de la cuenta (ejemplo: Activa, Inactiva, Cerrada, etc.)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, default=1)  # Tablero asociado a la cuenta

    def __str__(self):
        return self.name


class Labels(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# modelo de items tablero 
class Transaction(models.Model):
    TIPO_CHOICES = [('ingreso', 'Ingreso'),
                    ('egreso', 'Egreso')]
    
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
        ('Transferencia Bancaria', 'Transferencia Bancaria'),
        ('PayPal', 'PayPal'),
        ('Criptomoneda', 'Criptomoneda'),
        ('Cheque', 'Cheque'),
        ('Otro', 'Otro')
    ]
    
    typet = models.CharField('Tipo de transaccion', max_length=30, choices=TIPO_CHOICES)  # tipo de transaccion
    Account = models.ForeignKey(Account, on_delete=models.CASCADE, default=1,blank=True, null=True) # tablero donde se genero
    board = models.ForeignKey(Board, on_delete=models.CASCADE, default=1)  # Tablero asociado la trassacion 
    user = models.TextField(blank=True, null=True)
    status = models.IntegerField('Estado', default=1) # estatus 0 programada, 1 realizada, 2 realizada agrupada, 3
    date = models.DateField() # fecha de creacion 
    amount = models.DecimalField(max_digits=10, decimal_places=2) # monto de la transaccion 
    description = models.TextField(blank=True, null=True) ## descriocion del movimiento 
    payment_method = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES) # metodo de pago 
    addressee_sender = models.CharField(max_length=100) # enviado a nombre de la persona , generar modelo basado para crear enlace  
    labels = models.ManyToManyField(Labels, blank=True) ## falta modelo basado en creacion 
    reference = models.CharField(max_length=7, unique=True, editable=False) # numero de identificacion para generar facturas de movimiento 
    
    def save(self, *args, **kwargs):
        # Generar referencia única y aleatoria
        self.reference = ''.join(random.choices(string.digits + string.ascii_letters, k=5))  # Cinco letras aleatorias
        self.reference += ''.join(random.choices(string.digits, k=2))  # Dos números aleatorios
        super().save(*args, **kwargs)



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
    expensedate = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)   # Categorías asociadas al pago 
    taxes = models.CharField(max_length=100)
    paid = models.BooleanField(default=False) 
    paymenttype = models.CharField(max_length=100)


# pago recurrentes , progamados mes a mes o en un tiempo determinado 
class RecurringPayment(models.Model):
    user = models.ForeignKey(AstradUser, on_delete=models.CASCADE)
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
    
    # Nombre de la lista de compras
    name = models.CharField(max_length=255)
    # Descripción opcional de la lista de compras
    description  = models.TextField(blank=True)
    # Fecha y hora de creación de la lista de compras
    created_at  = models.DateTimeField(auto_now_add=True)
    # Fecha y hora de la última actualización de la lista de compras
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# items de esa compra 
class ListItem(models.Model):
    # Relación con la lista de compras
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    # Nombre del producto
    name = models.CharField(max_length=255)
    # Precio del producto con hasta 10 dígitos en total y 2 decimales
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Checkbox para indicar si el producto ha sido comprado
    purchased = models.BooleanField(default=False)
    # Timestamp para la fecha de actualización (se actualiza automáticamente)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

## notificacion del usuario 
class UserNotification(models.Model):
    message = models.TextField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)
    user = models.ForeignKey(AstradUser, on_delete=models.CASCADE)
    type = models.TextField(default=0) # 0-NoClasificado, 1-PagoPrestamo
    class Meta:
        ordering = ['-date']