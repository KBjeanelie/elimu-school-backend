import os
from django.db import models
from backend.models.gestion_ecole import Career, Etablishment
from elimu_school import settings
from ckeditor.fields import RichTextField

from backend.models.user_account import Student
from elimu_school.constant import hours_of_the_day

# Create your models here.
class Information(models.Model):
    
    title = models.CharField(max_length=50)
    
    date_info = models.DateField(blank=True, null=True)
    
    content = RichTextField(blank=True, null=True)
    
    file = models.FileField(upload_to='info_files', blank=True)
    
    status = models.BooleanField(default=True)
    
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Information : {self.title}"
    
    def file_exists(self):
        if self.file:
            return os.path.exists(settings.MEDIA_ROOT / str(self.file))
        return False
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        
        # Supprimer l'objet
        super(Information, self).delete(*args, **kwargs)


class Event(models.Model):
    
    title = models.CharField(max_length=50)
    
    start_date = models.DateField(blank=True, null=True)
    
    end_date = models.DateField(blank=True, null=True)
    
    content =  RichTextField(blank=True, null=True)
    
    status = models.BooleanField(default=True)
    
    file = models.FileField(upload_to='events_files/', blank=True)
    
    photo = models.ImageField(upload_to='events_image/', blank=True)
    
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Evenement : {self.title}"
    
    def file_exists(self):
        if self.file:
            return os.path.exists(settings.MEDIA_ROOT / str(self.file))
        return False
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        if self.photo and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.photo))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.photo)))
        
        # Supprimer l'objet
        super(Event, self).delete(*args, **kwargs)


class EventParticipate(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    
    start_hours = models.CharField(max_length=20, choices=hours_of_the_day)
    
    end_hours = models.CharField(max_length=20, choices=hours_of_the_day)
    
    amount = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)



class Group(models.Model):
    
    title = models.CharField(max_length=20)
    
    career = models.ForeignKey(Career, on_delete=models.CASCADE,null=True, blank=True)
    
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    

class DiscussionGroup(models.Model):
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class GroupMessage(models.Model):
    
    discussion_group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class GroupMedia(models.Model):
    
    discussion_group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, blank=True, null=True)
    
    legend = models.CharField(max_length=60, blank=True)
    
    file = models.FileField(upload_to='group_media')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="contacts", blank=True, null=True)
    
    can_discuss_with = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="can_be_discussed_with", blank=True, null=True)
    
    is_friend = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class StudentDiscussion(models.Model):
    
    content = models.TextField()
    
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_discussions")
    
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="received_discussions")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class StudentDiscussionMedia(models.Model):
    
    legend = models.TextField(blank=True)
    
    file = models.FileField(upload_to='student_media')
    
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_media")
    
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="received_media")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)