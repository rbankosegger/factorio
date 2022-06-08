import os 
import sys 
import unittest
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from factorio import Factorio

class TestFactorio(unittest.TestCase):

    def test_direct_output_any(self):

        inmap = """
            free((0..4,0)).
            place(b1,(0,0)).
        """

        custom_specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_direct_output_to((b1, any), b2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))'}),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(3,0))',
                        'place(gen_obj_inserter((b1,any),b2),(2,0))',
                        'place_belt(gen_obj_belt((b1,any),b2),(1,0))'
                      }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(4,0))',
                        'place(gen_obj_inserter((b1,any),b2),(3,0))',
                        'place_belt(gen_obj_belt((b1,any),b2),(1,0))',
                        'place_belt(gen_obj_belt((b1,any),b2),(2,0))'
                      }),
        }

        instance = Factorio(inmap, graph, custom_specs)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_direct_output_to_one_of_multiple_distinct_points(self):

        inmap = """
            free((0..2,0)).
            free((0..2,1)).
            place(b1,(0,0)).
        """

        custom_specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_direct_output_to((b1, associate_multiple(join)), b2).
            supply_touch_multiple_associate(join, (0,1)).
            supply_touch_multiple_associate(join, (1,0)).

        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,1))'}),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))'}),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(2,1))',
                        'place(gen_obj_inserter((b1,associate_multiple(join)),b2),(1,1))',
                        'place_belt(gen_obj_belt((b1,associate_multiple(join)),b2),(0,1))',
                      }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,1))',
                        'place(gen_obj_inserter((b1,associate_multiple(join)),b2),(1,1))',
                        'place_belt(gen_obj_belt((b1,associate_multiple(join)),b2),(1,0))',
                        'place_belt(gen_obj_belt((b1,associate_multiple(join)),b2),(2,0))',
                        'place_belt(gen_obj_belt((b1,associate_multiple(join)),b2),(2,1))',
                      }),
        }

        instance = Factorio(inmap, graph, custom_specs)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_iron_drill_into_smelter_right(self):

        inmap = """
            free((0..5,0)).    
            free((0..5,1)).    
            place_ground_resource(iron_ore,(0,0)).
            place_ground_resource(iron_ore,(1,0)).
            place_ground_resource(iron_ore,(0,1)).
            place_ground_resource(iron_ore,(1,1)).
        """

        graph = """
            supply_node_spec(inst_drill, burner_mining_drill(iron_ore)).   
            supply_node_spec(inst_furnace, stone_furnace).

            supply_direct_output_to((inst_drill, associate_multiple(outputs_burner_mining_drill)),
                                    inst_furnace).
        """

        models = {

            # Direct connection, no inserter needed
            frozenset( {'place(inst_drill,(0,0))', 'place(inst_furnace,(2,0))'} ),

            # Connection via belt and inserter, with variations on belt and inserter placements
            frozenset( {'place(inst_drill,(0,0))', 'place(inst_furnace,(4,0))',
                        'place(gen_obj_inserter((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,0))',
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,0))',
                       }),
            frozenset( {'place(inst_drill,(0,0))', 'place(inst_furnace,(4,0))',
                        'place(gen_obj_inserter((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,0))', 
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,0))',
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,1))'} ),
            frozenset( {'place(inst_drill,(0,0))', 'place(inst_furnace,(4,0))',
                        'place(gen_obj_inserter((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,0))', 
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,0))',
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,1))',
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,1))'} ),
            frozenset( {'place(inst_drill,(0,0))', 'place(inst_furnace,(4,0))',
                        'place(gen_obj_inserter((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,1))', 
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,0))',
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,1))'
                       } ),
        }

        instance = Factorio(inmap, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_supply_insert_from_to(self):

        inmap = """
            free((0..4,0)).
            place(b1,(0,0)).
        """

        custom_specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_insert_from_to(b1, b2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 
                        'place(gen_obj_inserter(b1,b2),(1,0))',
                        'place(b2,(2,0))',
                      }),
            frozenset({ 'place(b1,(0,0))', 
                        'place(gen_obj_inserter_out(b1,b2),(1,0))',
                        'place_belt(gen_obj_belt(b1,b2),(2,0))',
                        'place(gen_obj_inserter_in(b1,b2),(3,0))',
                        'place(b2,(4,0))',
                      }),
        }

        instance = Factorio(inmap, graph, custom_specs)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_cogwheel_supply_chain(self):

        inmap = """
            free((0..9,0)).    
            free((0..9,1)).    
            free((0..9,2)).    
            place_ground_resource(iron_ore,(0,0)).
            place_ground_resource(iron_ore,(1,0)).
            place_ground_resource(iron_ore,(0,1)).
            place_ground_resource(iron_ore,(1,1)).
        """

        graph = """
            supply_node_spec(inst_drill, burner_mining_drill(iron_ore)).   
            supply_node_spec(inst_furnace, stone_furnace).
            supply_node_spec(inst_assembler, assembling_machine_1).

            supply_direct_output_to((inst_drill, associate_multiple(outputs_burner_mining_drill)), inst_furnace).
            supply_insert_from_to(inst_furnace, inst_assembler).

            % Use custom placement constraints to get only relevant answer sets
            :- place_belt(_,XY), place_belt(_,XY2), XY>XY2.
            :- place(_,(X,Y)), Y!=0.
        """

        models = {

            # Case 1: drill and furnace connected directly, one inserter between furnace and assembly machine
            frozenset( {'place(inst_drill,(0,0))', 
                        'place(inst_furnace,(2,0))',
                        'place(gen_obj_inserter(inst_furnace,inst_assembler),(4,0))',
                        'place(inst_assembler,(5,0))',
                       }),

            # Case 2: drill and furnace connected with inserter, one inserter between furnace and assembly machine
            frozenset( {'place(inst_drill,(0,0))', 
                        'place_belt(gen_obj_belt((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(2,0))',
                        'place(gen_obj_inserter((inst_drill,associate_multiple(outputs_burner_mining_drill)),inst_furnace),(3,0))',
                        'place(inst_furnace,(4,0))',
                        'place(gen_obj_inserter(inst_furnace,inst_assembler),(6,0))',
                        'place(inst_assembler,(7,0))',
                       }),

            # Case 3: drill and furnace connected directly, two inserters and belt between furnace and assembly machine
            frozenset( {'place(inst_drill,(0,0))', 
                        'place(inst_furnace,(2,0))',
                        'place(gen_obj_inserter_out(inst_furnace,inst_assembler),(4,0))',
                        'place_belt(gen_obj_belt(inst_furnace,inst_assembler),(5,0))',
                        'place(gen_obj_inserter_in(inst_furnace,inst_assembler),(6,0))',
                        'place(inst_assembler,(7,0))',
                       }),

        }

        instance = Factorio(inmap, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)
