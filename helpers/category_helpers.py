from models.category_model import Category


def get_all_categories():
    return Category.query.all()


def get_category_ancestors(category):
    ancestors = []
    while category.parent:
        category = category.parent
        ancestors.insert(0, category)
    return ancestors


def get_selected_category_and_ancestors(category_id):
    selected_category = None
    ancestor_ids = []

    if category_id:
        selected_category = Category.query.get_or_404(category_id)
        ancestors = get_category_ancestors(selected_category)
        ancestor_ids = [ancestor.id for ancestor in ancestors]

    return selected_category, ancestor_ids
