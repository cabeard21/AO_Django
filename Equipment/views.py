from django.shortcuts import render

from .models import *

from ao_bin_utils.ao_bin_data import AoBinData
import ao_bin_utils.ao_bin_tools as aot

def list_efficient_items(request):

    equipment_sets = EquipmentSet.objects.all()

    equipment_set_list = []
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
        efficient_set['enchant_lvls'] = [int(x.split('@')[-1]) if '@' in x else 0 for x in efficient_set['item_names']]
        efficient_set['item_names'] =  list(map(lambda x: abd.get_local_name(x), efficient_set['item_names']))
        efficient_set['prices'] = list(map(lambda x: f"{float(x):,.2f}", efficient_set['prices']))

        equipment_set_list.append(efficient_set)

    return render(request, 'equipment.html', {
        'equipment_set_list': equipment_set_list,
    })
