import os 
import sys 
import unittest
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from factorio import Factorio

class TestPlacementSpecifications(unittest.TestCase):

    def test_single_placement(self):

        inmap = """
            free((0,0)). free((0,1)). free((1,0)). free((1,1)). 
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 2, 2).
        """

        graph = """
            pipe_node_spec(f1, fs1).
        """

        models = {
            frozenset({ 'place(f1,(0,0))'}),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)


    def test_simple_placement(self):

        inmap = """
            free((0,0)). free((0,1)). free((1,0)). free((1,1)). 
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 1, 1).

            spec(fs2).
            spec_size(fs2, 1, 2).
        """

        graph = """
            pipe_node_spec(f1, fs1).
            pipe_node_spec(f2, fs1).
            pipe_node_spec(f3, fs2).
        """

        models = {
            frozenset({ 'place(f1,(0,0))', 'place(f2,(0,1))', 'place(f3,(1,0))' }),
            frozenset({ 'place(f1,(0,1))', 'place(f2,(0,0))', 'place(f3,(1,0))' }),
            frozenset({ 'place(f1,(1,0))', 'place(f2,(1,1))', 'place(f3,(0,0))' }),
            frozenset({ 'place(f1,(1,1))', 'place(f2,(1,0))', 'place(f3,(0,0))' }),
        }
        
        instance = Factorio(inmap, specs, graph)
        instance.solve()

        self.assertSetEqual(instance.models, models)


    def test_pre_placement(self):

        inmap = """
            free((0,0)). free((0,1)). free((1,0)). free((1,1)). 
            place(f3, (0,0)).
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 1, 1).

            spec(fs2).
            spec_size(fs2, 2, 1).
        """

        graph = """
            pipe_node_spec(f1, fs1).
            pipe_node_spec(f2, fs1).
            pipe_node_spec(f3, fs2).
        """

        models = {
            frozenset({ 'place(f1,(0,1))', 'place(f2,(1,1))', 'place(f3,(0,0))' }),
            frozenset({ 'place(f1,(1,1))', 'place(f2,(0,1))', 'place(f3,(0,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()

        self.assertSetEqual(instance.models, models)

    def test_obstacle_placement(self):

        # `free((1,1))` is not given, which means that something blocks (1,1)
        inmap = """
            free((0,0)). free((0,1)). free((1,0)).
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 2, 2).
        """

        graph = """
            pipe_node_spec(f1, fs1).
        """

        # We cannot place building `fs1` due to obstacles -> There are no answer sets!
        models = set()

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)


    def test_placement_on_resources(self):

        inmap = """
            free((0,0)). free((0,1)). free((1,0)). free((1,1)). free((2,0)). free((2,1)). 
            place_ground_resource(r1, (0,0)). 
            place_ground_resource(r1, (2,0)). 
            place_ground_resource(r1, (2,1)).
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 1, 2).

            spec_minimal_ground_resource_needs(fs1, r1, 1).
        """

        graph = """
            pipe_node_spec(f1, fs1).
        """

        models = {
            frozenset({ 'place(f1,(0,0))'}),
            frozenset({ 'place(f1,(2,0))'}),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_placement_on_resources_2(self):

        inmap = """
            free((0,0)). free((0,1)). free((1,0)). free((1,1)). free((2,0)). free((2,1)). 
            place_ground_resource(r1, (1,0)). 
            place_ground_resource(r1, (2,0)). 
            place_ground_resource(r1, (2,1)).
        """

        specs = """
            spec(fs1).
            spec_size(fs1, 2, 2).

            spec_minimal_ground_resource_needs(fs1, r1, 3).
        """

        graph = """
            pipe_node_spec(f1, fs1).
        """

        models = {
            frozenset({ 'place(f1,(1,0))'}),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)
