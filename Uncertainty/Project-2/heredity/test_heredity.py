from heredity import joint_probability
from heredity import individual_probability
from heredity import calculate_parent_gene_contribution
from pytest import approx

people = {
    "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
    "James": {"name": "James", "mother": None, "father": None, "trait": True},
    "Lily": {"name": "Lily", "mother": None, "father": None, "trait": False},
}


def test_joint_probability():
    assert joint_probability(people, {"Harry"}, {"James"}, {"James"}) == 0.0026643247488


def test_individual_probability():
    num_genes = {"Lily": 0, "James": 2, "Harry": 1}
    assert individual_probability(people, "Lily", num_genes, False) == approx(0.9504)
    assert individual_probability(people, "James", num_genes, True) == approx(0.0065)
    assert individual_probability(people, "Harry", num_genes, False) == approx(0.431288)


def test_calculate_parent_gene_contribution():
    assert calculate_parent_gene_contribution(0) == 0.01
    assert calculate_parent_gene_contribution(1) == 0.5
    assert calculate_parent_gene_contribution(2) == 0.99


if __name__ == "__main__":
    test_individual_probability()
