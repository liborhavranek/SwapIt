import os
import uuid
from extensions import db
from models.image_model import Image
from werkzeug.utils import secure_filename
from blueprints.product_functions.allowed_files import allowed_file


def process_images(images, product_id):
    upload_folder = os.path.join('static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for image_file in images:
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(upload_folder, unique_filename)
            image_file.save(image_path)
            image_url = os.path.join('uploads', unique_filename)
            new_image = Image(image_url=image_url, product_id=product_id)
            db.session.add(new_image)
    db.session.commit()
