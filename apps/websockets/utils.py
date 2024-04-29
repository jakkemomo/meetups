from channels.db import database_sync_to_async

from apps.websockets.models import Chat


@database_sync_to_async
def get_chat_async(event_id):
    return Chat.objects.filter(pk=event_id).first()


@database_sync_to_async
def has_chat_permissions(user, chat):
    participants = chat.participants.all()
    return user in participants


list_chats_raw = '''
            SELECT 
                websockets_chat.id,
                websockets_chat.type,
                last_messages.message_text  as last_message_text,
                last_messages.created_by_id as last_message_created_by,
                last_messages.created_at    as last_message_created_at,
                CASE
                    WHEN last_messages.created_by_id = %s THEN 1 ELSE 0
                    END AS last_message_is_owner
            FROM websockets_chat
            LEFT JOIN (
                SELECT 
                    websockets_message.id,
                    websockets_message.chat_id,
                    websockets_message.message_text,
                    websockets_message.created_by_id,
                    MAX(websockets_message.created_at)
                        OVER (PARTITION BY websockets_message.chat_id) AS created_at
                    FROM websockets_message
                    WHERE websockets_message.created_at in (
                        SELECT MAX(websockets_message.created_at)
                        FROM websockets_message
                        GROUP BY websockets_message.chat_id
                    )
                    ORDER BY websockets_message.id
            ) AS last_messages
            ON websockets_chat.id = last_messages.chat_id
            WHERE websockets_chat.id IN (
                SELECT chat_id 
                FROM websockets_chat_participants 
                WHERE user_id = %s
                )
ORDER BY websockets_chat.id;
            '''
