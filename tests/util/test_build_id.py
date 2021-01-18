import dash_express as dx


def test_deterministic_uid():
    dx.util.reset_uid_random_seed()
    id1 = dx.build_id(name="foo")
    id2 = dx.build_id(name="bar")

    dx.util.reset_uid_random_seed()
    id3 = dx.build_id(name="foo")
    id4 = dx.build_id(name="bar")

    assert id1 == {"uid": "e3e70682-c209-4cac-629f-6fbed82c07cd", "name": "foo"}
    assert id3 == id1

    assert id2 == {"uid": "82e2e662-f728-b4fa-4248-5e3a0a5d2f34", "name": "bar"}
    assert id4 == id2


def test_name_position_argument():
    id = dx.build_id("component_name")
    assert set(id) == {"uid", "name"}
    assert id["name"] == "component_name"


def test_kwargs_only():
    id = dx.build_id(p1="component_name", index=12)
    assert set(id) == {"uid", "p1", "index"}
    assert id["p1"] == "component_name"
    assert id["index"] == 12


def test_positional_name_and_kwargs():
    id = dx.build_id("component_name", index=12, kind="foo")
    assert set(id) == {"uid", "name", "index", "kind"}
    assert id["name"] == "component_name"
    assert id["index"] == 12
    assert id["kind"] == "foo"
