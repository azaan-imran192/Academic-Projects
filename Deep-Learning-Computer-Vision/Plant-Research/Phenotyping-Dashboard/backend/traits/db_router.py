"""
Database Router for Plant Phenotyping Project
Place at: traits/db_router.py

Routes:
  PlantTraitsMySQL  →  mysql_wwf  (remote MySQL pheno_lums)
  Everything else   →  default    (local SQLite)
"""


class TraitsRouter:

    MYSQL_MODELS = {"planttraitsmysql"}

    def _is_mysql(self, model):
        return model._meta.model_name in self.MYSQL_MODELS

    def db_for_read(self, model, **hints):
        if self._is_mysql(model):
            return "mysql_wwf"
        return "default"

    def db_for_write(self, model, **hints):
        if self._is_mysql(model):
            return "mysql_wwf"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Never auto-migrate PlantTraitsMySQL — table created manually
        if model_name == "planttraitsmysql":
            return False
        # Don't migrate anything else to mysql_wwf
        if db == "mysql_wwf":
            return False
        return True