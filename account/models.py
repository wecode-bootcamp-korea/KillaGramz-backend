from django.db                      import models

class Account(models.Model):
    email       = models.EmailField(max_length = 254, null=True)
    password    = models.CharField(max_length=700)
    fullname    = models.CharField(max_length=200)
    username    = models.CharField(max_length=200)
    phone       = models.CharField(max_length=100, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.username + " " + self.fullname + " " + str(self.email) + " " + str(self.phone)