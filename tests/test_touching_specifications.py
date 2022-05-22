import os 
import sys 
import unittest
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from factorio import Factorio

class TestInputSpecifications(unittest.TestCase):

    def test_single_touching(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)). free((4,0)).
            place(b2, (1,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).

            spec(bs2).
            spec_size(bs2, 2, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).
            pipe_touch(b1,b2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_single_touching_reflexivity(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)). free((4,0)).
            place(b2, (1,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).

            spec(bs2).
            spec_size(bs2, 2, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).
            pipe_touch(b2,b1).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)


    def test_one_to_two_inputs(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)). free((4,0)).
            free((2,1)).
            place(b3, (1,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).

            spec(bs2).
            spec_size(bs2, 2, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs2).
            pipe_touch(b1,b3).
            pipe_touch(b2,b3).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(3,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(2,1))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(0,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(2,1))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(0,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(3,0))', 'place(b3,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_four_in_circle(self):

        inmap = """
            free((0,0)). free((1,0)). free((0,1)). free((1,1)).
            place(b1, (0,0)).
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
            pipe_touch(b1,b2).
            pipe_touch(b2,b3).
            pipe_touch(b3,b4).
            pipe_touch(b4,b1).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,1))', 'place(b3,(1,1))', 'place(b4,(1,0))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))', 'place(b3,(1,1))', 'place(b4,(0,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point_both_any(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)). free((4,0)).
            place(b2, (1,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).

            spec(bs2).
            spec_size(bs2, 2, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).
            pipe_touch_point((b1,any),(b2,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point_both_any_reflexive(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)). free((3,0)). free((4,0)).
            place(b2, (1,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).

            spec(bs2).
            spec_size(bs2, 2, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).
            pipe_touch_point((b2,any),(b1,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b1,(-1,0)),(b2,any)).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(0,0))' }),
            frozenset({ 'place(b1,(2,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point_reflexive(self):

        inmap = """
            free((0,0)). free((1,0)). free((2,0)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b1,any),(b2,(1,0))).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(0,0))' }),
            frozenset({ 'place(b1,(2,0))', 'place(b2,(1,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point_2(self):

        inmap = """
            free((0,0)). free((0,1)). free((0,2)).
            free((1,0)). free((1,1)). free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 2).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b2,(-1,-1)), (b1,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_point_2_reflexive(self):

        inmap = """
            free((0,0)). free((0,1)). free((0,2)).
            free((1,0)). free((1,1)). free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 2).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b1,any), (b2,(-1,-1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_two_points(self):

        inmap = """
            free((0,0)). free((0,1)). free((0,2)).
            free((1,0)). free((1,1)). free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 2).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b1,(1,1)),(b2,(-1,-1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_two_points_reflexive(self):

        inmap = """
            free((0,0)). free((0,1)). free((0,2)).
            free((1,0)). free((1,1)). free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 2).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b2,(-1,-1)), (b1,(1,1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_one_of_multiple_distinct_points(self):

        inmap = """
            free((0,0)). free((0,1)). free((0,2)).
            free((1,0)). free((1,1)). free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1, 1, 2).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_touch_point((b2,associate_multiple(touch1)), (b1,associate_multiple(touch2))).
            pipe_touch_multiple_associate(touch1, (-1,-1)).
            pipe_touch_multiple_associate(touch1, (1,1)).
            pipe_touch_multiple_associate(touch2, (-1,-1)).
            pipe_touch_multiple_associate(touch2, (1,1)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,0))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_one_of_multiple_distinct_points_2(self):

        inmap = """
            free((0..4,0..4)).
            place(b1,(1,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1,2,2).

            spec(bs2).
            spec_size(bs2,1,1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).

            pipe_touch_point((b1,associate_multiple(touch1)), (b2,any)).
            pipe_touch_multiple_associate(touch1, (0,-1)).
            pipe_touch_multiple_associate(touch1, (2,0)).
            pipe_touch_multiple_associate(touch1, (1,2)).
            pipe_touch_multiple_associate(touch1, (-1,1)).
        """

        models = {
            frozenset({ 'place(b1,(1,1))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(3,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(2,3))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,2))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_at_one_of_multiple_distinct_points_2_reflexive(self):

        inmap = """
            free((0..4,0..4)).
            place(b1,(1,1)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1,2,2).

            spec(bs2).
            spec_size(bs2,1,1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs2).

            pipe_touch_point((b2,any), (b1,associate_multiple(touch1))).
            pipe_touch_multiple_associate(touch1, (0,-1)).
            pipe_touch_multiple_associate(touch1, (2,0)).
            pipe_touch_multiple_associate(touch1, (1,2)).
            pipe_touch_multiple_associate(touch1, (-1,1)).
        """

        models = {
            frozenset({ 'place(b1,(1,1))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(3,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(2,3))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,2))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)


    def test_interdependent_touch_locations(self):

        inmap = """
                            free((1,0)).
            free((0,1)).    free((1,1)).    free((2,1)).
                            free((1,2)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1,1,1).
        """

        graph = """
            pipe_node_spec(b1, bs1).
            pipe_node_spec(b2, bs1).
            pipe_node_spec(b3, bs1).

            pipe_touch_on_axis(b1,b2,b3).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(1,1))', 'place(b3,(1,2))' }),
            frozenset({ 'place(b1,(1,2))', 'place(b2,(1,1))', 'place(b3,(1,0))' }),

            frozenset({ 'place(b1,(0,1))', 'place(b2,(1,1))', 'place(b3,(2,1))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(1,1))', 'place(b3,(0,1))' }),
        }

        instance = Factorio(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)
