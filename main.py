from fastapi import FastAPI

app = FastAPI(
    title="📱 Requests App Service",
    description="The service part of the diploma project by Ramil Bashirov",
    version="0.1.0"
)

@app.get(path="/")
def main():
    return "Hello World!"



if __name__ == "__main__":
    main()
