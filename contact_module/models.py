from django.db import models


class ContactSubjectItem(models.Model):
    subject_item=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subject_item


class ContactModel(models.Model):
    name=models.CharField(max_length=127)
    email=models.EmailField()
    subject=models.ForeignKey(ContactSubjectItem, on_delete=models.SET_NULL, null=True, blank=False)
    text=models.TextField(blank=False,null=True)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.subject}'
    

class UserEmailForNews(models.Model):
    email=models.EmailField()

    def __str__(self):
        return self.email