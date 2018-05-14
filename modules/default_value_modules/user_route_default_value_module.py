import models.app_models.user_route_models.user_route_model as user_route_model

#получаем дефолтные значения по роутам для разработчика
def get_default_routes_for_developer():
    default_route_model = user_route_model.UserRoutes(True,True,True,False,True,False,True,True,True,True)
    return default_route_model


#получаем дефолтные значения по роутам для администратора системы
def get_default_routes_for_administrator():
    default_route_model = user_route_model.UserRoutes(True,False,False,True,False,True,True,True,True,True)
    return default_route_model

#получаем дефолтные значения по роутам для настройщика системы
def get_default_routes_for_master():
    default_route_model = user_route_model.UserRoutes(True,False,False,True,False,False,True,True,False,False)
    return default_route_model

#получаем дефолтные значения по роутам для пользователя
def get_default_routes_for_user():
    default_route_model = user_route_model.UserRoutes(True,False,False,False,False,False,True,True,False,False)
    return default_route_model
