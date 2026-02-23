from rest_framework import serializers

from .models import Exercise, Level, ReadingSession


class LevelSerializer(serializers.ModelSerializer):
    exercise_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Level
        fields = ["id", "name", "slug", "difficulty", "description", "cover_image", "order", "exercise_count"]


class ExerciseSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source="level.name", read_only=True)

    class Meta:
        model = Exercise
        fields = ["id", "title", "text", "max_score", "order", "level", "level_name", "created_at"]
        read_only_fields = ["id", "created_at"]


class ExerciseCreateSerializer(serializers.Serializer):
    level_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    text = serializers.CharField()
    max_score = serializers.FloatField(default=100.0, min_value=1.0, max_value=1000.0)
    order = serializers.IntegerField(default=0, min_value=0)


class ExerciseUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    text = serializers.CharField(required=False)
    max_score = serializers.FloatField(required=False, min_value=1.0, max_value=1000.0)
    order = serializers.IntegerField(required=False, min_value=0)


class FeedbackSerializer(serializers.Serializer):
    """Nested serializer for AI evaluation feedback within a session."""
    correct_words = serializers.ListField(child=serializers.CharField())
    incorrect_words = serializers.ListField(child=serializers.DictField())
    missing_words = serializers.ListField(child=serializers.CharField())
    suggestions = serializers.ListField(child=serializers.CharField(), required=False)
    overall_comment = serializers.CharField(required=False)


class ReadingSessionSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source="exercise.title", read_only=True)
    level_name = serializers.CharField(source="exercise.level.name", read_only=True)
    level_slug = serializers.CharField(source="exercise.level.slug", read_only=True)

    class Meta:
        model = ReadingSession
        fields = [
            "id", "exercise", "exercise_title", "level_name", "level_slug",
            "score", "accuracy", "transcription", "feedback",
            "duration_seconds", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class LevelStatsSerializer(serializers.Serializer):
    """Aggregated per-level stats for the student dashboard."""
    level_name = serializers.CharField(source="exercise__level__name")
    level_slug = serializers.CharField(source="exercise__level__slug")
    difficulty = serializers.CharField(source="exercise__level__difficulty")
    total_sessions = serializers.IntegerField()
    avg_score = serializers.FloatField()
    avg_accuracy = serializers.FloatField()
    best_score = serializers.FloatField()
    total_score = serializers.FloatField()
