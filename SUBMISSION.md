# SkillProof — GenLayer Portal submission

**Category:** Developer → Intelligent Contracts

**Proposed title:** SkillProof — AI Rubric Assessment with Validator Consensus

**Description:**

SkillProof is an original GenLayer Intelligent Contract for evaluating public learner responses against predefined educational rubrics. The author commits a topic, rubric and response, then requests an AI decision: MEETS_RUBRIC, NEEDS_REVISION or INCONCLUSIVE. Independent GenLayer validators re-evaluate the same inputs and compare the exact outcome before recording a public receipt. The contract rejects duplicate exercise identifiers, unauthorized reviews, repeated assessments, malformed model results and invalid text. It provides lightweight formative feedback without making false claims about verified identities, academic qualifications or plagiarism detection. Real SDK Direct and GenVM tests are documented in the repository; any live network claim must be supported by a separate finalized Studionet receipt.

**Repository:** https://github.com/maho0638/SkillProof

**Proof status:** Real Studionet deployment and state read-back verified; exact links below.

## Verified public Studionet deployment — 9 November 2026

**Mandatory evidence — GitHub Repository**
https://github.com/maho0638/SkillProof

**Mandatory evidence — GenLayer Explorer Contract**
https://explorer-studio.genlayer.com/address/0x0eB4387956775E5BA9aC08F4AfF10E69678E10Bf

**Live end-to-end CI evidence**
https://github.com/maho0638/SkillProof/actions/runs/42606514810

**Successful SDK and GenVM lint checks**
https://github.com/maho0638/SkillProof/actions/runs/42605937864

**Observed on-chain result:** `MEETS_RUBRIC`

- Submission transaction: `0xefa13163853a05d279e5249eadfae1515573e68fa606d275a194490c5c658b5a`
- Assessment transaction: `0x1de8bcc56333c8f42f07b0ec826388ba56dbb70d5e817759a2225d0b5880cba2`

Only public Studionet was used, not mainnet. No Portal submission is performed by this repository.
