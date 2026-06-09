from evrptw.data.io import load_instance


def test_sample_instance_has_expected_node_sets():
    instance = load_instance("data/samples/tiny_evrptw.json")

    assert instance.customer_ids == (1, 2, 3)
    assert instance.station_ids == (4,)
    assert instance.distance(0, 1) > 0

