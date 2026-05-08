from app.config.database import get_db_connection


def get_levels(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT xp FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    user_xp = user["xp"]

    cursor.execute("SELECT * FROM levels ORDER BY id")
    levels = cursor.fetchall()

    result = []

    for level in levels:
        if user_xp >= level["unlock_xp"]:
            status = "completed"
        else:
            status = "locked"

        result.append({
            "id": level["id"],
            "title": level["title"],
            "desc": level["description"],
            "status": status
        })

    return result


def get_level_content(level_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT sign_name, image_url, video_url
        FROM learning_content
        WHERE level_id=%s
    """, (level_id,))

    return cursor.fetchall()