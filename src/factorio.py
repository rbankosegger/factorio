import math
from collections import defaultdict
from types import SimpleNamespace
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.collections import PatchCollection

from gridworld import GridWorld


class Factorio(GridWorld):

    def __init__(self, inmap, graph, custom_specs=""):

        self.visualizable_models = list()

        factorio_specs = """
            spec(burner_mining_drill(coal)).
            spec_size(burner_mining_drill(coal),2,2).
            spec_minimal_ground_resource_needs(burner_mining_drill(coal), coal, 4).

            spec(burner_mining_drill(iron_ore)).
            spec_size(burner_mining_drill(iron_ore),2,2).
            spec_minimal_ground_resource_needs(burner_mining_drill(iron_ore), iron_ore, 4).

            spec(burner_mining_drill(copper_ore)).
            spec_size(burner_mining_drill(copper_ore),2,2).
            spec_minimal_ground_resource_needs(burner_mining_drill(copper_ore), copper_ore, 4).

            supply_touch_multiple_associate(outputs_burner_mining_drill, ( 0, -1)).
            supply_touch_multiple_associate(outputs_burner_mining_drill, ( 2,  0)).
            supply_touch_multiple_associate(outputs_burner_mining_drill, ( 1,  2)).
            supply_touch_multiple_associate(outputs_burner_mining_drill, (-1,  1)).

            spec(stone_furnace).
            spec_size(stone_furnace,2,2).

            spec(wooden_chest).
            spec_size(wooden_chest,1,1).

            spec(assembling_machine_1).
            spec_size(assembling_machine_1,3,3).

            spec(lab).
            spec_size(lab,3,3).

            % TODO: inserter(coal-powered, electric??)
            spec(inserter).
            spec_size(inserter,1,1).

            spec(small_electric_pole).
            spec_size(small_electric_pole,1,1).

        """

        factorio_lp = """

            % Direct connection of output from one building to some other building
            #defined supply_direct_output_to/2.
            1 = { supply_direct_output_choice1(A,B); supply_direct_output_choice2(A,B) } :- supply_direct_output_to(A,B).
            supply_touch_point(A, (B,any)) :- supply_direct_output_choice1(A,B).
            supply_node_spec(gen_obj_inserter(A,B), inserter) :- supply_direct_output_choice2(A,B).
            supply_belt(gen_obj_belt(A,B)) :- supply_direct_output_choice2(A,B).
            supply_belt_connect_in_order(gen_obj_belt((A,any),B),A,1) :- supply_direct_output_choice2((A,any),B).
            supply_belt_connect_in_order_on_axis(Belt, Inserter, Building, 2) :- 
                Belt = gen_obj_belt(A,B),
                Inserter = gen_obj_inserter(A,B),
                Building = B,
                supply_direct_output_choice2(A,B).

            supply_belt_connect_in_order(gen_obj_belt((A,associate_multiple(Join)),B), 
                                         (A, associate_multiple(Join)),1) 
                    :- supply_direct_output_choice2((A,associate_multiple(Join)),B).

            % Connect two buildings, either directly with one inserter 
            % or with two inserters and a belt inbetween
            #defined supply_insert_from_to/2.
            1 = { supply_insert_from_to_choice1(A,B); supply_insert_from_to_choice2(A,B) }
                :- supply_insert_from_to(A,B).
            supply_node_spec(gen_obj_inserter(A,B), inserter) :- supply_insert_from_to_choice1(A,B).
            supply_touch_on_axis(A,gen_obj_inserter(A,B),B) :- supply_insert_from_to_choice1(A,B).
            supply_node_spec(gen_obj_inserter_out(A,B), inserter) :- supply_insert_from_to_choice2(A,B).
            supply_node_spec(gen_obj_inserter_in(A,B), inserter) :- supply_insert_from_to_choice2(A,B).
            supply_belt(gen_obj_belt(A,B)) :- supply_insert_from_to_choice2(A,B).
            supply_belt_connect_in_order_on_axis(gen_obj_belt(A,B), gen_obj_inserter_out(A,B), A, 1) :- supply_insert_from_to_choice2(A,B).
            supply_belt_connect_in_order_on_axis(gen_obj_belt(A,B), gen_obj_inserter_in(A,B), B, 2) :- supply_insert_from_to_choice2(A,B).


            % Output formatting
            place_spec(Spec, XY, (SX,SY)) :- place(Building, XY), 
                supply_node_spec(Building, Spec),
                spec_size(Spec,SX,SY).


        """

        super().__init__(inmap, factorio_specs+custom_specs, graph)

        self.clingo_control.add('base', [], factorio_lp)

    def add_visualizable_model(self, model):

        loc_free = set()
        loc_res = set()
        loc_place_spec = set()
        loc_place_spec_per_type = defaultdict(list)
        loc_place_belt = set()
        loc_place_belt_dir = set()

        for sym in model.symbols(atoms=True):
            if sym.match('free', 1):
                sym_x, sym_y = sym.arguments[0].arguments[0:2]
                loc_free.add((sym_x.number, sym_y.number))
            elif sym.match('place_ground_resource', 2):
                res = str(sym.arguments[0])
                sym_x, sym_y = sym.arguments[1].arguments[0:2]
                loc_res.add((res, (sym_x.number, sym_y.number)))
            elif sym.match('place_spec', 3):
                spec = str(sym.arguments[0])
                sym_x, sym_y = sym.arguments[1].arguments[0:2]
                sym_sx, sym_sy = sym.arguments[2].arguments[0:2]
                loc_place_spec.add((spec, 
                                    (sym_x.number, sym_y.number), 
                                    sym_sx.number,
                                    sym_sy.number))

                loc_place_spec_per_type[spec].append(((sym_x.number, sym_y.number), 
                                                              sym_sx.number, 
                                                              sym_sy.number))

            elif sym.match('place_belt', 2):
                sym_x, sym_y = sym.arguments[1].arguments[0:2]
                loc_place_belt.add((sym_x.number, sym_y.number))


            elif sym.match('belt_connected', 4):
                if not str(sym.arguments[3]) == 'start':
                    sym_x0, sym_y0 = sym.arguments[3].arguments[0:2] 
                    sym_x1, sym_y1 = sym.arguments[1].arguments[0:2]
                    loc_place_belt_dir.add(((sym_x0.number, sym_y0.number), (sym_x1.number, sym_y1.number)))

        model_dict = SimpleNamespace(
            model_number = model.number,
            loc_free = loc_free,
            loc_free_xmin = min(x for x,y in loc_free),
            loc_free_xmax = max(x for x,y in loc_free),
            loc_free_ymin = min(y for x,y in loc_free),
            loc_free_ymax = max(y for x,y in loc_free),
            loc_res = loc_res,
            loc_place_spec = loc_place_spec,
            loc_place_spec_per_type = loc_place_spec_per_type,
            loc_place_belt = loc_place_belt,
            loc_place_belt_dir = loc_place_belt_dir,
        )

        self.visualizable_models.append(model_dict)


    def add_model(self, model):
        super().add_model(model)
        self.add_visualizable_model(model)

    def visualize_models(self, columns=3, filename=None):

        rows = math.ceil(len(self.visualizable_models) / columns)
        fix, axs = plt.subplots(rows, columns, figsize=(columns*4, rows*4))

        if rows > 1:
            axs_flat = [a for aa in axs for a in aa]
        else:
            axs_flat = axs

        if rows == 1 and columns == 1:
            axs_flat = [axs]

        for (mod, ax) in zip(self.visualizable_models, axs_flat):

            ax.set_title(f'Model {mod.model_number}')
            ax.set_facecolor('lightgrey')
            ax.set_xlim(mod.loc_free_xmin-1.0, mod.loc_free_xmax+1.0)
            ax.set_xticks(range(mod.loc_free_xmin, mod.loc_free_xmax+1))
            ax.set_ylim(mod.loc_free_ymin-1.0, mod.loc_free_ymax+1.0)
            ax.set_yticks(range(mod.loc_free_ymin, mod.loc_free_ymax+1))
            ax.invert_yaxis()
            ax.set_aspect('equal', adjustable='box')

            free_boxes = [patches.Rectangle((x-0.501,y-0.501), 1.02, 1.02) for x,y in mod.loc_free]
            pc = PatchCollection(free_boxes, facecolor='white')
            ax.add_collection(pc)

            def placeRect(xy,sx,sy): 
                x, y = xy
                return patches.Rectangle((x-0.5,y-0.5),sx,sy)

            def placeEllipse(xy,sx,sy):
                x, y = xy
                return patches.Ellipse((x,y),sx,sy)

            spec_viz = {
                'inserter': (placeEllipse, 'yellow', '..'),
                'burner_mining_drill(iron_ore)': (placeRect, 'blue', ''),
                'burner_mining_drill(copper_ore)': (placeRect, 'blue', ''),
                'burner_mining_drill(coal)': (placeRect, 'blue', ''),
                'assembling_machine_1': (placeRect, 'cyan', '\\'),
                'lab': (placeRect, 'magenta', 'oo'),
                'stone_furnace': (placeRect, 'red', '//'),
                'wooden_chest': (placeRect, 'magenta', '*'),
            }

            for spec, placements in mod.loc_place_spec_per_type.items():
                placeForm, color, hatch = spec_viz[spec]
                place_spec_boxes = [placeForm(*p) for p in placements]
                pc = PatchCollection(place_spec_boxes, facecolor=color, alpha=0.4, edgecolor='k',hatch=hatch)
                ax.add_collection(pc)

                if 'burner_mining_drill' in spec:

                    for xy, sx, sy  in placements:
                        x, y = xy
                        ax.plot([x+1], [y+1.5], 'bv', markersize=7, mec='white')
                        ax.plot([x+1.5], [y], 'b>', markersize=7, mec='white')
                        ax.plot([x], [y-0.5], 'b^', markersize=7, mec='white')
                        ax.plot([x-0.5], [y+1], 'b<', markersize=7, mec='white')

            place_belt_boxes = [patches.Rectangle((x-0.5,y-0.5),1,1) for (x,y) in mod.loc_place_belt]
            pc = PatchCollection(place_belt_boxes, facecolor='black', alpha=0.4,edgecolor='k',hatch=' ')
            ax.add_collection(pc)

            for (x0,y0), (x1,y1) in mod.loc_place_belt_dir:
                ax.arrow(x0,y0,(x1-x0)*1.0,(y1-y0)*1.0, head_width=.2, length_includes_head=True, color='k')

            resource_legend = {
                'iron_ore': 'gd',
                'copper_ore': 'rd',
                'coal': 'kd'
            }
            for res, (x,y) in mod.loc_res:
                ax.plot([x], [y], resource_legend[res], markeredgewidth=1, mec='white')


        plt.plot()

        if not filename:
            plt.show()
        else:
            plt.savefig(filename)

