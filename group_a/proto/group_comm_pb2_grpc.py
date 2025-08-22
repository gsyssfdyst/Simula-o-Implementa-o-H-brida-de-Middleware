
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from group_a.proto import group_comm_pb2 as group__a_dot_proto_dot_group__comm__pb2

GRPC_GENERATED_VERSION = '1.74.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in group_a/proto/group_comm_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GroupCommsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_unary(
                '/group_a.GroupComms/SendMessage',
                request_serializer=group__a_dot_proto_dot_group__comm__pb2.MessageRequest.SerializeToString,
                response_deserializer=group__a_dot_proto_dot_group__comm__pb2.MessageReply.FromString,
                _registered_method=True)
        self.Election = channel.unary_unary(
                '/group_a.GroupComms/Election',
                request_serializer=group__a_dot_proto_dot_group__comm__pb2.ElectionMessage.SerializeToString,
                response_deserializer=group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.FromString,
                _registered_method=True)
        self.Victory = channel.unary_unary(
                '/group_a.GroupComms/Victory',
                request_serializer=group__a_dot_proto_dot_group__comm__pb2.VictoryMessage.SerializeToString,
                response_deserializer=group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.FromString,
                _registered_method=True)
        self.Heartbeat = channel.unary_unary(
                '/group_a.GroupComms/Heartbeat',
                request_serializer=group__a_dot_proto_dot_group__comm__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=group__a_dot_proto_dot_group__comm__pb2.HeartbeatResponse.FromString,
                _registered_method=True)


class GroupCommsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendMessage(self, request, context):
        """Comunicação geral
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Election(self, request, context):
        """Algoritmo de Eleição Bully
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Victory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Heartbeat(self, request, context):
        """Heartbeat
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GroupCommsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=group__a_dot_proto_dot_group__comm__pb2.MessageRequest.FromString,
                    response_serializer=group__a_dot_proto_dot_group__comm__pb2.MessageReply.SerializeToString,
            ),
            'Election': grpc.unary_unary_rpc_method_handler(
                    servicer.Election,
                    request_deserializer=group__a_dot_proto_dot_group__comm__pb2.ElectionMessage.FromString,
                    response_serializer=group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.SerializeToString,
            ),
            'Victory': grpc.unary_unary_rpc_method_handler(
                    servicer.Victory,
                    request_deserializer=group__a_dot_proto_dot_group__comm__pb2.VictoryMessage.FromString,
                    response_serializer=group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.SerializeToString,
            ),
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=group__a_dot_proto_dot_group__comm__pb2.HeartbeatRequest.FromString,
                    response_serializer=group__a_dot_proto_dot_group__comm__pb2.HeartbeatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'group_a.GroupComms', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('group_a.GroupComms', rpc_method_handlers)



class GroupComms(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/group_a.GroupComms/SendMessage',
            group__a_dot_proto_dot_group__comm__pb2.MessageRequest.SerializeToString,
            group__a_dot_proto_dot_group__comm__pb2.MessageReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Election(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/group_a.GroupComms/Election',
            group__a_dot_proto_dot_group__comm__pb2.ElectionMessage.SerializeToString,
            group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Victory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/group_a.GroupComms/Victory',
            group__a_dot_proto_dot_group__comm__pb2.VictoryMessage.SerializeToString,
            group__a_dot_proto_dot_group__comm__pb2.ResponseMessage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/group_a.GroupComms/Heartbeat',
            group__a_dot_proto_dot_group__comm__pb2.HeartbeatRequest.SerializeToString,
            group__a_dot_proto_dot_group__comm__pb2.HeartbeatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
