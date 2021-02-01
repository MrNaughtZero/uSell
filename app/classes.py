from app import app
from werkzeug.utils import secure_filename
import os
import string
from random import choice
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url


class Uploads():
    def __init__(self, uploaded_file):
        ''' Pass through request.files '''
        self.uploaded_file = uploaded_file
        
    @staticmethod
    def generate_file_id(Length=56):
        generate = string.ascii_letters + string.ascii_uppercase + string.digits
        return ''.join(choice(generate) for i in range(Length))

    def save_upload(self):        
        if secure_filename(self.uploaded_file.filename) == '':
            return None

        file_id = self.generate_file_id()
        upload_result = upload(self.uploaded_file, public_id=file_id)
        
        return cloudinary_url(upload_result['public_id'])[0]

    @staticmethod
    def remove_upload(file_id):
        destroy(file_id)