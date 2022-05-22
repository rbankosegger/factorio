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

            :- violate(_).

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
        for i, model in enumerate(self.models):
            print(f'Model {i+1} = [')
            for symbol in sorted(list(model)):
                print(f'  {symbol}')
            print(']')

        print(f'Total: {i+1} models')

    def solve(self):
        self.clingo_control.ground([('base', [])])
        self.clingo_control.solve(on_model=lambda m: self.add_model(m))

