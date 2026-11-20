# `dockers/` — Loop Engineering 실습 환경 (Docker Compose)

Langfuse(LLM 관측·프롬프트 관리) + PostgreSQL + 앱 컨테이너(Python 3.13 · Claude Code CLI · Antigravity CLI(`agy`) · langfuse SDK)를 한 번에 올립니다.
호스트 포트는 게시하지 않으며, 볼륨 경로와 주요 환경 변수는 모두 `.env`에서 설정합니다.

## 1. 구성

| 서비스 | 이미지 / 빌드 | 역할 |
| :--- | :--- | :--- |
| `db_postgres` | `postgres:16` | Langfuse 전용 DB (`POSTGRES_DATA_DIR`에 영속화) |
| `langfuse` | `langfuse/langfuse:2` (Docker Hub) | Trace 수집 · 프롬프트 관리 (조직·프로젝트·API Key 자동 생성) |
| `app` | `Dockerfile` (Python 3.13 + Node.js) | `claude` · `agy` CLI, `langfuse` SDK, 저장소 코드 실행 환경 |

`app`에서 Langfuse 접속 주소는 `http://langfuse:3000`(내부 네트워크)입니다.

## 2. 실행

```bash
cd dockers
cp .env.example .env          # 최초 1회. 시크릿은 openssl rand -hex 32 로 교체 권장
docker compose up -d --build
docker compose ps
docker compose exec app bash  # 앱 컨테이너 진입 (작업 디렉터리: /apps/learn_Loop_engineering)
```

컨테이너 안에서:

```bash
claude --version                                  # Claude Code CLI
agy --version                                     # Antigravity CLI
claude                                            # 최초 1회 로그인 (또는 .env 의 ANTHROPIC_API_KEY)
python3 scripts/verify_chapters.py --all          # 전 단원 통합 검증
python3 ch11/support-assistant/trace_to_prompt.py --demo --json
```

종료/정리:

```bash
docker compose down            # 컨테이너 종료 (볼륨 데이터 유지)
docker compose down -v         # 동일 + 익명 볼륨 제거 (bind 경로 데이터는 호스트에 남음)
```

## 3. `.env` 주요 항목

| 항목 | 설명 | 기본값 |
| :--- | :--- | :--- |
| `APP_SOURCE_DIR` | 실습 코드 마운트 경로 (`dockers/` 기준 상대 경로 가능) | `..` |
| `POSTGRES_DATA_DIR` | Langfuse DB 데이터 경로 | `./volumes/postgres` |
| `CLAUDE_HOST_DIR` | Claude CLI 로그인·설정 영속화 경로 | `./volumes/claude` |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` | DB 계정 | `admin` / `admin123` |
| `LANGFUSE_NEXTAUTH_SECRET` / `LANGFUSE_SALT` | Langfuse 시크릿 (필수) | `.env.example`의 안내값 교체 |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` | 초기 프로젝트 API Key 이자 SDK 접속 키 | `pk-lf-loop-engineering-public` / `sk-lf-loop-engineering-secret` |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY` | LLM 키 (비우면 `offline-fallback`) | 빈 값 |
| `AGENT_PLATFORM` | `auto` · `claude` · `chatgpt` · `gemini` · `offline` | `auto` |

> `.env`는 API 키가 들어갈 수 있으므로 git에서 제외되어 있습니다. 저장소에는 `.env.example`만 포함됩니다.
> `*_BASE_URL`, `*_MODEL`은 값이 있을 때만 주석을 해제하세요. 빈 값으로 선언하면 어댑터 기본값을 덮어씁니다.

## 4. Langfuse 화면 확인 (선택)

포트를 게시하지 않으므로 브라우저 접속이 필요할 때만 임시 포워딩을 사용합니다.

```bash
docker run --rm -p 3000:3000 --network learn_loop_engineering_default \
  alpine/socat TCP-LISTEN:3000,fork,reachaddr TCP:langfuse:3000
# 브라우저: http://localhost:3000  (admin@example.com / admin123456)
```

## 5. 참고

- 기존 `ch11-eval-and-llmops/support-assistant/litellm_proxy/`의 LiteLLM Proxy는 별도 구성이며, 이 Compose에는 포함되지 않습니다.
- 앱 컨테이너는 `PYTHONDONTWRITEBYTECODE=1`로 실행되어 호스트 저장소에 `__pycache__`를 만들지 않습니다.
