"""
AI-Assisted Priority Recommendation Engine.
Computes priorityScore = (0.4 * urgency) + (w_difficulty * difficulty_norm) + (0.3 * effort_norm).
Uses user-specific difficulty weight when available and produces explainable recommendations.
"""

from datetime import date
from typing import List, Tuple

# Default weights (urgency, difficulty, effort)
DEFAULT_URGENCY_WEIGHT = 0.4
DEFAULT_DIFFICULTY_WEIGHT = 0.3
DEFAULT_EFFORT_WEIGHT = 0.3


def _urgency(days_left: float) -> float:
    """Urgency rises as the deadline approaches; overdue and due-today tasks are critical."""
    if days_left is None:
        return 0.0
    if days_left <= 0:
        return 1.0
    if days_left <= 1:
        return 0.95
    if days_left <= 3:
        return 0.8
    if days_left <= 7:
        return 0.55
    if days_left <= 14:
        return 0.3
    return 0.1


def _normalize_difficulty(d: int) -> float:
    """Map difficulty 1-5 to 0-1 (higher = harder)."""
    if d is None:
        return 0.5
    return max(0.0, min(1.0, (d - 1) / 4.0))


def _normalize_effort(hours: float, max_hours: float = 20.0) -> float:
    """Map effort hours to 0-1 scale (capped at max_hours)."""
    if hours is None or hours <= 0:
        return 0.0
    return min(1.0, hours / max_hours)


def compute_priority_score(
    days_left: float,
    difficulty: int,
    effort_hours: float,
    difficulty_weight: float = DEFAULT_DIFFICULTY_WEIGHT,
) -> float:
    """
    Compute priority score for one assignment.
    priorityScore = (0.4 * urgency) + (difficulty_weight * difficulty_norm) + (effort_weight * effort_norm).
    """
    difficulty_weight = max(0.0, min(0.5, difficulty_weight or DEFAULT_DIFFICULTY_WEIGHT))
    effort_weight = max(0.0, min(0.5, 1.0 - DEFAULT_URGENCY_WEIGHT - difficulty_weight))
    return (
        (DEFAULT_URGENCY_WEIGHT * _urgency(days_left))
        + (difficulty_weight * _normalize_difficulty(difficulty))
        + (effort_weight * _normalize_effort(effort_hours))
    )


def get_days_left(deadline, today=None):
    """Return days until deadline (can be negative if past)."""
    if today is None:
        today = date.today()
    if hasattr(deadline, "date"):
        deadline = deadline.date()
    delta = deadline - today
    return delta.days


def priority_label(assignment, score: float, today=None) -> str:
    """Convert a numeric score into a student-friendly priority label."""
    days_left = get_days_left(assignment.deadline, today)
    if days_left <= 1 or score >= 0.7:
        return "Critical"
    if days_left <= 3 or score >= 0.5:
        return "High"
    if days_left <= 7 or score >= 0.3:
        return "Medium"
    return "Low"


def explain_priority(assignment, today=None) -> str:
    """Explain why an assignment is recommended, using deadline, effort, and difficulty."""
    days_left = get_days_left(assignment.deadline, today)
    effort = assignment.estimated_effort_hours or 0
    difficulty = assignment.difficulty or 1

    if days_left < 0:
        timing = f"it is overdue by {abs(days_left)} day{'s' if abs(days_left) != 1 else ''}"
    elif days_left == 0:
        timing = "it is due today"
    elif days_left == 1:
        timing = "the deadline is tomorrow"
    else:
        timing = f"the deadline is in {days_left} days"

    reasons = [timing]
    if effort >= 8:
        reasons.append("the estimated effort is high")
    elif effort >= 4:
        reasons.append("it needs a moderate amount of time")

    if difficulty >= 4:
        reasons.append("the difficulty is high")
    elif difficulty == 3:
        reasons.append("the difficulty is moderate")

    return "Recommended because " + " and ".join(reasons) + "."


def recommended_order(assignments: list, today=None, difficulty_weight: float = DEFAULT_DIFFICULTY_WEIGHT) -> List[Tuple]:
    """
    Sort assignments by priority score descending.
    assignments: list of objects with .deadline, .difficulty, .estimated_effort_hours.
    Returns list of (assignment, priority_score) tuples, highest score first.
    """
    if today is None:
        today = date.today()
    scored = []
    for a in assignments:
        days_left = get_days_left(a.deadline, today)
        score = compute_priority_score(
            days_left,
            a.difficulty,
            a.estimated_effort_hours,
            difficulty_weight=difficulty_weight,
        )
        scored.append((a, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
