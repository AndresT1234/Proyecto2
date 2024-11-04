# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import dfs_pb2 as dfs__pb2

GRPC_GENERATED_VERSION = '1.67.1'
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
        + f' but the generated code in dfs_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DataNodeStub(object):
    """Servicio para el DataNode
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StoreBlock = channel.unary_unary(
                '/dfs.DataNode/StoreBlock',
                request_serializer=dfs__pb2.StoreBlockRequest.SerializeToString,
                response_deserializer=dfs__pb2.StoreBlockResponse.FromString,
                _registered_method=True)
        self.RetrieveBlock = channel.unary_unary(
                '/dfs.DataNode/RetrieveBlock',
                request_serializer=dfs__pb2.RetrieveBlockRequest.SerializeToString,
                response_deserializer=dfs__pb2.RetrieveBlockResponse.FromString,
                _registered_method=True)


class DataNodeServicer(object):
    """Servicio para el DataNode
    """

    def StoreBlock(self, request, context):
        """Almacenar un bloque
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveBlock(self, request, context):
        """Recuperar un bloque
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StoreBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreBlock,
                    request_deserializer=dfs__pb2.StoreBlockRequest.FromString,
                    response_serializer=dfs__pb2.StoreBlockResponse.SerializeToString,
            ),
            'RetrieveBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveBlock,
                    request_deserializer=dfs__pb2.RetrieveBlockRequest.FromString,
                    response_serializer=dfs__pb2.RetrieveBlockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dfs.DataNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('dfs.DataNode', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DataNode(object):
    """Servicio para el DataNode
    """

    @staticmethod
    def StoreBlock(request,
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
            '/dfs.DataNode/StoreBlock',
            dfs__pb2.StoreBlockRequest.SerializeToString,
            dfs__pb2.StoreBlockResponse.FromString,
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
    def RetrieveBlock(request,
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
            '/dfs.DataNode/RetrieveBlock',
            dfs__pb2.RetrieveBlockRequest.SerializeToString,
            dfs__pb2.RetrieveBlockResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)