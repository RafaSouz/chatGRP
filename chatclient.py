from asyncio import Future
from email import message
import threading
import logging
import grpc
import service_pb2
import service_pb2_grpc
import const
from concurrent import futures

class client(service_pb2_grpc.chatServicer):

    def sendMsg(self, request, context):
        print(f"New message to: {request.nameD} From: {request.nameR}") 
        print("\n")
        print(f"Text: {request.text}") 
        print("\n")
        return service_pb2_grpc.Empty()

def receiveMsg():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_chatServicer_to_server(sendMsg(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def run(nameR,nameD,ipD,text):

    #print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    # print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel(const.CHAT_SERVER_HOST) as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.sendMsg(service_pb2.MessageData(nameR=nameR,nameD=nameD,ipD=ipD,text=text))

def inputdados():
    nameD = input("ENTER DESTINATION: ")
    text = input("ENTER MESSAGE: ")
    return nameD,text

if __name__ == '__main__':
    logging.basicConfig()

    recv = threading.Thread(target=receiveMsg)
    recv.daemon = False
    recv.start()

    nameR = str(sys.argv[1])
    print(nameR)

    while True:
        nameD,text=inputdados()
        ipD = const.registry[nameD]
        run(nameR,nameD,ipD,text)
