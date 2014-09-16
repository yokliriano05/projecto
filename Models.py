#====================================================================
#   Tablas (DB)
#===================================================================
from google.appengine.ext import db

class TUsuario(db.Model):
    US_Nombre = db.StringProperty(required = True)
    Us_Apellidos  = db.StringProperty(required = True)
    US_Direccion = db.StringProperty(required = True)
    US_Correo = db.EmailProperty( required = True)
    US_Contrasena = db.StringProperty(required = True)

    US_Preferencia = db.StringProperty( required = False)
    US_Companeros = db.StringProperty( required = False)
    US_Sigue = db.StringProperty(required = False)
    Us_Seguidores = db.StringProperty( required = False)
    
    US_Fecha_Registro = db.DateTimeProperty(auto_now_add = True)

class TCategoria(db.Model):
    CA_Nombre = db.TextProperty(required = True)
    CA_Subcategoria = db.TextProperty(required = False)
    CA_Principal = db.TextProperty(required = True)

class TArticulos(db.Model):
    AR_Nombre = db.StringProperty(required = True)
    AR_Vendedor = db.StringProperty(required = True) #usuario dueno del articulo
    AR_Descripcion = db.TextProperty(required = False)
    AR_Categoria = db.TextProperty(required = True)
    AR_Precio = db.FloatProperty(required = True)
    AR_CantidadExistente = db.IntegerProperty(required = False)

class TCuentas_Electronica(db.Model):
    CE_Usuario = db.TextProperty(required = True)
    CE_Paypal = db.EmailProperty(required = False)
    CE_Tarjeta_Electronica = db.TextProperty(required = False)

class TVentas(db.Model):
    Articulo = db.StringProperty(required=True)
    Precio = db.FloatProperty(required = True)
    Vendedor = db.StringProperty(required  = True)
    Comprador = db.StringProperty(required = True)
    FechaVenta = db.DateTimeProperty(auto_now_add = True)


#===================================================================
#  Fin de tablas
#===================================================================