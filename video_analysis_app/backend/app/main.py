from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Video Insights API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    video_url: HttpUrl
    language: str = "zh"


class SummaryResponse(BaseModel):
    one_liner: str
    key_points: List[str]
    structured_summary: dict


class HotTopic(BaseModel):
    title: str
    source: str
    published_at: datetime
    relevance_reason: str


class AnalyzeResponse(BaseModel):
    task_id: str
    status: str
    created_at: datetime


class TaskResult(BaseModel):
    task_id: str
    status: str
    transcript: str
    summary: SummaryResponse
    hot_topics: List[HotTopic]


_FAKE_DB: dict = {}


@app.get("/health")
def health() -> dict:
    return {"ok": True, "timestamp": datetime.now(timezone.utc)}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def create_analysis_task(payload: AnalyzeRequest) -> AnalyzeResponse:
    task_id = str(uuid4())
    now = datetime.now(timezone.utc)
    _FAKE_DB[task_id] = {
        "task_id": task_id,
        "status": "completed",
        "transcript": f"这是来自 {payload.video_url} 的示例转写内容。",
        "summary": {
            "one_liner": "该视频主要讨论 AI 视频分析产品的构建路径。",
            "key_points": [
                "定义 MVP 功能：转写、摘要、热点。",
                "搭建异步任务流水线并存储分析结果。",
                "结合实时新闻做热点关联输出。",
            ],
            "structured_summary": {
                "background": "用户希望构建视频分析网站。",
                "arguments": "先做可用 MVP，再逐步增强实时热点能力。",
                "conclusion": "采用 API + 任务队列架构可快速迭代。",
            },
        },
        "hot_topics": [
            {
                "title": "多模态模型推动视频理解产品升级",
                "source": "Tech Daily",
                "published_at": now,
                "relevance_reason": "与视频理解和摘要生成直接相关。",
            },
            {
                "title": "企业加速部署 AI 内容分析平台",
                "source": "AI Weekly",
                "published_at": now,
                "relevance_reason": "与落地场景和商业化路径一致。",
            },
        ],
    }
    return AnalyzeResponse(task_id=task_id, status="completed", created_at=now)


@app.get("/api/tasks/{task_id}", response_model=TaskResult)
def get_task_result(task_id: str) -> TaskResult:
    task = _FAKE_DB.get(task_id)
    if not task:
        return TaskResult(
            task_id=task_id,
            status="not_found",
            transcript="",
            summary=SummaryResponse(
                one_liner="",
                key_points=[],
                structured_summary={},
            ),
            hot_topics=[],
        )
    return TaskResult(**task)
