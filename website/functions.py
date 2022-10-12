import os
from werkzeug.utils import secure_filename


def check_upload_file(file_data, folder_path):
    # get file data from form
    # fp = form.image.data
    if (file_data is None):
        return None

    filename = file_data.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/img/' + folder_path, secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/img/' + folder_path + '/' + secure_filename(filename)
    # save the file and return the db upload path
    file_data.save(upload_path)
    return db_upload_path
