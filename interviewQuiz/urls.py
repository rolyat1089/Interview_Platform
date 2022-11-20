from django.urls import path
from interviewQuiz.views import *

urlpatterns = [
    path('TestView/', TestView.as_view(), name = 'TestView'),  
    path('TestFlag/', TestAttemptFlag.as_view(), name = "Attempt Flag"),
    path('TestEndFlag/', TestEndFlag.as_view(), name = "Test end"), 
    path('SpecTestProf/', StudsViewForProf.as_view(), name = "Particular Test Students"),  

    # path('ViewTestsAdmin/', ViewTestsAdmin.as_view(), name = "Admin tests"),  
    # path('CreateTestsAdmin/', CreateTestsAdmin.as_view(), name = "Create Tests"),  
    # path('TestQuestionsAdmin/', CreateQuestionsAdmin.as_view(), name = "Test questions Admin"), 
    
]
