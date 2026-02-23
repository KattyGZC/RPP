"""
Management command to populate the database with initial sample data.
Run with: python manage.py seed_data
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.accounts.models import UserRole
from apps.exercises.models import DifficultyLevel, Exercise, Level


class Command(BaseCommand):
    help = "Populate database with initial levels, exercises, and demo users"

    def handle(self, *args, **kwargs):
        self._create_levels()
        self._create_exercises()
        self._create_demo_users()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def _create_levels(self):
        levels_data = [
            {"name": "Básico", "slug": "basico", "difficulty": DifficultyLevel.BASIC,
             "description": "Textos cortos y simples para comenzar a leer.", "order": 1},
            {"name": "Intermedio", "slug": "intermedio", "difficulty": DifficultyLevel.INTERMEDIATE,
             "description": "Textos de mediana complejidad con vocabulario más variado.", "order": 2},
            {"name": "Avanzado", "slug": "avanzado", "difficulty": DifficultyLevel.ADVANCED,
             "description": "Textos más largos con estructuras gramaticales complejas.", "order": 3},
        ]
        for data in levels_data:
            Level.objects.get_or_create(slug=data["slug"], defaults=data)
        self.stdout.write("  ✓ Levels created")

    def _create_exercises(self):
        basic = Level.objects.get(slug="basico")
        intermediate = Level.objects.get(slug="intermedio")
        advanced = Level.objects.get(slug="avanzado")

        exercises = [
            # Básico
            {"level": basic, "title": "El sol", "order": 1, "max_score": 100,
             "text": "El sol sale por la mañana. El sol da luz y calor. Nos gusta el sol."},
            {"level": basic, "title": "Mi mascota", "order": 2, "max_score": 100,
             "text": "Tengo un perro. Mi perro se llama Toby. Toby es muy juguetón y alegre."},
            {"level": basic, "title": "La familia", "order": 3, "max_score": 100,
             "text": "Mi mamá me quiere mucho. Mi papá trabaja duro. Somos una familia feliz."},
            # Intermedio
            {"level": intermediate, "title": "El río", "order": 1, "max_score": 150,
             "text": "El río baja de las montañas con mucha fuerza. El agua es limpia y cristalina. Los niños van a nadar cuando hace calor."},
            {"level": intermediate, "title": "Las estaciones", "order": 2, "max_score": 150,
             "text": "El año tiene cuatro estaciones. En verano hace mucho calor. En invierno hace frío y a veces nieva. La primavera es la estación de las flores."},
            # Avanzado
            {"level": advanced, "title": "El ciclo del agua", "order": 1, "max_score": 200,
             "text": "El agua de los océanos se evapora con el calor del sol. Luego sube al cielo y forma las nubes. Cuando las nubes se enfrían, el agua cae como lluvia o nieve. Así comienza el ciclo del agua de nuevo."},
        ]

        for data in exercises:
            Exercise.objects.get_or_create(
                level=data["level"], title=data["title"],
                defaults=data
            )
        self.stdout.write("  ✓ Exercises created")

    def _create_demo_users(self):
        # Demo teacher
        teacher, created = User.objects.get_or_create(
            username="profesor_demo",
            defaults={
                "first_name": "María",
                "last_name": "García",
                "email": "profesor@demo.com",
            }
        )
        if created:
            teacher.set_password("demo1234")
            teacher.save()
            teacher.profile.role = UserRole.TEACHER
            teacher.profile.save()

        # Demo student
        student, created = User.objects.get_or_create(
            username="estudiante_demo",
            defaults={
                "first_name": "Carlos",
                "last_name": "López",
                "email": "estudiante@demo.com",
            }
        )
        if created:
            student.set_password("demo1234")
            student.save()

        self.stdout.write("  ✓ Demo users created")
        self.stdout.write("    Teacher: profesor_demo / demo1234")
        self.stdout.write("    Student: estudiante_demo / demo1234")
