from meters.utils import  SingletonCache


def get_meters_context( request ):
    # передача во все шаблоны автоматом
    # ss = SelectionSingleton()
    # menu = ss.get_menu()
    menu = SingletonCache.get_menu()
    return {'mainmenu': menu}