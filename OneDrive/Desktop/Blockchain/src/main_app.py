

from traffic_simulator import launchTrafficPhase
from detection_module import DetectionModule
from blockchain_logger import BlockchainLogger
from evaluation_module import EvaluationModule

import time

def simulate_and_log_traffic():
    # Initialize modules
    detector = DetectionModule()
    logger = BlockchainLogger()
    
    # Simulation parameters
    target_url = "http://localhost:8000"
    rps = 2
    timeout = 3
    duration = 10

    # Simulate Normal Traffic
    print("\n🚦 Starting Normal Traffic Phase...")
    for _ in range(10):
        ip = "192.168.1.10"
        detection_status = detector.check_traffic(ip)
        is_attack = detection_status == "detected"
        logger.create_block(ip, detection_status, is_attack)
        time.sleep(1.0 / rps)

    # Simulate Attack Traffic
    print("\n⚠️ Starting Attack Traffic Phase...")
    for _ in range(40):
        ip = "10.0.0.5"
        detection_status = detector.check_traffic(ip)
        is_attack = detection_status == "detected"
        logger.create_block(ip, detection_status, is_attack)
        time.sleep(0.1)

def evaluate_results():
    evaluator = EvaluationModule()
    metrics = evaluator.calculate_metrics()

    print("\n📊 Evaluation Metrics")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"True Positives: {metrics['true_positives']}")
    print(f"False Positives: {metrics['false_positives']}")
    print(f"False Negatives: {metrics['false_negatives']}")
    print(f"True Negatives: {metrics['true_negatives']}")
    print(f"Accuracy: {metrics['accuracy']:.2f}")
    print(f"Status: {metrics['status']}")

if __name__ == "__main__":
    print("🔧 Running Modular Traffic Simulation...")
    simulate_and_log_traffic()
    evaluate_results()
