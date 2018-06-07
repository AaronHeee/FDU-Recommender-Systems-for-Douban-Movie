# coding=utf8


from django.conf.urls import url

from demo import frontend_views, backend_views

urlpatterns = [
    url(r'^$', frontend_views.IndexView.as_view(), name='index'),
    url(r'^frontend_charts_list/$', frontend_views.FrontendEchartsTemplate.as_view(), name='frontend_demo'),
    url('^backend_charts_list/$', backend_views.BackendEChartsTemplate.as_view(), name='backend_demo'),

    url(r'multiple/Page/', backend_views.PageDemoView.as_view(), name='page_demo'),
    url(r'multiple/NamedCharts/', backend_views.NamedChartsView.as_view(), name='namedcharts_demo'),
    url(r'^demo/temperature/', backend_views.TemperatureEChartsView.as_view()),

    # Options Json for frontend views
    url(r'options/simpleBar/', frontend_views.SimpleBarView.as_view()),
    url(r'options/simpleKLine/', frontend_views.SimpleKLineView.as_view()),
    url(r'options/simpleMap/', frontend_views.SimpleMapView.as_view()),
    url(r'options/simplePie/', frontend_views.SimplePieView.as_view()),
    url(r'options/wordCloud/', frontend_views.WordCloudView.as_view()),
]
