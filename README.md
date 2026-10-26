# Paper2: six experiments + collective workflow (research scaffold)

## Important scientific boundary
This repository is a runnable **protocol-integration/demo scaffold**, not a production cryptographic implementation and not a reproduction of the 2025 LiteQSign paper's performance claims.

- `DemoHMACAdapter` is intentionally a symmetric HMAC-based test adapter. It is **not** LiteQSign, not a public-key signature, and not post-quantum signature evidence.
- The group leader verifies each member independently. This is **batch processing**, not cryptographic signature aggregation.
- The key exchange and authenticated-encryption module are demonstration adapters unless replaced by validated ML-KEM and AES-GCM implementations.
- No SIS solution is fabricated. A valid aggregate-signature scheme must be specified and independently reviewed before claiming cryptographic aggregation.
- Never use demo mode for real devices, real secrets, or journal claims about quantum resistance.

## Requirements
Python 3.10+; standard library only for demo mode.

## Run all six individual experiments
From this directory:
```bash
python -m experiments.exp1_liteqsign
python -m experiments.exp2_batch_processing
python -m experiments.exp3_key_establishment
python -m experiments.exp4_security_tests
python -m experiments.exp5_benchmark
python -m experiments.exp6_reproducibility
```

## Run the collective workflow and common metrics
```bash
python -m experiments.run_all
```
Outputs are written to `results/` as CSV/JSON. Results are measurements of this demo implementation on the machine where the command runs, not published-paper results.

## Replace demo adapters for research mode
1. Integrate the exact LiteQSign reference code and version from the 2025 paper. Keep it in a separate module and preserve license/attribution.
2. Implement its real key generation, stateful signing, verifier-side public-key construction, and verification; add reference test vectors.
3. Replace `DemoKEM` with a vetted ML-KEM implementation conforming to NIST FIPS 203.
4. Replace `DemoAEAD` with AES-256-GCM from a vetted cryptographic library, with nonce uniqueness enforcement.
5. Replace per-member batch processing only if a separately specified and proven aggregation construction is available.
6. Run physical MCU energy measurements for claims about ATxmega128A1/other hardware. Host CPU timing is not a proxy for MCU energy.

## Six workstreams
1. Signature interface/state/integrity tests.
2. Per-device proof verification and group processing.
3. Key establishment + secure-channel interface.
4. Negative tests: tampering, replay, revocation, invalid signature, ciphertext tampering.
5. Performance, throughput, latency, bytes, confidence intervals.
6. Reproducibility metadata, raw CSVs, generated summary and plots.

## Research reporting rule
Report each metric as one of:
- `measured_demo`: measured from this scaffold;
- `measured_reference`: measured using the actual reference implementation;
- `target`: a goal not yet achieved;
- `not_measured`: requires hardware/library/data not present.

Do not describe targets as achieved results.
