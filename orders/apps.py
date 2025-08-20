from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        """
        Override the ready() method to perform initialization at app startup time.
        
        This is where you can put initialization code that needs to run after all
        models are loaded.
        
        In this case, the orders app hooks into the post_save signal of the OrderItem
        model and into the post_delete signal of the OrderItem model to automatically
        update the total of the related Order model whenever an OrderItem is created,
        updated, or deleted.
        """
        import orders.signals