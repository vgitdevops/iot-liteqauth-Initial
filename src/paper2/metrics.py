from __future__ import annotations
import math, statistics, time

def summarize(values):
    values = list(values)
    if not values:
        return {"n": 0}
    n = len(values)
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if n > 1 else 0.0
    # Approximate normal 95% CI for scaffold reporting; use a justified method in final paper.
    half = 1.96 * sd / math.sqrt(n) if n > 1 else 0.0
    return {"n": n, "mean": mean, "median": statistics.median(values),
            "stdev": sd, "ci95_low_approx": mean-half, "ci95_high_approx": mean+half,
            "min": min(values), "max": max(values)}

def time_call(fn, repeats=30):
    vals=[]
    for _ in range(repeats):
        t=time.perf_counter()
        fn()
        vals.append(time.perf_counter()-t)
    return summarize(vals)
