# 🧠 Sentinel Media AI
### An Agentic Multimodal Intelligence Platform

**Sentinel Media AI** is a production-grade, agentic AI system that watches video, listens to audio, reasons over multimodal content, and enables intelligent decision-making through retrieval-augmented generation (RAG).

Unlike traditional transcription or summarization tools, Sentinel uses multiple collaborating AI agents to extract structured knowledge, detect risks, generate insights, and provide contextual, memory-aware conversations over long-form media.

---

## 🚀 Key Capabilities

* **🎬 Multimodal Ingestion:** Support for MP4, MP3, and direct YouTube links.
* **🎧 Advanced Speech-to-Text:** Accurate transcription with speaker identification and timestamp awareness.
* **🎥 Visual Understanding:** Scene-level video analysis to understand "what is happening" visually.
* **🧠 Agentic Reasoning:** Multi-agent collaboration to synthesize complex multimodal data.
* **⚠️ Risk & Sensitivity Detection:** Automated flagging of sensitive content or compliance risks.
* **🏷️ Knowledge Extraction:** Automated topic, entity, and intent extraction.
* **🔍 Hybrid Retrieval:** Elasticsearch-powered vector and keyword search.
* **💬 Contextual RAG Chat:** Interactive chat with memory specifically tuned to the processed media.
* **📊 Interactive UI:** Clean, intuitive dashboard built with Streamlit.

---

## 🧩 System Architecture

Sentinel follows a modular, agent-driven architecture where each agent specializes in a distinct cognitive task and collaborates through a centralized orchestration layer.



This design mirrors real-world AI systems used in enterprise media intelligence, compliance monitoring, and knowledge extraction pipelines.

---

## 🤖 Agentic Design

The system is powered by a specialized fleet of agents, each producing structured outputs for maximum traceability:

* **Audio Intelligence Agent:** Handles phonetics, transcription, and speaker diarization.
* **Video Intelligence Agent:** Analyzes visual frames, OCR, and scene transitions.
* **Emotion & Tone Agent:** Detects sentiment, urgency, and emotional shifts.
* **Reasoning Agent:** The "brain" that connects visual and auditory data points.
* **Tagging Agent:** Categorizes content and extracts metadata/entities.
* **Risk Detection Agent:** Monitors for compliance, bias, or safety concerns.
* **RAG Chat Agent:** Provides the interface for users to query the media's knowledge base.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **LLMs** | OpenAI GPT-4o / GPT-4o-mini |
| **Audio Processing** | OpenAI Whisper |
| **Agent Framework** | Agno / CrewAI |
| **Search & Retrieval** | Elasticsearch (Vector + Keyword) |
| **User Interface** | Streamlit |
| **Database** | SQLite / Postgres |
| **Video Processing** | FFmpeg |

---

## ⚙️ Installation

### Prerequisites
Before you begin, ensure you have the following installed:
* **Python 3.9+**
* **FFmpeg** (Required for audio/video processing)
* **Elasticsearch** (Local instance or Cloud)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/sentinel-media-ai.git](https://github.com/yourusername/sentinel-media-ai.git)
cd sentinel-media-ai
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a .env file in the root directory and add your credentials:
```bash
OPENAI_API_KEY=your_openai_key
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_API_KEY=your_es_key
DATABASE_URL=sqlite:///sentinel.db
```

## 🚀 Quick Start
```bash
streamlit run app.py
```

## Author

**Sagnik Mukherjee**  
[GitHub Profile](https://github.com/sagnik0712mukherjee)