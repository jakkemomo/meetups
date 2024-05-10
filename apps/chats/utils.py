from channels.db import database_sync_to_async

from apps.chats.models import Chat


@database_sync_to_async
def get_chat_async(event_id):
    return Chat.objects.filter(pk=event_id).first()


@database_sync_to_async
def has_chat_permissions(user, chat):
    participants = chat.participants.all()
    return user in participants


list_chats_raw = '''
            SELECT 
                chats_chat.id,
                chats_chat.type,
                last_messages.message_text  as last_message_text,
                last_messages.created_by_id as last_message_created_by,
                last_messages.created_at    as last_message_created_at,
                CASE
                    WHEN last_messages.created_by_id = %s THEN 1 ELSE 0
                    END AS last_message_is_owner
            FROM chats_chat
            LEFT JOIN (
                SELECT 
                    chats_message.id,
                    chats_message.chat_id,
                    chats_message.message_text,
                    chats_message.created_by_id,
                    MAX(chats_message.created_at)
                        OVER (PARTITION BY chats_message.chat_id) AS created_at
                    FROM chats_message
                    WHERE chats_message.created_at in (
                        SELECT MAX(chats_message.created_at)
                        FROM chats_message
                        GROUP BY chats_message.chat_id
                    )
                    ORDER BY chats_message.id
            ) AS last_messages
            ON chats_chat.id = last_messages.chat_id
            WHERE chats_chat.id IN (
                SELECT chat_id 
                FROM chats_chat_participants 
                WHERE user_id = %s
                )
            ORDER BY chats_chat.id;
            '''
