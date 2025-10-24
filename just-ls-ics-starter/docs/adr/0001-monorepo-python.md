# ADR-0001: Monorepo 与 Python 为主

- 决策：采用 monorepo，主语言选 Python，保留 C++/UI 子目录占位。
- 背景：硬件控制与调度链路以 Python 异步生态更成熟（FastAPI/Pydantic/asyncio），
  天文生态（Astropy 等）匹配度高。
- 影响：统一依赖、CI、发布流程；C++ 驱动可作为可选模块集成。
