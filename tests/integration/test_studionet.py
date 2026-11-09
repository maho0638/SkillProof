"""Public Studionet proof: full consensus-based match and TWO wallet attestations."""
import hashlib
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, tag, consensus=False):
    kwargs = dict(wait_interval=10000, wait_retries=100)
    if consensus:
        kwargs["consensus_max_rotations"] = 4
    receipt = call.transact(**kwargs)
    assert tx_execution_succeeded(receipt), f"{tag}: {receipt.get('hash', '')}"
    print(f"{tag}_TX={receipt.get('hash', '')}", flush=True)
    return receipt


def state(contract, key):
    return json.loads(str(contract.get_exchange(args=[key]).call()))


def test_full_peer_exchange(default_account, accounts):
    learner = next((
        account for account in accounts
        if str(account.address).lower() != str(default_account.address).lower()
    ), None)
    assert learner is not None, "A second independent Studionet wallet is required"
    contract = get_contract_factory("SkillProof").deploy(
        account=default_account, consensus_max_rotations=4,
    )
    assert len(str(contract.address)) == 42
    learner_contract = contract.connect(learner)
    print(f"SKILLPROOF_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{contract.address}", flush=True)
    print(f"SKILLPROOF_V2_TEACHER={default_account.address}", flush=True)
    print(f"SKILLPROOF_V2_LEARNER={learner.address}", flush=True)
    confirmed(contract.publish_offer(args=[
        "public-offer-v2-001", "Python functions and tests",
        "An introductory 45-minute lesson on writing and testing Python functions for beginners.",
        45,
    ]), "SKILLPROOF_V2_OFFER")
    offer = json.loads(str(contract.get_offer(args=["public-offer-v2-001"]).call()))
    assert offer["teacher"].lower() == str(default_account.address).lower()
    confirmed(learner_contract.request_exchange(args=[
        "public-exchange-v2-001", "public-offer-v2-001",
        "I want an introductory lesson on writing and testing Python functions for beginners.",
    ]), "SKILLPROOF_V2_MATCH_CONSENSUS", consensus=True)
    result = state(contract, "public-exchange-v2-001")
    print(f"SKILLPROOF_V2_MATCH_RESULT={result['match_result']}", flush=True)
    assert result["match_result"] == "MATCH"
    assert result["state"] == "MATCHED"
    assert result["teacher"].lower() != result["learner"].lower()
    assert result["learner"].lower() == str(learner.address).lower()
    # Both wallets must attest the SAME hash; neither can finalize unilaterally.
    digest = hashlib.sha256(b"SkillProof-v2 public example: Python functions and tests lesson completed with mutual assent.").hexdigest()
    confirmed(learner_contract.attest_session(args=["public-exchange-v2-001", digest]),
              "SKILLPROOF_V2_LEARNER_ATTESTATION")
    mid = state(contract, "public-exchange-v2-001")
    assert mid["state"] == "MATCHED" and mid["learner_digest"] == digest
    assert mid["teacher_digest"] == ""
    confirmed(contract.attest_session(args=["public-exchange-v2-001", digest]),
              "SKILLPROOF_V2_TEACHER_ATTESTATION")
    final = state(contract, "public-exchange-v2-001")
    assert final["state"] == "ATTESTED"
    assert final["teacher_digest"] == final["learner_digest"] == digest
    print(f"SKILLPROOF_V2_SESSION_SHA256={digest}", flush=True)
    print("SKILLPROOF_V2_TWO_WALLET_FINAL_STATE=ATTESTED", flush=True)
