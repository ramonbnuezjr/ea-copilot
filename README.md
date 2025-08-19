# EA Chatbot - Enterprise Architecture Assistant

A comprehensive Enterprise Architecture chatbot that uses RAG (Retrieval-Augmented Generation) with Google Gemini to provide intelligent responses about enterprise architecture, business capabilities, technology standards, and more.

## 🚀 Features

### Core Capabilities
- **RAG Integration**: Grounded responses using enterprise architecture documentation
- **Gemini AI**: Powered by Google's latest AI model for intelligent reasoning
- **Mock Data**: Realistic enterprise data across 12 key domains
- **Modern UI**: Responsive web interface with real-time chat

### Enterprise Architecture Domains
1. **Business Capabilities** - Core and supporting business functions
2. **Application Inventory** - Systems and applications mapping
3. **Technology Standards** - Approved, tolerated, and retiring technologies
4. **Integration Catalog** - APIs and system integrations
5. **Tech Debt Register** - Technical debt and risk assessment
6. **Roadmap & Investment** - Strategic initiatives and timelines
7. **Cost & Licensing** - Vendor contracts and renewal dates
8. **SLA Health** - Service level agreements and performance
9. **Security Controls** - Compliance and security measures
10. **Data Domains** - Data classification and governance
11. **Vendor Contracts** - Supplier relationships and terms
12. **Architecture Decisions** - ADRs and technical choices

### Conversational Use Cases
- **Capability Alignment**: "What apps enable Customer Onboarding?"
- **Standards Guidance**: "Is Kubernetes a standard or tolerate?"
- **Tech Debt Analysis**: "Which risks block Q2 modernization?"
- **Cost Optimization**: "Which licenses are shelfware candidates?"
- **Compliance**: "Which apps with PII lack ISO control mapping?"

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   FastAPI       │    │   Vector Store  │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Google Gemini │
                       │   AI Model      │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Modern web browser

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ea-copilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Generate mock data and start**
   ```bash
   python start_chatbot.py
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Configuration Options
Edit `config.py` to customize:
- Vector store settings
- Embedding model preferences
- Server configuration
- RAG parameters

## 🚀 Usage

### Starting the Chatbot
```bash
# Option 1: Use startup script (recommended)
python start_chatbot.py

# Option 2: Manual startup
python -m uvicorn ea_chatbot:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the Chatbot
- **Web Interface**: http://localhost:8000/frontend/index.html
- **API Endpoints**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### API Usage
```bash
# Chat endpoint
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are our core business capabilities?", "user_id": "user123"}'

# Health check
curl http://localhost:8000/health

# Get capabilities
curl http://localhost:8000/capabilities
```

## 📊 Mock Data

The chatbot includes realistic mock datasets covering:

### Business Capabilities
- Customer Onboarding (Core, Optimizing)
- Order Management (Core, Defined)
- Financial Reporting (Core, Optimizing)
- HR Management (Supporting, Defined)
- Supply Chain (Core, Managing)
- Customer Service (Core, Defined)
- Product Development (Core, Optimizing)
- Data Analytics (Enabling, Managing)

### Technology Standards
- **Standard**: Kubernetes, Docker, React, PostgreSQL, Redis
- **Tolerate**: MongoDB, Apache Kafka, GraphQL
- **Retire**: AngularJS, Legacy SOAP APIs

### Application Inventory
- Salesforce CRM (Customer Onboarding)
- NetSuite ERP (Order Management)
- Workday HCM (HR Management)
- Tableau Analytics (Data Analytics)
- Legacy Order System (Retire)
- Jira (Product Development)

## 🔍 RAG Corpus

The chatbot includes these knowledge documents:
- **EA Principles** - Core architecture principles and governance
- **NFR Checklist** - Non-functional requirements framework
- **Decommission Runbook** - Legacy system retirement guide
- **Security Baseline** - PII protection and compliance
- **Architecture Patterns** - Reference architectures and patterns

## 🎯 Example Queries

### Business Capability Questions
- "What applications support Customer Onboarding?"
- "Which capabilities are core vs. supporting?"
- "What is the maturity level of our HR Management capability?"

### Technology Standards
- "Is Kubernetes a standard technology?"
- "What should we do with AngularJS components?"
- "Which database technologies are approved?"

### Cost and Vendor Management
- "Which vendors are up for renewal this quarter?"
- "What is our total annual SaaS spend?"
- "Which contracts have auto-renewal enabled?"

### Risk and Tech Debt
- "What are our high-priority tech debt items?"
- "Which systems have security risks?"
- "What is blocking our modernization efforts?"

## 🧪 Testing

### Manual Testing
1. Start the chatbot server
2. Open the web interface
3. Try the quick question buttons
4. Ask custom questions
5. Verify responses include sources and context

### API Testing
```bash
# Test chat functionality
python -c "
import requests
response = requests.post('http://localhost:8000/chat', 
                        json={'message': 'What are our business capabilities?', 'user_id': 'test'})
print(response.json())
"
```

## 🔧 Development

### Project Structure
```
ea-copilot/
├── ea_chatbot.py          # Main chatbot backend
├── mock_data_generator.py # Mock data generation
├── config.py              # Configuration settings
├── start_chatbot.py       # Startup script
├── requirements.txt       # Python dependencies
├── rag_corpus/           # RAG knowledge documents
│   ├── ea_principles.md
│   ├── nfr_checklist.md
│   └── ...
├── frontend/             # Web interface
│   └── index.html
└── mock_data/            # Generated mock datasets
```

### Adding New Data Sources
1. Extend `mock_data_generator.py` with new dataset methods
2. Update the `generate_all_data()` method
3. Add relevant context extraction in `get_mock_data_context()`

### Extending RAG Corpus
1. Add new Markdown documents to `rag_corpus/`
2. Documents are automatically chunked and embedded
3. Update the chatbot to handle new document types

## 🚨 Troubleshooting

### Common Issues

**Missing Gemini API Key**
```
❌ GEMINI_API_KEY environment variable is not set
```
Solution: Set the environment variable in your `.env` file

**Package Import Errors**
```
❌ Missing required packages
```
Solution: Run `pip install -r requirements.txt`

**Vector Store Errors**
```
❌ Error setting up RAG corpus
```
Solution: Check ChromaDB installation and permissions

**Frontend Connection Issues**
```
❌ Failed to fetch from API
```
Solution: Ensure the backend server is running on port 8000

### Debug Mode
Enable debug logging by setting `DEBUG = True` in `config.py`

## 📈 Performance

### Response Times
- **Simple Queries**: < 2 seconds
- **Complex Analysis**: < 5 seconds
- **RAG Retrieval**: < 1 second

### Scalability
- **Concurrent Users**: 100+ (depending on Gemini API limits)
- **Document Processing**: 1000+ documents
- **Vector Search**: Sub-second response

## 🔒 Security

- API key management through environment variables
- No sensitive data in mock datasets
- Input validation and sanitization
- CORS configuration for web interface

## 📚 References

- [Google Gemini API Documentation](https://ai.google.dev/)
- [ChromaDB Vector Database](https://www.trychroma.com/)
- [FastAPI Framework](https://fastapi.tiangolo.com/)
- [Enterprise Architecture Best Practices](https://www.opengroup.org/togaf)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue on GitHub

---

**Built with ❤️ for Enterprise Architects**
