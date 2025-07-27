from decouple import config
import sys
import uvicorn

if __name__ == "__main__":
    sys.path.insert(0, '..')
    port = int(config('PORT'))
    uvicorn.run("core.app:app", host="0.0.0.0", port=port, reload=True)