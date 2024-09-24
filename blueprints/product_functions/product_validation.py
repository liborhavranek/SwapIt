from blueprints.product_functions.allowed_files import allowed_file


def validate_product_form(form, images):
    errors = []

    title = form.get('title')
    description = form.get('description')
    purchase_price = form.get('purchase_price')
    swap_price = form.get('swap_price')
    main_category = form.get('category')
    selected_categories = form.getlist('selected_category')
    exchange_method = form.get('exchange_method')
    desired_exchange = form.get('desired_exchange')
    city = form.get('city')
    postal_code = form.get('postal_code')
    condition = form.get('condition')
    availability = form.get('availability')
    if selected_categories:
        category_id = selected_categories[-1]
    else:
        category_id = main_category
    if not title:
        errors.append('Název věci je povinný.')
    elif len(title) < 2:
        errors.append('Název musí obsahovat alespoň 2 znaky.')
    elif len(title) > 50:
        errors.append('Název nesmí být delší než 50 znaků.')
    if not description:
        errors.append('Popis je povinný.')
    elif len(description) < 20:
        errors.append('Popis musí obsahovat alespoň 20 znaků.')
    elif len(description) > 5000:
        errors.append('Popis nesmí být delší než 5000 znaků.')
    if not category_id:
        errors.append('Zadejte do jaké kategorie spadá předmět.')
    if not exchange_method:
        errors.append('Zadejte jaký preferujete způsob výměny.')
    if not purchase_price or not swap_price:
        errors.append('Ceny jsou povinné.')
    else:
        try:
            purchase_price_value = float(purchase_price)
            swap_price_value = float(swap_price)
            if purchase_price_value < 0:
                errors.append('Pořizovací cena nesmí být záporná.')
            if swap_price_value < 0:
                errors.append('Cena za výměnu nesmí být záporná.')
        except ValueError:
            errors.append('Ceny musí být čísla.')
    if not condition:
        errors.append('Zadejte jaký je stav předmětu.')
    if not availability:
        errors.append('Zadejte dostupnost předmětu.')
    if not desired_exchange:
        errors.append('Vyplňte co chcete za výměnu.')
    elif len(desired_exchange) < 20:
        errors.append('Co chci za výměnu musí obsahovat alespoň 20 znaků.')
    elif len(desired_exchange) > 5000:
        errors.append('Co chci za výměnu nesmí být delší než 5000 znaků.')
    if not city:
        errors.append('Zadejte jméno města.')
    elif len(city) < 2:
        errors.append('Název města musí obsahovat alespoň 2 znaky.')
    elif len(city) > 50:
        errors.append('Název města nesmí být delší než 50 znaků.')
    if not postal_code:
        errors.append('PSČ je povinné.')
    elif len(postal_code) != 5 or not postal_code.isdigit():
        errors.append('PSČ musí mít 5 čísel.')
    if not images or len(images) == 0:
        errors.append('Musíte nahrát alespoň jednu fotografii produktu.')
    else:
        valid_image_found = False
        for image_file in images:
            if image_file and allowed_file(image_file.filename):
                valid_image_found = True
                break
        if not valid_image_found:
            errors.append('Musíte nahrát alespoň jednu platnou fotografii ve formátu PNG, JPG, JPEG nebo GIF.')
    return errors, category_id
