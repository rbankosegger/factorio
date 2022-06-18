import os 
import sys 
import json

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from factorio import Factorio

inmap = """
    free((0..9,0..5)).
    free((1..6,6..9)).
    place_ground_resource(iron_ore,(0..3,0..2)).
    place_ground_resource(coal,(1..5,6..9)).
"""

graph = """
    %%% Coal supply chain
    supply_node_spec(inst_coal_drill_1, burner_mining_drill(coal)).   
    supply_node_spec(inst_coal_drill_2, burner_mining_drill(coal)).   
    %supply_node_spec(inst_coal_drill_3, burner_mining_drill(coal)).   

    supply_node_spec(inst_ins_coal_drill_1, inserter).
    supply_node_spec(inst_ins_coal_drill_2, inserter).
    %supply_node_spec(inst_ins_coal_drill_3, inserter).

    supply_touch_multiple_associate(join_coal_1, XY) :- supply_touch_multiple_associate(outputs_burner_mining_drill, XY).
    supply_touch_multiple_associate(join_coal_2, XY) :- supply_touch_multiple_associate(outputs_burner_mining_drill, XY).

    supply_belt(inst_coal_belt).
    supply_belt_connect_in_order(inst_coal_belt, (inst_coal_drill_1, associate_multiple(join_coal_1)), 1).
    supply_belt_connect_in_order(inst_coal_belt, (inst_coal_drill_2, associate_multiple(join_coal_2)), 1).
    %supply_belt_connect_in_order(inst_coal_belt, (inst_coal_drill_3, associate_multiple(outputs_burner_mining_drill)), 1).

    supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_drill_1, inst_coal_drill_1, 2).
    supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_drill_2, inst_coal_drill_2, 2).
    %supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_drill_3, inst_coal_drill_3, 2).

    %%% Iron plate supply chain
    supply_node_spec(inst_iron_drill_1, burner_mining_drill(iron_ore)).   
    supply_node_spec(inst_iron_drill_2, burner_mining_drill(iron_ore)).   

    supply_node_spec(inst_iron_furnace_1, stone_furnace).
    supply_node_spec(inst_ins_iron_furnace_1, inserter).

    supply_node_spec(inst_iron_furnace_2, stone_furnace).
    supply_node_spec(inst_ins_iron_furnace_2, inserter).

    supply_touch_multiple_associate(join_iron_1, XY) :- supply_touch_multiple_associate(outputs_burner_mining_drill, XY).
    supply_touch_multiple_associate(join_iron_2, XY) :- supply_touch_multiple_associate(outputs_burner_mining_drill, XY).
    supply_belt(inst_iron_ore_belt).
    supply_belt_connect_in_order(inst_iron_ore_belt, (inst_iron_drill_1, associate_multiple(join_iron_1)), 1).
    supply_belt_connect_in_order(inst_iron_ore_belt, (inst_iron_drill_2, associate_multiple(join_iron_2)), 1).
    supply_belt_connect_in_order_on_axis(inst_iron_ore_belt, inst_ins_iron_furnace_1, inst_iron_furnace_1, 2).
    supply_belt_connect_in_order_on_axis(inst_iron_ore_belt, inst_ins_iron_furnace_2, inst_iron_furnace_2, 2).

    supply_node_spec(inst_ins_plate_1, inserter).
    supply_node_spec(inst_ins_plate_2, inserter).
    supply_node_spec(inst_ins_chest, inserter).
    supply_node_spec(inst_chest, wooden_chest).

    supply_belt(inst_plate_belt).
    supply_belt_connect_in_order_on_axis(inst_plate_belt, inst_ins_plate_1, inst_iron_furnace_1, 1).
    supply_belt_connect_in_order_on_axis(inst_plate_belt, inst_ins_plate_2, inst_iron_furnace_2, 1).
    supply_belt_connect_in_order_on_axis(inst_plate_belt, inst_ins_chest, inst_chest, 2).
    supply_touch_on_axis(inst_plate_belt, inst_ins_chest, inst_chest).


    %%% Deliver coal to iron furnaces
    supply_node_spec(inst_ins_coal_furnace_1, inserter).
    supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_furnace_1, inst_iron_furnace_1, 3).
    supply_node_spec(inst_ins_coal_furnace_2, inserter).
    supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_furnace_2, inst_iron_furnace_2, 3).

"""

def cfg_simple(instance, config):
    instance.clingo_control.configuration.configuration = config

def cfg_multiproc(instance, cores:int, mode:str):
    instance.clingo_control.configuration.solve.parallel_mode = f'{cores},{mode}'

def cfg_domain_heuristics(instance):
    instance.clingo_control.add('base', [], '#heuristic supply_insert_from_to_choice1(A,B) : supply_insert_from_to(A,B). [2,true]')
    instance.clingo_control.add('base', [], '#heuristic supply_direct_output_choice1(A,B) : supply_direct_output_to(A,B). [1,true]')

configs = [
    ('default-auto', lambda inst: cfg_simple(inst, 'auto')),
    ('default-frumpy', lambda inst: cfg_simple(inst, 'frumpy')),
    ('default-jumpy', lambda inst: cfg_simple(inst, 'jumpy')),
    ('default-tweety', lambda inst: cfg_simple(inst, 'tweety')),
    ('default-handy', lambda inst: cfg_simple(inst, 'handy')),
    ('default-crafty', lambda inst: cfg_simple(inst, 'crafty')),
    ('default-trendy', lambda inst: cfg_simple(inst, 'trendy')),
    ('default-many', lambda inst: cfg_simple(inst, 'many')),
    ('parallel-4-compete', lambda inst: cfg_multiproc(inst, 4,'compete')),
    ('parallel-4-split', lambda inst: cfg_multiproc(inst, 4,'split')),
    ('parallel-8-compete', lambda inst: cfg_multiproc(inst, 8,'compete')),
    ('parallel-8-split', lambda inst: cfg_multiproc(inst, 8,'split')),
    ('default-auto-domain-heuristics', cfg_domain_heuristics),
]


for i, (cfg_label, apply_cfg_to) in enumerate(configs):

    print(f'Progress: {i+1}/{len(configs)} started ...')

    instance = Factorio(inmap, graph)
    apply_cfg_to(instance)

    instance.solve(6)

    with open(f'3_data/{i}_{cfg_label}.json', 'w') as f:
        json.dump(instance.clingo_control.statistics, f, indent=4, separators=(',', ': '))

    instance.visualize_models(filename=f'3_data/{i}_{cfg_label}.png')
