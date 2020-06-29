from zquantum.core.circuit import Circuit, Gate, Qubit
from forestopenfermion import exponentiate
from openfermion import (
    jordan_wigner,
    bravyi_kitaev,
    FermionOperator,
    InteractionOperator,
)
from typing import Union


def exponentiate_fermion_operator(
    fermion_generator: Union[FermionOperator, InteractionOperator],
    transformation: str = "Jordan-Wigner",
) -> Circuit:
    """Create a circuit corresponding to the exponentiation of an operator. Works only for antihermitian fermionic operators.

    Args:
        fermion_generator (openfermion.FermionOperator or 
            openfermion.InteractionOperator): fermionic generator.
        fermion_transform (str): The name of the qubit to fermion transformation
            to use.

    Returns:
        zquantum.core.circuit.Circuit: Circuit corresponding to the exponentiation of the
            transformed operator. 
    """
    if transformation not in ["Jordan-Wigner", "Bravyi-Kitaev"]:
        raise RuntimeError(f"Unrecognized transformation {transformation}")

    # Transform generator to qubits
    if transformation == "Jordan-Wigner":
        transformation = jordan_wigner
    elif transformation == "Bravyi-Kitaev":
        transformation = bravyi_kitaev

    qubit_generator = transformation(fermion_generator)

    for term in qubit_generator.terms:
        qubit_generator.terms[term] = float(qubit_generator.terms[term].imag)
    qubit_generator.compress()

    # Quantum circuit implementing the excitation operators
    circuit = exponentiate(qubit_generator)

    return circuit
