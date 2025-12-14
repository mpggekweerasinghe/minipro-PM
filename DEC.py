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

# =====================================================
# 4. ARRIVAL PROCESS
# =====================================================

def arrival_generator(env, docks, metrics, interarrival_times, service_times):
    for _ in range(FARMERS_PER_DAY):
        env.process(farmer(env, docks, metrics, service_times))
        yield env.timeout(random.choice(interarrival_times))


def run_simulation(interarrival_times, workers_per_dock, service_times):
    env = simpy.Environment()

    capacity_per_dock = workers_per_dock // WORKERS_REQUIRED_PER_FARMER
    total_capacity = capacity_per_dock * ACTIVE_DOCKS

    docks = simpy.Resource(env, capacity=total_capacity)
    metrics = Metrics()

    env.process(arrival_generator(
        env, docks, metrics, interarrival_times, service_times
    ))

    env.run(until=SIM_TIME)

    utilization = metrics.busy_time / (total_capacity * SIM_TIME)

    return {
        "waiting": statistics.mean(metrics.waiting_times),
        "queue": statistics.mean(metrics.queue_lengths),
        "throughput": metrics.completed / SIM_TIME,
        "utilization": utilization * 100
    }

def experiment(interarrival_times, workers_per_dock, service_times):
    results = [
        run_simulation(interarrival_times, workers_per_dock, service_times)
        for _ in range(REPLICATIONS)
    ]

    return {
        "waiting": statistics.mean(r["waiting"] for r in results),
        "queue": statistics.mean(r["queue"] for r in results),
        "throughput": statistics.mean(r["throughput"] for r in results),
        "utilization": statistics.mean(r["utilization"] for r in results)
    }


def print_header():
    print("\n" + "=" * 68)
    print("DAMBULLA ECONOMIC CENTRE – DATA-CALIBRATED SIMULATION")

    print("System: 30-Dock Section (Avg. 26 Active Docks)")
    print("Simulation Horizon: 8 Hours (480 Minutes)")
    print("=" * 68)


def print_block(title, results):
    print("\n" + "-" * 68)
    print(f"SCENARIO: {title}")
    print("-" * 68)
    print(f"{'Mean Waiting Time':32s}: {results['waiting']:.2f} minutes")
    print(f"{'Mean Queue Length':32s}: {results['queue']:.2f} farmers")
    print(f"{'Throughput':32s}: {results['throughput']:.2f} farmers/min")
    print(f"{'Dock Utilization':32s}: {results['utilization']:.2f} %")

if __name__ == "__main__":

    print_header()

    # -------- BASELINE --------
    baseline = experiment(
        EMPIRICAL_INTERARRIVALS,
        BASE_WORKERS_PER_DOCK,
        BASE_SERVICE_TIMES
    )
    print_block("BASELINE (2 WORKERS, EMPIRICAL SERVICE)", baseline)

    # -------- MORE STAFF --------
    more_staff = experiment(
        EMPIRICAL_INTERARRIVALS,
        MORE_WORKERS_PER_DOCK,
        FAST_SERVICE_TIMES
    )
    print_block("MORE STAFF (4 WORKERS, FASTER SERVICE)", more_staff)

    # -------- ARRIVAL SMOOTHING --------
    smoothed_interarrivals = [x * 2 for x in EMPIRICAL_INTERARRIVALS]

    smoothing = experiment(
        smoothed_interarrivals,
        BASE_WORKERS_PER_DOCK,
        BASE_SERVICE_TIMES
    )
    print_block("ARRIVAL SMOOTHING (CONTROLLED ARRIVALS)", smoothing)