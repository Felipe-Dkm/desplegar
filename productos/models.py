from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Producto(models.Model):
    CATEGORIAS = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    foto = models.ImageField(upload_to='productos/')
    fecha_creacion = models.DateField(auto_now_add=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='Hombre')  # 👈 Campo de categoría

    def __str__(self):  # 👈 Corrige el método __str__
        return self.nombre
    
    
    
class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    def subtotal(self):
        return self.producto.precio * self.cantidad

    
   
#pasarela decompras



class Orden(models.Model):
    
    METODOS_PAGO = [
        ('nequi', 'Nequi'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO
    )
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def subtotal(self):
        return self.precio * self.cantidad

class Datos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    otro_campo = models.CharField(max_length=100)



class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} - {self.fecha_compra.strftime('%d/%m/%Y')}"


from .models import Historial

def confirmar(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        print("Contenido del carrito:", carrito)  # <-- Verifica si el carrito tiene productos
        
        for item_id, item_data in carrito.items():
            producto = Producto.objects.get(id=item_id)
            Historial.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=item_data['cantidad'],
                precio_total=producto.precio * item_data['cantidad']
            )
        
        # Limpia el carrito después de guardar la compra
        request.session['carrito'] = {}
        return redirect('historial')


