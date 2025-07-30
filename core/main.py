from decouple import config
import sys
import uvicorn

from common.config import settings

if __name__ == "__main__":
    sys.path.insert(0, '..')
    port=settings.PORT
    uvicorn.run("core.app:app", host="0.0.0.0", port=port, reload=True)