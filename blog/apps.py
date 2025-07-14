from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
<<<<<<< HEAD
=======
    
    def ready(self):
        import blog.signals
>>>>>>> main
