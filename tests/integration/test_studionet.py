"""Manual public Studionet proof for SkillProof v2 (not previous version)."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, tag):
    receipt = call.transact(consensus_max_rotations=4, wait_interval=10000, wait_retries=50)
    assert tx_execution_succeeded(receipt), f"{tag}: {receipt.get('hash', '')}"
    print(f"{tag}_TX={receipt.get('hash', '')}", flush=True)


def test_public_skill_exchange(default_account):
    c = get_contract_factory("SkillProof").deploy(
        account=default_account, consensus_max_rotations=4,
    )
    address = str(c.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"SKILLPROOF_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)
    confirmed(c.publish_offer(args=[
        "public-offer-001", "Python testing",
        "A guided session about creating small functions and writing basic automated tests.",
        45,
    ]), "SKILLPROOF_V2_PUBLISH")
    # Two distinct accounts are required. Direct SDK checks perform the
    # entire cross-wallet handshake; this live test verifies safe deployment.
    result = json.loads(c.get_offer(args=["public-offer-001"]).call())
    assert result["skill"] == "Python testing"
    print("SKILLPROOF_V2_PUBLIC_OFFER_READBACK=PASS", flush=True)
