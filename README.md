# Work Order API

用于 Backend V2 工程实践的工单系统后端项目。

当前项目已建立 FastAPI 应用、配置管理、测试分层、类型检查、代码检查和覆盖率检查基线。

## 环境要求

- Python 3.12
- uv

检查工具版本：

```bash
python3 --version
uv --version
```

## 安装依赖

```bash
uv sync --all-groups
```

项目会使用当前目录下的 `.venv`，不需要手动激活虚拟环境。

## 本地配置

根据配置模板创建本地环境变量文件：

```bash
cp .env.example .env
```

当前支持的环境变量：

| 环境变量 | 默认值 | 用途 |
|---|---|---|
| `WORK_ORDER_APP_NAME` | `Work Order API` | FastAPI 应用名称 |
| `WORK_ORDER_ENVIRONMENT` | `development` | 当前运行环境 |

`.env` 可能包含本地配置或敏感信息，不应提交到 Git。

`.env.example` 只保存变量名称和安全的示例值，可以提交到 Git。

## 启动服务

```bash
uv run uvicorn app.main:app --reload
```

服务默认运行在：

```text
http://127.0.0.1:8000
```

验证健康检查：

```bash
curl http://127.0.0.1:8000/health
```

预期响应：

```json
{"status":"ok"}
```

## 运行全部检查

```bash
./scripts/check.sh
```

该脚本依次执行：

1. Ruff 代码检查
2. Ruff 格式检查
3. Pyright 类型检查
4. pytest 测试
5. coverage 覆盖率统计

其中任何一项失败，脚本都会立即停止并返回失败状态。

## 单独运行检查

代码检查：

```bash
uv run ruff check app tests
```

格式检查：

```bash
uv run ruff format --check app tests
```

类型检查：

```bash
uv run pyright
```

运行测试：

```bash
uv run pytest -v
```

运行测试并查看覆盖率：

```bash
uv run pytest --cov=app --cov-report=term-missing
```

## 测试分层

```text
tests/
├── unit/          单元测试
├── integration/   接口集成测试
└── database/      数据库集成测试
```

当前测试包括：

- 配置加载单元测试
- `/health` 接口集成测试

数据库集成测试将在加入数据库功能后补充。

## 项目结构

```text
work-order-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── scripts/
│   └── check.sh
├── tests/
│   ├── unit/
│   │   └── test_config.py
│   ├── integration/
│   │   └── test_health.py
│   └── database/
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

## 当前状态

Backend V2 的 B2-0 工程基线正在建设中。

已经完成：

- FastAPI 最小应用
- Pydantic Settings 配置加载
- 单元测试与接口集成测试目录
- Ruff 代码和格式检查
- Pyright 类型检查
- pytest 与覆盖率报告
- 本地统一检查脚本

下一步：

- 添加 GitHub Actions
- 在提交和 Pull Request 时自动运行统一检查
- 主动制造一次 CI 失败并定位原因