import re
from typing import Dict, List

# ===========================================
# TECHNOLOGY & SOFTWARE DEVELOPMENT
# ===========================================

TECH_SKILLS = {
    'programming': [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
    ],
    'frameworks': [
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
        'tensorflow', 'pytorch', 'keras', 'fastapi', 'next.js',
    ],
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ci/cd', 'linux', 'bash', 'ansible',
    ],
    'databases': [
        'postgresql', 'mysql', 'mongodb', 'redis', 'oracle', 'sql server',
    ],
    'ai_ml': [
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data science', 'generative ai', 'llm', 'chatgpt',
    ]
}

# ===========================================
# BUSINESS & FINANCE
# ===========================================

BUSINESS_FINANCE_SKILLS = {
    'financial_analysis': [
        'financial modeling', 'excel', 'financial analysis', 'forecasting',
        'budgeting', 'variance analysis', 'financial reporting', 'gaap',
        'ifrs', 'sox compliance', 'financial statements',
    ],
    'accounting': [
        'bookkeeping', 'accounts payable', 'accounts receivable', 'reconciliation',
        'quickbooks', 'sage', 'xero', 'sap', 'oracle financials',
        'general ledger', 'journal entries', 'trial balance',
    ],
    'investment_banking': [
        'investment banking', 'mergers and acquisitions', 'm&a', 'ipos',
        'valuation', 'dcf', 'lbo', 'comps', 'pitch books',
        'bloomberg terminal', 'capital iq', 'factset',
    ],
    'business_analysis': [
        'business analysis', 'requirements gathering', 'process mapping',
        'stakeholder management', 'user stories', 'business intelligence',
        'kpi tracking', 'dashboard creation', 'data visualization',
    ],
    'consulting': [
        'strategy consulting', 'management consulting', 'business strategy',
        'market research', 'competitive analysis', 'swot analysis',
        'bcg matrix', 'porter five forces', 'case interviews',
    ]
}

# ===========================================
# MARKETING & SALES
# ===========================================

MARKETING_SALES_SKILLS = {
    'digital_marketing': [
        'seo', 'sem', 'google analytics', 'google ads', 'facebook ads',
        'content marketing', 'email marketing', 'social media marketing',
        'influencer marketing', 'affiliate marketing', 'ppc',
        'conversion rate optimization', 'a/b testing', 'growth hacking',
    ],
    'marketing_tools': [
        'hubspot', 'salesforce', 'mailchimp', 'hootsuite', 'buffer',
        'canva', 'adobe creative suite', 'wordpress', 'shopify',
        'google tag manager', 'hotjar', 'mixpanel',
    ],
    'sales': [
        'sales', 'b2b sales', 'b2c sales', 'account management',
        'lead generation', 'cold calling', 'negotiation', 'closing',
        'crm', 'salesforce crm', 'pipeline management', 'quota attainment',
        'prospecting', 'sales forecasting', 'sales presentations',
    ],
    'brand_marketing': [
        'brand strategy', 'brand positioning', 'brand awareness',
        'public relations', 'media relations', 'press releases',
        'event marketing', 'experiential marketing',
    ]
}

# ===========================================
# DESIGN & CREATIVE
# ===========================================

DESIGN_CREATIVE_SKILLS = {
    'graphic_design': [
        'graphic design', 'adobe photoshop', 'adobe illustrator',
        'adobe indesign', 'figma', 'sketch', 'typography',
        'color theory', 'layout design', 'print design',
    ],
    'ui_ux': [
        'ui design', 'ux design', 'user research', 'wireframing',
        'prototyping', 'usability testing', 'information architecture',
        'interaction design', 'design thinking', 'user personas',
        'user flows', 'journey mapping',
    ],
    'video_animation': [
        'video editing', 'adobe premiere', 'final cut pro', 'after effects',
        'motion graphics', '3d animation', 'blender', 'cinema 4d',
        'video production', 'cinematography', 'storyboarding',
    ],
    'content_creation': [
        'copywriting', 'content writing', 'technical writing',
        'creative writing', 'editing', 'proofreading', 'blogging',
        'storytelling', 'seo writing', 'ghostwriting',
    ]
}

# ===========================================
# HEALTHCARE & MEDICAL
# ===========================================

