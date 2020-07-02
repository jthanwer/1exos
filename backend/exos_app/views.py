from rest_framework.decorators import api_view
from rest_framework.response import Response
import core.constants as cst


@api_view()
def fetch_constants(request):
    return Response({
        "START_POINTS": cst.START_POINTS,
        "CHANGE": cst.CHANGE,
        "BONUS": cst.BONUS,
        "SELFCORREC_POINTS": cst.SELFCORREC_POINTS,
        "DEADLINE_POINTS": cst.DEADLINE_POINTS,
        "MULTIPLECORREC_POINTS": cst.MULTIPLECORREC_POINTS,
        "MEAN_PRICES": cst.MEAN_PRICES,
    })

# class IndexTemplateView(LoginRequiredMixin, TemplateView):
# class IndexTemplateView(TemplateView):
#     def get_template_names(self):
#         if settings.DEBUG:
#             template_name = 'index_dev.html'
#         else:
#             template_name = 'index.html'
#         return template_name



