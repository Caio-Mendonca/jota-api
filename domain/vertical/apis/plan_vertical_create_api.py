from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from domain.vertical.actions import  plan_vertical_create
from domain.plan.models import Plan
from domain.vertical.models import Vertical
from domain.vertical.serializers import  CreatePlanVerticalSerializer, PlanVerticalOutputSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Cria uma realação entre plano X vertical",
    tags=["Verticais"],
    request=CreatePlanVerticalSerializer,
    responses={201: None},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def plan_vertical_create_api(request):
    serializer = CreatePlanVerticalSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    plan_id = request.data.get("plan_id")
    vertical_id = request.data.get("vertical_id")
    try:
        plan = Plan.objects.get(id=plan_id)
        vertical = Vertical.objects.get(id=vertical_id)
    except (Plan.DoesNotExist, Vertical.DoesNotExist):
        return Response({"detail": "Invalid plan_id or vertical_id."}, status=status.HTTP_404_NOT_FOUND)

    relation = plan_vertical_create(plan=plan, vertical=vertical, user=request.user)
    serializer = PlanVerticalOutputSerializer(relation) 

    return Response(serializer.data, status=status.HTTP_201_CREATED)