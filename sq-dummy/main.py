import random

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/scan")
async def scan():
    def random_issues():
        return {
            "total": random.randint(0, 100),
            "critical": random.randint(0, 100),
            "major": random.randint(0, 100),
            "minor": random.randint(0, 100),
        }

    return {
        "overall_coverage": round(random.uniform(0, 100), 1),
        "bugs": random_issues(),
        "code_smells": random_issues(),
        "vulnerabilities": random_issues(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
