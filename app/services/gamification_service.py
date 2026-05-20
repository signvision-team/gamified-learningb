from app.config.database import get_db_connection


# =========================
# STEP 5: XP SYSTEM
# =========================
def calculate_xp(is_correct, confidence):
    if not is_correct:
        return 0

    base_xp = 10
    bonus = int(confidence * 10)

    return base_xp + bonus


# =========================
# STEP 6: LEVEL SYSTEM
# =========================
def update_level(cursor, user_id):
    cursor.execute("SELECT xp FROM users WHERE id=%s", (user_id,))
    xp = cursor.fetchone()[0]

    new_level = (xp // 100) + 1

    cursor.execute(
        "UPDATE users SET level=%s WHERE id=%s",
        (new_level, user_id)
    )


# =========================
# STEP 7: STREAK SYSTEM
# =========================
def update_streak(cursor, user_id, is_correct):
    cursor.execute("SELECT streak FROM users WHERE id=%s", (user_id,))
    streak = cursor.fetchone()[0]

    if is_correct:
        streak += 1
    else:
        streak = 0

    cursor.execute(
        "UPDATE users SET streak=%s WHERE id=%s",
        (streak, user_id)
    )


# =========================
# STEP 8: BADGE SYSTEM
# =========================
def give_badge(cursor, user_id, badge_name):
    cursor.execute("""
        SELECT id FROM badges
        WHERE user_id=%s AND badge_name=%s
    """, (user_id, badge_name))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO badges (user_id, badge_name, description)
            VALUES (%s, %s, %s)
        """, (user_id, badge_name, "Unlocked achievement"))


def check_badges(cursor, user_id):
    cursor.execute("SELECT xp, streak FROM users WHERE id=%s", (user_id,))
    xp, streak = cursor.fetchone()

    if xp >= 100:
        give_badge(cursor, user_id, "XP Master")

    if streak >= 5:
        give_badge(cursor, user_id, "Streak Master")


# =========================
# MAIN ENGINE FUNCTION
# =========================
def process_prediction(data):
    user_id = data["user_id"]
    sign_name = data["sign_name"]
    predicted = data["predicted"]
    confidence = data["confidence"]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: correctness
        is_correct = (sign_name == predicted)

        # Step 2: XP
        xp = calculate_xp(is_correct, confidence)

        # Step 3: update XP
        cursor.execute("""
            UPDATE users
            SET xp = xp + %s
            WHERE id = %s
        """, (xp, user_id))

        # Step 4–6
        update_level(cursor, user_id)
        update_streak(cursor, user_id, is_correct)
        check_badges(cursor, user_id)

        # Step 7: session save
        cursor.execute("""
            INSERT INTO sessions (user_id, sign_name, is_correct, confidence, xp_earned)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, sign_name, is_correct, confidence, xp))

        conn.commit()

        return {
            "correct": is_correct,
            "xp_earned": xp,
         "total_xp": current_user_xp,   # NEW
         "level": new_level,           # NEW
          "streak": streak  
        }

    finally:
        cursor.close()
        conn.close()