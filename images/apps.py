from django.apps import AppConfig


'''In order to register your signal receiver functions, when you use the receiver()
decorator, you just need to import the signals module of your application inside
the ready() method of the application configuration class. This method is called
as soon as the application registry is fully populated'''

class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # import signal handlers
        import images.signals

'''You import the signals for this application in the ready() method so that they are
imported when the images application is loaded.'''