from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
import random
import string

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(('El email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    
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
    

    # membresía 
    membership_paid = models.BooleanField(default=False)
    membership_expiry_date = models.DateField(null=True, blank=True)
    
    # user

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # general 
    role = models.CharField(max_length=50, choices=ROLES_CHOICES, default='Usuario Estándar')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    cdunico = models.CharField(max_length=7, unique=True, editable=False, blank=True)
    
    # Añade related_name a las relaciones groups y user_permissions
    username = None
    groups = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if not self.cdunico:
            self.cdunico = self.generate_unique_cdunico()
        super().save(*args, **kwargs)

    def generate_unique_cdunico(self):
        while True:
            cdunico = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            if User.objects.filter(cdunico=cdunico).count() == 0:
                return cdunico
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'astrad_user'


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
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'category'





    
# Modelo para Cuenta
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario dueño de la cuenta
    name = models.CharField(max_length=100)  # Nombre de la cuenta
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo de la cuenta
    currency = models.CharField(max_length=3)  # Moneda de la cuenta (ejemplo: USD, EUR, MXN, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la cuenta
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización de la cuenta
    account_type = models.CharField(max_length=50)  # Tipo de cuenta (ejemplo: Cuenta Corriente, Cuenta de Ahorros, Tarjeta de Crédito, etc.)
    status = models.CharField(max_length=20)  # Estado de la cuenta (ejemplo: Activa, Inactiva, Cerrada, etc.)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = 'account'
    
## modelo de patrimonio 

class Patrimony(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Nombre de la cuenta
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo de la cuenta
    currency = models.CharField(max_length=3)  # Moneda de la cuenta (ejemplo: USD, EUR, MXN, etc.)
    patrimony_type = models.CharField(max_length=50)  # Tipo de cuenta (ejemplo: Cuenta Corriente, Cuenta de Ahorros, Tarjeta de Crédito, etc.)
    updated_at = models.DateTimeField(auto_now=True)
    type_dos = models.IntegerField() # activo - 1  o pasivo - 2  
    status = models.CharField(max_length=20)
    # board = models.ForeignKey(Board, on_delete=models.CASCADE )
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Patrimony"
        verbose_name_plural = "Patrimonies"
        db_table = 'patrimony'



class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario asociado a la tarjeta
    name = models.CharField(max_length=100)  # Nombre o identificador de la tarjeta
    balance = models.DecimalField(max_digits=12, decimal_places=2)  # Saldo actual disponible en la tarjeta
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)  # Límite de crédito de la tarjeta
    cut_off_date = models.DateField()  # Fecha de corte del estado de cuenta
    handling_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cuota de manejo inicial en cero
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de intereses de la tarjeta
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización
    status = models.CharField(max_length=20)  # Estado actual de la tarjeta

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"
        db_table = 'credit_card'

class Labels(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"
        db_table = 'labels'


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
    patrimony = models.ForeignKey(Patrimony, on_delete=models.CASCADE, default=1,blank=True, null=True) # tablero donde se genero
    # board = models.ForeignKey(Board, on_delete=models.CASCADE, default=1)  # Tablero asociado la trassacion 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField('Estado', default=1) # estatus 0 programada, 1 realizada, 2 realizada agrupada, 3
    date = models.DateField() # fecha de creacion 
    amount = models.DecimalField(max_digits=10, decimal_places=2) # monto de la transaccion 
    description = models.TextField(blank=True, null=True) ## descriocion del movimiento 
    payment_method = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES) # metodo de pago 
    addressee_sender = models.CharField(max_length=100) # enviado a nombre de la persona , generar modelo basado para crear enlace  
    category = models.ForeignKey(Category, blank=True,on_delete=models.CASCADE) ## falta modelo basado en creacion 
    reference = models.CharField(max_length=7, unique=True, editable=False) # numero de identificacion para generar facturas de movimiento 
    
    def save(self, *args, **kwargs):
        # Generar referencia única y aleatoria
        self.reference = ''.join(random.choices(string.digits + string.ascii_letters, k=5))  # Cinco letras aleatorias
        self.reference += ''.join(random.choices(string.digits, k=2))  # Dos números aleatorios
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = 'transaction'



# Modelo para Factura
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Cuenta asociada a la factura
    description = models.CharField(max_length=255)  # Descripción de la factura
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto de la factura
    due_date = models.DateField()  # Fecha de vencimiento de la factura
    is_paid = models.BooleanField(default=False)  # Indica si la factura está pagada o no
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la factura
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización de la factura

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        db_table = 'bill'
# Modelo para Pago
class Payment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Cuenta asociada al pago
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)  # Factura asociada al pago (opcional)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    date = models.DateField()  # Fecha del pago
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación del pago
    updated_at = models.DateTimeField(auto_now=True)  # Última fecha y hora de actualización del pago
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = 'payment'


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField()
    closet = models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Service")
        verbose_name_plural = ("Services")
        db_table = 'services'

    def __str__(self):
        return self.name

class Roomie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name

class Guest(models.Model):
    name = models.CharField(max_length=100)
    roomie = models.ForeignKey(Roomie, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    arrival_date = models.DateField()  # Fecha de llegada del invitado
    departure_date = models.DateField()  # Fecha de salida del invitado
    class Meta:
        verbose_name = ("Guest")
        verbose_name_plural = ("Guests")
        db_table = 'guests'

    def days_presence(self):
        return (self.arrival_date - self.departure_date).days + 1
    
    def __str__(self):
        return self.name
    
class Calculation(models.Model):
    roomie = models.ForeignKey(Roomie, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    value =  models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = ("Calculation")
        verbose_name_plural = ("Calculations")
        db_table = 'calculation'






"""  
modelo de pagos basico para generar los pagos que se dieron en el mes y generar un resumen 


"""

class Spent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(null=False, blank=False)
    expensedate = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)   # Categorías asociadas al pago 
    taxes = models.CharField(max_length=100)
    paid = models.BooleanField(default=False) 
    paymenttype = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Spent"
        verbose_name_plural = "Spents"
        db_table = 'spent'


# pago recurrentes , progamados mes a mes o en un tiempo determinado 
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
    
    class Meta:
        verbose_name = "RecurringPayment"
        verbose_name_plural = "RecurringPayments"
        db_table = 'recurringPayment'
    
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
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ShoppingList"
        verbose_name_plural = "ShoppingLists"
        db_table = 'shoppingList'
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
    class Meta:
        verbose_name = "ListItem"
        verbose_name_plural = "ListItems"
        db_table = 'listitem'

## notificacion del usuario 
class UserNotification(models.Model):
    message = models.TextField()
    date = models.DateTimeField()
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField(default=0) # 0-NoClasificado, 1-PagoPrestamo
    class Meta:
        ordering = ['-date']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        db_table = 'notification'
        


""" 
Modelos de Presupuestos 
"""


class Budget(models.Model):
    # Tablero asociado en el presupuesto 
    # board = models.ForeignKey(Board, on_delete=models.CASCADE, default=1)
    # Usuario dueño de la cuenta
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    # Nombre del presupuesto
    name = models.CharField(max_length=200, help_text="Nombre del presupuesto")
    # Descripción opcional del presupuesto
    description = models.TextField(blank=True, null=True, help_text="Descripción del presupuesto")
    # Monto total del presupuesto
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total del presupuesto",default=0.0)
    # Fecha y hora en que se actualizó el presupuesto por última vez
    updated_at = models.DateTimeField(auto_now=True)
    # estado del presupouesto 
    state = models.BooleanField(default=True, help_text="Indica si esta activo o no ")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        db_table = 'budget'

class BudgetCategory(models.Model):
    # Nombre de la categoría
    name = models.CharField(max_length=200, help_text="Nombre de la categoría")
    # Descripción opcional del presupuesto
    description = models.TextField(blank=True, null=True, help_text="Descripción del presupuesto")

    
    def __str__(self):
        return self.name
    
    @classmethod
    def initial_data(cls):
        initial_data = [
            {"name": "Vivienda", "description": "Gastos relacionados con alquiler o hipoteca y servicios básicos del hogar."},
            {"name": "Transporte", "description": "Gastos relacionados con el transporte diario."},
            {"name": "Alimentos", "description": "Gastos relacionados con la compra de alimentos y comestibles."},
            {"name": "Servicios Públicos", "description": "Gastos relacionados con servicios públicos como electricidad, agua, y gas."},
            {"name": "Seguros", "description": "Pagos de seguros como salud, automóvil, o vivienda."},
            {"name": "Cuidado de la Salud", "description": "Gastos relacionados con la salud, como medicamentos y visitas médicas."},
            {"name": "Entretenimiento", "description": "Gastos destinados a entretenimiento y actividades recreativas."},
            {"name": "Ahorros", "description": "Fondos destinados al ahorro para metas específicas o emergencias."},
            {"name": "Deudas", "description": "Pagos mensuales de préstamos o tarjetas de crédito."},
            {"name": "Misceláneos", "description": "Otros gastos no categorizados en las categorías anteriores."},
        ]
        
        for category in initial_data:
            BudgetCategory.objects.create(name=category["name"], description=category["description"])
    
    class Meta:
        verbose_name = "BudgetCategory"
        verbose_name_plural = "BudgetCategorys"
        db_table = 'budgetCategory'

class BudgetItem(models.Model):
    # Categoría a la que pertenece el ítem
    category = models.ForeignKey(BudgetCategory, related_name='items', on_delete=models.CASCADE)
    # Nombre del ítem
    name = models.CharField(max_length=200, help_text="Nombre del ítem")
    # Descripción opcional del ítem
    description = models.TextField(blank=True, null=True, help_text="Descripción del ítem")
    # Monto del ítem
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto del ítem")
    # Indica si el ítem ha sido pagado
    is_paid = models.BooleanField(default=False, help_text="Indica si el ítem ha sido pagado")

    budget =  models.ForeignKey(Budget, related_name='budget', on_delete=models.CASCADE)
    

    
    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name = "Budget Item"
            verbose_name_plural = "Budget Items"
            db_table = 'budget_item'


## carga de datos basicos 

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'common':
        Category.initial_data()
        BudgetCategory.initial_data()

