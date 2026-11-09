"""Resume verified v2 Studionet contract after transient 504 RPC in attestation flow.

Initial successful deployment + MATCH consensus run:
https://github.com/maho0638/SkillProof/actions/runs/42618038936

This test does not re-deploy. It resumes the SAME contract, reading the chain
before each write so already-finalized actions are not duplicated.
"""
import hashlib
import json
import time

from gltest import get_contract_factory
from gltest.clients import get_gl_client
from gltest.assertions import tx_execution_succeeded

ADDRESS = "0x7892Ba2bbD8397ec321Ac8254A793cEEc5A6b2B4"
EXCHANGE_ID = "public-exchange-v2-001"
EXPECTED_TEACHER = "0x5fb81463849fc524988Ef2074aD5A7E35eE43FFB"
EXPECTED_LEARNER = "0x41Dc85A8a665D96206899FEafE8BC390c3274726"
PENDING_LEARNER_TX = "0xa2101af591d33faa7d06bced74973ebb4e17b3c6292cc704c54d96aae5ecc740"
DIGEST = hashlib.sha256(
    b"SkillProof-v2 public example: Python functions and tests lesson completed with mutual assent."
).hexdigest()


def is_transient(exc):
    error = str(exc)
    return any(term in error for term in (
        "504", "502", "503", "520", "522", "Gateway", "timed out",
        "ConnectionError", "ReadTimeout", "Request to",
    ))


def with_rpc_retries(call, purpose, attempts=8):
    for index in range(attempts):
        try:
            return call()
        except Exception as exc:
            if not is_transient(exc) or index + 1 == attempts:
                raise
            print(f"{purpose}_TRANSIENT_RPC_ERROR_ATTEMPT_{index + 1}", flush=True)
            time.sleep(min(5 * (index + 1), 20))


def read(contract):
    return json.loads(str(with_rpc_retries(
        lambda: contract.get_exchange(args=[EXCHANGE_ID]).call(), "READ_STATE"
    )))


def attest(contract, actor, field):
    state = read(contract)
    if state["state"] == "ATTESTED":
        assert state["teacher_digest"] == state["learner_digest"] == DIGEST
        return
    if state[field]:
        assert state[field] == DIGEST
        print(f"{actor}_ALREADY_CONFIRMED_ON_CHAIN", flush=True)
        return
    assert state["state"] == "MATCHED"
    try:
        tx = contract.attest_session(args=[EXCHANGE_ID, DIGEST]).transact(
            wait_interval=10000, wait_retries=100,
        )
        assert tx_execution_succeeded(tx)
        print(f"SKILLPROOF_V2_{actor}_TX={tx.get('hash', '')}", flush=True)
    except Exception as exc:
        if not is_transient(exc):
            raise
        # A 504 may occur AFTER a transaction has already been submitted.
        # Do not blindly resubmit; first look for its confirmed chain effect.
        print(f"{actor}_SUBMITTED_RPC_UNAVAILABLE_VERIFY_BY_STATE", flush=True)
        for count in range(12):
            time.sleep(6)
            try:
                refreshed = read(contract)
                if refreshed[field] == DIGEST:
                    print(f"{actor}_VERIFIED_AFTER_RPC_TIMEOUT", flush=True)
                    return
            except Exception as rpc_exc:
                if not is_transient(rpc_exc):
                    raise
        raise RuntimeError(f"{actor} transaction outcome could not be confirmed; no duplicate was sent") from exc


def test_resume_two_wallet_attestation(default_account, accounts):
    learner = next((
        account for account in accounts
        if str(account.address).lower() == EXPECTED_LEARNER.lower()
    ), None)
    assert str(default_account.address).lower() == EXPECTED_TEACHER.lower(), (
        "Current signer changed; do not perform untrusted writes"
    )
    assert learner is not None, "Original learner signer unavailable"
    factory = get_contract_factory("SkillProof")
    teacher_contract = factory.build_contract(
        contract_address=ADDRESS, account=default_account,
    )
    learner_contract = teacher_contract.connect(learner)
    print(f"SKILLPROOF_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{ADDRESS}", flush=True)
    first = read(teacher_contract)
    assert first["teacher"].lower() == EXPECTED_TEACHER.lower()
    assert first["learner"].lower() == EXPECTED_LEARNER.lower()
    assert first["match_result"] == "MATCH"
    assert first["state"] in ("MATCHED", "ATTESTED")
    print(f"SKILLPROOF_V2_INITIAL_STATE={first['state']}", flush=True)
    print(f"SKILLPROOF_V2_LEARNER_PREVIOUS_TX={PENDING_LEARNER_TX}", flush=True)

    attest(learner_contract, "LEARNER_ATTESTATION", "learner_digest")
    mid = read(teacher_contract)
    assert mid["learner_digest"] == DIGEST
    attest(teacher_contract, "TEACHER_ATTESTATION", "teacher_digest")
    final = read(teacher_contract)
    assert final["state"] == "ATTESTED"
    assert final["teacher_digest"] == final["learner_digest"] == DIGEST
    print(f"SKILLPROOF_V2_FINAL_SHA256={DIGEST}", flush=True)
    print("SKILLPROOF_V2_TWO_WALLET_FINAL_STATE=ATTESTED", flush=True)
