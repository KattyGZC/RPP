# Read Praxis Project

Plataforma web de **práctica de lectura en español con evaluación por inteligencia artificial**. Los estudiantes leen textos en voz alta y reciben retroalimentación detallada basada en transcripción de audio con Whisper y análisis NLP.

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| Autenticación | JWT (djangorestframework-simplejwt) |
| Base de datos | PostgreSQL 15 |
| Cache | Redis 7 |
| IA — Transcripción | OpenAI Whisper (local, gratuito) |
| IA — Evaluación | spaCy + rapidfuzz (NLP local) |
| IA — Feedback rico | Claude / OpenAI (opcional, via .env) |
| Frontend | React 18 + TypeScript + Vite |
| Estilos | Tailwind CSS |
| Estado | Zustand + TanStack Query |
| Infraestructura | Docker + docker-compose |

---

## Arquitectura

```
RPP/
├── backend/
│   ├── config/
│   │   └── settings/          # base.py / development.py / production.py
│   ├── apps/
│   │   ├── accounts/          # Usuarios, perfiles, roles (Student/Teacher)
│   │   ├── exercises/         # Niveles, ejercicios, sesiones de lectura
│   │   └── evaluation/        # Motor de IA (Strategy Pattern)
│   │       └── providers/
│   │           ├── base.py           # Interfaces abstractas
│   │           ├── whisper_provider.py  # Whisper local (default)
│   │           ├── nlp_provider.py      # spaCy + rapidfuzz (default)
│   │           ├── claude_provider.py   # Anthropic Claude (opcional)
│   │           └── openai_provider.py   # OpenAI (opcional)
│   └── core/                  # Excepciones, paginación, permisos, responses
└── frontend/
    └── src/
        ├── api/               # Clientes HTTP tipados
        ├── hooks/             # Custom hooks (useAuth, useExercises, useMediaRecorder)
        ├── store/             # Estado global (Zustand)
        ├── components/        # UI reutilizable, layout, exercises, dashboard
        └── pages/             # Páginas por ruta
```

### Patrones de Diseño Aplicados

| Patrón | Dónde | Por qué |
|--------|-------|---------|
| **Repository** | `apps/*/repositories.py` | Desacopla la lógica de negocio del ORM |
| **Service Layer** | `apps/*/services.py` | Centraliza reglas de negocio, vistas delgadas |
| **Strategy** | `evaluation/providers/` | Intercambiar proveedor de IA con un cambio en `.env` |
| **Factory** | `evaluation/factory.py` | Crea el proveedor correcto según la configuración |
| **Observer** | `accounts/signals.py` | Crea perfil automáticamente al registrar usuario |

---

## Inicio Rápido (Docker)

### Prerrequisitos
- Docker Desktop 4.x o Docker Engine + Compose V2

### 1. Clonar y configurar

```bash
git clone <repo-url> && cd RPP
cp .env.example .env.dev
# Edita .env.dev con tus valores si es necesario
```

### 2. Levantar entorno de desarrollo

```bash
make dev
# o directamente:
docker compose -f docker-compose.dev.yml up
```

### 3. Migrations y datos iniciales

```bash
make migrate
make seed
```

### 4. Acceder

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |

**Usuarios demo creados por `seed_data`:**
- Profesor: `profesor_demo` / `demo1234`
- Estudiante: `estudiante_demo` / `demo1234`

---

## Configuración de IA

El sistema usa el **patrón Strategy** para los proveedores de IA. Cambiar de proveedor no requiere modificar código, solo variables de entorno:

### Modo gratuito (default)
```env
AI_TRANSCRIPTION_PROVIDER=whisper_local
AI_FEEDBACK_PROVIDER=nlp_local
WHISPER_MODEL_SIZE=small   # tiny | base | small | medium
```

### Con Claude (feedback pedagógico rico)
```env
AI_FEEDBACK_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
```

### Con OpenAI (transcripción API + GPT feedback)
```env
AI_TRANSCRIPTION_PROVIDER=openai
AI_FEEDBACK_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

> **Nota sobre Whisper:** El primer inicio descarga el modelo (~244MB para `small`). Se cachea en un Docker volume para reinicios posteriores.

---

## API Reference

### Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login → tokens JWT + user |
| POST | `/api/auth/refresh/` | Refresca access token |
| POST | `/api/auth/logout/` | Blacklist refresh token |

### Accounts
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Registro de usuario |
| GET | `/api/accounts/me/` | Perfil del usuario autenticado |
| PATCH | `/api/accounts/me/` | Actualizar perfil |
| GET | `/api/accounts/students/` | Lista de estudiantes (teacher only) |

### Exercises
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/exercises/levels/` | Lista de niveles |
| GET | `/api/exercises/?level=<slug>` | Ejercicios por nivel |
| POST | `/api/exercises/` | Crear ejercicio (teacher only) |
| PATCH | `/api/exercises/<id>/` | Actualizar ejercicio |
| DELETE | `/api/exercises/<id>/` | Eliminar ejercicio (soft delete) |
| GET | `/api/exercises/progress/` | Progreso del usuario actual |
| GET | `/api/exercises/progress/<user_id>/` | Progreso de un estudiante (teacher only) |

### Evaluation
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/evaluation/evaluate/` | Evaluar audio (multipart: audio + exercise_id) |

---

## Comandos Útiles

```bash
make test           # Ejecutar todos los tests
make test-coverage  # Tests con reporte de cobertura
make lint           # Verificar estilo de código
make format         # Auto-formatear código (isort + black)
make shell          # Django shell
make psql           # PostgreSQL shell
make logs           # Tail logs de todos los servicios
make clean          # Eliminar containers y volúmenes
```

---

## Tests

```bash
# Backend
make test

# Cobertura
make test-coverage
```

Tests incluidos:
- `apps/accounts/tests/test_services.py` — Registro, validación de usuarios
- `apps/exercises/tests/test_services.py` — CRUD ejercicios, validación de puntajes
- `apps/evaluation/tests/test_evaluation.py` — Motor NLP, feedback, normalización

---

## Decisiones de Arquitectura

### ¿Por qué Whisper en lugar del browser Speech API?
El Web Speech API solo funciona en Chrome/Edge y requiere internet. Whisper es open-source, funciona offline, tiene soporte superior para español, y produce transcripciones ~40% más precisas.

### ¿Por qué PostgreSQL en lugar de SQLite?
SQLite es suficiente para desarrollo local, pero PostgreSQL ofrece concurrencia real, soporte nativo de JSONB para el campo `feedback`, y es el estándar para producción.

### ¿Por qué el patrón Repository?
Evita que las vistas y servicios dependan directamente del ORM. Facilita tests (se puede mockear el repositorio) y permite cambiar el motor de base de datos sin tocar la lógica de negocio.

### ¿Por qué separar `TranscriptionProvider` de `FeedbackProvider`?
Son responsabilidades distintas. Un cliente puede querer Whisper local para transcripción pero Claude para feedback, sin re-implementar nada. El patrón Strategy lo hace posible con cero cambios de código.
