"""GenLayer SDK Direct tests: in-process contract, storage, validator agreement."""
import json


def create(c, eid="exercise-001"):
    c.submit(
        eid,
        "Computer security fundamentals",
        "Describe two distinct reasons to use multi-factor authentication and explain why a password alone is insufficient.",
        "MFA adds a separate factor beyond a password and reduces risk if stolen passwords are reused or leaked."
    )


def mock(vm, answer):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*Check a learner response against a provided rubric.*",
                json.dumps({"assessment": answer}))


def test_register_read_public_record(direct_deploy):
    c = direct_deploy("contracts/SkillProof.py")
    create(c)
    entry = json.loads(c.get_exercise("exercise-001"))
    assert entry["assessment"] == "PENDING"
    assert entry["topic"] == "Computer security fundamentals"


def test_validator_consensus_accepts_agreement_rejects_disagreement(direct_vm, direct_deploy):
    c = direct_deploy("contracts/SkillProof.py")
    create(c)
    mock(direct_vm, "NEEDS_REVISION")
    c.assess("exercise-001")
    assert json.loads(c.get_exercise("exercise-001"))["assessment"] == "NEEDS_REVISION"
    assert direct_vm.run_validator() is True
    mock(direct_vm, "MEETS_RUBRIC")
    assert direct_vm.run_validator() is False


def test_authorization_duplicate_and_one_time_assessment(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/SkillProof.py")
    create(c)
    original_sender = direct_vm.sender
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only submitter can assess"):
        c.assess("exercise-001")
    direct_vm.sender = original_sender
    with direct_vm.expect_revert("Exercise already exists"):
        create(c)
    mock(direct_vm, "INCONCLUSIVE")
    c.assess("exercise-001")
    with direct_vm.expect_revert("Already assessed"):
        c.assess("exercise-001")


def test_bad_fields_and_missing_record(direct_vm, direct_deploy):
    c = direct_deploy("contracts/SkillProof.py")
    with direct_vm.expect_revert("Invalid text length"):
        c.submit("too", "AI", "Explain what the system should evaluate.", "A valid explanatory response with detail.")
    with direct_vm.expect_revert("Disallowed control characters"):
        c.submit("exercise-002", "Security", "Explain what the system should evaluate.", "This answer contains a hidden mark.\u202e")
    with direct_vm.expect_revert("Exercise not found"):
        c.get_exercise("missing")
