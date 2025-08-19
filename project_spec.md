# EA Chatbot MVP – Project Specification

## Scope
Build an enterprise architecture (EA) chatbot that:
- Uses RAG for grounding.
- Runs inference with Google Gemini.
- Encodes ServiceNow EA best practices and application inventory.
- Provides general EA best practices.

## Features
1. **RAG Integration**
   - Documents: EA Principles, NFR Checklist, Decommission Runbook, etc.
   - Retrieval: embed corpus + mock datasets into vector store.

2. **Intelligent Mock Data (Tables)**
   - Business Capability Map & Mappings
   - Integration & API Catalog
   - Tech Standards Registry
   - ADRs / ARB Outcomes
   - Tech Debt & Risk Register
   - Roadmap & Investment Themes
   - Cost & Licensing Snapshot
   - SLA/OLA & Operational Health
   - Security & Compliance Controls
   - Data Domains & Lineage
   - CMDB Slice
   - Vendor & Contracts

3. **Conversational Use Cases**
   - Capability alignment: “What apps enable Customer Onboarding?”
   - Standards guidance: “Is Kubernetes a standard or tolerate?”
   - Tech debt trade-offs: “Which risks block Q2 modernization?”
   - Cost optimization: “Which licenses are shelfware candidates?”
   - Compliance: “Which apps with PII lack ISO control mapping?”

## Architecture
- **Frontend**: Chat UI (web or Slack prototype).
- **Backend**: 
  - ✅ Retrieval pipeline: embeddings + vector DB (ChromaDB + sentence transformers).
  - 🔄 Gemini API for inference - Next milestone.
  - ✅ Dataset store (CSV + JSON formats).
- **Integration Hooks**: 
  - ServiceNow EA application inventory (mocked in MVP).
  - Potential future: API to pull live ServiceNow CMDB slices.

## Current Status
- **MVP Foundation**: ✅ Complete
- **RAG System**: ✅ Fully functional
- **Knowledge Base**: ✅ 9 comprehensive documents
- **Mock Data**: ✅ 12 realistic datasets
- **Vector Store**: ✅ ChromaDB with 166 document chunks
- **Next Milestone**: 🔄 Gemini AI integration

## Deliverables
- ✅ RAG corpus (9 comprehensive docs, 166 chunks, 78,756 characters)
- ✅ Mock datasets (12 tables with realistic distributions and cross-references)
- ✅ Vector store with embeddings (ChromaDB + sentence transformers)
- 🔄 Deployed chatbot (prototype) - Next milestone
- 🔄 Usage guide - In progress
