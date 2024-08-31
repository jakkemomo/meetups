from channels.db import database_sync_to_async

from apps.chats.models import Chat


@database_sync_to_async
def get_chat_async(event_id):
    return Chat.objects.filter(pk=event_id).first()


@database_sync_to_async
def has_chat_permissions(user, chat):
    participants = chat.participants.all()
    return user in participants


list_chats_raw = """
            WITH last_messages AS (
                SELECT
                    cm.id,
                    cm.chat_id,
                    cm.message_text,
                    cm.created_by_id,
                    cm.created_at,
                    ROW_NUMBER() OVER (PARTITION BY cm.chat_id ORDER BY cm.created_at DESC) AS rn
                FROM
                    chats_message cm
            ),
            unread_messages AS (
                SELECT
                    chat_id,
                    COUNT(*) AS unread_message_counter
                FROM
                    chats_message
                WHERE
                    status = 'unread'
                GROUP BY
                    chat_id
            )
            SELECT
                cc.id,
                cc.type,
                lm.message_text AS last_message_text,
                lm.created_by_id AS last_message_created_by,
                lm.created_at AS last_message_created_at,
                CASE
                    WHEN lm.created_by_id = %s THEN 1 ELSE 0
                END AS last_message_is_owner,
                COALESCE(um.unread_message_counter, 0) AS unread_message_counter
            FROM
                chats_chat cc
            LEFT JOIN last_messages lm ON cc.id = lm.chat_id AND lm.rn = 1
            LEFT JOIN unread_messages um ON cc.id = um.chat_id
            WHERE
                cc.id IN (
                    SELECT chat_id
                    FROM chats_chat_participants
                    WHERE user_id = %s
                )
            ORDER BY
                cc.id;
            """
