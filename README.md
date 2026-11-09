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

**Evidence policy:** SkillProof v2 has its own new verified Studionet deployment and complete two-wallet, consensus-backed lifecycle receipt. Earlier SkillProof v1 addresses are historical, not v2 evidence.

## SkillProof v2 real public Studionet evidence — 9 November 2026

- **New v2 contract / Explorer:** https://explorer-studio.genlayer.com/address/0x128c10a32Cad9c478c5C05113aB24C1B1F6CD036
- **Complete independent two-wallet live execution, consensus + readback:** https://github.com/maho0638/SkillProof/actions/runs/42619075598
- **Official 5 Direct SDK tests + GenVM static verification:** https://github.com/maho0638/SkillProof/actions/runs/42618038812
- **Deployed source revision:** `446e017b6b34d56fd707ac87afcba29f0206a374`
- **Teacher / offer tx:** `0xa3f3680339a0f22747edc201a38ea317d428ed227f2e3328459396e04abf3b68`
- **Learner request and validator consensus MATCH tx:** `0x7e01e7386a5e74cbf881f9e940f9eafcc376e8eb93ae687fafe0e773d49905f3`
- **Learner signed session digest tx:** `0x41ed30bb59a6e6a2e92634946ea5861d259a215c86b71fd67769be67856a2d65`
- **Teacher signed the SAME digest tx:** `0x7d4d944002a846969149df467a8db025c179b70c7f6faec992a23acdfe47b84e`
- **Public final state:** `ATTESTED`, matching SHA-256 `febd06a715f8153f03b7c6d520d7ee013dafd0bfeb3f3b0e8b476c58a57322a1`

Both signers were distinct testnet accounts. The last state was independently read back on-chain, after both transactions completed. This is a content-bound mutual consent **record**, not proof of actual skill, attendance, or academic credentials. No mainnet transactions occurred.
