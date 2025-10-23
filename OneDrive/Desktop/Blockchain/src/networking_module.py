import threading
import requests
import time
successCount = 0
failCount = 0
statusCodes = []
lock = threading.Lock()

def sendRequests(targetUrl, rps, timeout, duration, label):
    global successCount, failCount
    interval = 1.0 / rps
    endTime = time.perf_counter() + duration

    while time.perf_counter() < endTime:
        start = time.perf_counter()
        try:
            response = requests.get(targetUrl, timeout=timeout)
            with lock:
                successCount += 1
                statusCodes.append(f"{label}:{response.status_code}")
        except:
            with lock:
                failCount += 1
                statusCodes.append(f"{label}:Error")

        elapsed = time.perf_counter() - start
        sleepFor = interval - elapsed
        if sleepFor > 0:
            time.sleep(sleepFor)

def launchTrafficPhase(threadCount, targetUrl, rps, timeout, duration, label):
    threads = []
    for _ in range(threadCount):
        thread = threading.Thread(target=sendRequests, args=(targetUrl, rps, timeout, duration, label))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def runSimulation():
    targetUrl = "http://localhost:8000"
    rps = 2
    timeout = 3
    duration = 10

    print(" Starting normal traffic...")
    launchTrafficPhase(threadCount=10, targetUrl=targetUrl, rps=rps, timeout=timeout, duration=duration, label="Normal")

    print(" Launching attack traffic...")
    launchTrafficPhase(threadCount=40, targetUrl=targetUrl, rps=rps, timeout=timeout, duration=duration, label="Attack")

    print("\n Simulation Summary")
    print(f"✅ Successful requests: {successCount}")
    print(f"❌ Failed requests: {failCount}")
