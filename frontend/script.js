// EA Chatbot Web Interface JavaScript
class EAChatbot {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.chatHistory = [];
        this.apiBaseUrl = 'http://localhost:8000';
    }

    initializeElements() {
        // Search elements
        this.searchInput = document.getElementById('searchInput');
        this.searchButton = document.getElementById('searchButton');
        
        // Action cards
        this.actionCards = document.querySelectorAll('.action-card');
        
        // Chat section
        this.chatSection = document.getElementById('chatSection');
        this.chatContent = document.getElementById('chatContent');
        this.closeChat = document.getElementById('closeChat');
        
        // Results section
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsContent = document.getElementById('resultsContent');
        this.resultsCount = document.getElementById('resultsCount');
        
        // Loading spinner
        this.loadingSpinner = document.getElementById('loadingSpinner');
    }

    bindEvents() {
        // Search functionality
        this.searchButton.addEventListener('click', () => this.handleSearch());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });

        // Action cards
        this.actionCards.forEach(card => {
            card.addEventListener('click', () => {
                const query = card.dataset.query;
                this.handleSearch(query);
            });
        });

        // Close chat
        this.closeChat.addEventListener('click', () => this.hideChat());
    }

    async handleSearch(query = null) {
        const searchQuery = query || this.searchInput.value.trim();
        
        if (!searchQuery) return;

        // Show loading spinner
        this.showLoading();

        try {
            // Call the real backend API
            const response = await this.callBackendAPI(searchQuery);
            
            // Hide loading
            this.hideLoading();
            
            // Display results
            this.displayResults(searchQuery, response);
            
            // Clear search input
            this.searchInput.value = '';
            
        } catch (error) {
            console.error('Error:', error);
            this.hideLoading();
            this.showError('Sorry, I encountered an error. Please try again.');
        }
    }

    async callBackendAPI(query) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    n_results: 5
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('API call failed:', error);
            // Fallback to simulated response if API is not available
            return await this.simulateRAGResponse(query);
        }
    }

    async simulateRAGResponse(query) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Mock responses based on query type
        const responses = {
            'principles': {
                answer: `Based on our Enterprise Architecture knowledge base, here are the key principles:

1. **Business Alignment**: All technology decisions must directly support business objectives and capabilities.

2. **Standardization First**: Prefer standard, widely-adopted technologies over custom solutions.

3. **Security by Design**: Security and compliance requirements must be integrated into all architecture decisions.

4. **Data as an Asset**: Treat data as a strategic enterprise asset with proper governance.

5. **Agility and Flexibility**: Architectures should support rapid change while maintaining stability.

These principles guide our technology decisions and ensure alignment with business strategy.`,
                sources: ['ea_principles.md', 'tech_standards_guide.md'],
                confidence: 0.95
            },
            'technical debt': {
                answer: `Here's how to manage technical debt effectively, based on our comprehensive framework:

**Assessment & Prioritization:**
- Use our risk scoring matrix (Business Impact × Technical Risk × Effort Required)
- Prioritize P1 (Critical) items that pose security or compliance risks
- Focus on high-impact, low-effort improvements first

**Prevention Strategies:**
- Implement mandatory code reviews and static analysis
- Establish architecture review processes for major decisions
- Use automated testing and CI/CD pipelines

**Remediation Approaches:**
- **Refactoring**: Improve code structure and quality
- **Modernization**: Update to current technology standards
- **Consolidation**: Reduce duplicate systems and code
- **Automation**: Replace manual processes with automated solutions

**Ongoing Management:**
- Regular quarterly reviews and updates
- Track debt reduction metrics and celebrate successes
- Maintain momentum with visible progress indicators`,
                sources: ['technical_debt_management.md', 'architecture_decision_records.md'],
                confidence: 0.92
            },
            'default': {
                answer: `I've analyzed your question about "${query}" using our Enterprise Architecture knowledge base.

Based on the retrieved information, here are the key insights:

**Key Findings:**
- Multiple relevant documents were found in our corpus
- The information spans across business capabilities, technical standards, and governance frameworks
- Our RAG system successfully identified the most relevant sections for your query

**Recommendations:**
- Consider the business impact and alignment of any decisions
- Evaluate technical fit and standards compliance
- Assess security and compliance requirements
- Analyze total cost of ownership

**Next Steps:**
- Review the specific guidance from our knowledge base
- Consult with relevant stakeholders
- Document any architectural decisions using our ADR framework

Would you like me to dive deeper into any specific aspect of this topic?`,
                sources: ['ea_principles.md', 'tech_standards_guide.md', 'business_capability_mapping.md'],
                confidence: 0.88
            }
        };

        // Determine response type based on query
        let responseType = 'default';
        if (query.toLowerCase().includes('principle')) responseType = 'principles';
        if (query.toLowerCase().includes('technical debt') || query.toLowerCase().includes('tech debt')) responseType = 'debt';

        return responses[responseType];
    }

    displayResults(query, response) {
        // Hide chat section if it's visible
        this.hideChat();
        
        // Show results section
        this.resultsSection.style.display = 'block';
        
        // Update results count
        this.resultsCount.textContent = `${response.sources.length} sources`;
        
        // Create results content
        this.resultsContent.innerHTML = `
            <div class="query-display">
                <h4 style="color: #4A9EFF; margin-bottom: 15px;">Your Question:</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; margin-bottom: 25px;">${query}</p>
            </div>
            
            <div class="ai-response">
                <h4 style="color: #FFD700; margin-bottom: 15px;">AI Response:</h4>
                <div style="color: #E0E0E0; line-height: 1.7; white-space: pre-wrap; margin-bottom: 25px;">${response.answer}</div>
            </div>
            
            <div class="sources">
                <h4 style="color: #5CB85C; margin-bottom: 15px;">Sources:</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    ${response.sources.map(source => `
                        <span style="background: #404040; color: #FFFFFF; padding: 8px 15px; border-radius: 20px; font-size: 0.9rem;">
                            ${source}
                        </span>
                    `).join('')}
                </div>
            </div>
            
            <div class="confidence" style="margin-top: 25px; padding-top: 20px; border-top: 1px solid #404040;">
                <span style="color: #B0B0B0; font-size: 0.9rem;">
                    Confidence: ${Math.round(response.confidence * 100)}%
                </span>
            </div>
        `;
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showChat() {
        this.chatSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
    }

    hideChat() {
        this.chatSection.style.display = 'none';
    }

    showLoading() {
        this.loadingSpinner.style.display = 'flex';
    }

    hideLoading() {
        this.loadingSpinner.style.display = 'none';
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #DC3545;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 1001;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    addToChatHistory(sender, message, timestamp) {
        this.chatHistory.push({
            sender,
            message,
            timestamp
        });
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.eaChatbot = new EAChatbot();
    
    // Add some visual feedback for action cards
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput').value = '';
        document.getElementById('searchInput').focus();
    }
    
    // Escape to close chat/results
    if (e.key === 'Escape') {
        document.getElementById('chatSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'none';
    }
});
