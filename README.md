# 📚 ERIA — Education Regulation Impact Analyzer

### Simplifying Complex Education Policies into Actionable Insights

ERIA (Education Regulation Impact Analyzer) is an AI-powered application designed to analyze complex education regulations, guidelines, circulars, and policy documents and convert them into clear, stakeholder-friendly insights.

The system uses the Google Gemini API and a Streamlit dashboard to analyze education policy documents and explain their purpose, historical context, stakeholder impact, risks, opportunities, and expected implications across different timeframes.

---

## 🎯 Project Overview

Education regulations and academic policies are often written in complex legal, administrative, and academic language.

Students, faculty, institutions, administrators, and compliance teams may find it difficult to quickly understand:

- What a regulation proposes or changes
- Why the regulation was introduced
- How it relates to previous regulations or amendments
- Which stakeholders are affected
- What benefits and constraints may arise
- What implementation challenges institutions may face
- What the short-term, medium-term, and long-term implications may be

ERIA addresses this problem by providing an AI-powered policy analysis platform that transforms lengthy education documents into structured and easy-to-understand insights.

---

## 💡 Key Features

### 📄 1. Multiple Document Input Methods

Users can provide education policy documents through:

- PDF file upload
- Direct PDF URL

The application is designed to work with education regulations, guidelines, circulars, and related policy documents.

---

### 🏷️ 2. Regulation Topic Classification

ERIA automatically identifies the broad category of the uploaded education document.

Examples include:

- Curriculum
- Admissions
- Examination
- Faculty Policy
- Accreditation
- Scholarships
- Academic Regulations
- Institutional Policy

The system also provides a reason for the assigned category.

---

### 📝 3. AI-Powered Simplified Summary

ERIA converts complex policy language into an easy-to-understand summary.

The summary focuses on:

- What the policy says
- Why it matters
- What it changes
- Who is affected
- What stakeholders should understand

---

### 🎯 4. Purpose Analysis

The system identifies the purpose and intent of the regulation based on the information available in the source document.

---

### 🕒 5. Chronology & Policy Mapping

ERIA analyzes the historical context of the document and identifies relevant:

- Predecessor regulations
- Amendments
- Historical notes
- Related frameworks and policies
- Committees or institutional bodies

The Streamlit dashboard presents this information through a policy timeline and relationship mapping view.

---

### 👥 6. Stakeholder Impact Analysis

ERIA identifies potential benefits and constraints for major education stakeholders.

#### 🎓 Students
- Benefits
- Constraints
- Recommendations

#### 👨‍🏫 Faculty
- Benefits
- Constraints
- Recommendations

#### 🏛️ Institutions
- Benefits
- Constraints
- Recommendations

#### 👔 Administrators
- Benefits
- Constraints
- Recommendations

#### 📋 Accreditation & Compliance Teams
- Benefits
- Constraints

---

### ⚠️ 7. Risk & Implementation Analysis

The system identifies potential implementation concerns such as:

- Controversial areas
- Implementation issues
- Institutional readiness challenges
- Compliance and resource challenges

This helps institutions understand possible operational and compliance implications.

---

### 📅 8. Impact Assessment

ERIA provides structured impact analysis across three timeframes:

| Timeframe | Analysis |
|-----------|----------|
| 🟢 Short Term | 0–1 year |
| 🟡 Medium Term | 1–5 years |
| 🔵 Long Term | More than 5 years |

Future-oriented observations are explicitly identified as AI inference where applicable.

---

### ✅ 9. Positives & Negatives

The system provides a simple bullet-point analysis of:

- Positive aspects
- Negative aspects
- Constraints
- Potential opportunities

---

### 💡 10. Opportunity Detection

ERIA identifies potential academic and institutional opportunities that may emerge from the regulation.

---

### 📋 11. Stakeholder Recommendations

The system generates practical recommendations for:

- Students
- Faculty
- Institutions
- Administrators

---

### ⏱️ 12. Processing-Time Measurement

The dashboard records and displays the approximate time required to process and analyze each document.

This supports the project's processing-time evaluation metric.

---

# 🏗️ System Workflow

```text
                 ┌──────────────────────┐
                 │   Education Policy   │
                 │       Document       │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   PDF Upload / URL   │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │ Document Processing  │
                 │ & Ingestion          │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │    Google Gemini     │
                 │     LLM Analysis     │
                 └──────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     Classification    Chronology       Stakeholder
                        Mapping           Impact
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │ Risk & Impact     │
                  │ Assessment        │
                  └─────────┬─────────┘
                            │
                  ┌─────────▼─────────┐
                  │ Structured JSON   │
                  │ Analysis          │
                  └─────────┬─────────┘
                            │
                  ┌─────────▼─────────┐
                  │    Streamlit      │
                  │    Dashboard      │
                  └───────────────────┘
