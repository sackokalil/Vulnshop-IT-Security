from flask import Blueprint, render_template


#-------------------------User-Seitige Handlungen------------------------------------

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def product_list():
    return render_template("shop/index.html")
    #Später wird product_list eine ganz andere datei zurückgeben
    #(list_product.htmm).


@product_bp.route('/<int:product_id>')
def detail_product(product_id):
    return render_template('shop/product.html')
    #SPäter wird das Product anhand seiner id aus der Datenbank abgerufen.



#-----------------------------------Admin part----------------------------------------------

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin/products")


@admin_product_bp.route("/")
def admin_product_list():
    return render_template("admin/products/list.html")
    #Diese route ist noch nicht werwendet worden