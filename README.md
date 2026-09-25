# Compute singlet insertions and flavour scans

Research notebooks for constructing charge-compatible singlet insertions,
selecting singlet vacuum expectation values (VEVs) to set to zero, fitting
fermion mass matrices and quark mixing, and evaluating additional operator
monomials. This repository covers **models with one Higgs pair**.


## Workflow


| Stage | File | Purpose |
| --- | --- | --- |
| 1 | [generating library.ipynb](generating%20library.ipynb) | Filter to single-Higgs models and generate Yukawa, mu-term, and R-parity violating terms |
| 2a | [compute_killed_vevs0.py](compute_killed_vevs0.py) | Find minimal zero-VEV choices for each model in one batch |
| 2b | [make_a_unique_killed_vevs_library.ipynb](make_a_unique_killed_vevs_library.ipynb) | Combine the batch results |
| 3 | [method2 1.3.ipynb](method2%201.3.ipynb) | Fit singlet VEVs, coefficients, and real rotations; save accepted candidates |




## Run the stages

Source data:

| File | Contents |
| --- | --- |
| `ks.json` | Per-model nonperturbative singlet charges |
| `CohSigns.json` | Per-model records used to construct perturbative charges after the original fixed row deletion |
| `fieldcharges.json` | Per-model `[tens, fives, [H_down, H_up]]` charge lists |
| `labels.json` | Model labels aligned with the charge arrays |
| `higgsnum.json` | Higgs-pair counts used to select the single-Higgs models |

The generation notebook selects entries with Higgs-pair count 1 and filters
all aligned arrays together. With `USE_TEST_MODEL = True`, it uses the explicit
charges already present in the original notebook instead of these source files.

1. In `generating library.ipynb`, leave `USE_TEST_MODEL = False`, choose `P`, and
   run the cells in order. The active default `P = 12` is computationally large;
   use a small cutoff for an initial check. Candidate vectors are streamed,
   but the search still grows combinatorially.
2. This has been run on a cluster. Run the batch solver for each generated job, then run the merge notebook.
   Keep its `N_BATCHES` consistent with the generation notebook:

   ```bash
   for job in {0..9}; do
       python compute_killed_vevs0.py "$job"
   done
   ```

3. Run `method2 1.3.ipynb` on whatever list of models you have. It saves `insertions_matrices.json`, `viable_models.json`,
   and `fit_settings.json`. The seed and CKM retry budget are explicit.

To inspect generation without external data, set `USE_TEST_MODEL = True` and
`P = 1` in the first notebook. 
