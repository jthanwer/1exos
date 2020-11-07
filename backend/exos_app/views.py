from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import core.constants as cst


@api_view()
@permission_classes([AllowAny])
def fetch_constants(request):
    return Response({
        "START_POINTS": cst.START_POINTS(),
        "CHANGE": cst.CHANGE(),
        "BONUS": cst.BONUS(),
        "SELFCORREC_POINTS": cst.SELFCORREC_POINTS(),
        "DEADLINE_POINTS": cst.DEADLINE_POINTS(),
        "MULTIPLECORREC_POINTS": cst.MULTIPLECORREC_POINTS(),
        "MEAN_PRICES": cst.MEAN_PRICES(),
        "MAX_PRICES": cst.MAX_PRICES(),
    })



