"""Full v2 proof on public GenLayer Studionet, with receipt-safe RPC retry.

Both signers are created within THIS ONE test run (the suite changes them
between GitHub runs). Each signed write is submitted ONCE. We preserve the
transaction hash BEFORE polling so HTTP 504 cannot force resubmission.
"""
import hashlib
import json
import time

from gltest import get_contract_factory
from gltest.clients import get_gl_client
from gltest.assertions import tx_execution_succeeded


def transient(exc):
    message = str(exc)
    return any(x in message for x in (
        "Gateway", "504", "503", "502", "520", "522",
        "ConnectionError", "ReadTimeout", "timed out",
        "Request to",
    ))


def read_reliably(func, label):
    for attempt in range(18):
        try:
            return func()
        except Exception as exc:
            if not transient(exc) or attempt == 17:
                raise
            print(f"{label}_RPC_RETRY_{attempt+1}", flush=True)
            time.sleep(min(4 + attempt * 2, 18))
    raise AssertionError("Unreachable")


def signed_once(client, contract, method, args, account, label, consensus=False):
    # Do not automatically retry submission. A 504 during submission could
    # mask a real transaction; retry only after we have captured the hash.
    kwargs = {
        "address": contract.address,
        "function_name": method,
        "account": account,
        "args": args,
    }
    if consensus:
        kwargs["consensus_max_rotations"] = 4
    tx_hash = client.write_contract(**kwargs)
    print(f"{label}_TX_SUBMITTED={tx_hash}", flush=True)
    for poll in range(18):
        try:
            receipt = client.wait_for_transaction_receipt(
                transaction_hash=tx_hash,
                interval=10000,
                retries=80,
            )
            assert tx_execution_succeeded(receipt), f"{label} not accepted: {tx_hash}"
            print(f"{label}_TX={tx_hash}", flush=True)
            return tx_hash
        except Exception as exc:
            if not transient(exc) or poll == 17:
                raise
            print(f"{label}_WAIT_RPC_RETRY_{poll+1}", flush=True)
            time.sleep(min(4 + poll * 2, 18))
    raise AssertionError(f"{label} receipt not found: {tx_hash}")


def record(contract, exchange_id):
    return json.loads(str(read_reliably(
        lambda: contract.get_exchange(args=[exchange_id]).call(),
        "EXCHANGE_READ",
    )))


def test_real_two_wallet_exchange(default_account, accounts):
    learner = next((
        account for account in accounts
        if str(account.address).lower() != str(default_account.address).lower()
    ), None)
    assert learner is not None, "A distinct learner wallet is required"
    contract = get_contract_factory("SkillProof").deploy(
        account=default_account,
        consensus_max_rotations=4,
        wait_interval=10000,
        wait_retries=120,
    )
    address = str(contract.address)
    assert address.startswith("0x") and len(address) == 42
    client = get_gl_client()
    print(f"SKILLPROOF_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)
    print(f"SKILLPROOF_V2_TEACHER={default_account.address}", flush=True)
    print(f"SKILLPROOF_V2_LEARNER={learner.address}", flush=True)
    offer_id = "live-mentor-offer-v2-01"
    exchange_id = "live-learning-pair-v2-01"
    signed_once(client, contract, "publish_offer", [
        offer_id, "Python unit testing",
        "A beginner-oriented 45-minute lesson covering how to write and test Python functions.",
        45,
    ], default_account, "SKILLPROOF_V2_OFFER")
    offer = json.loads(str(read_reliably(
        lambda: contract.get_offer(args=[offer_id]).call(), "OFFER_READ",
    )))
    assert offer["teacher"].lower() == str(default_account.address).lower()
    signed_once(client, contract, "request_exchange", [
        exchange_id, offer_id,
        "I want a beginner-oriented 45-minute lesson on writing and testing Python functions.",
    ], learner, "SKILLPROOF_V2_MATCH_CONSENSUS", consensus=True)
    initial = record(contract, exchange_id)
    print(f"SKILLPROOF_V2_MATCH_RESULT={initial['match_result']}", flush=True)
    assert initial["match_result"] == "MATCH"
    assert initial["state"] == "MATCHED"
    assert initial["learner"].lower() == str(learner.address).lower()
    assert initial["teacher"].lower() != initial["learner"].lower()
    digest = hashlib.sha256(
        b"SkillProof v2 public demonstration note agreed by mentor and learner."
    ).hexdigest()
    signed_once(client, contract, "attest_session", [exchange_id, digest],
                learner, "SKILLPROOF_V2_LEARNER_ATTESTATION")
    interim = record(contract, exchange_id)
    assert interim["state"] == "MATCHED"
    assert interim["learner_digest"] == digest
    assert interim["teacher_digest"] == ""
    signed_once(client, contract, "attest_session", [exchange_id, digest],
                default_account, "SKILLPROOF_V2_TEACHER_ATTESTATION")
    final = record(contract, exchange_id)
    assert final["state"] == "ATTESTED"
    assert final["teacher_digest"] == final["learner_digest"] == digest
    print(f"SKILLPROOF_V2_MATCHED_SESSION_SHA256={digest}", flush=True)
    print("SKILLPROOF_V2_FULL_TWO_WALLET_CHAIN_PROOF=PASS", flush=True)
