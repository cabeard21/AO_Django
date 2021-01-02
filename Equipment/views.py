from django.shortcuts import render

from .models import *

from ao_bin_utils.ao_bin_data import AoBinData
import ao_bin_utils.ao_bin_tools as aot

import time

def list_efficient_items(request):

    equipment_sets = EquipmentSet.objects.all()

    equipment_set_list = []
    equipment_set_names = []
    equipment_set_costs = []

    for equipment_set in equipment_sets:
        # Get input variables
        abd = AoBinData()
        target_ip = equipment_set.get_target_ips()
        item_list = list(map(lambda x: abd.get_unique_name(x), equipment_set.get_items()))
        mastery = equipment_set.get_mastery()
        min_tiers = equipment_set.get_min_tiers()
        location = 'Lymhurst'

        # Perform calculation
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
        efficient_set['target_ip'] = target_ip

        ordered_efficient_set= {
            'item_names': efficient_set['item_names'],
            'tiers': efficient_set['tiers'],
            'qualities': efficient_set['qualities'],
            'prices': efficient_set['prices'],
            'item_powers': efficient_set['item_powers'],
            'target_ip': efficient_set['target_ip'],
        }

        # Save output
        equipment_set_list.append(ordered_efficient_set)

        # Save Meta data
        equipment_set_names.append(equipment_set.set_name)
        equipment_set_costs.append(total_cost)

    return render(request, 'equipment.html', {
        'equipment_set_list': equipment_set_list,
        'equipment_set_names': equipment_set_names,
        'equipment_set_costs': equipment_set_costs,
    })
