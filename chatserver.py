from asyncio import Future
from importlib.resources import Package
import grpc
import service_pb2
import service_pb2_grpc
import const
from concurrent import futures

class serverChat (service_pb2_grpc.chatServicer):
    
    def receiveMsg(nameD,nameR,text,ipD):
        print(f"From: {nameR}") 
        print('\n')
        print(f"To: {nameD}") 
        print('\n')
        print(f"Say: {text}") 
        print('\n')
        with grpc.insecure_channel(ipD) as channel:
            stub = service_pb2_grpc.MessageStub(channel)
            response = stub.SendMessage(service_pb2.MessageData(nameR=nameR,nameD=nameD,ipD=ipD,text=text))
            return service_pb2_grpc.Empty()

    def sendMsg(self, request, context):
        receiveMsg(request.nameD, request.nameR, request.text, request.ipD)
        return service_pb2_grpc.Empty()


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_chatServicer_to_server(serverChat(), server)
    server.add_insecure_port('[::]:50051')
    print('Server open!')
    server.start()
    server.wait_for_termination()
    
