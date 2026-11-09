# SkillProof v2 — AI-matched peer learning, two-party attestation

**A new protocol, replacing the earlier rubric-grading prototype.**

SkillProof is a GenLayer Intelligent Contract that pairs a public **mentoring offer** with a learner's **learning goal** by validator-reviewed AI semantic matching. If the topics fit, the protocol opens an exchange between **two different addresses**. An on-chain completion receipt exists **only when both participants independently submit the same 64-character SHA-256 digest** of their shared session notes.

This is a reciprocal-consent protocol, **not AI grading**. There are no PASS/FAIL rubric results, no credentials, no tokens, no escrow, no learner scores and no automated proof of real-world attendance.

## Mechanism

1. **Mentor publishes** an immutable public skill offer with an outline and session duration (15–180 minutes).
2. **Learner requests** an exchange using an independent address and their learning objective. GenLayer leader and validators independently re-evaluate semantic compatibility; they must agree on MATCH/NO_MATCH.
3. **Both parties attest** the *same* SHA-256 digest of a mutually understood session-note document. A mismatching digest is rejected without changing state.
4. **Public receipt** records distinct teacher and learner addresses and a common agreed session digest only after BOTH signatures. The receipt is neither transferable nor revocable.

Methods: `publish_offer`, `request_exchange`, `attest_session`, `get_offer`, `get_exchange`.

## What makes this different

Prior RubricLedger and TenderLens are criteria-based task acceptance or tender evaluation contracts. SkillProof v2 **never evaluates a submitted answer against criteria**. Its consensus operation only matches learning topics; the state transition with value is **mutual cryptographic-content attestation requiring two wallets**. A learner cannot produce an attestation alone, and an uninterested mentor can decline by not signing.

**Limitations:** Nothing authenticates a participant's real-world skills, note content, learning outcomes or attendance. Two cooperating addresses can make false claims, and wallet addresses are not verified identities. Text and hashes are public. Do not store student/private information.

## Reproduce official Direct SDK tests

```bash
python -m pip install 'genlayer-py @ git+https://github.com/genlayerlabs/genlayer-py@v0.18' 'genlayer-test @ git+https://github.com/genlayerlabs/genlayer-testing-suite@v0.29' 'genvm-linter @ git+https://github.com/genlayerlabs/genvm-linter@main' pytest
python -m pytest -q tests/test_direct_sdk.py
genvm-lint check contracts/SkillProof.py
```

**Evidence policy:** Previous SkillProof v1 Studionet deployment and its receipt are historical and **do not validate this v2 contract**. This rebuild requires a fresh v2 deployment and live receipt before a GenLayer Portal submission.