HEALTHCARE_SKILLS = {
    'clinical': [
        'patient care', 'clinical assessment', 'diagnosis', 'treatment planning',
        'medical terminology', 'vital signs', 'medication administration',
        'wound care', 'iv therapy', 'phlebotomy', 'cpr', 'bls', 'acls',
    ],
    'medical_specialties': [
        'cardiology', 'oncology', 'pediatrics', 'geriatrics', 'surgery',
        'emergency medicine', 'radiology', 'anesthesiology', 'psychiatry',
        'obstetrics', 'gynecology', 'orthopedics', 'neurology',
    ],
    'healthcare_admin': [
        'epic', 'cerner', 'meditech', 'electronic health records', 'ehr',
        'hipaa compliance', 'medical coding', 'icd-10', 'cpt codes',
        'medical billing', 'insurance verification', 'claims processing',
    ],
    'pharmacy': [
        'pharmacology', 'drug interactions', 'dispensing', 'compounding',
        'medication therapy management', 'immunizations', 'counseling',
    ]
}

# ===========================================
# ENGINEERING (NON-SOFTWARE)
# ===========================================

ENGINEERING_SKILLS = {
    'mechanical': [
        'cad', 'autocad', 'solidworks', 'catia', 'creo', 'ansys',
        'fea', 'cfd', 'thermodynamics', 'fluid mechanics', 'mechanics',
        'machine design', 'manufacturing', 'gd&t', 'tolerance analysis',
    ],
    'electrical': [
        'circuit design', 'pcb design', 'eagle', 'altium', 'labview',
        'power systems', 'control systems', 'plc', 'scada',
        'embedded systems', 'microcontrollers', 'arduino', 'raspberry pi',
    ],
    'civil': [
        'structural analysis', 'autocad civil 3d', 'revit', 'etabs', 'staad pro',
        'construction management', 'surveying', 'geotechnical', 'hydraulics',
        'project planning', 'quantity estimation', 'bim',
    ],
    'chemical': [
        'process engineering', 'aspen plus', 'hysys', 'chemcad',
        'distillation', 'reaction engineering', 'process safety',
        'mass transfer', 'heat transfer', 'process optimization',
    ]
}

# ===========================================
# HUMAN RESOURCES
# ===========================================

HR_SKILLS = {
    'recruitment': [
        'recruiting', 'talent acquisition', 'sourcing', 'screening',
        'interviewing', 'ats', 'applicant tracking system', 'linkedin recruiter',
        'boolean search', 'candidate assessment', 'onboarding',
    ],
    'hr_operations': [
        'hris', 'workday', 'adp', 'bamboohr', 'payroll', 'benefits administration',
        'compensation', 'employee relations', 'performance management',
        'hris reporting', 'compliance', 'labor law',
    ],
    'training_development': [
        'training', 'learning and development', 'instructional design',
        'e-learning', 'lms', 'talent development', 'leadership development',
        'coaching', 'mentoring', 'organizational development',
    ]
}

# ===========================================
# OPERATIONS & SUPPLY CHAIN
# ===========================================

OPERATIONS_SKILLS = {
    'supply_chain': [
        'supply chain management', 'logistics', 'inventory management',
        'procurement', 'vendor management', 'purchasing', 'sourcing',
        'warehouse management', 'demand planning', 'forecasting',
        'sap', 'oracle scm', 'erp systems',
    ],
    'operations': [
        'operations management', 'process improvement', 'lean', 'six sigma',
        'kaizen', '5s', 'value stream mapping', 'root cause analysis',
        'project management', 'pmp', 'agile', 'scrum',
    ],
    'quality': [
        'quality assurance', 'quality control', 'iso 9001', 'iso 14001',
        'gmp', 'fda regulations', 'validation', 'documentation',
        'audit', 'statistical process control', 'spc',
    ]
}

# ===========================================
# LEGAL & COMPLIANCE
# ===========================================

LEGAL_SKILLS = {
    'legal': [
        'contract law', 'legal research', 'legal writing', 'litigation',
        'contract negotiation', 'due diligence', 'compliance',
        'regulatory compliance', 'corporate law', 'intellectual property',
        'patents', 'trademarks', 'employment law', 'real estate law',
    ],
    'legal_tech': [
        'westlaw', 'lexisnexis', 'clio', 'legal software', 'e-discovery',
        'document review', 'contract management software',
    ]
}

# ===========================================
# EDUCATION & TEACHING
# ===========================================

EDUCATION_SKILLS = {
    'teaching': [
        'curriculum development', 'lesson planning', 'classroom management',
        'differentiated instruction', 'assessment', 'student engagement',
        'educational technology', 'learning management system', 'lms',
        'google classroom', 'canvas', 'blackboard', 'moodle',
    ],
    'specializations': [
        'special education', 'esl', 'stem education', 'early childhood education',
        'higher education', 'online teaching', 'instructional design',
    ]
}

