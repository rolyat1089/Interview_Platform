from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from interviewQuiz.models import InterviewTest, InterviewTestAttempt
from rest_framework.response import Response
from interviewQuiz.serializers import *
from login.models import Account
import pytz
from django.utils import timezone
from login.serializers import StudSerializer
# Create your views here.


utc = pytz.UTC
#for both interviewer and interviewee if we want to see all the tests after login, this call is used. 
class TestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            if cuser.is_candidate == True and cuser.is_assessor == False and InterviewTest.objects.filter(accounts = cuser).exists() == True:
                Tests = InterviewTest.objects.filter(accounts = cuser)
                FilteredTests = []
                for inditests in Tests:
                    tnow = timezone.now()
                    dtime = inditests.DisplayTime
                    etime = inditests.EndTime
                    if tnow >= dtime and tnow <= etime:
                        FilteredTests.append(inditests)
                serializedTests = TestSerializer(FilteredTests, many = True)
                AttemptData = []
                for test in FilteredTests:
                    if InterviewTestAttempt.objects.filter(accounts = cuser, Test = test).exists() == True:
                        Cattempt = InterviewTestAttempt.objects.filter(accounts = cuser, Test = test)[0]
                        AttemptData.append(Cattempt)
                serializedAttemptData = InterviewTestAttemptSerializer(AttemptData, many = True)
                ResponseData = {
                    'TestData' : serializedTests.data,
                    'AttemptData' : serializedAttemptData.data,
                }
                return Response(data = ResponseData, status = 200)
            elif cuser.is_candidate == False and cuser.is_assessor == True:
                Tests = InterviewTest.objects.filter(accounts = cuser)
                serializedTests = TestSerializer(Tests, many = True)
                return Response(data = serializedTests.data, status = 200)
            elif cuser.is_candidate == True and cuser.is_assessor == False and InterviewTest.objects.filter(accounts = cuser).exists() == False:
                return Response(data = "NO test assigned to user", status = 400)
            else:
                return Response(data = "User Type Wrong", status = 400)
                
        else:
            return Response(data = "User does not exist", status = 400)


