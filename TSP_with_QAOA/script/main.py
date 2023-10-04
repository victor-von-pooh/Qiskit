import time
import json

from qiskit import Aer
from qiskit.providers import Options
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_provider import IBMProvider

from utility_functions import (
    create_tsp,
    create_init_state,
    execution,
    result_shower
)


if __name__ == "__main__":
    with open('../meta/meta.json') as f:
        meta_data = json.load(f)

    SHOTS = meta_data['shots']
    ITERATIONS = meta_data['iterations']
    PROBLEM = create_tsp(
        meta_data['problem']['data_path'],
        meta_data['problem']['num_cities']
    )
    OPTION = Options(shots=SHOTS)

    if meta_data['mode'] == 'simulation':
        backend_sim = Aer.get_backend("qasm_simulator")
        meo_sim = execution(
            backend_sim,
            OPTION,
            ITERATIONS,
            1,
            qc=create_init_state(meta_data['problem']['num_cities'])
        )

        start = time.time()
        result_sim = meo_sim.solve(PROBLEM)
        end = time.time()

        print(f"Time : {int(end - start)} sec")
        result_shower(result_sim)

    elif meta_data['mode'] == 'device':
        QiskitRuntimeService.save_account(
            channel="ibm_quantum",
            token=meta_data['token'],
            overwrite=True
        )

        provider = IBMProvider()
        instance = "ibm-q/open/main"

        backend_device = provider.get_backend(
            "ibm_brisbane",
            instance=instance
        )
        meo_device = execution(
            backend_device,
            OPTION,
            ITERATIONS,
            1,
            qc=create_init_state(meta_data['problem']['num_cities'])
        )

        result_device = meo_device.solve(PROBLEM)

        result_shower(result_device)

    else:
        print('mode in meta data is incorrect')
