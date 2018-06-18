import matplotlib.pyplot as plt

from rundmcmc.chain import MarkovChain
from rundmcmc.ingest import ingest
from rundmcmc.loggers import ConsoleLogger, ListLogger
from rundmcmc.make_graph import (add_data_to_graph, construct_graph,
                                 get_list_of_data, pull_districts)
from rundmcmc.partition import Partition, propose_random_flip
from rundmcmc.run import run
from rundmcmc.updaters import cut_edges, statistic_factory
from rundmcmc.validity import Validator, contiguous


def main():
    graph = construct_graph(*ingest('./testData/wyoming_test.shp', 'GEOID'))

    cd_data = get_list_of_data('./testData/wyoming_test.shp', ['CD', 'ALAND'])

    add_data_to_graph(cd_data, graph, ['CD', 'ALAND'])

    assignment = pull_districts(graph, 'CD')
    validator = Validator([contiguous])
    updaters = {
        'area': statistic_factory('ALAND', alias='area'),
        'cut_edges': cut_edges
    }

    initial_partition = Partition(graph, assignment, updaters)
    accept = lambda x: True
    # Exposes the chain object to the Runner.
    chain = MarkovChain(propose_random_flip, validator, accept,
                        initial_partition, total_steps=100)

    loggers = [ListLogger('area'), ConsoleLogger(interval=10)]

    results = run(chain, loggers)

    areas = [value for record in results[0] for key, value in record.items()]
    print(areas)
    plt.hist(areas)


if __name__ == "__main__":
    main()
