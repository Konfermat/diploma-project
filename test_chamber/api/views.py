from django.db.models import Prefetch
from rest_framework import viewsets
from .models import Step, StepElement, TestElement, TestOption
from .serializers import StepDetailSerializer

# сделай сам

class StepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepDetailSerializer

    def get_queryset(self):
        test_prefetch = Prefetch(
            'test_content__options',
            queryset=TestOption.objects.all()
        )
        
        elements_prefetch = Prefetch(
            'elements',
            queryset=StepElement.objects.select_related('text_content', 'test_content').prefetch_related(test_prefetch)
        )
        
        return Step.objects.prefetch_related(elements_prefetch)
