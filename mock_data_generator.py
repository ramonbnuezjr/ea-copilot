import json
import pandas as pd
import os
from typing import Dict, List


class EAMockDataGenerator:
    """Generates realistic mock data for EA chatbot based on project specifications."""
    
    def __init__(self, output_dir: str = "./mock_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_business_capabilities(self) -> List[Dict]:
        """Generate business capability map with realistic mappings."""
        capabilities = [
            {"id": "CAP001", "name": "Customer Onboarding", 
             "level": "Core", "owner": "Sales Operations", 
             "maturity": "Optimizing"},
            {"id": "CAP002", "name": "Order Management", 
             "level": "Core", "owner": "Operations", 
             "maturity": "Defined"},
            {"id": "CAP003", "name": "Financial Reporting", 
             "level": "Core", "owner": "Finance", 
             "maturity": "Optimizing"},
            {"id": "CAP004", "name": "HR Management", 
             "level": "Supporting", "owner": "HR", 
             "maturity": "Defined"},
            {"id": "CAP005", "name": "Supply Chain", 
             "level": "Core", "owner": "Operations", 
             "maturity": "Managing"},
            {"id": "CAP006", "name": "Customer Service", 
             "level": "Core", "owner": "Customer Success", 
             "maturity": "Defined"},
            {"id": "CAP007", "name": "Product Development", 
             "level": "Core", "owner": "Engineering", 
             "maturity": "Optimizing"},
            {"id": "CAP008", "name": "Data Analytics", 
             "level": "Enabling", "owner": "Data Science", 
             "maturity": "Managing"}
        ]
        return capabilities
    
    def generate_application_inventory(self) -> List[Dict]:
        """Generate application inventory with capability mappings."""
        apps = [
            {"id": "APP001", "name": "Salesforce CRM", "type": "SaaS", "capability": "CAP001", "status": "Active", "vendor": "Salesforce", "cost_per_month": 5000},
            {"id": "APP002", "name": "NetSuite ERP", "type": "SaaS", "capability": "CAP002", "status": "Active", "vendor": "Oracle", "cost_per_month": 8000},
            {"id": "APP003", "name": "Workday HCM", "type": "SaaS", "capability": "CAP004", "status": "Active", "vendor": "Workday", "cost_per_month": 3000},
            {"id": "APP004", "name": "Tableau Analytics", "type": "SaaS", "capability": "CAP008", "status": "Active", "vendor": "Salesforce", "cost_per_month": 2000},
            {"id": "APP005", "name": "Legacy Order System", "type": "On-Premise", "capability": "CAP002", "status": "Retire", "vendor": "Internal", "cost_per_month": 1000},
            {"id": "APP006", "name": "Jira", "type": "SaaS", "capability": "CAP007", "status": "Active", "vendor": "Atlassian", "cost_per_month": 1500}
        ]
        return apps
    
    def generate_tech_standards(self) -> List[Dict]:
        """Generate tech standards with realistic distributions (60% tolerate, 30% standard, 10% retire)."""
        standards = [
            {"technology": "Kubernetes", "category": "Container Orchestration", "status": "Standard", "rationale": "Industry standard for container management"},
            {"technology": "Docker", "category": "Containerization", "status": "Standard", "rationale": "De facto container standard"},
            {"technology": "React", "category": "Frontend Framework", "status": "Standard", "rationale": "Modern, widely adopted framework"},
            {"technology": "AngularJS", "category": "Frontend Framework", "status": "Retire", "rationale": "End of life, security concerns"},
            {"technology": "MongoDB", "category": "Database", "status": "Tolerate", "rationale": "Use case specific, not general purpose"},
            {"technology": "PostgreSQL", "category": "Database", "status": "Standard", "rationale": "Enterprise-grade relational database"},
            {"technology": "Apache Kafka", "category": "Message Queue", "status": "Tolerate", "rationale": "Complex but powerful for specific use cases"},
            {"technology": "Redis", "category": "Cache", "status": "Standard", "rationale": "Industry standard caching solution"},
            {"technology": "Legacy SOAP APIs", "category": "Integration", "status": "Retire", "rationale": "Outdated protocol, security risks"},
            {"technology": "GraphQL", "category": "API", "status": "Tolerate", "rationale": "Emerging standard, evaluate per use case"}
        ]
        return standards
    
    def generate_integration_catalog(self) -> List[Dict]:
        """Generate integration and API catalog."""
        integrations = [
            {"id": "INT001", "name": "Salesforce to NetSuite", "type": "Data Sync", "status": "Active", "frequency": "Real-time", "reliability": "99.9%"},
            {"id": "INT002", "name": "Payment Gateway API", "type": "External API", "status": "Active", "frequency": "On-demand", "reliability": "99.95%"},
            {"id": "INT003", "name": "Legacy System Bridge", "type": "Data Migration", "status": "Deprecated", "frequency": "Batch", "reliability": "95%"},
            {"id": "INT004", "name": "HR System Integration", "type": "Data Sync", "status": "Active", "frequency": "Daily", "reliability": "99%"},
            {"id": "INT005", "name": "Analytics Data Pipeline", "type": "ETL", "status": "Active", "frequency": "Hourly", "reliability": "98%"}
        ]
        return integrations
    
    def generate_tech_debt(self) -> List[Dict]:
        """Generate tech debt and risk register with realistic risk distribution."""
        tech_debt = [
            {"id": "TD001", "description": "Legacy Order System", "severity": "High", "impact": "Customer Experience", "effort": "Large", "priority": "P1"},
            {"id": "TD002", "description": "Outdated AngularJS Components", "severity": "Medium", "impact": "Developer Productivity", "effort": "Medium", "priority": "P2"},
            {"id": "TD003", "description": "Manual Data Reconciliation", "severity": "Low", "impact": "Operational Efficiency", "effort": "Small", "priority": "P3"},
            {"id": "TD004", "description": "SOAP API Dependencies", "severity": "High", "impact": "Security", "effort": "Large", "priority": "P1"},
            {"id": "TD005", "description": "Unused Database Indexes", "severity": "Low", "impact": "Performance", "effort": "Small", "priority": "P3"}
        ]
        return tech_debt
    
    def generate_roadmap(self) -> List[Dict]:
        """Generate roadmap and investment themes."""
        roadmap = [
            {"id": "ROAD001", "theme": "Digital Transformation", "priority": "P1", "timeline": "Q2 2025", "budget": 500000, "status": "Planning"},
            {"id": "ROAD002", "theme": "Legacy Modernization", "priority": "P1", "timeline": "Q3 2025", "budget": 300000, "status": "Planning"},
            {"id": "ROAD003", "theme": "Data Platform Enhancement", "priority": "P2", "timeline": "Q4 2025", "budget": 200000, "status": "Research"},
            {"id": "ROAD004", "theme": "Security Hardening", "priority": "P1", "timeline": "Q1 2025", "budget": 150000, "status": "In Progress"}
        ]
        return roadmap
    
    def generate_cost_licensing(self) -> List[Dict]:
        """Generate cost and licensing snapshot with renewal dates."""
        costs = [
            {"vendor": "Salesforce", "product": "CRM Platform", "annual_cost": 60000, "renewal_date": "2025-12-31", "status": "Active"},
            {"vendor": "Oracle", "product": "NetSuite ERP", "annual_cost": 96000, "renewal_date": "2025-06-30", "status": "Active"},
            {"vendor": "Workday", "product": "HCM Platform", "annual_cost": 36000, "renewal_date": "2025-09-30", "status": "Active"},
            {"vendor": "Atlassian", "product": "Jira + Confluence", "annual_cost": 18000, "renewal_date": "2025-03-31", "status": "Active"},
            {"vendor": "Legacy Vendor", "product": "Order System", "annual_cost": 12000, "renewal_date": "2025-02-28", "status": "Deprecated"}
        ]
        return costs
    
    def generate_sla_health(self) -> List[Dict]:
        """Generate SLA/OLA and operational health metrics."""
        sla_health = [
            {"service": "Customer Portal", "sla_target": "99.9%", "current_uptime": "99.95%", "mttr": "15min", "status": "Healthy"},
            {"service": "Order Processing", "sla_target": "99.5%", "current_uptime": "99.2%", "mttr": "45min", "status": "Warning"},
            {"service": "Payment Gateway", "sla_target": "99.99%", "current_uptime": "99.98%", "mttr": "5min", "status": "Healthy"},
            {"service": "HR System", "sla_target": "99.0%", "current_uptime": "98.8%", "mttr": "2hr", "status": "Warning"},
            {"service": "Analytics Platform", "sla_target": "99.0%", "current_uptime": "99.5%", "mttr": "1hr", "status": "Healthy"}
        ]
        return sla_health
    
    def generate_security_controls(self) -> List[Dict]:
        """Generate security and compliance controls."""
        security = [
            {"control": "ISO 27001", "status": "Compliant", "last_audit": "2024-12-01", "next_audit": "2025-12-01", "coverage": "95%"},
            {"control": "SOC 2 Type II", "status": "Compliant", "last_audit": "2024-06-01", "next_audit": "2025-06-01", "coverage": "90%"},
            {"control": "GDPR Compliance", "status": "Compliant", "last_audit": "2024-09-01", "next_audit": "2025-09-01", "coverage": "100%"},
            {"control": "PII Data Protection", "status": "Partial", "last_audit": "2024-11-01", "next_audit": "2025-05-01", "coverage": "75%"},
            {"control": "API Security", "status": "Compliant", "last_audit": "2024-10-01", "next_audit": "2025-04-01", "coverage": "100%"}
        ]
        return security
    
    def generate_data_domains(self) -> List[Dict]:
        """Generate data domains and lineage."""
        data_domains = [
            {"domain": "Customer Data", "classification": "PII", "retention_policy": "7 years", "data_owner": "Sales Operations", "compliance": "GDPR"},
            {"domain": "Financial Data", "classification": "Confidential", "retention_policy": "10 years", "data_owner": "Finance", "compliance": "SOX"},
            {"domain": "HR Data", "classification": "PII", "retention_policy": "7 years", "data_owner": "HR", "compliance": "GDPR"},
            {"domain": "Product Data", "classification": "Internal", "retention_policy": "5 years", "data_owner": "Engineering", "compliance": "Internal"},
            {"domain": "Operational Data", "classification": "Internal", "retention_policy": "3 years", "data_owner": "Operations", "compliance": "Internal"}
        ]
        return data_domains
    
    def generate_vendor_contracts(self) -> List[Dict]:
        """Generate vendor and contracts information."""
        vendors = [
            {"vendor": "Salesforce", "contract_type": "Enterprise", "start_date": "2023-01-01", "end_date": "2025-12-31", "auto_renewal": True},
            {"vendor": "Oracle", "contract_type": "Enterprise", "start_date": "2023-06-01", "end_date": "2025-06-30", "auto_renewal": False},
            {"vendor": "Workday", "contract_type": "Enterprise", "start_date": "2023-09-01", "end_date": "2025-09-30", "auto_renewal": True},
            {"vendor": "Atlassian", "contract_type": "Standard", "start_date": "2023-03-01", "end_date": "2025-03-31", "auto_renewal": True},
            {"vendor": "Legacy Vendor", "contract_type": "Legacy", "start_date": "2018-01-01", "end_date": "2025-02-28", "auto_renewal": False}
        ]
        return vendors
    
    def generate_adrs(self) -> List[Dict]:
        """Generate Architecture Decision Records."""
        adrs = [
            {"id": "ADR001", "title": "Kubernetes Adoption", "status": "Accepted", "date": "2024-01-15", "context": "Need for container orchestration", "decision": "Adopt Kubernetes", "consequences": "Increased complexity but better scalability"},
            {"id": "ADR002", "title": "PostgreSQL as Primary Database", "status": "Accepted", "date": "2024-03-20", "context": "Database standardization", "decision": "Use PostgreSQL", "consequences": "Better performance and reliability"},
            {"id": "ADR003", "title": "React Frontend Framework", "status": "Accepted", "date": "2024-02-10", "context": "Frontend modernization", "decision": "Adopt React", "consequences": "Better developer experience and performance"},
            {"id": "ADR004", "title": "Legacy System Retirement", "status": "Pending", "date": "2024-11-01", "context": "Technical debt reduction", "decision": "Plan retirement", "consequences": "Migration effort required"}
        ]
        return adrs
    
    def generate_all_data(self):
        """Generate all mock datasets and save to files."""
        datasets = {
            "business_capabilities": self.generate_business_capabilities(),
            "application_inventory": self.generate_application_inventory(),
            "tech_standards": self.generate_tech_standards(),
            "integration_catalog": self.generate_integration_catalog(),
            "tech_debt": self.generate_tech_debt(),
            "roadmap": self.generate_roadmap(),
            "cost_licensing": self.generate_cost_licensing(),
            "sla_health": self.generate_sla_health(),
            "security_controls": self.generate_security_controls(),
            "data_domains": self.generate_data_domains(),
            "vendor_contracts": self.generate_vendor_contracts(),
            "adrs": self.generate_adrs()
        }
        
        # Save as JSON files
        for name, data in datasets.items():
            file_path = os.path.join(self.output_dir, f"{name}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Also save as CSV for easier analysis
            df = pd.DataFrame(data)
            csv_path = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(csv_path, index=False)
        
        print(f"Generated {len(datasets)} mock datasets in {self.output_dir}")
        return datasets


if __name__ == "__main__":
    generator = EAMockDataGenerator()
    generator.generate_all_data()
