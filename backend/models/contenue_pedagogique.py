import os
from django.db import models
from backend.models.gestion_ecole import Career, Etablishment, Sector
from backend.models.user_account import Teacher
from elimu_school import settings

class eBook(models.Model):
        
        title = models.CharField(max_length=120)

        author = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)

        sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=True, null=True)

        career = models.ForeignKey(Career, on_delete=models.CASCADE, blank=True, null=True)

        photo_cover = models.ImageField(upload_to='images_ebook')

        attachement = models.FileField(upload_to='ebook_folder')

        is_private = models.BooleanField(default=False)

        school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)

        created_at = models.DateTimeField(auto_now_add=True)

        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
                return f"file : {self.title}"

        def delete(self, *args, **kwargs):
                # Supprimer le fichier associé s'il existe
                if self.photo_cover and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.photo_cover))):
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(self.photo_cover)))
                if self.attachement and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.attachement))):
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(self.attachement)))

                # Supprimer l'objet
                super(eBook, self).delete(*args, **kwargs)




# # Class representing a Folder
# class Folder(models.Model):
    
#     label = models.CharField(max_length=20)
    
#     owner = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Dossier : {self.label} crée par {self.owner}"

# # Class representing a File
# class File(models.Model):
    
#     label = models.CharField(max_length=20)
    
#     inFolder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    
#     attachement = models.FileField(upload_to='public_folder')
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"file : {self.label}"

# Class representing a BookCategory
# class BookCategory(models.Model):
    
#     label = models.CharField(max_length=20)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Categorie Livre : {self.label}"

# Class representing a Book
# class Book(models.Model):
    
#     label = models.CharField(max_length=120)
    
#     author = models.CharField(max_length=120)
    
#     code_isbn = models.CharField(max_length=120)
    
#     location = models.CharField(max_length=120, blank=True)
    
#     attachement = models.FileField(upload_to='public_folder', blank=True)
    
#     sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#        return f"file : {self.label}"
    
# Class representing an eBook

