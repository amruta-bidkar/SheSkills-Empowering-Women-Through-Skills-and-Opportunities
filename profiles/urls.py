from django.urls import path
from . import views


urlpatterns = [

    path(
        'create/',
        views.create_profile,
        name='create_profile'
    ),

    path(
        'my-profile/',
        views.my_profile,
        name='my_profile'
    ),

    path(
        'edit/',
        views.edit_profile,
        name='edit_profile'
    ),
path(
        'add-skill/',
        views.add_skill,
        name='add_skill'
),
path(
    'add-portfolio/',
    views.add_portfolio,
    name='add_portfolio'
),
path(
        'marketplace/',
        views.marketplace,
        name='marketplace'
),

path(
    'provider/<int:provider_id>/',
    views.provider_detail,
    name='provider_detail'
),

]