import os 
import sys 
import unittest
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from factorio import Factorio

class TestBeltSpecifications(unittest.TestCase):

    def test_simple_belt(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)).
            place(b2,(3,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order(belt, b2, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(3,0))', 'place_belt(belt,(1,0))', 'place_belt(belt,(2,0))' }),
            frozenset({ 'place(b1,(1,0))', 'place(b2,(3,0))', 'place_belt(belt,(2,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_one_belt_two_ordered_targets(self):

        inmap = """
                            free((1,0)).
            free((0,1)).    free((1,1)).    free((2,1)).    free((3,1)).

            place(b1,(0,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).
            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order(belt, b2, 2).
            pipe_belt_connect_in_order(belt, b3, 3).
        """

        models = {
            frozenset({ 'place(b1,(0,1))', 'place(b2,(1,0))', 'place(b3,(2,1))', 
                        'place_belt(belt,(1,1))' }),
            frozenset({ 'place(b1,(0,1))', 'place(b2,(2,1))', 'place(b3,(1,0))', 
                        'place_belt(belt,(1,1))' }),
            # This set is still okay because ordering needs to be "greater than or equal"
            frozenset({ 'place(b1,(0,1))', 'place(b2,(1,0))', 'place(b3,(3,1))', 
                        'place_belt(belt,(1,1))', 'place_belt(belt,(2,1))' }),
            # The follwing set is ruled out due to ordering:
            # frozenset({ 'place(b1,(0,1))', 'place(b2,(3,1))', 'place(b3,(1,0))', 
            #             'place_belt(belt,(1,1))', 'place_belt(belt,(2,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_belt_no_branching(self):

        inmap = """
            free((0,0)).    free((1,0)).    free((2,0)).
            free((0,1)).                    free((2,1)).    
            free((0,2)).    free((1,2)).    free((2,2)).

            place(b1,(0,1)).
            place(b2,(2,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order(belt, b2, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,1))', 'place(b2,(2,1))',
                        'place_belt(belt,(0,0))', 'place_belt(belt,(1,0))', 'place_belt(belt,(2,0))' }),
            frozenset({ 'place(b1,(0,1))', 'place(b2,(2,1))',
                        'place_belt(belt,(0,2))', 'place_belt(belt,(1,2))', 'place_belt(belt,(2,2))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_belt_winding(self):

        inmap = """
            free((0,0)).
            free((0,1)).    free((1,1)).
            free((0,2)).    free((1,2)).
            free((0,3)).    free((1,3)).
            free((0,4)).

            place(b1,(0,0)).
            place(b2,(0,4)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order(belt, b2, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))', 'place_belt(belt,(0,2))', 'place_belt(belt,(0,3))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))', 'place_belt(belt,(0,2))', 'place_belt(belt,(0,3))',
                        'place_belt(belt,(1,1))', 'place_belt(belt,(1,2))'}),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))', 'place_belt(belt,(0,2))', 'place_belt(belt,(0,3))',
                                                  'place_belt(belt,(1,2))', 'place_belt(belt,(1,3))'}),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))',                           'place_belt(belt,(0,3))',
                        'place_belt(belt,(1,1))', 'place_belt(belt,(1,2))', 'place_belt(belt,(1,3))'}),

            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))', 'place_belt(belt,(0,2))', 'place_belt(belt,(0,3))',
                        'place_belt(belt,(1,1))', 'place_belt(belt,(1,2))', 'place_belt(belt,(1,3))' }),

            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,4))',
                        'place_belt(belt,(0,1))', 'place_belt(belt,(0,2))', 'place_belt(belt,(0,3))',
                                                                            'place_belt(belt,(1,3))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_two_belts(self):

        inmap = """
            free((0,0)).    free((1,0)).
            free((0,1)).    free((1,1)).
            free((0,2)).    free((1,2)).

            place(b1,(0,0)).
            place(b3,(1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).
            pipe_node_spec(b4, bs1).

            pipe_belt(belt1).
            pipe_belt_connect_in_order(belt1, b1, 1).
            pipe_belt_connect_in_order(belt1, b2, 2).
            pipe_belt(belt2).
            pipe_belt_connect_in_order(belt2, b3, 1).
            pipe_belt_connect_in_order(belt2, b4, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,2))', 'place(b3,(1,2))', 'place(b4,(1,0))',
                        'place_belt(belt1,(0,1))', 'place_belt(belt2,(1,1))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))', 'place(b3,(1,2))', 'place(b4,(0,1))',
                        'place_belt(belt1,(1,0))', 'place_belt(belt2,(0,2))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_belt_on_axis(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)).
            free((0,1)). free((1,1)). free((2,1)). free((3,1)).
            place(b1,(0,0)).
            place(b2,(2,1)).
            %place(b3,(3,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).

            pipe_touch(b2,b3).

            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order_on_axis(belt, b2, b3, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(2,1))',  'place(b3,(3,1))', 
                        'place_belt(belt,(0,1))', 'place_belt(belt,(1,1))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(2,1))',  'place(b3,(3,1))', 
                        'place_belt(belt,(1,0))', 'place_belt(belt,(1,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_belt_not_on_axis(self):

        inmap = """
            free((0,0)). free((1,0)).
            free((0,1)). free((1,1)). free((2,1)).
            place(b1,(0,0)).
            place(b2,(1,1)).
            place(b3,(2,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).

            pipe_touch(b2,b3).

            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order(belt, b2, 2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))',  'place(b3,(2,1))', 
                        'place_belt(belt,(0,1))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))',  'place(b3,(2,1))', 
                        'place_belt(belt,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_belt_on_axis_with_order(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)).
                         free((1,1)). free((2,1)). 
                         free((1,2)). free((2,2)). 

            place(b1,(0,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).
            pipe_node_spec(b4, bs1).
            pipe_node_spec(b5, bs1).

            pipe_touch(b2,b3).
            pipe_touch(b4,b5).

            pipe_belt(belt).
            pipe_belt_connect_in_order(belt, b1, 1).
            pipe_belt_connect_in_order_on_axis(belt, b2, b3, 2).
            pipe_belt_connect_in_order_on_axis(belt, b4, b5, 3).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 
                        'place(b2,(1,1))',  'place(b3,(1,2))', 
                        'place(b4,(2,1))',  'place(b5,(2,2))', 
                        'place_belt(belt,(1,0))', 'place_belt(belt,(2,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    # TODO: Belt connected to building at one of multiple points
    # TODO: Belt connected on  axis with robot and factory
    ###########
    # Later: two inserters with belt inbetween may reduce to one inserter
    # Later: Needs power source as input specification

