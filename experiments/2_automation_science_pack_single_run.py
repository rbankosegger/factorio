import os 
import sys 
import json
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from factorio import Factorio

inmap = """
    free((0..6,0..6)).
    free((0..6,0..6)).
    place_ground_resource(iron_ore,(0,0)).
    place_ground_resource(iron_ore,(1,0)).
    place_ground_resource(iron_ore,(0,1)).
    place_ground_resource(iron_ore,(1,1)).
    place_ground_resource(copper_ore,(1,8)).
    place_ground_resource(copper_ore,(2,8)).
    place_ground_resource(copper_ore,(1,9)).
    place_ground_resource(copper_ore,(2,9)).

    place(inst_iron_furnace, (4,4)).
"""

graph = """
    supply_node_spec(inst_iron_drill, burner_mining_drill(iron_ore)).   
    supply_node_spec(inst_iron_furnace, stone_furnace).
    supply_direct_output_to((inst_iron_drill, associate_multiple(outputs_burner_mining_drill)), inst_iron_furnace).

    supply_node_spec(inst_gear_assembler, assembling_machine_1).
    supply_insert_from_to(inst_iron_furnace, inst_gear_assembler).
"""
#inmap = """
#    free((0..9,0..5)).
#    free((1..6,6..9)).
#    place_ground_resource(iron_ore,(0,0)).
#    place_ground_resource(iron_ore,(1,0)).
#    place_ground_resource(iron_ore,(0,1)).
#    place_ground_resource(iron_ore,(1,1)).
#    place_ground_resource(copper_ore,(1,8)).
#    place_ground_resource(copper_ore,(2,8)).
#    place_ground_resource(copper_ore,(1,9)).
#    place_ground_resource(copper_ore,(2,9)).
#"""
#
#graph = """
#    supply_node_spec(inst_iron_drill, burner_mining_drill(iron_ore)).   
#    supply_node_spec(inst_iron_furnace, stone_furnace).
#    supply_direct_output_to((inst_iron_drill, associate_multiple(outputs_burner_mining_drill)), inst_iron_furnace).
#
#    supply_node_spec(inst_copper_drill, burner_mining_drill(copper_ore)).   
#    supply_node_spec(inst_copper_furnace, stone_furnace).
#    supply_direct_output_to((inst_copper_drill, associate_multiple(outputs_burner_mining_drill)), inst_copper_furnace).
#
#    supply_node_spec(inst_gear_assembler, assembling_machine_1).
#    supply_insert_from_to(inst_iron_furnace, inst_gear_assembler).
#
#    supply_node_spec(inst_scipack_assembler, assembling_machine_1).
#    supply_insert_from_to(inst_gear_assembler, inst_scipack_assembler).
#    supply_insert_from_to(inst_copper_furnace, inst_scipack_assembler).
#
#    supply_node_spec(inst_lab, lab).
#    supply_insert_from_to(inst_scipack_assembler, inst_lab).
#
#"""

instance = Factorio(inmap, graph)
instance.clingo_control.configuration.configuration = 'auto'
instance.clingo_control.configuration.configuration = 'frumpy'
#instance.clingo_control.configuration.configuration = 'jumpy'
#instance.clingo_control.configuration.configuration = 'tweety'
#instance.clingo_control.configuration.configuration = 'handy'
#instance.clingo_control.configuration.configuration = 'crafty'
#instance.clingo_control.configuration.configuration = 'trendy'
#instance.clingo_control.configuration.configuration = 'many'

instance.clingo_control.add('base', [], '#heuristic supply_insert_from_to_choice1(A,B) : supply_insert_from_to(A,B). [2,true]')
instance.clingo_control.add('base', [], '#heuristic supply_direct_output_choice_1(A,B) : supply_direct_output_to(A,B). [1,true]')
#instance.clingo_control.configuration.solve.parallel_mode = '8,split'

instance.solve(6)
instance.print_models()

print(json.dumps(instance.clingo_control.statistics, sort_keys=True, indent=4, separators=(',', ': ')))

#print(instance.clingo_control.configuration.solve.description('parallel_mode'))
#print(instance.clingo_control.configuration.solve.parallel_mode)

instance.visualize_models(filename='test.pdf')
