"""Find, for each number of closures N, the set of candidate schools whose closure saves the most.

Trying every combination is impossible (31 candidates choose 7 is 2.6 million sets, each needing a
full evaluation), so the search is greedy with local improvement:
  for N = 1, 2, ...:
    1. add the one candidate that gives the highest net savings on top of the best (N-1)-set;
    2. then try swapping any closed school for any other candidate; keep the first swap that improves
       net savings by more than $1, and repeat until no swap helps.
This takes about ten minutes for N up to 30.
"""
IMPROVEMENT_THRESHOLD = 1.0   # dollars


def best_closure_sets(model, max_n, log=print):
    """{N: PlanResult} for N = 0..max_n."""
    candidates = model.candidates
    best = {0: model.evaluate([])}
    current = []
    for n in range(1, max_n + 1):
        # 1. greedy addition (ties go to the later name alphabetically, as in the original runs)
        value, addition = max((model.evaluate(current + [c]).net_savings, c) for c in candidates if c not in current)
        current = current + [addition]

        # 2. one-for-one swaps until none improves
        improved = True
        while improved:
            improved = False
            for out in list(current):
                for replacement in candidates:
                    if replacement in current:
                        continue
                    trial = [x for x in current if x != out] + [replacement]
                    trial_value = model.evaluate(trial).net_savings
                    if trial_value > value + IMPROVEMENT_THRESHOLD:
                        current, value, improved = trial, trial_value, True
                        break
                if improved:
                    break

        best[n] = model.evaluate(current)
        log(f"N={n:2d} net ${value / 1e6:6.2f}M  closed={current}")
    return best
