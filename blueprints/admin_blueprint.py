from flask import Blueprint, render_template, request, session, current_app, flash, redirect, url_for, abort
from flask.views import MethodView
from flask_login import current_user, login_required
from blueprints.admin_blueprint_not_working.forms import AdminLoginForm
from extensions import db
from models.brand_model import Brand
from models.category_model import Category
from models.product_model import Product

admin_bp = Blueprint('admin_bp', __name__)


class AdminDashboardView(MethodView):
    decorators = [login_required]

    def get(self):
        if current_user.role not in ['user', 'manager', 'admin']:
            abort(403)
        if current_user.role == 'admin' or session.get('admin_access'):
            return render_template('admin/admin_dashboard.html')
        form = AdminLoginForm()
        return render_template('admin/admin_login.html', form=form)

    def post(self):
        if current_user.role not in ['user', 'manager', 'admin']:
            abort(403)
        form = AdminLoginForm()
        if form.validate_on_submit():
            access_password = form.access_password.data
            if access_password == current_app.config['ADMIN_ACCESS_PASSWORD']:
                session['admin_access'] = True
                return render_template('admin/admin_dashboard.html')
            flash('Nesprávné heslo.', 'danger')
        return render_template('admin/admin_login.html', form=form)


admin_bp.add_url_rule('/admin', view_func=AdminDashboardView.as_view('admin_dashboard'))


# Create Category View
class CreateCategoryView(MethodView):
    decorators = [login_required]

    def get(self):
        categories = self.fetch_categories()
        categories_with_subcategories = build_category_tree(categories, include_invisible=False)
        return render_template('admin/category/create_category.html', categories=categories,
                               categories_tree=categories_with_subcategories)

    def post(self):
        name = request.form['name']
        order = request.form.get('order', type=int)
        visible = request.form.get('visible') == 'on'
        icon = request.form.get('icon')  # Získání ikony

        if len(name) < 1:
            flash('Kategorie musí mít alespoň jeden znak.', 'danger')
            return redirect(url_for('admin_bp.create_category'))

        parent_id = request.form.get('parent_id')
        parent_category = Category.query.get(parent_id) if parent_id else None
        new_category = Category(name=name, parent=parent_category, order=order, visible=visible, icon=icon)

        db.session.add(new_category)
        db.session.commit()

        flash('Kategorie byla úspěšně vytvořena.', 'success')
        return redirect(url_for('admin_bp.category_list'))

    def fetch_categories(self):
        return Category.query.filter_by(parent_id=None).order_by(Category.order).all()



class EditCategoryView(MethodView):
    decorators = [login_required]

    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        categories = Category.query.filter(Category.id != category_id).order_by(Category.order).all()
        categories_with_subcategories = build_category_tree(categories, include_invisible=False)
        return render_template('admin/category/edit_category.html', category=category, categories=categories,
                               categories_tree=categories_with_subcategories)

    def post(self, category_id):
        category = Category.query.get_or_404(category_id)
        name = request.form['name']
        order = request.form.get('order', type=int)
        visible = request.form.get('visible') == 'on'
        parent_id = request.form.get('parent_id')
        icon = request.form.get('icon')

        if len(name) < 1:
            flash('Kategorie musí mít alespoň jeden znak.', 'danger')
            return redirect(url_for('admin_bp.edit_category', category_id=category_id))

        parent_category = Category.query.get(parent_id) if parent_id else None

        # Aktualizace atributů kategorie
        category.name = name
        category.order = order
        category.visible = visible
        category.parent = parent_category
        category.icon = icon

        db.session.commit()
        flash('Kategorie byla úspěšně upravena.', 'success')
        return redirect(url_for('admin_bp.category_list'))


# Delete Category View
class DeleteCategoryView(MethodView):
    decorators = [login_required]

    def post(self, category_id):
        category = Category.query.get_or_404(category_id)  # Získáme kategorii podle ID nebo vrátíme 404

        self.delete_subcategories(category)
        db.session.delete(category)
        db.session.commit()

        flash('Kategorie a všechny její podkategorie byly úspěšně smazány.', 'success')
        return redirect(url_for('admin_bp.category_list'))

    def delete_subcategories(self, category):
        for subcategory in category.subcategories:
            self.delete_subcategories(subcategory)
            db.session.delete(subcategory)


