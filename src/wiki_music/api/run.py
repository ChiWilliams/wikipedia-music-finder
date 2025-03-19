import uvicorn

def main():
    uvicorn.run(
        "wiki_music.api.main:app",
        host="0.0.0.0",
        port=5000,
    )

if __name__ == "__main__":
    main() 