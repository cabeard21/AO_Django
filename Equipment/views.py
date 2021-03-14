from django.shortcuts import render

from .models import *

from ao_bin_utils.ao_bin_data import AoBinData
import ao_bin_utils.ao_bin_tools as aot

from ao_bin_utils.my_thread import (
    MyThread, work_queue, queue_lock, set_exit_flag
)

import time

def list_efficient_items(request, id=None):

    equipment_sets = EquipmentSet.objects.all()

    equipment_set_list = []
    equipment_set_names = []
    equipment_set_costs = []
    equipment_set_chars = []
    equipment_set_ids = []

    # Check for set in cache
    equipment_sets_evaluated = []
    for equipment_set in equipment_sets:
        if id and equipment_set.id == id:
            # Force refresh
            eval_current_set = True
        else:
            eval_current_set = False

        if not eval_current_set:
            result = LoadEfficientItemResult(equipment_set)
            if result and result[1].seconds/60 < 60: # Only refresh if older than given minutes
                equipment_set_list.append(result[0][0])
                equipment_set_names.append(result[0][1])
                equipment_set_costs.append(result[0][2])
                equipment_set_chars.append(result[0][3])
                equipment_set_ids.append(equipment_set.id)
            else:
                eval_current_set = True

        if eval_current_set:
            equipment_sets_evaluated.append(equipment_set)

    # Evaluate remaining sets
    if len(equipment_sets_evaluated) > 0:
        set_exit_flag(0)

        threads = []
        result_list = []
        for i in range(len(equipment_sets_evaluated)):
            thread = MyThread(
                lambda x: efficient_items_process(x), work_queue, result_list
            )
            thread.start()
            threads.append(thread)

        queue_lock.acquire()
        for equipment_set in equipment_sets_evaluated:
            work_queue.put(equipment_set)

        queue_lock.release()

        while not work_queue.empty():
            pass

        set_exit_flag(1)

        for t in threads:
            t.join()

        for thread_res in result_list:
            if len(thread_res[5]) > 0:
                # There were failed items, try to use cached results
                result = LoadEfficientItemResult(equipment_set)
                if result:
                    equipment_set_list.append(result[0][0])
                    equipment_set_names.append(result[0][1])
                    equipment_set_costs.append(result[0][2])
                    equipment_set_chars.append(result[0][3])
                    equipment_set_ids.append(equipment_set.id)

            equipment_set_list.append(thread_res[0])
            equipment_set_names.append(thread_res[1])
            equipment_set_costs.append(thread_res[2])
            equipment_set_chars.append(thread_res[3])
            equipment_set_ids.append(thread_res[4])

            SaveEfficientItemResult(thread_res)

    # Sorty by set name?
    sorted_tuples = sorted(
                        zip(equipment_set_list,
                            equipment_set_names,
                            equipment_set_costs,
                            equipment_set_chars,
                            equipment_set_ids),
                        key=lambda x: x[1]
                        )
    equipment_set_list = []
    equipment_set_names = []
    equipment_set_costs = []
    equipment_set_chars = []
    equipment_set_ids = []
    for tup in sorted_tuples:
        equipment_set_list.append(tup[0])
        equipment_set_names.append(tup[1])
        equipment_set_costs.append(tup[2])
        equipment_set_chars.append(tup[3])
        equipment_set_ids.append(tup[4])

    return render(request, 'equipment.html', {
        'equipment_set_list': equipment_set_list,
        'equipment_set_names': equipment_set_names,
        'equipment_set_costs': equipment_set_costs,
        'equipment_set_chars': equipment_set_chars,
        'equipment_set_ids': equipment_set_ids,
    })


def LoadEfficientItemResult(equipment_set):
    for result in EfficientItemResult.objects.all():
        if result.equipment_set_name == equipment_set.set_name:
            try:
                equipment_char = Character.objects.get(char_name=result.equipment_set_character)
            except:
                equipment_char = None

            return (
                    (eval(result.ordered_efficient_set),
                    result.equipment_set_name,
                    result.total_cost,
                    equipment_char),

                    result.get_age()
                    ) # (tuple of result[0-3], age)

    return None


def SaveEfficientItemResult(result):
    try:
        eir = EfficientItemResult.objects.get(equipment_set_name=result[1])
    except:
        eir = EfficientItemResult.objects.create()

    eir.ordered_efficient_set = repr(result[0])
    eir.equipment_set_name = result[1]
    eir.total_cost = result[2]
    eir.equipment_set_character = str(result[3])
    eir.save()


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
    # Sort by price (This should probably be in the get_calculation method?)
    sorted_set = sorted(zip(efficient_set['item_names'], 
                            efficient_set['item_powers'],
                            efficient_set['prices'],
                            efficient_set['qualities']), key=lambda x: -x[2])
    efficient_set = {
        'item_names': [],
        'qualities': [],
        'item_powers': [],
        'prices': [],
    }
    for name, ip, price, quality in sorted_set:
        efficient_set['item_names'].append(name)
        efficient_set['qualities'].append(quality)
        efficient_set['item_powers'].append(ip)
        efficient_set['prices'].append(price)

    # Find failed items
    failed_item_indexes = []
    for i, x in enumerate(efficient_set['prices']):
        if x == 0:
            failed_item_indexes.append(i)

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

    return (ordered_efficient_set,
            equipment_set.set_name,
            total_cost,
            equipment_set.character,
            equipment_set.id,
            failed_item_indexes)
