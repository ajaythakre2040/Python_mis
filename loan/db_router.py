class LoanRouter:
    route_app_labels = {"loan"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "readonly"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return None  # Block writes
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return False  # Block migrations for loan app
        return True
