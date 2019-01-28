import json
import requests
import tlog
from flask_restful import Resource

class RestEndpoint(Resource):
    def post(self):
        print("Got a thingy thing at the rest endpoint: ")

class RestTest():
    def __init__(self, testFileDict, consumerTopic, kafkaBrokers):
        self.testFileDict=testFileDict
        self.consumerTopic=consumerTopic
        self.kafkaBrokers=kafkaBrokers

    def test(self):
        tlog.info("Creating test cases...")
        tcList = []
        for inputFilename, expectedOutputFilename in self.testFileDict.items():
           inputData = json.loads(open(inputFilename, 'r').read())
           expectedOutputData = json.loads(open(expectedOutputFilename, 'r').read())
           tc = RestTestCase(inputData, expectedOutputData)
           tcList.append(tc)
        tlog.info("Test cases created.")

        # Send test data
        for index, testCase in enumerate(tcList, start=1):
           tlog.info("Sending REST request for test case %d/%d" % (index, len(tcList)))
           sendRESTRequest(json.dumps(testCase.input), self.kafkaBrokers)


class RestTestCase():
    def __init__(self, input, expectedOutput):
        self.input = input
        self.expectedOutput = expectedOutput

        mcin = str(input['tim']['msgCnt'])
        mcout = str(expectedOutput['payload']['data']['MessageFrame']['value']['TravelerInformation']['msgCnt'])
        assert mcin == mcout, "Message count input and output do not match: input=%s, output=%s" % (mcin, mcout)
        self.msgCnt = mcin

    def test(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(RestEndpoint, "/tim")
        app.run(port='8082')

        # Create interceptor server


        # Send test message

        # Wait for Response

        # Validate response

def sendRESTRequest(body, kafkaBrokers):
    response=requests.post('http://' + kafkaBrokers + ':8080/tim', data = body)
    tlog.info("Response code: " + str(response.status_code))
