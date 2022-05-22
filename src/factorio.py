import clingo

class Factorio:
    def __init__(self, inmap, specs, graph):
        self.models = set()

        lp = """

            to_place(Building) :- pipe_node_spec(Building, _).
            1 = { place(Building, XY) : free(XY) } :- to_place(Building).
            1 >= { place(Building, XY) : to_place(Building) } :- free(XY).

            associate(Building, (X,Y)) :- place(Building, (X0, Y0)), 
                                          pipe_node_spec(Building, Spec),
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
                pipe_node_spec(Building, Spec),
                spec_minimal_ground_resource_needs(Spec, Resource, _),
                N = #count{ XY : coversResource(Building, Resource, XY) }.
            violate(ground_resource_needs(Building, IsRes)) :- pipe_node_spec(Building, Spec),
                spec_minimal_ground_resource_needs(Spec, Resource, MinRes),
                coversResourceCnt(Building, Resource, IsRes),
                IsRes < MinRes.
            :- violate(ground_resource_needs(_,_)).

            #defined pipe_touch/2.
            adj((X,Y), (X+1,Y)) :- free((X,Y)), free((X+1,Y)).
            adj((X,Y), (X,Y+1)) :- free((X,Y)), free((X,Y+1)).
            adj(L2, L1) :- adj(L1, L2).
            buildings_touch(B1,B2) :- pipe_touch(B1, B2), associate(B1, L1), associate(B2, L2), adj(L1,L2).
            violate(buildings_touch(B1, B2)) :- pipe_touch(B1, B2),  not buildings_touch(B1, B2).
            :- violate(buildings_touch(_,_)).

            #defined pipe_touch_point/2.
            pipe_touch(B1, B2) :- pipe_touch_point((B1,_), (B2,_)).

%            buildings_touch_point(B1,B2) :- pipe_touch_point((B1,(DX,DY)), (B2,any)),
%                associate(B1,L1),
%                associate(B2,(X,Y)),
%                adj(L1,(X,Y)),
%                place(B1,(BX,BY)),
%                X=BX+DX,
%                Y=BY+DY.
%            buildings_touch_point(B1,B2) :- pipe_touch_point((B1,any), (B2,(DX,DY))),
%                associate(B1,(X,Y)),
%                associate(B2,L2),
%                adj(L2,(X,Y)),
%                place(B2,(BX,BY)),
%                X=BX+DX,
%                Y=BY+DY.
%            buildings_touch_point(B1,B2) :- pipe_touch_point((B1,(DX1,DY1)), (B2,(DX2,DY2))),
%                associate(B1,(BX1,BY1)),
%                associate(B2,(BX2,BY2)),
%                adj((XB1,YB1),(BX2,BY2)),
%                place(B1,(PX1,PY1)),
%                place(B2,(PX2,PY2)),
%                BX1=PX2+DX2,
%                BY1=PY2+DY2,
%                BX2=PX1+DX1,
%                BY2=PY1+DY1.
%            violate(buildings_dont_touch_point(B1,B2)) :- pipe_touch_point((B1,P1), (B2,P2)), 
%                P1!=any, 
%                not buildings_touch_point(B1,B2).
%            violate(buildings_dont_touch_point(B1,B2)) :- pipe_touch_point((B1,P1), (B2,P2)), 
%                P2!=any, 
%                not buildings_touch_point(B1,B2).
%
%            buildings_touch_point(B1,B2) :- pipe_touch_point((B1,(DX,DY)), (B2,any)),
%                associate(B1,L1),
%                associate(B2,(X,Y)),
%                adj(L1,(X,Y)),
%                place(B1,(BX,BY)),
%                X=BX+DX,
%                Y=BY+DY.

            touching_point(B1,B2,L1) :- pipe_touch_point((B1,_), (B2,_)),
                associate(B1,L1),
                associate(B2,L2),
                adj(L1,L2).
            touching_point(B1,B2,L2) :- pipe_touch_point((B1,_), (B2,_)),
                associate(B1,L1),
                associate(B2,L2),
                adj(L1,L2).


            required_touching_point(B2, (X+DX,Y+DY)) :- 
                pipe_touch_point((B1,(DX,DY)), (B2,_)),
                place(B1,(X,Y)).

            required_touching_point(B1, (X+DX,Y+DY)) :- 
                pipe_touch_point((B1,_), (B2,(DX,DY))),
                place(B2,(X,Y)).

            required_touching_point_touched(B,P) :-
                required_touching_point(B,P),
                associate(B,P).

            violate(required_touching_point_not_touched(B,P)) :-
                required_touching_point(B,P),
                not required_touching_point_touched(B,P).

            :- violate(required_touching_point_not_touched(_,_)).


            #defined pipe_touch_multiple_associate/2.
            required_possible_touching_point(B2, (X+DX,Y+DY), A) :- 
                pipe_touch_point((B1,associate_multiple(A)), (B2,_)),
                pipe_touch_multiple_associate(A, (DX,DY)),
                place(B1,(X,Y)).
            required_possible_touching_point(B1, (X+DX,Y+DY), A) :- 
                pipe_touch_point((B1,_), (B2,associate_multiple(A))),
                pipe_touch_multiple_associate(A, (DX,DY)),
                place(B2,(X,Y)).

            touching_association_fulfilled(B,A) :-
                required_possible_touching_point(B,P,A),
                associate(B,P).
            violate(touching_association_not_fulfilled(B,A)) :-
                required_possible_touching_point(B,_,A),
                not touching_association_fulfilled(B,A).

            :- violate(touching_association_not_fulfilled(_,_)).


            #defined pipe_touch_on_axis/3.
            pipe_touch(A, B) :- pipe_touch_on_axis(A,B,_).
            pipe_touch(B, C) :- pipe_touch_on_axis(_,B,C).
            touching_points_on_axis(LA,(A,B,C)) :- pipe_touch_on_axis(A,B,C),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).
            touching_points_on_axis(LB,(A,B,C)) :- pipe_touch_on_axis(A,B,C),
                associate(A,LA),
                associate(B,LB),
                adj(LA,LB).
            touching_points_on_axis(LB,(A,B,C)) :- pipe_touch_on_axis(A,B,C),
                associate(B,LB),
                associate(C,LC),
                adj(LB,LC).
            touching_points_on_axis(LC,(A,B,C)) :- pipe_touch_on_axis(A,B,C),
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

            % #show violate/1.
            #show place/2.
        """

        self.clingo_control = clingo.Control()
        self.clingo_control.configuration.solve.models=0
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

    def solve(self):
        self.clingo_control.ground([('base', [])])
        self.clingo_control.solve(on_model=lambda m: self.add_model(m))

