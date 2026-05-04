# Video Analysis Website Starter

这是一个可快速启动的 MVP 脚手架，包含：

- `backend/`：FastAPI 接口（视频分析任务、summary、热点返回）
- `frontend/`：简易静态页面，调用后端接口展示结果

## 运行后端

```bash
cd video_analysis_app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端地址：`http://127.0.0.1:8000`

## 运行前端

直接用任意静态服务器打开：

```bash
cd video_analysis_app/frontend/src
python -m http.server 5500
```

前端地址：`http://127.0.0.1:5500`

## 当前页面能力

- 深色控制台 UI
- 分析任务加载状态和错误提示
- 摘要结果卡片化展示（一句话、关键要点、结构化总结）
- 热点关联列表展示（来源、时间、关联原因）

## 下一步建议

1. 接入真实 ASR（Whisper / 第三方语音服务）
2. 增加任务队列（Celery + Redis）
3. 热点改为实时抓取 + 向量检索
4. 增加用户登录和历史记录
