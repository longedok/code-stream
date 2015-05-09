from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'streams', views.StreamsViewset)
router.register(r'technologies', views.TechnologyViewSet)
router.register(r'series', views.SeriesViewSet)
router.register(r'materials', views.MaterialViewSet)

urlpatterns = router.urls