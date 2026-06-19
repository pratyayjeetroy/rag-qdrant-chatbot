import redis
from rq import Queue
from rq.worker import SimpleWorker   # 🔥 IMPORTANT

redis_conn = redis.Redis(host='localhost', port=6379)
queue = Queue("rag_queue", connection=redis_conn)

if __name__ == "__main__":
    print("🚀 Worker started (Windows mode)...")
    
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()