from rewardkit import criteria
for n in ("gate_present", "unsafe_all_blocked", "clean_reference_passes", "false_rejects_within_allowance"):
    criteria.check(n, name=n)
