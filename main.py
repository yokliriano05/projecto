#first change
import webapp2, re, os, jinja2
from Models import *

pages_dir = os.path.join(os.path.dirname(__file__),'pages')


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(pages_dir),
	autoescape = True)

PAGE_RE = r'(?:[a-zA-Z0-9_-]+/?)*'
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

#===================================================================
#    functions
#===================================================================
def hash_str(s):
	#return hashlib.md5(s).hexdigest()
	#return hmac.new(SECRET,s).hexdigest()
	return hmac.new(SECRET,s,hashlib.sha256).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	string = h.split('|')[0]
	if make_secure_val(string) == h:
		return string

def make_salt():
	return ''.join(random.choice(string.letters) for x in range(5))

def make_pw_hash(name, pw, salt=""):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
	""" return True or False if h and the make pw are the same"""
	return h == make_pw_hash(name, pw, h.split(',')[1])
#===================================================================
#    Endfunctions
#===================================================================




class Handler(webapp2.RequestHandler):

	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,_estilo,**parametros):
		t = jinja_env.get_template(_estilo)
		return t.render(parametros)

	def render(self,_estilo,**kw):
		Usuario = self.request.cookies.get("Usuario")
		kw['Usuario'] = Usuario
		self.write(self.render_str(_estilo,**kw))

class Raiz(Handler):
	def get(self):
		self.redirect('/inicio')

class Inicio(Handler):

	def get(self):
		# todos_articulos = db.GqlQuery("SELECT * FROM TArticulos ORDER BY created DESC").get()
		todos_articulos = list(TArticulos.all())
		#username = self.request.cookies.get('Username')
		if not todos_articulos:
			todos_articulos = ["No hay articulos publicados","Fulanito", "Fulanito2","No hay articulos publicados","Fulanito", "Fulanito2"]
		self.render("inicio.html", todos_articulos = todos_articulos, TituloPagin = "Inicio")

class AgregarArticulo(Handler):
	"""docstring for AgregarArticulo"""
	def get(self):
		self.render('nuevo_articulo.html')
		
class Registro(Handler):
	def get(self):
		self.write_form()
	
	def post(self):
		Nombre = self.request.get('nombre')
		Apellidos = self.request.get('apellidos')
		contrasena = self.request.get('contrasena')
		verificacion = self.request.get('verificacion')
		email = self.request.get('email')

		usuario_error = ""
		contrasena_error = ""
		verificacion_error = ""
		email_error = ""

		if not self.valid_username(usuario): 
			usuario_error = "No se aceptan espacios en blanco"
			
		if not self.valid_password(contrasena):
			contrasena_error = "Debe de introducir una contrasena"
			
		if not contrasena_error:
			if verificacion:
				if not self.valid_verify(contrasena, verificacion):
					verificacion_error="Las contrasenas no son las mismas"
			else: verificacion_error="Debe de repetir la contrasena"
		if Users.all().filter("Username =", Nombre).filter("Apellido =", Apellido).get():
			usuario_error = "Usuario ya existe!"
		if not email:            
			email_error = 'Debe introducir un correo'
		if not self.valid_email(email):
			email_error = 'El correo no es valido'

		if contrasena_error or usuario_error or verificacion_error or email_error:
			self.write_form(usuario = usuario, contrasena = contrasena, verificacion = verificacion, email=email,usuario_error = usuario_error,
			contrasena_error = contrasena_error, verificacion_error = verificacion_error, email_error = email_error)

		else: 
			self.redirect('/bienvenida?usuario='+self.request.get('usuario'))

	def write_form(self, usuario = "", contrasena ="", verificacion ="", email ="", usuario_error ="", contrasena_error ="", verificacion_error ="", email_error =""):
		self.render("registro.html", usuario_error = usuario_error, contrasena_error = contrasena_error, verificacion_error = verificacion_error,email_error = email_error, NoMostrar = True)



	def valid_username(self,username):
		return USERNAME_RE.match(username)

	def valid_verify(self,password,verify):
		if password==verify:
			return True
		return False

	def valid_password(self,password):
		return PASSWORD_RE.match(password)

	def valid_email(self,email):
		return EMAIL_RE.match(email)


class BienvenidaR(Handler):

	def get(self):
		usuario = self.request.get('usuario')
		if usuario:
			self.render("bienvenido.html" , usuario = usuario)
		else: self.redirect('/registro')

class Acceder(Handler):

	def get(self):
		self.render("inicia-seccion.html", NoMostrar = True)

	def post(self):
		self.redirect('/')




app = webapp2.WSGIApplication([
	# (PAGE_RE, Inicio),
	('/registro', Registro),
	('/bienvenida', BienvenidaR),
	('/acceder', Acceder),
	('/agregar-articulo', AgregarArticulo),
	('/'+PAGE_RE, Inicio)
	], debug=True)
