from django.db.models import Sum
from apps.product.models import QuotaDistribution
from apps.warehouse.models import InventoryQuotaSaleTransaction
from apps.authentication.models import Organization, OrganizationStats
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def update_organization_stats(instance: Organization):
    """ update all stats of organization from quota """

    if hasattr(instance, 'stats'):
        stat = instance.stats
    else:
        stat = OrganizationStats.objects.create(organization=instance)

    # set organization stats from quotas, distributions transactions & etc
    stat.total_quota_received = instance.assigned_quotas.count()
    stat.active_quotas_weight = instance.assigned_quotas.filter(is_closed=False).count()
    stat.closed_quotas_weight = instance.assigned_quotas.filter(is_closed=True).count()
    stat.total_distributed = instance.distributions.count()
    stat.total_inventory_in = instance.inventory.count()
    stat.total_sold = instance.distributions.all().aggregate(
        total_sold=Sum('been_sold')
    )['total_sold'] or 0

    stat.save(update_fields=[
        "total_quota_received",
        "active_quotas_weight",
        "closed_quotas_weight",
        "total_distributed",
        "total_inventory_in",
        "total_sold",
    ])


@receiver([post_save, post_delete], sender=QuotaDistribution)
@receiver([post_save, post_delete], sender=InventoryQuotaSaleTransaction)
def organization_stats(sender, instance, **kwargs):
    if sender == QuotaDistribution:
        update_organization_stats(instance.assigned_organization)
    elif sender == InventoryQuotaSaleTransaction:
        update_organization_stats(instance.inventory_entry.organization)
