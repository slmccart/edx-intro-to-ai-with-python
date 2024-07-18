from heredity import joint_probability
from heredity import individual_probability
from heredity import probability_of_gene_from_parent
from pytest import approx

people = {
    "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
    "James": {"name": "James", "mother": None, "father": None, "trait": True},
    "Lily": {"name": "Lily", "mother": None, "father": None, "trait": False},
}

people_no_traits = {
    "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
    "James": {"name": "James", "mother": None, "father": None, "trait": False},
    "Lily": {"name": "Lily", "mother": None, "father": None, "trait": False},
}


def test_joint_probability():
    # Simple family with traits and genes
    assert joint_probability(people, {"Harry"}, {"James"}, {"James"}) == approx(
        0.002664, rel=1e-3
    )

    # Simple family with no genes and no traits
    assert joint_probability(people_no_traits, {}, {}, {}) == approx(0.876432)


def test_individual_probability():
    # Simple family with traits and genes
    num_genes = {"Lily": 0, "James": 2, "Harry": 1}
    assert individual_probability(people, "Lily", num_genes, False) == approx(0.9504)
    assert individual_probability(people, "James", num_genes, True) == approx(0.0065)
    assert individual_probability(people, "Harry", num_genes, False) == approx(0.431288)

    # Simple family with no genes and no traits
    num_genes = {"Lily": 0, "James": 0, "Harry": 0}
    assert individual_probability(people_no_traits, "Lily", num_genes, False) == approx(
        0.9504
    )
    assert individual_probability(
        people_no_traits, "James", num_genes, False
    ) == approx(0.9504)
    assert individual_probability(
        people_no_traits, "Harry", num_genes, False
    ) == approx(0.9703, rel=1e-4)


def test_probability_of_gene_from_parent():
    assert probability_of_gene_from_parent(0) == 0.01
    assert probability_of_gene_from_parent(1) == 0.5
    assert probability_of_gene_from_parent(2) == 0.99


if __name__ == "__main__":
    test_individual_probability()
