import os 
import sys 
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

    supply_belt(inst_coal_belt).
    supply_belt_connect_in_order(inst_coal_belt,inst_coal_drill_1,1).

    supply_node_spec(inst_ins_coal_drill_1, inserter).
    supply_belt_connect_in_order_on_axis(inst_coal_belt,inst_ins_coal_drill_1, inst_coal_drill_1, 2).


    %%% Iron plate supply chain
    supply_node_spec(inst_iron_drill, burner_mining_drill(iron_ore)).   
    supply_node_spec(inst_iron_furnace, stone_furnace).
    supply_node_spec(inst_chest, wooden_chest).
    supply_direct_output_to((inst_iron_drill, associate_multiple(outputs_burner_mining_drill)), inst_iron_furnace).
    supply_insert_from_to(inst_iron_furnace, inst_chest).

    %%% Deliver coal to iron furnaces
    supply_node_spec(cins_drill, inserter).
    supply_belt_connect_in_order_on_axis(inst_coal_belt, cins_drill, inst_iron_drill, 3).
    % supply_node_spec(inst_ins_coal_furnace_2, inserter).
    % supply_belt_connect_in_order_on_axis(inst_coal_belt, inst_ins_coal_furnace_2, inst_iron_furnace_2, 3).

"""

instance = Factorio(inmap, graph)
instance.solve(6)
instance.print_models()
instance.visualize_models()
