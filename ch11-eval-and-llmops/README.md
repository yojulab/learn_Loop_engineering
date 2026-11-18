# 제11장. 프로덕션의 눈과 저울: 평가(Eval)와 LLMOps

## 1. 단원 학습 목표 & 12대 스택 4계층 위치

- **학습 목표 1**: `Launch → Observe → Evaluate → Improve` 4단계 LLMOps 개선 루프를 구축한다.
- **학습 목표 2**: `production` 라벨 교체만으로 앱 재배포 없이 프롬프트를 교체·롤백하는 `seed_prompts.py` 및 `compile_prompt`를 구현한다.
- **학습 목표 3**: 규칙 기반·정답/LLM-as-a-Judge·안전성 3종 Eval 평가기(`evaluator.py`)로 품질 회귀를 차단한다.
- **학습 목표 4**: 외부 Langfuse 키 없이도 로컬 JSONL 폴백(`langfuse_ops.py`)으로 트레이스·점수·회귀 비교를 재현한다.

| 계층 (Layer) | 12대 스택 요소 | 본 단원의 핵심 구현 |
| :--- | :--- | :--- |
| **Layer 4. 위임과 검증** | ⑫ Eval & LLMOps | `support-assistant/seed_prompts.py`, `prompting.py`, `evaluator.py`, `langfuse_ops.py`, `regression_compare.py` |

## 2. 아키텍처 다이어그램 (Mermaid)

```mermaid
flowchart LR
    T["SupportTicket"] --> F["langfuse_ops (production 라벨 조회)"]
    F --> C["prompting.compile_prompt"]
    C --> A["응답 생성 (오프라인 폴백)"]
    A --> E["evaluator (3종 Eval 채점)"]
    E --> L["Trace / Score JSONL 기록"]
    L --> R["regression_compare (버전 비교)"]
```

## 3. 디렉터리 및 소스 파일 구조

- 정식 경로: `ch11-eval-and-llmops/support-assistant/`
- 도서 본문 `💻 Git 예제` 호환 경로: `ch11/support-assistant/` (`-> ../ch11-eval-and-llmops/support-assistant`)

| 파일 | 역할 |
| :--- | :--- |
| `models.py` | `SupportTicket`, `PromptRecord`, `EvalReport` |
| `langfuse_ops.py` | Langfuse 연동 인터페이스 + 오프라인 로컬 JSONL 폴백 |
| `seed_prompts.py` | `support-answer` v1(`production`) / v2(`candidate`) 시드 등록 |
| `prompting.py` | `compile_prompt(prompt, ticket: SupportTicket) -> str` |
| `evaluator.py` | 규칙 기반·정답/Judge·안전성 3종 Eval 평가기 |
| `regression_compare.py` | 버전 간 품질 점수·통과율·지연·비용 회귀 비교기 |

## 4. 컨테이너 실행 & 테스트 명령어

```bash
cd /apps/learn_hermes_engineering
python3 ch11-eval-and-llmops/support-assistant/regression_compare.py
python3 -m unittest discover -s ch11-eval-and-llmops/support-assistant/tests -p "test_*.py" -v
```

## 5. 핵심 체크리스트

- [ ] `LANGFUSE_PUBLIC_KEY` 미설정 시에도 로컬 JSONL 폴백 모드로 모든 기능이 동작하는가?
- [ ] `promote_label("support-answer", version=2, label="production")`로 무배포 교체가 동작하는가?
- [ ] `regression_compare.py`가 버전별 평균 점수와 통과율 차이를 리포트하는가?
