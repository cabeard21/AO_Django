from django.apps import AppConfig
from django.db.models.signals import post_save


class EquipmentConfig(AppConfig):
    name = 'Equipment'

    def ready(self) -> None:
        post_save.connect(
            clear_cache,
            sender='Equipment.EquipmentSet',
            dispatch_uid="eq_pre_save_identifier"
        )

        return super().ready()


def clear_cache(instance, created: bool, **kwargs) -> None:
    """Clear cached results when a model is saved."""
    from Equipment.models import EfficientItemResult

    if created:
        return

    cache: list[EfficientItemResult] = EfficientItemResult.objects.all()

    for result in cache:
        if instance.set_name == result.equipment_set_name:
            result.delete()
