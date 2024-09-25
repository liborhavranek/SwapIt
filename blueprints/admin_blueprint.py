from flask_login import current_user, login_required

from flask import Blueprint, render_template, request, session, current_app, flash, redirect, url_for, abort

from extensions import db
from models.brand_model import Brand
from models.category_model import Category
from models.product_model import Product

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role not in ['user', 'manager',  'admin']:
        abort(403)
    if current_user.role == 'admin':
        return render_template('admin/admin_dashboard.html')
    if request.method == 'POST':
        access_password = request.form.get('access_password')
        if access_password == current_app.config['ADMIN_ACCESS_PASSWORD']:
            session['admin_access'] = True
            return render_template('admin/admin_dashboard.html')
        else:
            flash('Nesprávné heslo.', 'danger')
    if not session.get('admin_access'):
        return render_template('admin/admin_login.html')
    session.pop('admin_access', None)
    return redirect(url_for('auth_bp.login'))


@admin_bp.route('/create_category', methods=['GET', 'POST'])
def create_category():
    categories = Category.query.all()
    categories_with_subcategories = build_category_tree(categories, include_invisible=False)

    if request.method == 'POST':
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

    def fetch_categories():
        return Category.query.filter_by(parent_id=None).order_by(Category.order).all()

    categories = fetch_categories()
    return render_template('admin/category/create_category.html', categories=categories,
                           categories_tree=categories_with_subcategories)


@admin_bp.route('/category_list')
def category_list():
    categories = Category.query.all()
    categories_with_subcategories = build_category_tree(categories, include_invisible=True)
    return render_template('admin/category/category_list.html', categories_tree=categories_with_subcategories)


@admin_bp.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == 'POST':
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

    categories = Category.query.filter(Category.id != category_id).order_by(Category.order).all()
    categories_with_subcategories = build_category_tree(categories, include_invisible=False)

    return render_template('admin/category/edit_category.html', category=category, categories=categories,
                           categories_tree=categories_with_subcategories)


@admin_bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)  # Získáme kategorii podle ID nebo vrátíme 404

    def delete_subcategories(category):
        for subcategory in category.subcategories:
            delete_subcategories(subcategory)
            db.session.delete(subcategory)

    delete_subcategories(category)
    db.session.delete(category)
    db.session.commit()

    flash('Kategorie a všechny její podkategorie byly úspěšně smazány.', 'success')
    return redirect(url_for('admin_bp.category_list'))


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


@admin_bp.route('/create_brand', methods=['GET', 'POST'])
def create_brand():
    brands = Brand.query.all()
    brands_with_subbrands = build_brand_tree(brands, include_invisible=False)

    if request.method == 'POST':
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

    def fetch_brands():
        return Brand.query.filter_by(parent_id=None).order_by(Brand.order).all()

    brands = fetch_brands()
    return render_template('admin/brand/create_brand.html', brands=brands,
                           brands_tree=brands_with_subbrands)


@admin_bp.route('/brand_list')
def brand_list():
    brands = Brand.query.all()
    brands_with_subbrands = build_brand_tree(brands, include_invisible=True)
    return render_template('admin/brand/brand_list.html', brands_tree=brands_with_subbrands)


@admin_bp.route('/edit_brand/<int:brand_id>', methods=['GET', 'POST'])
def edit_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)

    if request.method == 'POST':
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

    brands = Brand.query.filter(Brand.id != brand_id).order_by(Brand.order).all()
    brands_with_subbrands = build_brand_tree(brands, include_invisible=False)

    return render_template('admin/brand/edit_brand.html', brand=brand, brands=brands,
                           brands_tree=brands_with_subbrands)


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


@admin_bp.route('/delete_brand/<int:brand_id>', methods=['POST'])
def delete_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)  # Získáme značku podle ID nebo vrátíme 404

    def delete_subbrands(brand):
        for subbrand in brand.subbrands:
            delete_subbrands(subbrand)
            db.session.delete(subbrand)

    delete_subbrands(brand)
    db.session.delete(brand)
    db.session.commit()

    flash('Značka a všechny její podznačky byly úspěšně smazány.', 'success')
    return redirect(url_for('admin_bp.brand_list'))


@admin_bp.route('/product_list')
def product_list():
    products = Product.query.all()
    return render_template('admin/products/product_list.html', products=products)



@admin_bp.route('/create_sample_data', methods=['POST'])
@login_required
def create_sample_data():
    if current_user.role != 'admin':
        abort(403)

    # Smazání stávajících kategorií a značek
    Category.query.delete()
    Brand.query.delete()

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
        # Hlavní kategorie s ikonou
        root_category = Category(name=category_name, visible=True, icon=category_info["icon"])
        db.session.add(root_category)

        # Podkategorie a pod-podkategorie bez ikony
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