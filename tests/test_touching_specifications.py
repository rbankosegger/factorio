import os 
import sys 
import unittest
# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from gridworld import GridWorld

class TestTouchingSpecifications(unittest.TestCase):

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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).
            supply_touch(b1,b2).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).
            supply_touch(b2,b1).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_node_spec(b3, bs2).
            supply_touch(b1,b3).
            supply_touch(b2,b3).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(3,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(2,1))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(0,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(2,1))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(0,0))', 'place(b3,(1,0))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(3,0))', 'place(b3,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_node_spec(b3, bs1).
            supply_node_spec(b4, bs1).
            supply_touch(b1,b2).
            supply_touch(b2,b3).
            supply_touch(b3,b4).
            supply_touch(b4,b1).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(0,1))', 'place(b3,(1,1))', 'place(b4,(1,0))' }),
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))', 'place(b3,(1,1))', 'place(b4,(0,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).
            supply_touch_point((b1,any),(b2,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).
            supply_touch_point((b2,any),(b1,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(3,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b1,(-1,0)),(b2,any)).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(0,0))' }),
            frozenset({ 'place(b1,(2,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b1,any),(b2,(1,0))).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(0,0))' }),
            frozenset({ 'place(b1,(2,0))', 'place(b2,(1,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b2,(-1,-1)), (b1,any)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b1,any), (b2,(-1,-1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b1,(1,1)),(b2,(-1,-1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b2,(-1,-1)), (b1,(1,1))).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_touch_point((b2,associate_multiple(touch1)), (b1,associate_multiple(touch2))).
            supply_touch_multiple_associate(touch1, (-1,-1)).
            supply_touch_multiple_associate(touch1, (1,1)).
            supply_touch_multiple_associate(touch2, (-1,-1)).
            supply_touch_multiple_associate(touch2, (1,1)).
        """

        models = {
            frozenset({ 'place(b1,(0,0))', 'place(b2,(1,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).

            supply_touch_point((b1,associate_multiple(touch1)), (b2,any)).
            supply_touch_multiple_associate(touch1, (0,-1)).
            supply_touch_multiple_associate(touch1, (2,0)).
            supply_touch_multiple_associate(touch1, (1,2)).
            supply_touch_multiple_associate(touch1, (-1,1)).
        """

        models = {
            frozenset({ 'place(b1,(1,1))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(3,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(2,3))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,2))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs2).

            supply_touch_point((b2,any), (b1,associate_multiple(touch1))).
            supply_touch_multiple_associate(touch1, (0,-1)).
            supply_touch_multiple_associate(touch1, (2,0)).
            supply_touch_multiple_associate(touch1, (1,2)).
            supply_touch_multiple_associate(touch1, (-1,1)).
        """

        models = {
            frozenset({ 'place(b1,(1,1))', 'place(b2,(1,0))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(3,1))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(2,3))' }),
            frozenset({ 'place(b1,(1,1))', 'place(b2,(0,2))' }),
        }

        instance = GridWorld(inmap, specs, graph)
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
            supply_node_spec(b1, bs1).
            supply_node_spec(b2, bs1).
            supply_node_spec(b3, bs1).

            supply_touch_on_axis(b1,b2,b3).
        """

        models = {
            frozenset({ 'place(b1,(1,0))', 'place(b2,(1,1))', 'place(b3,(1,2))' }),
            frozenset({ 'place(b1,(1,2))', 'place(b2,(1,1))', 'place(b3,(1,0))' }),

            frozenset({ 'place(b1,(0,1))', 'place(b2,(1,1))', 'place(b3,(2,1))' }),
            frozenset({ 'place(b1,(2,1))', 'place(b2,(1,1))', 'place(b3,(0,1))' }),
        }

        instance = GridWorld(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)

    def test_touch_on_axis_with_larger_buildings(self):

        # Buildings `1`, `2`, `3` must be placed 
        # with their touching points on the same axis.
        # Building `1` is pre-placed in the corner.
        # 4 answer sets should be possible:
        # ###___   >   ###___ ###___ ###33_ ###_33
        # ###___   >   ###___ ###___ ###33_ ###_33
        # ###__#   >   ###__# ###__# ###22# ###22#
        # _____#   >   3322_# __22_# ___22# ___22#
        # ____11   >   332211 332211 ____11 ____11
        # __##11   >   __##11 33##11 __##11 __##11

        inmap = """
            free((3..5,0)).
            free((3..5,1)).
            free((3..4,2)).
            free((0..4,3)).
            free((0..5,4)).
            free((0..1,5)). free((4..5,5)).

            place(b1,(4,4)).
        """

        specs = """
            spec(bs1).
            spec_size(bs1,2,2).
        """

        graph = """
            supply_node_spec(b1,bs1).
            supply_node_spec(b2,bs1).
            supply_node_spec(b3,bs1).
            supply_touch_on_axis(b1,b2,b3).
        """

        models = {
            frozenset({ 'place(b1,(4,4))', 'place(b2,(2,3))', 'place(b3,(0,3))' }),
            frozenset({ 'place(b1,(4,4))', 'place(b2,(2,3))', 'place(b3,(0,4))' }),
            frozenset({ 'place(b1,(4,4))', 'place(b2,(3,2))', 'place(b3,(3,0))' }),
            frozenset({ 'place(b1,(4,4))', 'place(b2,(3,2))', 'place(b3,(4,0))' }),
        }

        instance = GridWorld(inmap, specs, graph)
        instance.solve()
        self.assertSetEqual(instance.models, models)
