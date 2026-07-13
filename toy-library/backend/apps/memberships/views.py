from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsStaff

from . import services
from .models import Membership, MembershipTier
from .serializers import (
    ChangeTierSerializer,
    MembershipSerializer,
    MembershipSignupSerializer,
    MembershipTierSerializer,
    SignOffSerializer,
)


class MembershipTierListView(generics.ListAPIView):
    serializer_class = MembershipTierSerializer
    permission_classes = [permissions.AllowAny]
    queryset = MembershipTier.objects.filter(is_active=True)


class MyMembershipView(generics.RetrieveAPIView):
    serializer_class = MembershipSerializer

    def get_object(self):
        membership = (
            Membership.objects.select_related("tier")
            .filter(user=self.request.user)
            .order_by("-created_at")
            .first()
        )
        if membership is None:
            from rest_framework.exceptions import NotFound

            raise NotFound("No membership found for this user")
        return membership


class MembershipSignupView(generics.GenericAPIView):
    serializer_class = MembershipSignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            membership = services.signup_membership(request.user, serializer.validated_data["tier_code"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(MembershipSerializer(membership).data, status=201)


class MembershipViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        qs = Membership.objects.select_related("tier").order_by("-created_at")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ("activate", "signoff"):
            return [IsStaff()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        membership = self.get_object()
        try:
            membership = services.activate_membership(membership, request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(MembershipSerializer(membership).data)

    @action(detail=True, methods=["post"], url_path="change-tier")
    def change_tier(self, request, pk=None):
        membership = self.get_object()
        serializer = ChangeTierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_tier = MembershipTier.objects.get(
                code=serializer.validated_data["new_tier_code"], is_active=True
            )
        except MembershipTier.DoesNotExist:
            return Response({"detail": "No active membership tier with that code"}, status=400)
        try:
            membership = services.change_tier(membership, new_tier, request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(MembershipSerializer(membership).data)

    @action(detail=True, methods=["post"])
    def signoff(self, request, pk=None):
        membership = self.get_object()
        serializer = SignOffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            sign_off = services.process_signoff(
                membership,
                request.user,
                serializer.validated_data["amount_returned"],
                serializer.validated_data.get("reason", ""),
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        from .serializers import MembershipSignOffSerializer

        return Response(MembershipSignOffSerializer(sign_off).data)
