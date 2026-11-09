# SkillProof — Rubric-based learning assessment on GenLayer

A compact GenLayer Intelligent Contract for assessing short, **public** learning responses against a clearly stated rubric.

**Different from previous projects:** SkillProof reviews a learner's demonstrated reasoning against an educational rubric, not legal contract language, refrigerated shipment temperatures, or environmental claims.

## How it works

- `submit(exercise_id, topic, rubric, learner_response)` writes a public exercise using a unique identifier.
- `assess(exercise_id)` allows only the submitter to request a single AI assessment. Independent GenLayer validators re-evaluate the response and must agree on **MEETS_RUBRIC**, **NEEDS_REVISION**, or **INCONCLUSIVE**.
- `get_exercise(exercise_id)` returns the publicly stored rubric, response and decision.

The rubric is set by the submitter and cannot be changed afterward. Repeated assessments, unauthorized review, invalid inputs and malformed model outputs are rejected. There is no transferable certificate, escrow, payment or credential.

**Limitations:** The result is formative automated feedback, *not* a verified skill credential, academic grade or proof of a student's identity. The contract does not authenticate authorship, prevent plagiarism or verify the rubric's quality. All submitted responses are publicly visible; do not submit personal/student data.

## Verification

```bash
python -m pip install 'genlayer-py @ git+https://github.com/genlayerlabs/genlayer-py@v0.18' 'genlayer-test @ git+https://github.com/genlayerlabs/genlayer-testing-suite@v0.29' 'genvm-linter @ git+https://github.com/genlayerlabs/genvm-linter@main' pytest
python -m pytest -q tests/test_direct_sdk.py
genvm-lint check contracts/SkillProof.py
```

`.github/workflows/checks.yml` runs SDK Direct tests and GenVM lint. `.github/workflows/studionet.yml` is a separate optional **public testnet** proof. Direct tests alone do not establish finalized on-chain consensus; never claim deployment without the real Explorer receipt.

See [SUBMISSION.md](SUBMISSION.md) for the Portal information and verified evidence once available.
