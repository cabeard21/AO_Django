from django.shortcuts import render

from .models import *

from ao_bin_utils.ao_bin_data import AoBinData
import ao_bin_utils.ao_bin_tools as aot

def list_efficient_items(request):

    equipment_sets = EquipmentSet.objects.all()

    equipment_set_list = []
    equipment_set_names = []
    equipment_set_ips = []
    equipment_set_costs = []
    abd = AoBinData()
    for equipment_set in equipment_sets:
        target_ip = equipment_set.target_ip
        item_list = list(map(lambda x: abd.get_unique_name(x), equipment_set.get_items()))
        mastery = equipment_set.get_mastery()
        min_tiers = equipment_set.get_min_tiers()
        location = 'Lymhurst'

        efficient_set_tool = aot.AoBinTools(
            aot.EfficientItemPower(
                target_ip, item_list, mastery, min_tiers, location
            )
        )

        efficient_set = efficient_set_tool.get_calculation()
        # Format output (maybe this should be a decorator?)
        efficient_set['tiers'] = list(map(lambda x: abd.get_item_tier(x), efficient_set['item_names']))
        efficient_set['item_names'] =  list(map(lambda x: abd.get_local_name(x), efficient_set['item_names']))
        total_cost = f"{sum(efficient_set['prices']):,.0f}"
        efficient_set['prices'] = list(map(lambda x: f"{float(x):,.0f}", efficient_set['prices']))
        efficient_set['qualities'] = list(map(lambda x: abd.get_quality_name(x), efficient_set['qualities']))

        equipment_set_list.append(efficient_set)

        # Set Meta data
        equipment_set_names.append(equipment_set.set_name)
        equipment_set_ips.append(equipment_set.target_ip)
        equipment_set_costs.append(total_cost)

    return render(request, 'equipment.html', {
        'equipment_set_list': equipment_set_list,
        'equipment_set_names': equipment_set_names,
        'equipment_set_ips': equipment_set_ips,
        'equipment_set_costs': equipment_set_costs,
    })