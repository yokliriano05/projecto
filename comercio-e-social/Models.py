#====================================================================
#   Tablas (DB)
#===================================================================
class TUsuario(db.Model):

    Nombre_Usuario = db.StringProperty(required = True)
    Contrasena = db.StringProperty(required = True)
    Email = db.EmailProperty( required = True)
    Fecha_Registro = db.DateTimeProperty(auto_now_add = True)

class TArticles(db.Model):
    Nombre = db.StringProperty(required = True)
    Descripcion = db.TextProperty(required = False)
    Propietario = db.StringProperty(required = True) #usuario dueno del articulo
    Precio = db.FloatProperty(required = True)
    CantidadExistente = db.IntegerProperty(required = False)

class TVentas(db.Model):
    Articulo = db.StringProperty(required=True)
    Precio = db.FloatProperty(required = True)
    Vendedor = db.StringProperty(required  = True)
    Comprador = db.StringProperty(required = True)
    FechaVenta = db.DateTimeProperty(auto_now_add = True)


#===================================================================
#  Fin de tablas
#===================================================================