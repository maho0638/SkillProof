"""Official GenLayer Direct tests for SkillProof's genuinely two-party protocol."""
import json


def offer(contract):
    contract.publish_offer(
        "offer-python-001", "Python programming",
        "A forty-minute introduction to writing Python functions, loops and tests.",
        40,
    )


def mock(vm, compatible):
    vm.clear_mocks()
    vm.mock_llm(
        r"(?s).*You are matching a learner's stated learning GOAL.*",
        json.dumps({"compatible": compatible}),
    )


def request(contract, key="exchange-001"):
    contract.request_exchange(
        key, "offer-python-001",
        "I want to learn to write Python functions and automated tests.",
    )


def test_teacher_learner_two_signatures_and_matching_digest(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    teacher = direct_vm.sender
    offer(c)
    direct_vm.sender = direct_bob
    mock(direct_vm, True)
    request(c)
    entry = json.loads(c.get_exchange("exchange-001"))
    assert entry["state"] == "MATCHED"
    assert entry["teacher"] != entry["learner"]
    assert direct_vm.run_validator() is True
    mock(direct_vm, False)
    assert direct_vm.run_validator() is False

    digest = "a" * 64
    c.attest_session("exchange-001", digest)
    assert json.loads(c.get_exchange("exchange-001"))["state"] == "MATCHED"
    direct_vm.sender = teacher
    c.attest_session("exchange-001", digest)
    receipt = json.loads(c.get_exchange("exchange-001"))
    assert receipt["state"] == "ATTESTED"
    assert receipt["teacher_digest"] == receipt["learner_digest"] == digest
    with direct_vm.expect_revert("Exchange not open for attestation"):
        c.attest_session("exchange-001", digest)


def test_negative_match_never_creates_credential(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    offer(c)
    direct_vm.sender = direct_bob
    mock(direct_vm, False)
    request(c)
    assert json.loads(c.get_exchange("exchange-001"))["state"] == "NOT_COMPATIBLE"
    with direct_vm.expect_revert("Exchange not open for attestation"):
        c.attest_session("exchange-001", "b" * 64)


def test_conflicting_digest_does_not_complete_session(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    teacher = direct_vm.sender
    offer(c)
    direct_vm.sender = direct_bob
    mock(direct_vm, True)
    request(c)
    c.attest_session("exchange-001", "1" * 64)
    direct_vm.sender = teacher
    with direct_vm.expect_revert("Session digests disagree"):
        c.attest_session("exchange-001", "2" * 64)
    assert json.loads(c.get_exchange("exchange-001"))["state"] == "MATCHED"
    c.attest_session("exchange-001", "1" * 64)
    assert json.loads(c.get_exchange("exchange-001"))["state"] == "ATTESTED"


def test_self_exchange_duplicate_and_missing_record(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    offer(c)
    with direct_vm.expect_revert("Offer already exists"):
        offer(c)
    with direct_vm.expect_revert("Self-exchange is forbidden"):
        request(c)
    direct_vm.sender = direct_bob
    mock(direct_vm, True)
    request(c)
    with direct_vm.expect_revert("Exchange already exists"):
        request(c)
    with direct_vm.expect_revert("Offer not found"):
        c.get_offer("missing")
    with direct_vm.expect_revert("Exchange not found"):
        c.get_exchange("missing")


def test_invalid_input_and_untrusted_ai_output(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    with direct_vm.expect_revert("Session duration out of range"):
        c.publish_offer("offer-invalid", "Python programming", "Practical foundations of Python.", 3)
    with direct_vm.expect_revert("Disallowed control characters"):
        c.publish_offer("offer-invalid", "Python programming", "Practical foundations of Python.\u202e", 40)
    offer(c)
    direct_vm.sender = direct_bob
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r"(?s).*You are matching a learner's stated learning GOAL.*",
                       json.dumps({"compatible": "true"}))
    with direct_vm.expect_revert("Invalid match response"):
        request(c)
    mock(direct_vm, True)
    request(c)
    with direct_vm.expect_revert("Invalid SHA-256 digest"):
        c.attest_session("exchange-001", "not-a-sha256")
    with direct_vm.expect_revert("Invalid SHA-256 digest"):
        c.attest_session("exchange-001", "A" * 64)
