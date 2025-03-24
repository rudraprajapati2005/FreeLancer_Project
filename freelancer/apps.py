from django.apps import AppConfig


class FreelancerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "freelancer"

    def ready(self):
        # Import the template tags module to register the filters
        import freelancer.templatetags.custom_filters
