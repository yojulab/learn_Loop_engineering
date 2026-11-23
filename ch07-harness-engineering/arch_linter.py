"""제7장: Types -> Config -> Repo -> Service -> Runtime -> UI 계층 위반 탐지 및 수정 가이드 린터."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

LAYER_ORDER: list[str] = ["Types", "Config", "Repo", "Service", "Runtime", "UI"]
LAYER_INDEX: dict[str, int] = {name.lower(): idx for idx, name in enumerate(LAYER_ORDER)}


@dataclass
class LintViolation:
    file: str
    line: int
    from_layer: str
    to_layer: str
    violation_type: str
    fix_guide: str


def _detect_layer(rel_path: Path) -> str | None:
    for part in rel_path.parts:
        key = part.lower()
        if key in LAYER_INDEX:
            return LAYER_ORDER[LAYER_INDEX[key]]
    return None


def _extract_imported_modules(py_file: Path) -> list[tuple[int, str]]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
    imports: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append((node.lineno, node.module))
    return imports


def _resolve_target_layer(module_name: str) -> str | None:
    for segment in module_name.split("."):
        key = segment.lower()
        if key in LAYER_INDEX:
            return LAYER_ORDER[LAYER_INDEX[key]]
    return None


def check_architecture(root_dir: Path | str) -> list[LintViolation]:
    """지정 디렉터리 내 Python 파일의 계층 역방향/건너뛰기 의존 위반을 검사한다."""
    root = Path(root_dir)
    violations: list[LintViolation] = []
    if not root.is_dir():
        return violations

    for py_file in sorted(root.rglob("*.py")):
        rel = py_file.relative_to(root)
        from_layer = _detect_layer(rel)
        if from_layer is None:
            continue
        from_idx = LAYER_INDEX[from_layer.lower()]

        for lineno, mod in _extract_imported_modules(py_file):
            to_layer = _resolve_target_layer(mod)
            if to_layer is None or to_layer == from_layer:
                continue
            to_idx = LAYER_INDEX[to_layer.lower()]

            if to_idx > from_idx:
                violations.append(
                    LintViolation(
                        file=str(rel),
                        line=lineno,
                        from_layer=from_layer,
                        to_layer=to_layer,
                        violation_type="reverse_dependency",
                        fix_guide=(
                            f"여기가 틀렸으니 이렇게 고쳐라: {from_layer} 계층({rel}:{lineno})이 "
                            f"상위 {to_layer} 계층({mod})을 역참조하고 있습니다. "
                            f"공유 인터페이스를 Types 계층으로 내리거나 {to_layer} 계층에서 {from_layer}를 호출하도록 역전하세요."
                        ),
                    )
                )
            elif from_idx - to_idx > 1:
                expected_prev = LAYER_ORDER[from_idx - 1]
                violations.append(
                    LintViolation(
                        file=str(rel),
                        line=lineno,
                        from_layer=from_layer,
                        to_layer=to_layer,
                        violation_type="layer_skip",
                        fix_guide=(
                            f"여기가 틀렸으니 이렇게 고쳐라: {from_layer} 계층({rel}:{lineno})이 "
                            f"중간 계층을 건너뛰어 {to_layer} 계층({mod})을 직접 임포트했습니다. "
                            f"직전 인접 계층인 {expected_prev}를 통해 의존하도록 수정하세요."
                        ),
                    )
                )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="제7장 계층 아키텍처 린터")
    parser.add_argument("--root", required=True, help="검사할 앱 루트 경로")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    violations = check_architecture(args.root)
    if args.json:
        print(json.dumps([asdict(v) for v in violations], ensure_ascii=False, indent=2))
    else:
        if not violations:
            print(f"[ARCH-OK] No layer violations in {args.root}")
        else:
            for v in violations:
                print(f"[ARCH-VIOLATION] {v.file}:{v.line} ({v.violation_type}: {v.from_layer} -> {v.to_layer})")
                print(f"  -> {v.fix_guide}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
