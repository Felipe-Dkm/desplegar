from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # type: ignore
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from .models import Producto
from .models import CarritoItem
from .models import Datos
from django.core.mail import send_mail


# Create your views here.
def index(request):
    if request.user.is_authenticated:
            return redirect ('home')
    return render(request, 'index.html')



def perfil(request):
    return render(request, 'perfil.html')

def contactenos(request):
    return render(request, 'contactenos.html')


def editar_perfil(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil después de editar
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'editar_perfil.html', {'form': form})



def logout_request(request):
    logout(request)
    return redirect('index') 

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/tienda.html', {'productos': productos})

def base(request):
    return render(request, 'base.html')

def manual(request):
    return render(request, 'manual.html')

def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def mapanoti(request):
    return render(request, "mapanoti.html")

def galeria(request):
    productos = Producto.objects.all()
    return render(request, 'galeria.html', {'productos': productos})

def editar_perfil(request, uidb64, token):
    return render(request, 'editar_perfil.html', {'uidb64': uidb64, 'token': token})
def confirmar(request):
    return render(request, "confirmar.html")

def resetear(request):
    return render(request, "restablecer.html")
def historial(request):
    compras = Historial.objects.filter(usuario=request.user)
    return render(request, 'productos/historial.html', {'compras': compras})






# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Por favor, ingresa ambos campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirige a la página principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

# Vista de registro
def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)  # Iniciar sesión automáticamente
            messages.success(request, "¡Registro exitoso!.")
            return redirect('login')  # Redirige a la página de login

    return render(request, 'registro.html')


#vista de restablecer
def resetear(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/editar_perfil/{uid}/{token}/")
            send_mail(
                "Restablecimiento de contraseña",
                f"Haz clic en el siguiente enlace para cambiar tu contraseña: {enlace}",
                "tu_correo@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un enlace de restablecimiento a su correo.")
            return redirect("login")
        else:
            messages.error(request, "No se encontró un usuario con ese correo electrónico.")
            return redirect("resetear")  # Redirige de nuevo a la página de reseteo
    
    return render(request, "resetear.html")

#vista de editar_perfil (cambiar contraseña)
def editar_perfil(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contraseña = request.POST["password"]
            user.set_password(nueva_contraseña)
            user.save()
            return redirect("confirmar")

        return render(request, "editar_perfil.html")  # Página para cambiar contraseña

    return redirect("login")  # Si el enlace es inválido, redirige al login

#vista para que funcione editar perfil
def perfil(request):
    usuario = request.user
    uidb64 = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)

    return render(request, "perfil.html", {"usuario_uid": uidb64, "usuario_token": token})

# Vista de cierre de sesión (logout)
def logout_view(request):
    auth_logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de login



#carrito


from .models import Producto, CarritoItem
def productos(request):
    categoria = request.GET.get('categoria', 'todos')  # Capturar categoría
    talla = request.GET.get('talla', None)  # Capturar talla (si se envía)
    color = request.GET.get('color', None)  # Capturar color (si se envía)

    producto_lista = Producto.objects.all()

    # Filtrar por categoría si es diferente de 'todos'
    if categoria and categoria != 'todos':
        if categoria.lower() == 'hombre':
            producto_lista = producto_lista.filter(categoria='Hombre')
        elif categoria.lower() == 'mujer':
            producto_lista = producto_lista.filter(categoria='Mujer')

    # Filtrar por talla si está en la URL
    if talla:
        producto_lista = producto_lista.filter(talla=talla)

    # Filtrar por color si está en la URL
    if color:
        producto_lista = producto_lista.filter(color=color)

    # Manejo de agregar productos al carrito
    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id')
        try:
            producto = Producto.objects.get(id=producto_id)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None
                )
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None
                )
            
            if not created:
                carrito_item.cantidad += 1
                carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")

    return render(request, 'productos.html', {
        'productos': producto_lista
    })


def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    for item in carrito_items:
        total += item.subtotal()
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Item eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')


#vista de pasarela de compras




from .models import Orden, OrdenItem, CarritoItem 
from .forms import PedidoForm


def pasarela(request):
    carrito_items = []
    total = 0

    # Obtener los productos del carrito según el usuario o sesión
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)

    # Si el carrito está vacío, mostrar advertencia
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')

    # Calcular el total del pedido
    for item in carrito_items:
        total += item.subtotal()

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        metodo_pago = request.POST.get('metodo_pago')

        if form.is_valid() and metodo_pago:
            orden = form.save(commit=False)

            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key

            orden.total = total
            orden.metodo_pago = metodo_pago
            orden.save()

            # Guardar los productos en la orden
            for item in carrito_items:
                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    precio=item.producto.precio,
                    cantidad=item.cantidad
                )

            # Vaciar el carrito después del pago
            carrito_items.delete()

            # 📧 Enviar el correo de confirmación
            enviar_correo_confirmacion(orden)

            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmar', orden_id=orden.id)
        else:
            messages.error(request, "Por favor selecciona un método de pago válido.")
    else:
        # Precargar los datos del usuario en el formulario
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos = Datos.objects.get(usuario=request.user)
                initial_data = {
                    'nombre': f"{datos.nombre} {datos.apellido}",
                    'email': request.user.email
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email
                }

        form = PedidoForm(initial=initial_data)

    return render(request, 'pasarela.html',  {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })
   
def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        else:
            orden = Orden.objects.get(id=orden_id, sesion_id=request.session.session_key)

        items = OrdenItem.objects.filter(orden=orden)

        return render(request, 'confirmacion.html', {
            'orden': orden,
            'items': items
        })

    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('productos')


def enviar_correo_confirmacion(Orden):
    send_mail(
        "Confirmación de tu Pedido en nuestra tienda",
        f"Hola {Orden.nombre},\n\nGracias por tu pedido en Urban style.\n\n"
        f"Método de pago: {Orden.metodo_pago}\n"
        f"Total: ${Orden.total}\n\n",
        "ibanezfelipe426@gmail.com",
        [Orden.email]
    )
  # 🔹 Enviar correo al administrador
    send_mail(
        f"Nuevo Pedido Recibido de {Orden.nombre}",
        f"📢 Nuevo Pedido Recibido\n\n"
        f"Cliente: {Orden.nombre}\nCorreo: {Orden.email}\n"
        f"Método de pago: {Orden.metodo_pago}\nTotal: ${Orden.total}\n\n",
        "ibanezfelipe426@gmail.com",
        ["ibanezfelipe426@gmail.com"]
    )

    #contactenos


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Ejemplo de envío de correo (ajústalo según tus necesidades)
        send_mail(
            f'Mensaje de {name}',
            message,
            email,
            ['ibanezfelipe426@gmail.com'],
        )

        messages.success(request, '¡Mensaje enviado con éxito!')
    
    return render(request, 'contactenos.html')

# Agregar productos al mensaje
    items = OrdenItem.objects.filter(orden=orden)
    for item in items:
        mensaje += f"\n - {item.cantidad} x {item.producto.nombre}(${item.precio} c/u)"

        mensaje += "\n\nGracias por confiar en nosotros. �\n\nSaludos,\nTu tienda online"


    send_mail(
    asunto,
    mensaje,
    'ibanezfelipe426@gmail.com', # Correo del remitente
    [orden.email],
    fail_silently=False,
    )
    
  #aparatdddo de historial  

from django.contrib.auth.decorators import login_required
from .models import Historial

@login_required
def historial(request):
    compras = Historial.objects.filter(usuario=request.user).order_by('-fecha_compra')
    return render(request, 'historial.html', {'compras': compras})



