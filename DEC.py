import simpy
import random
import statistics

# =====================================================
# 1. PARAMETERS DERIVED FROM REAL DATASET
# =====================================================

SIM_TIME = 480                  # minutes (5:00 a.m. – 1:00 p.m.)
REPLICATIONS = 10
FARMERS_PER_DAY = 450

# Average active docks from dataset (Day 1–4)
ACTIVE_DOCKS = 26

# Empirical inter-arrival times (minutes)
EMPIRICAL_INTERARRIVALS = [
    0.5, 0.5, 1.0, 1.5, 0.5, 1.0, 0.5, 1.0,
    0.5, 0.3, 1.0, 1.0, 0.7, 0.3, 0.5,
    1.0, 0.5, 1.0, 0.5
]

# Empirical service times (minutes) from dataset
BASE_SERVICE_TIMES = [40, 45, 50, 55, 60, 65, 70, 75, 80]
FAST_SERVICE_TIMES = [30, 35, 40, 45, 50]

# Workers
WORKERS_REQUIRED_PER_FARMER = 2
BASE_WORKERS_PER_DOCK = 2
MORE_WORKERS_PER_DOCK = 4

# Coordination / setup delay (realistic)
SETUP_DELAY = 3

# =====================================================
# 2. METRICS CLASS
# =====================================================

class Metrics:
    def __init__(self):
        self.waiting_times = []
        self.queue_lengths = []
        self.busy_time = 0.0
        self.completed = 0

# =====================================================
# 3. FARMER PROCESS
# =====================================================

def farmer(env, docks, metrics, service_times):
    arrival_time = env.now
    metrics.queue_lengths.append(len(docks.queue))

    with docks.request() as request:
        yield request

        wait = env.now - arrival_time
        metrics.waiting_times.append(wait)

        # Setup / coordination delay
        yield env.timeout(SETUP_DELAY)

        service_time = random.choice(service_times)
        start = env.now
        yield env.timeout(service_time)

        metrics.busy_time += env.now - start
        metrics.completed += 1