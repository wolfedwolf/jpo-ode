import json
import queue
import requests
import threading
import time
import tlog
from kafka import KafkaConsumer

class KafkaTest():
    def __init__(self, testFileDict, consumerTopic, kafkaBrokers):
        self.testFileDict=testFileDict
        self.consumerTopic=consumerTopic
        self.kafkaBrokers=kafkaBrokers

    def test(self):
        tlog.info("Test routine started...")
        msgQueue=queue.Queue()

        tlog.info("Creating Kafka listener thread...")
        kafkaListenerThread=threading.Thread(target=listenToKafkaTopic,args=(self.consumerTopic,msgQueue, len(self.testFileDict), self.kafkaBrokers),)
        kafkaListenerThread.start()
        tlog.info("Kafka listener created.")

        tlog.info("Waiting for broker connection...")
        time.sleep(5)

        tlog.info("Creating test cases...")
        tcList = []
        for inputFilename, expectedOutputFilename in self.testFileDict.items():
           inputData = json.loads(open(inputFilename, 'r').read())
           expectedOutputData = json.loads(open(expectedOutputFilename, 'r').read())
           tc = KafkaTestCase(inputData, expectedOutputData)
           tcList.append(tc)
        tlog.info("Test cases created.")

        # Send test data
        for index, testCase in enumerate(tcList, start=1):
           tlog.info("Sending REST request for test case %d/%d" % (index, len(tcList)))
           sendRESTRequest(json.dumps(testCase.input), self.kafkaBrokers)

        # Perform validation
        tlog.info("Request sending complete.")

        tlog.info("Waiting for all messages to be received...")
        kafkaListenerThread.join()
        tlog.info("All messages received.")

        tlog.info("Validating output...")
        validate(tcList, msgQueue)
        tlog.info("Output validated.")

        tlog.info("All tests have passed.")
        tlog.info("Testing complete.")


class KafkaTestCase:
    def __init__(self, input, expectedOutput):
        self.input = input
        self.expectedOutput = expectedOutput

        mcin = str(input['tim']['msgCnt'])
        mcout = str(expectedOutput['payload']['data']['MessageFrame']['value']['TravelerInformation']['msgCnt'])
        assert mcin == mcout, "Message count input and output do not match: input=%s, output=%s" % (mcin, mcout)
        self.msgCnt = mcin

def sendRESTRequest(body, kafkaBrokers):
    response=requests.post('http://' + kafkaBrokers + ':8080/tim', data = body)
    tlog.info("Response code: " + str(response.status_code))

def listenToKafkaTopic(topic, msgQueue, expectedMsgCount, kafkaBrokers):
   tlog.info("Listening on topic: " + topic)
   consumer=KafkaConsumer(topic, bootstrap_servers=kafkaBrokers+':9092')
   msgsReceived=0
   for msg in consumer:
       msgsReceived += 1
       tlog.info(str(msgsReceived))
       msgQueue.put(msg)
       if msgsReceived >= expectedMsgCount:
           return

def createOutputList(fileDict):
    outputList=[]
    for infile, outfile in fileDict.items():
        outfileData=json.load(open(outfile, 'r').read())
        outputList.append(outfileData)
    return outputList

def findOutputFile(msgCnt, fileDict):
    for outfile in fileDict.queue:
        if json.loads(outfile.value)['payload']['data']['MessageFrame']['value']['TravelerInformation']['msgCnt'] == msgCnt:
            return outfile
    return None

def validate(testCaseList, actualMsgQueue):
    assert len(testCaseList) == actualMsgQueue.qsize(), "Input list length does not match output list length, input: %d, output: %d" % (len(testCaseList), actualMsgQueue.qsize())
    for msg in actualMsgQueue.queue:
        # Find corresponding output file
        msgCnt=json.loads(msg.value)['payload']['data']['MessageFrame']['value']['TravelerInformation']['msgCnt']
        expectedOutputFile=findOutputFile(msgCnt, actualMsgQueue)
        assert expectedOutputFile != None, "Unable to find matching output file for input file msgCnt=%s" % str(msgCnt)
        assert msg.value == expectedOutputFile.value, "Input file does not match expected output: expected <%s> but got <%s>" % (msg.value, expectedOutputFile.value)