# Category List View
class CategoryListView(MethodView):
    decorators = [login_required]

    def get(self):
        categories = Category.query.all()
        categories_with_subcategories = build_category_tree(categories, include_invisible=True)
        return render_template('admin/category/category_list.html', categories_tree=categories_with_subcategories)


# Registrace jednotlivých Class-Based Views
admin_bp.add_url_rule('/create_category', view_func=CreateCategoryView.as_view('create_category'))
admin_bp.add_url_rule('/edit_category/<int:category_id>', view_func=EditCategoryView.as_view('edit_category'))
admin_bp.add_url_rule('/delete_category/<int:category_id>', view_func=DeleteCategoryView.as_view('delete_category'))
admin_bp.add_url_rule('/category_list', view_func=CategoryListView.as_view('category_list'))

# functions
def build_category_tree(categories, include_invisible=False):
    if include_invisible:
        category_dict = {category.id: {'category': category, 'subcategories': []} for category in categories}
    else:
        category_dict = {category.id: {'category': category, 'subcategories': []} for category in categories if category.visible}
    root_categories = []
    for category in sorted(categories, key=lambda c: c.order):
        if include_invisible or category.visible:
            if category.parent_id is None:
                root_categories.append(category_dict[category.id])
            else:
                parent = category_dict.get(category.parent_id)
                if parent:
                    parent['subcategories'].append(category_dict[category.id])
    return root_categories


# Create Brand View
class CreateBrandView(MethodView):
    decorators = [login_required]

    def get(self):
        brands = self.fetch_brands()
        brands_with_subbrands = build_brand_tree(brands, include_invisible=False)
        return render_template('admin/brand/create_brand.html', brands=brands,
                               brands_tree=brands_with_subbrands)

    def post(self):
        name = request.form['name']
        order = request.form.get('order', type=int)
        visible = request.form.get('visible') == 'on'
        icon = request.form.get('icon')  # Získání ikony

        if len(name) < 1:
            flash('Značka musí mít alespoň jeden znak.', 'danger')
            return redirect(url_for('admin_bp.create_brand'))

        parent_id = request.form.get('parent_id')
        parent_brand = Brand.query.get(parent_id) if parent_id else None
        new_brand = Brand(name=name, parent=parent_brand, order=order, visible=visible, icon=icon)

        db.session.add(new_brand)
        db.session.commit()

        flash('Značka byla úspěšně vytvořena.', 'success')
        return redirect(url_for('admin_bp.brand_list'))

    def fetch_brands(self):
        return Brand.query.filter_by(parent_id=None).order_by(Brand.order).all()


# Edit Brand View
class EditBrandView(MethodView):
    decorators = [login_required]

    def get(self, brand_id):
        brand = Brand.query.get_or_404(brand_id)
        brands = Brand.query.filter(Brand.id != brand_id).order_by(Brand.order).all()
        brands_with_subbrands = build_brand_tree(brands, include_invisible=False)
        return render_template('admin/brand/edit_brand.html', brand=brand, brands=brands,
                               brands_tree=brands_with_subbrands)

    def post(self, brand_id):
        brand = Brand.query.get_or_404(brand_id)
        name = request.form['name']
        order = request.form.get('order', type=int)
        visible = request.form.get('visible') == 'on'
        parent_id = request.form.get('parent_id')
        icon = request.form.get('icon')

        if len(name) < 1:
            flash('Značka musí mít alespoň jeden znak.', 'danger')
            return redirect(url_for('admin_bp.edit_brand', brand_id=brand_id))

        parent_brand = Brand.query.get(parent_id) if parent_id else None

        # Aktualizace atributů značky
        brand.name = name
        brand.order = order
        brand.visible = visible
        brand.parent = parent_brand
        brand.icon = icon

        db.session.commit()
        flash('Značka byla úspěšně upravena.', 'success')
        return redirect(url_for('admin_bp.brand_list'))


# Delete Brand View
class DeleteBrandView(MethodView):
    decorators = [login_required]

    def post(self, brand_id):
        brand = Brand.query.get_or_404(brand_id)

        self.delete_subbrands(brand)
        db.session.delete(brand)
        db.session.commit()

        flash('Značka a všechny její podznačky byly úspěšně smazány.', 'success')
        return redirect(url_for('admin_bp.brand_list'))

    def delete_subbrands(self, brand):
        for subbrand in brand.subbrands:
            self.delete_subbrands(subbrand)
            db.session.delete(subbrand)


