# Placeholder for Messaging API Endpoints (Phase 2: Online Payments & Communication)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /messages (Send a message to another user)
def send_message():
    # TODO: Implement logic to send a message.
    # sender_id from authenticated user.
    # Request body:
    #   - receiver_id (User ID of the recipient)
    #   - content (text of the message)
    #   - lease_id (Optional: FK to Lease, to associate message with a specific tenancy context)
    #   - (Future: attachment_ids if implementing separate attachment uploads)
    # Creates a Message record.
    # Sets Message.has_attachments if relevant (though actual attachment handling might be more complex).
    # Generates a conversation_id if not already existing for this pair + context.
    # Triggers a NEW_MESSAGE_ALERT Notification for the receiver_id.
    # Response: Details of the sent message.
    pass

# GET /messages/conversations (List all conversations for the user)
def list_user_conversations():
    # TODO: Implement logic to list all message conversations for the authenticated user.
    # A conversation is typically grouped by (sender_id, receiver_id, lease_id (optional)).
    # Response: List of conversation summaries, e.g.,
    #   { conversation_id, other_user_details, last_message_snippet, last_message_at, unread_count }
    # Supports pagination.
    pass

# GET /messages/conversation/{conversation_id} (Get messages for a specific conversation)
def get_conversation_messages(conversation_id: str):
    # TODO: Implement logic to retrieve messages for a specific conversation_id.
    # Authenticated user must be part of the conversation.
    # Marks messages as 'read' (updates Message.read_at) for the requesting user in this conversation upon retrieval.
    # Supports pagination for messages within the conversation.
    # Response: List of Message records (content, sender_id, sent_at, read_at, has_attachments).
    pass

# GET /messages/unread-summary (Get summary of unread messages for the user)
def get_unread_message_summary():
    # TODO: Implement logic to get a summary of unread messages for the authenticated user.
    # Response: { total_unread_count, unread_conversations: [{ conversation_id, unread_count, last_message_sender }] }
    pass

# (POST /messages/attachments - Future endpoint if handling attachments separately)
# def upload_message_attachment():
#   # TODO: Handle file upload, create Attachment record, link to message_id (possibly after message is created).
#   pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.message import Message
#
# message_bp = Blueprint('messages', __name__, url_prefix='/messages')
#
# @message_bp.route('', methods=['POST'])
# def send_message_route():
#     # data = request.get_json() # { receiver_id, content, lease_id (optional) }
#     # sender_id = get_current_user_id()
#     # Call send_message logic
#     return jsonify({"message": "Message sent", "message_id": 1, "conversation_id": "..."}), 201
#
# @message_bp.route('/conversations', methods=['GET'])
# def list_conversations_route():
#     # user_id = get_current_user_id()
#     # Call list_user_conversations logic
#     return jsonify([{"conversation_id": "conv1", "last_message_snippet": "Okay", "unread_count": 1}]), 200
#
# @message_bp.route('/conversation/<string:conversation_id>', methods=['GET'])
# def get_messages_route(conversation_id):
#     # user_id = get_current_user_id()
#     # Call get_conversation_messages logic, ensure user is part of conversation_id
#     return jsonify([{"message_id": 10, "content": "Hello!", "sender_id": 1, "sent_at": "..."}]), 200
#
# @message_bp.route('/unread-summary', methods=['GET'])
# def get_unread_summary_route():
#     # user_id = get_current_user_id()
#     # Call get_unread_message_summary logic
#     return jsonify({"total_unread_count": 5, "unread_conversations": []}), 200
