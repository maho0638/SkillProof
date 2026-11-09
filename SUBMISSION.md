# SkillProof v2 — Portal submission with verified public Studionet proof

**Proposed category:** Developer → Intelligent Contracts

**Proposed title:** SkillProof — Two-Party Learning Exchange with AI Topic Matching

**Description:** SkillProof is a GenLayer Intelligent Contract for decentralized peer learning coordination, not traditional grading. A mentor posts an immutable skill offer and session outline. A different wallet requests a learning exchange; GenLayer validators independently re-evaluate whether the objective genuinely matches the mentor's offered knowledge. If compatible, both participants must separately attest the same SHA-256 digest of shared session notes. Only matching attestations from the distinct teacher and learner addresses finalize a public exchange receipt. Unrelated offers, self-matches, unauthorized confirmations, mismatched digests, and replayed confirmations are blocked. Unlike rubric-based task assessment, the core protocol demonstrates two-party agreement and content-bound consent after a validator-approved semantic match.

**Repository:** https://github.com/maho0638/SkillProof

**Proof 1 — Required GenLayer Explorer Contract:** https://explorer-studio.genlayer.com/address/0x128c10a32Cad9c478c5C05113aB24C1B1F6CD036

**Proof 2 — Required GitHub Repository:** https://github.com/maho0638/SkillProof

**Proof 3 — Full on-chain two-wallet + consensus verification:** https://github.com/maho0638/SkillProof/actions/runs/42619075598

**Proof 4 — Official SDK tests and GenVM lint:** https://github.com/maho0638/SkillProof/actions/runs/42618038812

**Verified state:** Two different accounts (teacher and learner), AI validator consensus returned MATCH; the learner and teacher then each attested the same SHA-256 digest, and public readback showed ATTESTED.

**Transaction IDs:**
- Mentor offer: `0xa3f3680339a0f22747edc201a38ea317d428ed227f2e3328459396e04abf3b68`
- AI MATCH consensus: `0x7e01e7386a5e74cbf881f9e940f9eafcc376e8eb93ae687fafe0e773d49905f3`
- Learner attestation: `0x41ed30bb59a6e6a2e92634946ea5861d259a215c86b71fd67769be67856a2d65`
- Teacher attestation: `0x7d4d944002a846969149df467a8db025c179b70c7f6faec992a23acdfe47b84e`

**Deployed source revision:** `446e017b6b34d56fd707ac87afcba29f0206a374`.

**Note:** This verifies on-chain consent between two test wallets, not real-world attendance or qualifications. The user must submit the Portal contribution; no Portal post was sent automatically.
