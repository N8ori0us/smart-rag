/smart-rag-search/ (Isolated Repository for your RAG Application)
├── .gitignore (Filters out Python virtual envs and IDE metadata)
├── backend/ (Docker-ized Python core running on the Proxmox host)
│ ├── docker-compose.yml (Pins Python 3.11-slim and maps local volumes)
│ └── app/
│ └── rag_core.py (Handles chunking, parsing, and OpenRouter API calls)
└── mac-manager/ (Native Apple Swift App building inside Xcode)
└── GUDEngineManager.xcodeproj
