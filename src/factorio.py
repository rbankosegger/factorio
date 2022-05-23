import clingo

class Factorio:
    def __init__(self, inmap, specs, graph):
        self.models = set()

        lp = """

            to_place(Building) :- supply_node_spec(Building, _).
            1 = { place(Building, XY) : free(XY) } :- to_place(Building).
            1 >= { place(Building, XY) : to_place(Building) } :- free(XY).

            associate(Building, (X,Y)) :- place(Building, (X0, Y0)), 
                                          supply_node_spec(Building, Spec),
                                          spec_size(Spec, SX, SY),
                                          X = X0..(X0+SX-1),
                                          Y = Y0..(Y0+SY-1).
            
            violate(placed_on_not_free_terrain(XY)) :- associate(_, XY), not free(XY).
            violate(buildings_intersect(B1,B2,XY)) :- associate(B1, XY), associate(B2, XY), B1<B2.
            :- violate(placed_on_not_free_terrain(_)).
            :- violate(buildings_intersect(_,_,_)).

            #defined place_ground_resource/2.
            #defined spec_minimal_ground_resource_needs/3.
            coversResource(Building, Resource, XY) :- associate(Building, XY), 
                place_ground_resource(Resource, XY).
            coversResourceCnt(Building, Resource, N) :- 
                supply_node_spec(Building, Spec),
                spec_minimal_ground_resource_needs(Spec, Resource, _),
                N = #count{ XY : coversResource(Building, Resource, XY) }.
            violate(ground_resource_needs(Building, IsRes)) :- supply_node_spec(Building, Spec),
                spec_minimal_ground_resource_needs(Spec, Resource, MinRes),
                coversResourceCnt(Building, Resource, IsRes),
                IsRes < MinRes.
            :- violate(ground_resource_needs(_,_)).

            #defined supply_touch/2.
            adj((X,Y), (X+1,Y)) :- free((X,Y)), free((X+1,Y)).
            adj((X,Y), (X,Y+1)) :- free((X,Y)), free((X,Y+1)).
            adj(L2, L1) :- adj(L1, L2).
            buildings_touch(B1,B2) :- supply_touch(B1, B2), associate(B1, L1), associate(B2, L2), adj(L1,L2).
            violate(buildings_touch(B1, B2)) :- supply_touch(B1, B2),  not buildings_touch(B1, B2).
            :- violate(buildings_touch(_,_)).

            #defined supply_touch_point/2.
            supply_touch(B1, B2) :- supply_touch_point((B1,_), (B2,_)).
            touching_point(B1,B2,L1) :- supply_touch_point((B1,_), (B2,_)),
                associate(B1,L1),
                associate(B2,L2),
                adj(L1,L2).
            touching_point(B1,B2,L2) :- supply_touch_point((B1,_), (B2,_)),
                associate(B1,L1),
                associate(B2,L2),
                adj(L1,L2).


            required_touching_point(B2, (X+DX,Y+DY)) :- 
                supply_touch_point((B1,(DX,DY)), (B2,_)),
                place(B1,(X,Y)).

            required_touching_point(B1, (X+DX,Y+DY)) :- 
                supply_touch_point((B1,_), (B2,(DX,DY))),
                place(B2,(X,Y)).

            required_touching_point_touched(B,P) :-
                required_touching_point(B,P),
                associate(B,P).

            violate(required_touching_point_not_touched(B,P)) :-
                required_touching_point(B,P),
                not required_touching_point_touched(B,P).

            :- violate(required_touching_point_not_touched(_,_)).


            #defined supply_touch_multiple_associate/2.
            required_possible_touching_point(B2, (X+DX,Y+DY), A) :- 
                supply_touch_point((B1,associate_multiple(A)), (B2,_)),
                supply_touch_multiple_associate(A, (DX,DY)),
                place(B1,(X,Y)).
            required_possible_touching_point(B1, (X+DX,Y+DY), A) :- 
                supply_touch_point((B1,_), (B2,associate_multiple(A))),
                supply_touch_multiple_associate(A, (DX,DY)),
                place(B2,(X,Y)).

            touching_association_fulfilled(B,A) :-
                required_possible_touching_point(B,P,A),
                associate(B,P).
            violate(touching_association_not_fulfilled(B,A)) :-
                required_possible_touching_point(B,_,A),
                not touching_association_fulfilled(B,A).

            :- violate(touching_association_not_fulfilled(_,_)).


            #defined supply_touch_on_axis/3.
            supply_touch(A, B) :- supply_touch_on_axis(A,B,_).
            supply_touch(B, C) :- supply_touch_on_axis(_,B,C).
            touching_points_on_axis(LA,(A,B,C)) :- supply_touch_on_axis(A,B,C),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).
            touching_points_on_axis(LB,(A,B,C)) :- supply_touch_on_axis(A,B,C),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).
            touching_points_on_axis(LB,(A,B,C)) :- supply_touch_on_axis(A,B,C),
                associate(B,LB),
                associate(C,LC),
                adj(LB,LC).
            touching_points_on_axis(LC,(A,B,C)) :- supply_touch_on_axis(A,B,C),
                associate(B,LB),
                associate(C,LC),
                adj(LB,LC).
            touching_points_x_axis_violated(Join) :-
                touching_points_on_axis((X1,Y1), Join),
                touching_points_on_axis((X2,Y2), Join),
                X1<X2.
            touching_points_y_axis_violated(Join) :-
                touching_points_on_axis((X1,Y1), Join),
                touching_points_on_axis((X2,Y2), Join),
                Y1<Y2.
            violate(not_on_same_axis(Join)) :- 
                touching_points_x_axis_violated(Join),
                touching_points_y_axis_violated(Join).
            :- violate(not_on_same_axis(_)).

            
            #defined supply_belt/1.
            #defined supply_belt_connect_in_order/3.
            { place_belt(Belt, XY) : free(XY) } :- supply_belt(Belt).
            1 >= {  place(Building, XY)  : to_place(Building); 
                    place_belt(Belt, XY) : supply_belt(Belt)      } :- free(XY).
            associate(Belt, (X,Y)) :- place_belt(Belt, (X, Y)). 

            % Belt Touching
            supply_touch_point((Belt,any),(Building,any)) :- supply_belt_connect_in_order(Belt, Building, _).

            % Belt order and connectedness
            belt_lowest_touching_point(Belt, XY, I) :- 
                place_belt(Belt,XY),
                touching_point(Belt, Building, XY),
                I = #min { J : supply_belt_connect_in_order(Belt,_,J) }.
            -belt_start(Belt,XY,I) :-
                place_belt(Belt,XY),
                belt_lowest_touching_point(Belt,XY,I),
                belt_lowest_touching_point(Belt,XY2,I),
                XY2<XY.
            -belt_start(Belt,XY,I) :-
                place_belt(Belt,XY),
                belt_lowest_touching_point(Belt,XY,I),
                belt_lowest_touching_point(Belt,_,J),
                J<I.
            belt_start(Belt,XY) :-
                place_belt(Belt,XY),
                belt_lowest_touching_point(Belt,XY,I),
                not -belt_start(Belt,XY,I).
            -belt_order(Belt,XY,I) :- place_belt(Belt,XY), touching_point(Belt, Building, XY),
                supply_belt_connect_in_order(Belt,Building,I),
                touching_point(Belt, Building2, XY),
                supply_belt_connect_in_order(Belt,Building2,J),
                J>I.
            belt_order(Belt,XY,I) :- place_belt(Belt,XY), touching_point(Belt, Building, XY),
                supply_belt_connect_in_order(Belt,Building,I),
                not -belt_order(Belt,XY,I).
            violate(no_belt_start(Belt)) :- supply_belt(Belt), not belt_start(Belt,_).
            :- violate(no_belt_start(_)).
            belt_connected(Belt, XY, I, start) :- belt_start(Belt, XY), belt_order(Belt, XY, I).
            1 >= { belt_connected(Belt, P2, I, P1): adj(P1,P2), place_belt(Belt, P2), not belt_order(Belt, P2, _);
                   belt_connected(Belt, P2, J, P1): adj(P1,P2), place_belt(Belt, P2), belt_order(Belt, P2, J), J>=I } :- 
                belt_connected(Belt, P1, I, _).    
            violate(belt_not_connected(Belt, XY)) :- place_belt(Belt, XY), not belt_connected(Belt, XY, _, _).
            :- violate(belt_not_connected(_,_)).

            violate(belt_part_has_more_than_one_connection(Belt, XY)) :- 
                supply_belt(Belt),
                belt_connected(belt, XY, _, L1),
                belt_connected(belt, XY, _, L2),
                L1 < L2.
            :- violate(belt_part_has_more_than_one_connection(_,_)).
            
            #defined supply_belt_connect_in_order_on_axis/4.
            supply_belt_connect_in_order(Belt, Building, I) :- 
                supply_belt_connect_in_order_on_axis(Belt, Building, _, I).
            supply_touch(A, B) :- 
                supply_belt_connect_in_order_on_axis(Belt, A, B, _).
            touching_points_on_axis(XY, (Belt,A,B)) :-
                supply_belt_connect_in_order_on_axis(Belt, A, B, _),
                touching_point(Belt,A,XY).
            touching_points_on_axis(LA,(Belt,A,B)) :- 
                supply_belt_connect_in_order_on_axis(Belt, A, B, _),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).
            touching_points_on_axis(LB,(Belt,A,B)) :- 
                supply_belt_connect_in_order_on_axis(Belt, A, B, _),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).




            % Belt order
            %#show belt_lowest_touching_point/3.
            %#show belt_order/3.
            %#show belt_connected/4.
            %#show belt_start/2.
            %#show -belt_start/3.
            %#show supply_belt_connect_in_order/3.


            #show violate/1.
            #show place/2.
            #show place_belt/2.
        """

        self.clingo_control = clingo.Control()
        self.clingo_control.add('base', [], lp)
        self.clingo_control.add('base', [], inmap)
        self.clingo_control.add('base', [], specs)
        self.clingo_control.add('base', [], graph)

    def parse_model(self, clingo_model):
        return frozenset(str(s) for s in clingo_model.symbols(shown=True))

    def add_model(self, model):
        self.models.add(self.parse_model(model))

    def print_models(self):
        i = -1
        for i, model in enumerate(self.models):
            print(f'Model {i+1} = [')
            for symbol in sorted(list(model)):
                print(f'  {symbol}')
            print(']')

        print(f'Total: {i+1} models')

    def solve(self, models=0):
        self.clingo_control.configuration.solve.models=models
        self.clingo_control.ground([('base', [])])
        self.clingo_control.solve(on_model=lambda m: self.add_model(m))

