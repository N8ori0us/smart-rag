version 1
/smart-rag-search/
├── .gitignore (Filters out Python virtual envs and IDE metadata)
├── backend/ (Docker-ized Python core running on the Proxmox host)
│ ├── docker-compose.yml (Pins Python 3.11-slim and maps local volumes)
│ └── app/
│ └── rag_core.py (Handles chunking, parsing, and OpenRouter API calls)
└── mac-manager/ (Native Apple Swift App building inside Xcode)
└── GUDEngineManager.xcodeproj

version 1.1
/smart-rag/
├── LICENSE                (MIT Open-Source License)
├── .gitignore             (Filters environment masks and cache bloat)
├── README.md              (System engineering documentation)
├── backend/               (Docker-ized Python core running on the host)
│   ├── docker-compose.yml (Pins Python 3.11-slim container base)
│   └── app/
│       └── rag_core.py    (Handles chunking, vector parsing, and APIs)
└── mac-manager/           (Native Apple Swift desktop manager interface)
└── GUDEngineManager.xcodeproj