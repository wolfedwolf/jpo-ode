import argparse
import os
import sys
import rest_test
import kafka_test
import tlog

DOCKER_HOST_IP=os.getenv('DOCKER_HOST_IP')
assert DOCKER_HOST_IP != None, "Failed to get DOCKER_HOST_IP from environment variable"

def main():
    tlog.info("Starting test routine")
    parser = argparse.ArgumentParser(description="ODE test harness")
    parser.add_argument('test_type', type=str, help='Required test type "rest" or "kafka"')
    args = parser.parse_args()
    assert args.test_type != None, "Required argument 'test_type' omitted"
    testType = args.test_type

    # Create test
    testFileDict={
      "tim1_input.json": "tim1_output.json"
    }
    timBroadcastTopic='topic.J2735TimBroadcastJson'

    if testType == "rest":
        tlog.info("Testing as rest app")
        testCase = rest_test.RestTest(testFileDict, timBroadcastTopic, DOCKER_HOST_IP)
    elif testType == "kafka":
        tlog.info("Testing as kafka app")
        testCase = kafka_test.KafkaTest(testFileDict, timBroadcastTopic, DOCKER_HOST_IP)
    else:
        tlog.info("Unknown test type: <%s>, expected <%s> or <%s>"%(testType, "rest", "kafka"))
        sys.exit(1)

    testCase.test()

if __name__ == "__main__":
    main()
