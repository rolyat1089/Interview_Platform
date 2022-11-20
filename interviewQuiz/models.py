from django.db import models
from login.models import Account
# Create your models here.



class InterviewTest(models.Model):
    id = models.BigAutoField(primary_key=True)
    DisplayTime = models.DateTimeField(blank=True)
    EndTime = models.DateTimeField(blank=True)
    Title = models.CharField(max_length=300)
    Instructions = models.TextField(default=" ")
    TestTime = models.IntegerField(default=0)
    TestImage = models.URLField(default=" ")
    accounts = models.ManyToManyField(Account)

    def __str__(self) -> str:
        return str(self.Title)


                    


class InterviewTestAttempt(models.Model):
    Test = models.ForeignKey(InterviewTest, on_delete=models.CASCADE)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)
    StartTime = models.DateTimeField(auto_now_add=True)
    Attempted = models.BooleanField(default=False)
    Finished = models.BooleanField(default=False)


    class Meta:
        unique_together = [['Test', 'accounts']]
    def __str__(self) -> str:
        return str(str(self.Test) + " || " + str(self.accounts)) 


