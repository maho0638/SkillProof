"""Optional real public Studionet deployment and finalized state readback."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, name):
    receipt = call.transact(consensus_max_rotations=4, wait_interval=10000, wait_retries=50)
    assert tx_execution_succeeded(receipt), f"{name} failed: {receipt.get('hash', '')}"
    print(f"{name}_TX={receipt.get('hash', '')}", flush=True)


def test_real_studionet(default_account):
    c = get_contract_factory("SkillProof").deploy(
        account=default_account, consensus_max_rotations=4)
    address = str(c.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"SKILLPROOF_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)
    confirmed(c.submit(args=[
        "public-learning-sample-001", "Cybersecurity",
        "Explain why password reuse creates risk and name a mitigation action.",
        "Reused passwords expose other services when a breach happens. Use unique passwords with a password manager."
    ]), "SKILLPROOF_SUBMIT")
    assert json.loads(c.get_exercise(args=["public-learning-sample-001"]).call())["assessment"] == "PENDING"
    confirmed(c.assess(args=["public-learning-sample-001"]), "SKILLPROOF_ASSESS")
    entry = json.loads(c.get_exercise(args=["public-learning-sample-001"]).call())
    assert entry["assessment"] in {"MEETS_RUBRIC", "NEEDS_REVISION", "INCONCLUSIVE"}
    print(f"SKILLPROOF_FINAL_ASSESSMENT={entry['assessment']}", flush=True)
