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

instance = Factorio(inmap, graph)
instance.solve(6)
instance.print_models()
instance.visualize_models()
