from rest_framework import viewsets ,generics
from questions.models import Question , Answer
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from questions.api.serializers import QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated
from questions.api.permission import IsAuthorOrReadOnly

class QuestionViewSet(viewsets.ModelViewSet):
     queryset = Question.objects.all().order_by("-created_at")
     serializer_class = QuestionSerializer
     permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
     lookup_field = "slug"

     def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
   
    def perform_create(self,serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question,slug=kwarg_slug)
        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question")
        serializer.save(author = request_user,question=question)



class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
    lookup_field = "uuid"



class AnswerListAPIView(generics.ListAPIView):
    serializer_class =AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug = kwarg_slug).order_by("-created_at")