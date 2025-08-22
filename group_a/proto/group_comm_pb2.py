
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'group_a/proto/group_comm.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1egroup_a/proto/group_comm.proto\x12\x07group_a\"J\n\x0eMessageRequest\x12\x11\n\tsender_id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0clamport_time\x18\x03 \x01(\x03\"6\n\x0cMessageReply\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x14\n\x0clamport_time\x18\x02 \x01(\x03\"\'\n\x0f\x45lectionMessage\x12\x14\n\x0c\x63\x61ndidate_id\x18\x01 \x01(\x05\"#\n\x0eVictoryMessage\x12\x11\n\tleader_id\x18\x01 \x01(\x05\"\"\n\x0fResponseMessage\x12\x0f\n\x07success\x18\x01 \x01(\x08\"#\n\x10HeartbeatRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\"\"\n\x11HeartbeatResponse\x12\r\n\x05\x61live\x18\x01 \x01(\x08\x32\x8d\x02\n\nGroupComms\x12=\n\x0bSendMessage\x12\x17.group_a.MessageRequest\x1a\x15.group_a.MessageReply\x12>\n\x08\x45lection\x12\x18.group_a.ElectionMessage\x1a\x18.group_a.ResponseMessage\x12<\n\x07Victory\x12\x17.group_a.VictoryMessage\x1a\x18.group_a.ResponseMessage\x12\x42\n\tHeartbeat\x12\x19.group_a.HeartbeatRequest\x1a\x1a.group_a.HeartbeatResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'group_a.proto.group_comm_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MESSAGEREQUEST']._serialized_start=43
  _globals['_MESSAGEREQUEST']._serialized_end=117
  _globals['_MESSAGEREPLY']._serialized_start=119
  _globals['_MESSAGEREPLY']._serialized_end=173
  _globals['_ELECTIONMESSAGE']._serialized_start=175
  _globals['_ELECTIONMESSAGE']._serialized_end=214
  _globals['_VICTORYMESSAGE']._serialized_start=216
  _globals['_VICTORYMESSAGE']._serialized_end=251
  _globals['_RESPONSEMESSAGE']._serialized_start=253
  _globals['_RESPONSEMESSAGE']._serialized_end=287
  _globals['_HEARTBEATREQUEST']._serialized_start=289
  _globals['_HEARTBEATREQUEST']._serialized_end=324
  _globals['_HEARTBEATRESPONSE']._serialized_start=326
  _globals['_HEARTBEATRESPONSE']._serialized_end=360
  _globals['_GROUPCOMMS']._serialized_start=363
  _globals['_GROUPCOMMS']._serialized_end=632

