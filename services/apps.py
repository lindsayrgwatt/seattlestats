from django.apps import AppConfig
import logging

log = logging.getLogger(__name__)

class MyAppConfig(AppConfig):
    name = "services"
    verbose_name = "Seattle Services"

    def ready(self):
        
        print "The app services is configured"
        log.info("The app services is now configured")