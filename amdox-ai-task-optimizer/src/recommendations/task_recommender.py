TASK_MAP = {
    "happy": {
        "moderate": ["Routine productive tasks", "Light Collaborative work"],
        "high": ["Creative tasks", "Team Meetings"]
    },
    "neutral": {
        "moderate": ["Routine Tasks"],
        "high": ["Regular work items", "Documentation"]
    },
    "sad": {
        "moderate": ["Low Pressure tasks", "Supportive activities"],
        "high" : ["Very light Individual tasks", "Supportive activities"]
    },
    "stressed": {
        "moderate": ["Reduce Workload", "Work on low-pressure tasks"],
        "high": ["Take Short Break", "Reschedule demanding tasks"]
    },
    "angry": {
        "moderate": ["Independent work"],
        "high": ["Cool-down break", "Avoid meetings"]
    }
}
STRESS_SOFT_THRESHOLD = 0.35
HIGH_CONF = 0.8
MODERATE_CONF = 0.6
LOW_CONF = 0.4

def recommend_task(final_emotion, confidence):

    # Special handling for stress
    if final_emotion == "stressed" and (HIGH_CONF >= confidence >= STRESS_SOFT_THRESHOLD):
        return {
            "emotion": "stressed",
            "confidence": confidence,
            "recommendation_level": "soft",
            "tasks": [
                "Reduce workload temporarily",
                "Focus on low-pressure tasks",
                "Take short breaks if needed"
            ]
        }

    # Low confidence → neutral-safe
    if confidence < MODERATE_CONF:
        neutral_tasks = TASK_MAP.get("neutral", {})
        if isinstance(neutral_tasks, dict):
            tasks = neutral_tasks.get("moderate", [])
        else:
            tasks = neutral_tasks
            
        return {
            "emotion": final_emotion,
            "confidence": confidence,
            "recommendation_level": "low",
            "tasks": tasks
        }
    
    # Moderate / High confidence
    level = "moderate" if confidence < HIGH_CONF else "high"
    emotion_tasks = TASK_MAP.get(final_emotion, TASK_MAP["neutral"])
    
    # Extract tasks based on confidence level
    if isinstance(emotion_tasks, dict):
        tasks = emotion_tasks.get(level, emotion_tasks.get("moderate", []))
    else:
        tasks = emotion_tasks
    
    return {
        "emotion": final_emotion,
        "confidence": confidence,
        "recommendation_level": level,
        "tasks": tasks
    }

# Sample testing
# if __name__ == "__main__":
#     print(recommend_task("neutral", 0.9))
#     print(recommend_task("sad", 0.3))
#     print(recommend_task("angry", 0.82))