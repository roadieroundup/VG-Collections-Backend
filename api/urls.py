from django.urls import path

from . import auth_controller, game_controller, vglist_controller

# zagaz: qwerty123

urlpatterns = [

    path('auth/create', auth_controller.create_user, name='auth_create'),
    path('auth/login', auth_controller.login_user, name='auth_login'),
    path('auth/update/<str:pk>', auth_controller.update_profile, name='auth_update'),
    path('auth/logout', auth_controller.logout_user, name='auth_logout'),
    path('auth/renew', auth_controller.renew_token, name='auth_renew'),
    path('auth/delete/<str:pk>', auth_controller.delete_user, name='auth_delete'),
    ##############################
    path('profile/<str:pk>', auth_controller.get_profile_info, name='profile_get'),
    ##############################
    path('games/home', game_controller.games_home, name='games_home'),
    path('games/search', game_controller.search_results, name='games_search'),
    ##############################
    path('vglist/create', vglist_controller.create_vglist, name='vglist_create'),
    path('vglist/<str:pk>', vglist_controller.get_vglist, name='vglist_get'),
    path('vglist/all/<str:pk>', vglist_controller.get_all_user_vglists,
         name='vglist_get_all'),
    path('vglist/update/<str:pk>',
         vglist_controller.update_vglist, name='vglist_update'),
    path('vglist/delete/<str:pk>',
         vglist_controller.delete_vglist, name='vglist_delete'),
]