# ===========================================
# CUSTOMER SERVICE & SUPPORT
# ===========================================

CUSTOMER_SERVICE_SKILLS = {
    'customer_support': [
        'customer service', 'customer support', 'technical support',
        'troubleshooting', 'help desk', 'zendesk', 'freshdesk',
        'salesforce service cloud', 'ticketing systems', 'call center',
        'phone support', 'email support', 'chat support', 'live chat',
    ],
    'client_relations': [
        'account management', 'client relations', 'relationship management',
        'customer success', 'retention', 'upselling', 'cross-selling',
        'customer satisfaction', 'nps', 'customer feedback',
    ]
}

# ===========================================
# SOFT SKILLS (UNIVERSAL)
# ===========================================

SOFT_SKILLS = [
    'leadership', 'communication', 'teamwork', 'problem solving',
    'critical thinking', 'project management', 'time management',
    'adaptability', 'creativity', 'collaboration', 'mentoring',
    'presentation', 'analytical', 'strategic thinking', 'negotiation',
    'conflict resolution', 'decision making', 'emotional intelligence',
    'attention to detail', 'multitasking', 'organizational',
]

# ===========================================
# LANGUAGE SKILLS
# ===========================================

LANGUAGES = [
    'english', 'spanish', 'mandarin', 'french', 'german', 'japanese',
    'portuguese', 'arabic', 'hindi', 'russian', 'korean', 'italian',
    'bilingual', 'multilingual', 'native speaker', 'fluent', 'conversational',
]

# ===========================================
# CERTIFICATIONS BY INDUSTRY
# ===========================================

CERTIFICATIONS = {
    'tech': ['aws certified', 'azure certified', 'google cloud certified', 'cissp', 'pmp', 'scrum master', 'comptia'],
    'finance': ['cfa', 'cpa', 'frm', 'cma', 'cia', 'cfp'],
    'healthcare': ['rn', 'md', 'do', 'pa', 'np', 'cna', 'lpn', 'pharmacist'],
    'hr': ['phr', 'sphr', 'shrm-cp', 'shrm-scp'],
    'operations': ['six sigma', 'lean', 'pmp', 'cscp', 'cpim'],
}


def detect_industry(resume_text: str) -> List[str]:
    """
    Detect which industries the resume is related to.
    """
    resume_lower = resume_text.lower()
    industries = []
    
    # Check for industry indicators
    industry_keywords = {
        'technology': ['software', 'developer', 'engineer', 'programming', 'coding', 'tech'],
        'finance': ['financial', 'accounting', 'banking', 'investment', 'analyst', 'cpa', 'cfa'],
        'healthcare': ['medical', 'healthcare', 'clinical', 'patient', 'hospital', 'nurse', 'doctor'],
        'marketing': ['marketing', 'seo', 'social media', 'campaigns', 'brand'],
        'sales': ['sales', 'account executive', 'business development', 'revenue'],
        'design': ['design', 'creative', 'ui', 'ux', 'graphic', 'photoshop'],
        'hr': ['human resources', 'hr', 'recruiting', 'talent acquisition', 'hiring'],
        'operations': ['operations', 'supply chain', 'logistics', 'manufacturing'],
        'education': ['teaching', 'education', 'teacher', 'professor', 'instructor'],
        'legal': ['legal', 'attorney', 'lawyer', 'paralegal', 'law'],
    }
    
    for industry, keywords in industry_keywords.items():
        if any(keyword in resume_lower for keyword in keywords):
            industries.append(industry)
    
    return industries if industries else ['general']


