from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsStaffOrReadOnly

from . import services
from .models import Toy, ToyStatusLog
from .serializers import ToySerializer, ToyStatusLogSerializer, ToyTransitionSerializer


class ToyViewSet(viewsets.ModelViewSet):
    serializer_class = ToySerializer
    queryset = Toy.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status", "make", "condition", "source"]
    search_fields = ["model_name", "make", "description", "barcode_or_sku"]

    @action(detail=True, methods=["post"])
    def transition(self, request, pk=None):
        toy = self.get_object()
        serializer = ToyTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            toy = services.transition_toy_status(
                toy,
                serializer.validated_data["new_status"],
                actor=request.user,
                reason=serializer.validated_data.get("reason", ""),
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(self.get_serializer(toy).data)

    @action(detail=True, methods=["get"], url_path="status-log")
    def status_log(self, request, pk=None):
        toy = self.get_object()
        logs = toy.status_logs.all()
        return Response(ToyStatusLogSerializer(logs, many=True).data)
