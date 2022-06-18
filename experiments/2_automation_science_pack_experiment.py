import os 
import sys 
import json

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from factorio import Factorio

inmap = """
    free((0..9,0..5)).
    free((1..6,6..9)).
    place_ground_resource(iron_ore,(0,0)).
    place_ground_resource(iron_ore,(1,0)).
    place_ground_resource(iron_ore,(0,1)).
    place_ground_resource(iron_ore,(1,1)).
    place_ground_resource(copper_ore,(1,8)).
    place_ground_resource(copper_ore,(2,8)).
    place_ground_resource(copper_ore,(1,9)).
    place_ground_resource(copper_ore,(2,9)).
"""

graph = """
    supply_node_spec(inst_iron_drill, burner_mining_drill(iron_ore)).   
    supply_node_spec(inst_iron_furnace, stone_furnace).
    supply_direct_output_to((inst_iron_drill, associate_multiple(outputs_burner_mining_drill)), inst_iron_furnace).

    supply_node_spec(inst_copper_drill, burner_mining_drill(copper_ore)).   
    supply_node_spec(inst_copper_furnace, stone_furnace).
    supply_direct_output_to((inst_copper_drill, associate_multiple(outputs_burner_mining_drill)), inst_copper_furnace).

    supply_node_spec(inst_gear_assembler, assembling_machine_1).
    supply_insert_from_to(inst_iron_furnace, inst_gear_assembler).

    supply_node_spec(inst_scipack_assembler, assembling_machine_1).
    supply_insert_from_to(inst_gear_assembler, inst_scipack_assembler).
    supply_insert_from_to(inst_copper_furnace, inst_scipack_assembler).

    supply_node_spec(inst_lab, lab).
    supply_insert_from_to(inst_scipack_assembler, inst_lab).
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

    with open(f'2_data/{i}_{cfg_label}.json', 'w') as f:
        json.dump(instance.clingo_control.statistics, f, indent=4, separators=(',', ': '))

    instance.visualize_models(filename=f'2_data/{i}_{cfg_label}.png')