# Brand List View
class BrandListView(MethodView):
    decorators = [login_required]

    def get(self):
        brands = Brand.query.all()
        brands_with_subbrands = build_brand_tree(brands, include_invisible=True)
        return render_template('admin/brand/brand_list.html', brands_tree=brands_with_subbrands)


# Registrace Class-Based Views
admin_bp.add_url_rule('/create_brand', view_func=CreateBrandView.as_view('create_brand'))
admin_bp.add_url_rule('/edit_brand/<int:brand_id>', view_func=EditBrandView.as_view('edit_brand'))
admin_bp.add_url_rule('/delete_brand/<int:brand_id>', view_func=DeleteBrandView.as_view('delete_brand'))
admin_bp.add_url_rule('/brand_list', view_func=BrandListView.as_view('brand_list'))


def build_brand_tree(brands, include_invisible=False):
    if include_invisible:
        brand_dict = {brand.id: {'brand': brand, 'subbrands': []} for brand in brands}
    else:
        brand_dict = {brand.id: {'brand': brand, 'subbrands': []} for brand in brands if brand.visible}
    root_brands = []
    for brand in sorted(brands, key=lambda b: b.order):
        if include_invisible or brand.visible:
            if brand.parent_id is None:
                root_brands.append(brand_dict[brand.id])
            else:
                parent = brand_dict.get(brand.parent_id)
                if parent:
                    parent['subbrands'].append(brand_dict[brand.id])
    return root_brands


class ProductListView(MethodView):
    decorators = [login_required]

    def get(self):
        # Načtení všech produktů z databáze
        products = Product.query.all()
        return render_template('admin/products/product_list.html', products=products)

# Registrace class-based view pro zobrazení seznamu produktů
admin_bp.add_url_rule('/product_list', view_func=ProductListView.as_view('product_list'))


