from django.db                  import models
from account.models   import Account

class Comment(models.Model):
    account     = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    username    = models.CharField(max_length=200, null=True)
    content     = models.TextField()
    created_time= models.DateTimeField(auto_now_add = True)
    updated_time= models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'comments'
    
    def __str__(self):
        return self.username + ": " + self.content