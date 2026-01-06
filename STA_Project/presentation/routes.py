# presentation/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from logic.services import TraceabilityService, AuthService
from functools import wraps

web_bp = Blueprint('web', __name__, template_folder='templates')
service = TraceabilityService()
auth_service = AuthService()
auth_service.inicializar_admin()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session: return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rutas de Auth (Sin cambios) ---
@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if auth_service.validar_login(request.form['username'], request.form['password']):
            session['user'] = request.form['username']
            return redirect(url_for('web.index'))
        flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@web_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('web.login'))

# --- Rutas de Negocio ---
@web_bp.route('/')
@login_required
def index():
    productos = service.obtener_trazabilidad()
    kpis = service.obtener_estadisticas() # Datos para el dashboard
    return render_template('index.html', productos=productos, kpis=kpis)

@web_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        data = {
            'lote': request.form['lote'],
            'variedad': request.form['variedad'],
            'finca': request.form['finca'],
            'fecha_cosecha': request.form['fecha_cosecha'],
            'fecha_empaquetado': request.form['fecha_empaquetado'],
            'calidad_ok': request.form['calidad_ok'],
            'temperatura_transporte': request.form['temperatura_transporte'],
            'fecha_entrega': request.form['fecha_entrega']
        }
        service.registrar_producto(data)
        flash('Lote registrado exitosamente', 'success')
        return redirect(url_for('web.index'))
    return render_template('form.html', producto=None)

@web_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    producto = service.obtener_producto(id)
    if request.method == 'POST':
        data = {
            'lote': request.form['lote'],
            'variedad': request.form['variedad'],
            'finca': request.form['finca'],
            'fecha_cosecha': request.form['fecha_cosecha'],
            'fecha_empaquetado': request.form['fecha_empaquetado'],
            'calidad_ok': request.form['calidad_ok'],
            'temperatura_transporte': request.form['temperatura_transporte'],
            'fecha_entrega': request.form['fecha_entrega']
        }
        service.actualizar_producto(id, data)
        flash('Lote actualizado correctamente', 'info')
        return redirect(url_for('web.index'))
    return render_template('form.html', producto=producto)

@web_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    service.eliminar_producto(id)
    flash('Registro eliminado', 'warning')
    return redirect(url_for('web.index'))

@web_bp.route('/ver/<int:id>')
@login_required
def ver(id):
    producto = service.obtener_producto(id)
    return render_template('detail.html', p=producto)