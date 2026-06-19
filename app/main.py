from fastapi import FastAPI
import redis
from rq import Queue
from rq.job import Job
from app.tasks import process_query

app = FastAPI()

redis_conn = redis.Redis(host='localhost', port=6379)
queue = Queue("rag_queue", connection=redis_conn)


@app.post("/ask")
def ask(query: str):
    job = queue.enqueue(process_query, query)

    return {
        "job_id": job.id,
        "status": job.get_status()   # 🔥 better than hardcoded
    }


@app.get("/result/{job_id}")
def get_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return {"status": "not_found"}

    # 🔥 Proper status handling
    if job.is_queued:
        return {"status": "queued"}

    if job.is_started:
        return {"status": "processing"}

    if job.is_finished:
        return {
            "status": "finished",
            "result": job.result
        }

    if job.is_failed:
        return {
            "status": "failed",
            "error": str(job.exc_info)
        }

    return {"status": "unknown"}