def extract_skills(resume_text: str) -> Dict[str, any]:
    """
    Extract skills across all industries with intelligent categorization.
    """
    resume_lower = resume_text.lower()
    
    # Detect industries first
    detected_industries = detect_industry(resume_text)
    
    # Combine all skill dictionaries
    all_skill_categories = {
        'Technology': TECH_SKILLS,
        'Business & Finance': BUSINESS_FINANCE_SKILLS,
        'Marketing & Sales': MARKETING_SALES_SKILLS,
        'Design & Creative': DESIGN_CREATIVE_SKILLS,
        'Healthcare': HEALTHCARE_SKILLS,
        'Engineering': ENGINEERING_SKILLS,
        'Human Resources': HR_SKILLS,
        'Operations': OPERATIONS_SKILLS,
        'Legal': LEGAL_SKILLS,
        'Education': EDUCATION_SKILLS,
        'Customer Service': CUSTOMER_SERVICE_SKILLS,
    }
    
    found_skills = {}
    total_technical_skills = []
    
    # Extract skills from each category
    for category_name, subcategories in all_skill_categories.items():
        category_skills = []
        
        for subcategory, skills in subcategories.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, resume_lower):
                    category_skills.append(skill.title())
                    total_technical_skills.append(skill.title())
        
        if category_skills:
            found_skills[category_name] = sorted(list(set(category_skills)))
    
    # Extract soft skills
    found_soft = []
    for skill in SOFT_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_lower):
            found_soft.append(skill.title())
    
    # Extract languages
    found_languages = []
    for lang in LANGUAGES:
        pattern = r'\b' + re.escape(lang) + r'\b'
        if re.search(pattern, resume_lower):
            found_languages.append(lang.title())
    
    # Extract certifications
    found_certs = []
    for cert_category, certs in CERTIFICATIONS.items():
        for cert in certs:
            pattern = r'\b' + re.escape(cert) + r'\b'
            if re.search(pattern, resume_lower):
                found_certs.append(cert.upper())
    
    # Extract years of experience
    experience_pattern = r'(\d+)\+?\s*years?'
    experience_matches = re.findall(experience_pattern, resume_lower)
    total_experience = max([int(x) for x in experience_matches], default=0)
    
    return {
        'detected_industries': detected_industries,
        'technical_skills': sorted(list(set(total_technical_skills))),
        'skills_by_category': found_skills,
        'soft_skills': sorted(list(set(found_soft))),
        'languages': sorted(list(set(found_languages))),
        'certifications': sorted(list(set(found_certs))),
        'total_experience': total_experience,
        'total_skills': len(total_technical_skills) + len(found_soft),
    }


def generate_industry_specific_recommendations(skills_data: Dict) -> str:
    """
    Generate recommendations based on detected industry.
    """
    industries = skills_data.get('detected_industries', [])
    
    recommendations = []
    
    if 'technology' in industries:
        recommendations.append("""
### 💻 Technology Career Path:
- **High Demand**: Cloud (AWS/Azure), AI/ML, DevOps
- **Consider Learning**: Kubernetes, Docker, Microservices
- **Trending**: Generative AI, LLM development, Prompt Engineering
        """)
    
    if 'finance' in industries:
        recommendations.append("""
### 💰 Finance Career Path:
- **High Demand**: Financial modeling, Data analysis, Python
- **Consider Learning**: Bloomberg Terminal, SQL, Power BI
- **Certifications**: CFA, CPA valuable for advancement
        """)
    
    if 'healthcare' in industries:
        recommendations.append("""
### 🏥 Healthcare Career Path:
- **High Demand**: Healthcare IT, Telehealth, Data Analytics
- **Consider Learning**: Epic/Cerner systems, Healthcare analytics
- **Certifications**: Specialty certifications boost salary significantly
        """)
    
    if 'marketing' in industries:
        recommendations.append("""
### 📢 Marketing Career Path:
- **High Demand**: Digital marketing, SEO/SEM, Analytics
- **Consider Learning**: Google Analytics, HubSpot, Data visualization
- **Trending**: AI-powered marketing, Marketing automation
        """)
    
    if not recommendations:
        recommendations.append("""
### 🎯 General Career Advice:
- Identify your strongest skill category
- Research job market demand in your area
- Consider certifications relevant to your field
- Build portfolio/case studies to demonstrate skills
        """)
    
    return "\n".join(recommendations)

def generate_ats_suggestions(resume_text: str):
    """
    Generates ATS optimization suggestions based on resume content.
    This is a lightweight fallback function so the app does not crash.
    """
    if not resume_text:
        return "No resume content available for ATS analysis."

    suggestions = [
        "Use consistent formatting, avoid tables and text boxes.",
        "Add measurable achievements (numbers & metrics).",
        "Include job-title keywords from your target roles.",
        "Use standard section headings (Experience, Skills, Projects).",
        "Ensure all acronyms are expanded once (e.g., Machine Learning (ML)).",
        "Avoid images or decorative icons.",
        "Use simple fonts like Arial, Calibri, or Helvetica.",
    ]

    return "### ATS Optimization Suggestions\n" + "\n".join([f"- {s}" for s in suggestions])