class TestAttemptFlag(APIView):
    permission_classes = [IsAuthenticated]
    #this post request needs to be made at the start of the exam. 
    def post(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            TestData = {
                    'test_id' : request.data.get('test_id', None),
                }
            SerializedTestData = TestInputSerializer(data = TestData)
            if SerializedTestData.is_valid():
                testId = SerializedTestData.validated_data['test_id']
                if InterviewTest.objects.filter(id = testId).exists() == True and cuser.is_assessor == False and cuser.is_candidate == True:
                    CTest = InterviewTest.objects.filter(id = testId)[0]
                    SerializedTest = TestSerializer(CTest)
                    if InterviewTestAttempt.objects.filter(Test = CTest, accounts = cuser).exists() == False:
                        AttemptObject =  InterviewTestAttempt.objects.create(
                           Test = CTest, 
                           accounts = cuser,
                           Attempted = True
                        )
                        AttemptStartTime = AttemptObject.StartTime
                        
                        Detail = {
                            'AttemptStartTime': AttemptStartTime,
                            'TestData' : SerializedTest.data,
                        }
                        return Response(data = Detail, status = 200)
                    else:
                        AttemptObject = InterviewTestAttempt.objects.filter(Test = CTest, accounts = cuser)[0]
                        AttemptStartTime = AttemptObject.StartTime
                        Detail = {
                            'AttemptStartTime': AttemptStartTime,
                            'TestData' : SerializedTest.data,
                        }
                        return Response(data = Detail, status = 200)
                else:
                    return Response(data = "Test id passed is wrong", status = 400)
            else:
                return Response(data = SerializedTestData.errors, status = 404)
        else:
            return Response(data = "Cuser does not exist", status = 404)


class TestEndFlag(APIView):
        permission_classes = [IsAuthenticated]
        #needs to be called at the end of the test. 
        def post(self, request, *args, **kwargs):
            cuser = request.user
            if cuser != None:
                TestData = {
                'test_id' : request.data.get('test_id', None),
            }
                SerializedTestData = TestInputSerializer(data = TestData)
                if SerializedTestData.is_valid():
                    testId = SerializedTestData.validated_data['test_id']
                    if cuser.is_candidate == True and cuser.is_assessor == False:
                        if InterviewTest.objects.filter(id = testId).exists() == True:
                            CTest = InterviewTest.objects.filter(id = testId)[0]
                            if InterviewTestAttempt.objects.filter(Test = CTest, accounts = cuser).exists()== True:
                                CTestAttempt = InterviewTestAttempt.objects.filter(Test = CTest, accounts = cuser)[0]
                                CTestAttempt.Finished = True
                                CTestAttempt.save()
                                return Response(data = "Test Finished ", status = 200)
                            else:
                                return Response(data = "Something Is wrong", status=300)
                                #immediately log out the user
                        else:
                            return Response(data = "Test Id passes is wrong", status = 400)
                    else:
                        return Response(data = "Limited Access", status = 400)
                else:
                    return Response(data = SerializedTestData.errors, status = 404)
            else:
                return Response(data = "Cuser does not exist", status = 404)



class StudsViewForProf(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            TestData = {
                'test_id' : request.data.get('test_id', None),
            }
            SerializedTestData = TestInputSerializer(data = TestData)
            if SerializedTestData.is_valid():
                testId = SerializedTestData.validated_data['test_id']
                if cuser.is_candidate == False and cuser.is_assessor == True:
                    if InterviewTest.objects.filter(id = testId).exists() == True:
                        CTest = InterviewTest.objects.filter(id = testId)[0]
                        users = CTest.accounts.all()
                        filteredusers = []
                        for specuser in users:
                            if specuser.is_assessor == False and specuser.is_candidate == True:
                                filteredusers.append(specuser)
                        SerializedUsers = StudSerializer(filteredusers, many = True)
                        SerilizedTest = TestSerializer(CTest)
                        data = {
                            'users' : SerializedUsers.data, 
                            'test_Details' : SerilizedTest.data,  
                        }
                        return Response(data = data, status = 200)
                    else:
                        return Response(data = "Wrong Test Id Passed ", status = 300)
                else:
                    return Response(data = "User Type Wrong", status = 400)
            else:
                return Response(data = SerializedTestData.errors, status = 404)
        else:
            return Response(data = "Cuser does not exist", status = 404)



#************************ALL the classes written below are for admin panel, have not yet been used in the frontend code, hence have been commented. 

# class ViewTestsAdmin(APIView):    
#     permission_classes = [IsAuthenticated]
#     #this view is to display a list of all the tests to the admin.
#     def get(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             if cuser.is_admin == True:
#                 Tests = InterviewTest.objects.all()
#                 serializedTests = TestSerializerAdmin(Tests, many = True)
#                 return Response(data = serializedTests.data, status = 200)
#             else:
#                 return Response(data = "Access Denied", status = 300)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)


#     #this view is to delte a particular test. 
#     def delete(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             TestData = {
#                 'test_id' : request.data.get('test_id', None),
#             }
#             SerializedTestData = TestInputSerializer(data = TestData)
#             if SerializedTestData.is_valid():
#                 testId = SerializedTestData.validated_data['test_id']
#                 if cuser.is_admin == True:
#                     if InterviewTest.objects.filter(id = testId).exists() == True:
#                         InterviewTest.objects.filter(id = testId)[0].delete()
#                         return Response(data = "Test Deleted Successfully", status = 200)
#                     else:
#                         return Response(data = "Wrong Test Id Passed ", status = 400)
#                 else:
#                     return Response(data = "Access Denied", status = 300)
#             else:
#                 return Response(data = SerializedTestData.errors, status = 404)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)


#      #TODO: Find way to append user list.         
#     def put(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             TestIdData = {
#                 'test_id' : request.data.get('test_id', None),
#             }
#             SerializedTestIdData = TestInputSerializer(data = TestIdData)
#             if SerializedTestIdData.is_valid():
#                 testId = SerializedTestIdData.validated_data['test_id']
#                 TestData = {
#                     'display_time': request.data.get('display_time', None),
#                     'end_time': request.data.get('end_time', None),
#                     'title': request.data.get('title', None),
#                     'instructions': request.data.get('instructions', None), 
#                     'test_time': request.data.get('test_time', None),
#                 }
#                 SerializedTestData = TestDataSerializer(data = TestData)
#                 if SerializedTestData.is_valid():
#                     displayTime = SerializedTestData.validated_data['display_time']
#                     endTime = SerializedTestData.validated_data['end_time']
#                     title = SerializedTestData.validated_data['title']
#                     instructions = SerializedTestData.validated_data['instructions']
#                     testTime = SerializedTestData.validated_data['test_time']
#                     # userList = request.data['user_list']
#                     if cuser.is_admin == True:
#                         if InterviewTest.objects.filter(id = testId).exists() == True:
#                             CTest = InterviewTest.objects.filter(id = testId)[0]
#                             CTest.DisplayTime = displayTime
#                             CTest.EndTime = endTime
#                             CTest.Title = title
#                             CTest.Instructions = instructions
#                             CTest.TestTime = testTime
#                             CTest.save()
#                             # compare the user lists and assign the new list. 
#                             return Response(data = "Test Updated Successfully", status = 200)        
#                         else:
#                             return Response(data = "Wrong Test id passed", status = 400)
#                     else:
#                         return Response(data = "Access Denied", status = 300)
#                 else:
#                     return Response(data = SerializedTestData.errors, status = 404)
#             else:
#                 return Response(data = SerializedTestIdData.errors, status = 404)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)

# class CreateTestsAdmin(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         #this call just gives a list of all the interviewers and interwees registered on the platform. 
#         #so that we can assign them to a test while creating.
#         cuser = request.user
#         if cuser != None:
#             if cuser.is_admin == True:
#                 UserList = Account.objects.filter(is_admin = False)
#                 serializedUser = UserSerializer(UserList, many = True)
#                 return Response(data = serializedUser.data, status=200)
#             else:
#                 return Response(data = "Access Denied", status = 300)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)

#     #this call is to create a new test. 
#     def post(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             TestData = {
#                 'display_time': request.data.get('display_time', None),
#                 'end_time': request.data.get('end_time', None),
#                 'title': request.data.get('title', None),
#                 'instructions': request.data.get('instructions', None), 
#                 'test_time': request.data.get('test_time', None),
#             }
#             SerializedTestData = TestDataSerializer(data = TestData)
#             if SerializedTestData.is_valid():
#                 displayTime = SerializedTestData.validated_data['display_time']
#                 endTime = SerializedTestData.validated_data['end_time']
#                 title = SerializedTestData.validated_data['title']
#                 instructions = SerializedTestData.validated_data['instructions']
#                 testTime = SerializedTestData.validated_data['test_time']
#                 userList = request.data.get('user_list', None)   
#                 #basically we are sending the email addresses of the users back. 
#                 #TODO: we need to check the input of the user list also. 
#                 if cuser.is_admin == True:
#                     CTest = InterviewTest.objects.create(
#                         DisplayTime = displayTime, 
#                         EndTime = endTime, 
#                         Title = title, 
#                         Instructions = instructions, 
#                         TestTime = testTime, 
#                     )
#                     for users in userList:
#                         if Account.objects.filter(email = users).exists() == True:
#                             cstud = Account.objects.filter(email = users)[0]
#                             CTest.accounts.add(cstud)
#                     return Response(data = "Test Created Successfully", status = 200)        
#                 else:
#                     return Response(data = "Access Denied", status = 300)
#             else:
#                 return Response(data = SerializedTestData.errors, status = 404)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)

# class CreateQuestionsAdmin(APIView):
#     permission_classes = [IsAuthenticated]
#     #this call is to create a new question for a particular test. 
#     def post(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             TestData = {
#                 'test_id' : request.data.get('test_id', None),
#             }
#             SerializedTestData = TestInputSerializer(data = TestData)
#             if SerializedTestData.is_valid():
#                 # testId = request.data.get('test_id', None)
#                 testId = SerializedTestData.validated_data['test_id']
#                 QuestionData = {
#                     'question_name': request.data.get('question_name', None),
#                     'question': request.data.get('question', None),
#                     'question_time': request.data.get('question_time', None),
#                     'max_marks': request.data.get('max_marks', None)
#                 }
#                 SerializedQuestionData = QuestionDataSerializer(data = QuestionData)
#                 if SerializedQuestionData.is_valid():
#                     questionName =  SerializedQuestionData.validated_data['question_name']
#                     question =  SerializedQuestionData.validated_data['question']
#                     questionTime = SerializedQuestionData.validated_data['question_time']
#                     maxMarks = SerializedQuestionData.validated_data['max_marks']
#                     if cuser.is_admin == True:
#                         if InterviewTest.objects.filter(id = testId).exists() == True:
#                             CTest = InterviewTest.objects.filter(id = testId)[0]
#                             CQuestion = InterViewQuestions.objects.create(
#                                 Test = CTest, 
#                                 QuestionName = questionName,
#                                 Question = question, 
#                                 QuestionTime = questionTime, 
#                                 Maxmarks = maxMarks
#                             )
#                             TestUserList = CTest.accounts.all()
#                             FilteredUserList = []
#                             for specuser in TestUserList:
#                                 if specuser.is_candidate == True and specuser.is_assessor == False:
#                                     FilteredUserList.append(specuser)
#                             for CStud in FilteredUserList:
#                                 if Marksmodel.objects.filter(questions = CQuestion, accounts = CStud).exists() == False:
#                                     CMarksObject = Marksmodel.objects.create(
#                                         questions = CQuestion, 
#                                         accounts = CStud, 
#                                     )
#                             return Response(data = "Successfully added question", status = 200)                
#                         else:
#                             return Response(data = "Test ID passed is wrong" , status = 300)
#                     else:
#                         return Response(data = "Access Denied", status = 400)
#                 else:
#                     return Response(data = SerializedQuestionData.errors, satus = 400)
#             else:
#                 return Response(data = SerializedTestData.errors, status = 400)
#         else:
#             return Response(data = "Cuser does not exist", status=400)


#     #this call is to get all the questions for a particular test.         
#     def get(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             TestData = {
#                 'test_id' : request.data.get('test_id', None),
#             }
#             SerializedTestData = TestInputSerializer(data = TestData)
#             if SerializedTestData.is_valid():
#                 # testId = request.data.get('test_id', None)
#                 testId = SerializedTestData.validated_data['test_id']
#                 if cuser.is_admin == True:
#                     if InterviewTest.objects.filter(id = testId).exists() == True:
#                         CTest = InterviewTest.objects.filter(id = testId)[0]
#                         QuestionList = InterViewQuestions.objects.filter(Test = CTest)
#                         SerializedQuestions = SpecQuestionSerializer(QuestionList, many = True)
#                         return Response(data = SerializedQuestions.data, status = 200)
#                     else:
#                         return Response(data = "Test ID passed is wrong" , status = 300)
#                 else:
#                     return Response(data = "Access Denied", status = 400)
#             else:
#                 return Response(data = SerializedTestData.errors, status = 404)
#         else:
#             return Response(data = "Cuser does not exist", status = 400)

#     #this is to append a particular question for a particular test. 
#     def put(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             QuestionIdData = {
#                 'question_id' : request.data.get('question_id', None)
#             }
#             SerializedQuestionId = QuestionInputSerializer(data = QuestionIdData)
#             if SerializedQuestionId.is_valid():
#                 questionId = SerializedQuestionId.validated_data['question_id'] 
#                 # questionName = request.data.get('question_name', None)
#                 # question = request.data.get('question', None)
#                 # questionTime = request.data.get('question_time', None)
#                 # maxMarks = request.data.get('max_marks', None)
#                 QuestionData = {
#                     'question_name': request.data.get('question_name', None),
#                     'question': request.data.get('question', None),
#                     'question_time': request.data.get('question_time', None),
#                     'max_marks': request.data.get('max_marks', None)
#                 }
#                 SerializedQuestionData = QuestionDataSerializer(data = QuestionData)
#                 if SerializedQuestionData.is_valid():
#                     questionName =  SerializedQuestionData.validated_data['question_name']
#                     question =  SerializedQuestionData.validated_data['question']
#                     questionTime = SerializedQuestionData.validated_data['question_time']
#                     maxMarks = SerializedQuestionData.validated_data['max_marks']
#                     if cuser.is_admin == True:
#                         if InterViewQuestions.objects.filter(id = questionId).exists() == True:
#                             CQuestion = InterViewQuestions.objects.filter(id = questionId)[0]
#                             CQuestion.QuestionName = questionName,
#                             CQuestion.Question = question, 
#                             CQuestion.QuestionTime = questionTime, 
#                             CQuestion.MaxMarks = maxMarks, 
#                             CQuestion.save()
#                             return Response(data = "Successfully updated question", status = 200)
#                         else:
#                             return Response(data = "Wrong Question ID passed", status = 300)
#                     else:
#                         return Response(data = "Access Denied", status = 400)
#                 else:
#                     return Response(data = SerializedQuestionData.errors, status = 404)
#             else:
#                 return Response(data = SerializedQuestionId.errors, status = 404)
#         else:
#             return Response(data = "cuser does not exist", status = 404)
            
#     #this call is to delete a particular questtion. 
#     def delete(self, request, *args, **kwargs):
#         cuser = request.user
#         if cuser != None:
#             QuestionData = {
#                 'question_id' : request.data.get('question_id', None),
#             }
#             SerializedQuestionData = QuestionInputSerializer(data = QuestionData)
#             if SerializedQuestionData.is_valid():
#                 # questionId = request.data.get('question_id', None)
#                 questionId = SerializedQuestionData.validated_data['question_id']
#                 if cuser.is_admin == True:
#                     if InterViewQuestions.objects.filter(id = questionId).exists() == True:
#                         InterViewQuestions.objects.filter(id = questionId)[0].delete()
#                         return Response(data = "Question Deleted Successfully", status = 200)
#                     else:
#                         return Response(data = "Wrong Question ID passed", status = 300)
#                 else:
#                     return Response(data = "Access Denied", status = 400)
#             else:
#                 return Response(data = SerializedQuestionData.errors, status = 404)
#         else:
#             return Response(data = "Cuser does not exist", status = 404)




