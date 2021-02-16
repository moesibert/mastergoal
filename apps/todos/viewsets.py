from rest_framework.decorators import action
from rest_framework.renderers import HTMLFormRenderer
from rest_framework.response import Response
from apps.todos.serializers import ToDoSerializer, NormalToDoSerializer, RepetitiveToDoSerializer, \
    NeverEndingToDoSerializer, PipelineToDoSerializer, RepetitiveToDoSerializerWithoutPrevious, \
    PipelineToDoSerializerWithoutPrevious, NeverEndingToDoSerializerWithoutPrevious
from apps.todos.models import ToDo, NormalToDo, RepetitiveToDo, NeverEndingToDo, PipelineToDo
from apps.todos.utils import get_todo_in_its_proper_class
from rest_framework import viewsets, permissions


class FormAction:
    @action(detail=True, methods=['get'])
    def form(self, request, pk):
        instance = self.get_object()
        renderer = HTMLFormRenderer()
        renderer.template_pack = 'rest_framework/horizontal/'
        form = renderer.render(self.get_serializer(instance).data)
        data = {
            'form': form
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def createform(self, request):
        renderer = HTMLFormRenderer()
        renderer.template_pack = 'rest_framework/horizontal/'
        form = renderer.render(self.get_serializer().data)
        data = {
            'form': form
        }
        return Response(data)


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(instance) == NormalToDo:
            serializer = NormalToDoSerializer(instance, context={'request': request})
        elif type(instance) == RepetitiveToDo:
            serializer = RepetitiveToDoSerializer(instance, context={'request': request})
        elif type(instance) == NeverEndingToDo:
            serializer = NeverEndingToDoSerializer(instance, context={'request': request})
        elif type(instance) == PipelineToDo:
            serializer = PipelineToDoSerializer(instance, context={'request': request})
        else:
            raise Exception('No serializer was found.')
        return Response(serializer.data)

    def get_object(self):
        obj = super().get_object()
        obj = get_todo_in_its_proper_class(obj.pk)
        return obj

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user,
            ToDo,
            'ALL',
            include_archived_to_dos=True
        )

    def list(self, request, *args, **kwargs):
        normal_to_dos = ToDo.get_to_dos_user(
            self.request.user, NormalToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        normal_to_dos_serializer = NormalToDoSerializer(normal_to_dos, many=True, context={'request': request})

        repetitive_to_dos = ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        repetitive_to_dos_serializer = RepetitiveToDoSerializerWithoutPrevious(repetitive_to_dos, many=True,
                                                                               context={'request': request})
        never_ending_to_dos = ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        never_ending_to_dos_serializer = NeverEndingToDoSerializerWithoutPrevious(never_ending_to_dos, many=True,
                                                                                  context={'request': request})
        pipeline_to_dos = ToDo.get_to_dos_user(
            self.request.user, PipelineToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        pipeline_to_dos_serializer = PipelineToDoSerializerWithoutPrevious(pipeline_to_dos, many=True,
                                                                           context={'request': request})
        data = (
                normal_to_dos_serializer.data +
                repetitive_to_dos_serializer.data +
                never_ending_to_dos_serializer.data +
                pipeline_to_dos_serializer.data
        )
        return Response(data)


class NormalToDoViewSet(FormAction, viewsets.ModelViewSet):
    serializer_class = NormalToDoSerializer
    queryset = NormalToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NormalToDo, 'ALL',
            include_archived_to_dos=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, NormalToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RepetitiveToDoViewSet(FormAction, viewsets.ModelViewSet):
    serializer_class = RepetitiveToDoSerializer
    queryset = RepetitiveToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo, 'ALL',
            include_archived_to_dos=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, RepetitiveToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NeverEndingToDoViewSet(FormAction, viewsets.ModelViewSet):
    serializer_class = NeverEndingToDoSerializer
    queryset = NeverEndingToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo, 'ALL',
            include_archived_to_dos=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, NeverEndingToDo, 'ALL',
            include_archived_to_dos=request.user.show_archived_objects
        ).prefetch_related('next')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PipelineToDoViewSet(FormAction, viewsets.ModelViewSet):
    serializer_class = PipelineToDoSerializer
    queryset = PipelineToDo.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.get_to_dos_user(
            self.request.user, PipelineToDo, 'ALL',
            include_archived_to_dos=True
        )

    def list(self, request, *args, **kwargs):
        queryset = ToDo.get_to_dos_user(
            self.request.user, PipelineToDo, 'ALL',
            include_archived_to_dos=self.request.user.show_archived_objects
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
