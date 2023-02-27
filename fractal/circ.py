from numpy import pi
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.visualization import plot_bloch_multivector
import json

def make_data(z0, z1):
    label = ['|0>', '|1>']
    real_imag = ['real', 'imag']
    data = [dict(zip(real_imag, [float(z0.real), float(z0.imag)])), dict(zip(real_imag, [float(z1.real), float(z1.imag)]))]
    return dict(zip(label, data))

backend = Aer.get_backend('statevector_simulator')
circuit = QuantumCircuit(1, 1)

data = []
fig = plt.figure(figsize=(20, 20)) 

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    if i + 1 < 10:
        name = f'bloch/circ_00{i + 1}.png'
    else:
        name = f'bloch/circ_0{i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.ry(pi / 80, 0)

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    name = f'bloch/circ_0{40 + i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.rz(pi / 80, 0)

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    if 80 + i + 1 < 100:
        name = f'bloch/circ_0{80 + i + 1}.png'
    else:
        name = f'bloch/circ_{80 + i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.rx(-pi / 80, 0)

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    name = f'bloch/circ_{120 + i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.ry(pi / 80, 0)

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    name = f'bloch/circ_{160 + i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.rz(pi / 80, 0)

for i in range(40):
    out = execute(circuit, backend).result().get_statevector()

    data.append(make_data(out.data[0], out.data[1]))

    name = f'bloch/circ_{200 + i + 1}.png'

    plot_bloch_multivector(circuit, filename=name)

    circuit.rx(-pi / 80, 0)

labels = [f'state_{i}' for i in range(1, 241)]
dataset = dict(zip(labels, data))

with open('dataset.json', 'w') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)