class CreateSampleDataView(MethodView):
    decorators = [login_required]

    def post(self):
        # Kontrola oprávnění uživatele
        if current_user.role != 'admin':
            abort(403)

        # Smazání stávajících kategorií a značek
        Category.query.delete()
        Brand.query.delete()

        # Ukázková data kategorií
        categories_data = {
            "Knihy": {
                "icon": "bi bi-book",
                "subcategories": {
                    "Literatura": ["Romány", "Poezie", "Sci-fi"],
                    "Učebnice": ["Matematika", "Fyzika", "Jazyky"]
                }
            },
            "Oblečení": {
                "icon": "bi bi-bag",
                "subcategories": {
                    "Pánské": ["Trička", "Kalhoty", "Bundy"],
                    "Dámské": ["Šaty", "Sukně", "Kabelky"]
                }
            },
            "Auta": {
                "icon": "bi bi-car-front",
                "subcategories": {
                    "Osobní auta": ["Sedany", "SUV", "Kabriolety"],
                    "Nákladní auta": ["Dodávky", "Kamiony"]
                }
            },
            "Dům a zahrada": {
                "icon": "bi bi-house",
                "subcategories": {
                    "Nábytek": ["Stoly", "Židle", "Postele"],
                    "Zahradní vybavení": ["Křovinořezy", "Sekačky", "Zahradní hadice"]
                }
            },
            "Sport": {
                "icon": "bi bi-basketball",
                "subcategories": {
                    "Sportovní vybavení": ["Fotbalové míče", "Tenisové rakety", "Kopačky"],
                    "Fitness": ["Činky", "Běžecké pásy"]
                }
            },
            "Hudba": {
                "icon": "bi bi-music-note",
                "subcategories": {
                    "Hudební nástroje": ["Kytary", "Bicí", "Klavíry"],
                    "Příslušenství": ["Struny", "Paličky", "Stojany"]
                }
            },
            "Nábytek": {
                "icon": "bi bi-house",
                "subcategories": {
                    "Obývací pokoj": ["Sedačky", "Křesla", "Stoly"],
                    "Kuchyně": ["Skříňky", "Stoly", "Židle"]
                }
            },
            "Hračky": {
                "icon": "bi bi-joystick",
                "subcategories": {
                    "Pro chlapce": ["Auta", "Stavebnice", "Akční figurky"],
                    "Pro dívky": ["Panenky", "Kreativní sety", "Puzzle"]
                }
            },
            "Kuchyně": {
                "icon": "bi bi-tools",
                "subcategories": {
                    "Velké spotřebiče": ["Lednice", "Myčky", "Sporáky"],
                    "Malé spotřebiče": ["Mixéry", "Konvice", "Toustovače"]
                }
            },
            "Kancelář": {
                "icon": "bi bi-pen",
                "subcategories": {
                    "Psací potřeby": ["Pera", "Tužky", "Sešity"],
                    "Počítače": ["Notebooky", "Monitory", "Klávesnice"]
                }
            },
            "Obuv": {
                "icon": "bi bi-shoe",
                "subcategories": {
                    "Pánská obuv": ["Boty na běhání", "Polobotky", "Pantofle"],
                    "Dámská obuv": ["Baleríny", "Sandály", "Kozačky"]
                }
            },
            "Móda": {
                "icon": "bi bi-watch",
                "subcategories": {
                    "Doplňky": ["Hodinky", "Šperky", "Opasky"],
                    "Oblečení": ["Topy", "Sukně", "Kabáty"]
                }
            },
            "Cestování": {
                "icon": "bi bi-suitcase",
                "subcategories": {
                    "Zavazadla": ["Kufry", "Batohy", "Kabelky"],
                    "Cestovní vybavení": ["Plážové osušky", "Stan", "Spacáky"]
                }
            },
            "Domácí mazlíčci": {
                "icon": "bi bi-heart",
                "subcategories": {
                    "Psi": ["Vodítka", "Pelechy", "Krmivo"],
                    "Kočky": ["Škrabadla", "Hračky", "Krmivo"]
                }
            },
            "Dětské zboží": {
                "icon": "bi bi-basket",
                "subcategories": {
                    "Kočárky": ["Hluboké", "Sportovní", "Golfové"],
                    "Oblečení pro děti": ["Overaly", "Bundy", "Boty"]
                }
            }
        }

        # Vytvoření kategorií a podkategorií
        for category_name, category_info in categories_data.items():
            root_category = Category(name=category_name, visible=True, icon=category_info["icon"])
            db.session.add(root_category)

            for subcategory_name, sub_subcategories in category_info["subcategories"].items():
                sub_category = Category(name=subcategory_name, parent=root_category, visible=True, icon='')
                db.session.add(sub_category)

                for sub_subcategory_name in sub_subcategories:
                    sub_subcategory = Category(name=sub_subcategory_name, parent=sub_category, visible=True, icon='')
                    db.session.add(sub_subcategory)

        # Seznam značek pro různé kategorie
        brands_data = [
            {"name": "Apple", "category": "Elektronika", "icon": "bi bi-apple"},
            {"name": "Samsung", "category": "Elektronika", "icon": "bi bi-phone"},
            {"name": "Nike", "category": "Oblečení", "icon": "bi bi-person"},
            {"name": "Adidas", "category": "Sport", "icon": "bi bi-basketball"},
            {"name": "BMW", "category": "Auta", "icon": "bi bi-car-front"},
            {"name": "Ford", "category": "Auta", "icon": "bi bi-car-front"},
            {"name": "IKEA", "category": "Nábytek", "icon": "bi bi-house"},
            {"name": "Fender", "category": "Hudba", "icon": "bi bi-music-note"},
            {"name": "Bosch", "category": "Kuchyňské spotřebiče", "icon": "bi bi-tools"},
            {"name": "HP", "category": "Kancelářské potřeby", "icon": "bi bi-laptop"},
            {"name": "Puma", "category": "Obuv", "icon": "bi bi-person"},
            {"name": "Rolex", "category": "Móda", "icon": "bi bi-watch"}
        ]

        # Vytvoření značek
        for brand_data in brands_data:
            brand = Brand(name=brand_data["name"], visible=True, icon=brand_data["icon"])
            db.session.add(brand)

        # Commit do databáze
        db.session.commit()

        flash('Sada kategorií a značek byla úspěšně vytvořena.', 'success')
        return redirect(url_for('admin_bp.admin_dashboard'))

# Registrace class-based view pro vytvoření ukázkových dat
admin_bp.add_url_rule('/create_sample_data', view_func=CreateSampleDataView.as_view('create_sample_data'))
