#!/usr/bin/env python3
"""Compute minimal single-Higgs VEV-zero choices for one JSON batch."""

import argparse
import json
from pathlib import Path


def get_minimal_sets(choices):
    """Return deterministic, inclusion-minimal choices without duplicates."""
    minimal = []
    for choice in sorted(set(map(frozenset, choices)), key=lambda s: (len(s), sorted(s))):
        if not any(previous <= choice for previous in minimal):
            minimal.append(choice)
    return [tuple(sorted(choice)) for choice in minimal]


def killed_vevs_by_mu_term(mu_insertions):
    """Find minimal singlet sets intersecting every monomial support.

    No insertions require no zero VEVs: return [()]. A constant monomial
    has empty support and cannot be killed: return []. Exponents are
    assumed to be nonnegative integers in a common singlet basis.
    """
    choices = [()]
    for insertion in mu_insertions:
        support = {index for index, exponent in enumerate(insertion) if exponent > 0}
        choices = get_minimal_sets(
            set(choice) | {index} for choice in choices for index in support
        )
    return choices


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", type=int, help="Batch number, for example 0")
    parser.add_argument("--batch-dir", type=Path, default=Path("mu_terms_sublists"))
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    with (args.batch_dir / f"list{args.job}.json").open() as file:
        mu_terms = json.load(file)
    results = {
        model_id: killed_vevs_by_mu_term(insertions)
        for model_id, insertions in mu_terms.items()
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"killed_vevs_library{args.job}.json"
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Saved {len(results)} single-Higgs model choices to {output}")


if __name__ == "__main__":
    main()
