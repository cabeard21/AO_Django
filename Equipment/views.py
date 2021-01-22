from django.shortcuts import render

from .models import *

from ao_bin_utils.ao_bin_data import AoBinData
import ao_bin_utils.ao_bin_tools as aot

from ao_bin_utils.my_thread import (
    MyThread, work_queue, queue_lock, set_exit_flag
)

import time

def list_efficient_items(request):

    equipment_sets = EquipmentSet.objects.all()

    equipment_set_list = []
    equipment_set_names = []
    equipment_set_costs = []
    equipment_set_chars = []

    set_exit_flag(0)

    threads = []
    result_list = []
    for i in range(len(equipment_sets)):
        thread = MyThread(
            lambda x: efficient_items_process(x), work_queue, result_list
        )
        thread.start()
        threads.append(thread)

    queue_lock.acquire()
    for equipment_set in equipment_sets:
       work_queue.put(equipment_set)

    queue_lock.release()

    while not work_queue.empty():
        pass

    set_exit_flag(1)

    for t in threads:
        t.join()

    for thread_res in result_list:
        equipment_set_list.append(thread_res[0])
        equipment_set_names.append(thread_res[1])
        equipment_set_costs.append(thread_res[2])
        equipment_set_chars.append(thread_res[3])

    return render(request, 'equipment.html', {
        'equipment_set_list': equipment_set_list,
        'equipment_set_names': equipment_set_names,
        'equipment_set_costs': equipment_set_costs,
        'equipment_set_chars': equipment_set_chars,
    })


def efficient_items_process(equipment_set):
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

    return (ordered_efficient_set, equipment_set.set_name, total_cost, equipment_set.character)
