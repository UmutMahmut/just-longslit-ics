# 贡献指南

- 分支：使用 trunk-based 或 `feature/*` 分支，PR 合并到 `main`。
- 提交规范：遵循 Conventional Commits（如 `feat:`, `fix:`）。
- 代码规范：Ruff 格式化 + Lint，Mypy 做静态类型检查。
- 测试：每个模块需附带 pytest 单测；CI 会执行 lint/type/test。
- ADR：重要架构决策请记录在 `docs/adr/`。
