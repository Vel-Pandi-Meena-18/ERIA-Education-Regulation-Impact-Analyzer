import json
import os
import time

import requests
import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ERIA - Education Regulation Impact Analyzer",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📚 ERIA")
st.subheader("Education Regulation Impact Analyzer")

st.write(
    "Analyze education regulations and guidelines using AI."
)


# ============================================================
# GEMINI API
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# SESSION STATE
# ============================================================

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = None

if "document_name" not in st.session_state:
    st.session_state["document_name"] = None


# ============================================================
# INPUT METHOD
# ============================================================

input_method = st.radio(
    "Choose how you want to provide the document:",
    ["Upload PDF", "Paste URL"],
    horizontal=True
)


# ============================================================
# OPTION 1 — UPLOAD PDF
# ============================================================

if input_method == "Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload Regulation / Guideline PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        pdf_path = "temp_uploaded_document.pdf"

        with open(pdf_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        st.session_state["pdf_path"] = pdf_path
        st.session_state["document_name"] = uploaded_file.name

        st.success(
            f"✅ Uploaded: {uploaded_file.name}"
        )


# ============================================================
# OPTION 2 — PASTE URL
# ============================================================

else:

    document_url = st.text_input(
        "Paste the direct PDF URL here:",
        placeholder="https://example.com/document.pdf"
    )

    if st.button("Download Document"):

        if not document_url:

            st.warning(
                "Please enter a PDF URL first."
            )

        else:

            try:

                with st.spinner(
                    "Downloading document..."
                ):

                    response = requests.get(
                        document_url,
                        timeout=30
                    )

                    response.raise_for_status()

                    content_type = response.headers.get(
                        "content-type",
                        ""
                    ).lower()

                    if (
                        "application/pdf" not in content_type
                        and not document_url.lower().endswith(".pdf")
                    ):

                        st.error(
                            "The URL did not return a PDF document."
                        )

                        st.stop()

                    pdf_path = "temp_url_document.pdf"

                    with open(pdf_path, "wb") as file:
                        file.write(response.content)

                    st.session_state["pdf_path"] = pdf_path

                    file_name = document_url.split("/")[-1]

                    if "?" in file_name:
                        file_name = file_name.split("?")[0]

                    if not file_name.lower().endswith(".pdf"):
                        file_name = "URL_Document.pdf"

                    st.session_state["document_name"] = file_name

                st.success(
                    "✅ Document downloaded successfully."
                )

                st.write(
                    f"**Document:** "
                    f"{st.session_state['document_name']}"
                )

            except Exception as error:

                st.error(
                    f"Could not download the document: {error}"
                )


# ============================================================
# GET CURRENT DOCUMENT
# ============================================================

pdf_path = st.session_state.get("pdf_path")
document_name = st.session_state.get("document_name")


# ============================================================
# ANALYZE DOCUMENT
# ============================================================

if pdf_path is not None:

    st.info(
        f"Ready to analyze: **{document_name}**"
    )

    if st.button(
        "🔍 Analyze Document",
        type="primary"
    ):

        # Start processing timer
        start_time = time.perf_counter()

        try:

            # ==================================================
            # UPLOAD PDF TO GEMINI
            # ==================================================

            with st.spinner(
                "Uploading document to Gemini..."
            ):

                gemini_file = client.files.upload(
                    file=pdf_path
                )


            # ==================================================
            # ERIA PROMPT
            # ==================================================

            prompt = """
You are ERIA (Education Regulation Impact Analyzer).

Analyze the uploaded education policy document.

Return ONLY valid JSON.
Do not use Markdown.
Do not use code fences.

Return exactly this structure:

{
  "document_category": {
    "category": "",
    "reason": ""
  },

  "summary": "",

  "purpose": "",

  "chronology": {
    "predecessors": [],
    "amendments": [],
    "frameworks_and_policies": [],
    "committees": [],
    "historical_notes": []
  },

  "stakeholder_impact": {
    "students": {
      "benefits": [],
      "constraints": []
    },
    "faculty": {
      "benefits": [],
      "constraints": []
    },
    "institutions": {
      "benefits": [],
      "constraints": []
    },
    "administrators": {
      "benefits": [],
      "constraints": []
    },
    "accreditation_compliance_teams": {
      "benefits": [],
      "constraints": []
    }
  },

  "risk_and_implementation": {
    "controversial_areas": [],
    "implementation_issues": [],
    "institutional_readiness_challenges": [],
    "compliance_resource_challenges": []
  },

  "impact_assessment": {
    "short_term_0_1_year": [],
    "medium_term_1_5_years": [],
    "long_term_over_5_years": []
  },

  "positives": [],

  "negatives": [],

  "opportunities": [],

  "recommendations": {
    "students": [],
    "faculty": [],
    "institutions": [],
    "administrators": []
  }
}

IMPORTANT RULES:

1. Base factual claims ONLY on the uploaded document.
2. Do not invent facts, dates, amendments, committees or historical events.
3. If information is not mentioned, return an empty list.
4. The summary should be easy to understand and approximately 10-20 lines.
5. Clearly label reasonable future projections as "AI Inference".
6. Keep benefits and constraints separate.
7. Return ONLY valid JSON.
"""


            # ==================================================
            # GEMINI ANALYSIS
            # ==================================================

            with st.spinner(
                "🤖 ERIA is analyzing the document..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        gemini_file,
                        prompt
                    ]
                )


            # ==================================================
            # PROCESSING TIME
            # ==================================================

            processing_time = (
                time.perf_counter() - start_time
            )


            # ==================================================
            # CLEAN GEMINI RESPONSE
            # ==================================================

            result_text = response.text.strip()

            if result_text.startswith("```json"):

                result_text = result_text[
                    len("```json"):
                ].strip()

            if result_text.startswith("```"):

                result_text = result_text[
                    len("```"):
                ].strip()

            if result_text.endswith("```"):

                result_text = result_text[
                    :-3
                ].strip()


            # ==================================================
            # PARSE JSON
            # ==================================================

            eria_result = json.loads(
                result_text
            )

            st.success(
                "✅ ERIA analysis completed successfully!"
            )


            # ==================================================
            # PROCESSING TIME DISPLAY
            # ==================================================

            time_col1, time_col2 = st.columns(2)

            with time_col1:

                st.metric(
                    "⏱️ Processing Time",
                    f"{processing_time:.2f} seconds"
                )

            with time_col2:

                st.metric(
                    "📄 Document",
                    document_name
                )


            # ==================================================
            # DOCUMENT CATEGORY
            # ==================================================

            st.header("📌 Document Category")

            category_data = eria_result[
                "document_category"
            ]

            st.subheader(
                category_data["category"]
            )

            st.write(
                category_data["reason"]
            )


            # ==================================================
            # SUMMARY
            # ==================================================

            st.header("📝 Summary")

            st.write(
                eria_result["summary"]
            )


            # ==================================================
            # PURPOSE
            # ==================================================

            st.header("🎯 Purpose")

            st.write(
                eria_result["purpose"]
            )


            # ==================================================
            # CHRONOLOGY & POLICY MAPPING
            # ==================================================

            st.header(
                "🕒 Chronology & Policy Mapping"
            )

            chronology = eria_result[
                "chronology"
            ]


            # --------------------------------------------------
            # POLICY TIMELINE
            # --------------------------------------------------

            st.subheader(
                "📅 Policy Timeline"
            )

            timeline_items = []


            for item in chronology.get(
                "predecessors",
                []
            ):

                timeline_items.append(
                    {
                        "type": "Predecessor",
                        "text": item
                    }
                )


            for item in chronology.get(
                "amendments",
                []
            ):

                timeline_items.append(
                    {
                        "type": "Amendment",
                        "text": item
                    }
                )


            for item in chronology.get(
                "historical_notes",
                []
            ):

                timeline_items.append(
                    {
                        "type": "Historical",
                        "text": item
                    }
                )


            if timeline_items:

                for index, item in enumerate(
                    timeline_items
                ):

                    if index == len(
                        timeline_items
                    ) - 1:

                        connector = "└──"

                    else:

                        connector = "├──"

                    st.markdown(
                        f"""
**{connector} {item["type"]}**

{item["text"]}
"""
                    )

            else:

                st.info(
                    "No predecessor, amendment, "
                    "or historical timeline information "
                    "was identified."
                )


            # --------------------------------------------------
            # FRAMEWORKS & POLICIES
            # --------------------------------------------------

            st.subheader(
                "📚 Related Frameworks & Policies"
            )

            frameworks = chronology.get(
                "frameworks_and_policies",
                []
            )

            if frameworks:

                for item in frameworks:

                    st.write(
                        "🔹 " + item
                    )

            else:

                st.info(
                    "No related frameworks or policies "
                    "were identified."
                )


            # --------------------------------------------------
            # COMMITTEES
            # --------------------------------------------------

            st.subheader(
                "🏛️ Committees / Bodies"
            )

            committees = chronology.get(
                "committees",
                []
            )

            if committees:

                for item in committees:

                    st.write(
                        "🔹 " + item
                    )

            else:

                st.info(
                    "No committees or related bodies "
                    "were identified."
                )


            # --------------------------------------------------
            # POLICY RELATIONSHIP MAP
            # --------------------------------------------------

            st.subheader(
                "🔗 Policy Relationship Map"
            )

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.markdown(
                    "### 📜 Previous"
                )

                if chronology.get(
                    "predecessors"
                ):

                    for item in chronology[
                        "predecessors"
                    ]:

                        st.write(
                            "• " + item
                        )

                else:

                    st.write(
                        "No predecessor identified."
                    )


            with col2:

                st.markdown(
                    "### 🔄 Amendments"
                )

                if chronology.get(
                    "amendments"
                ):

                    for item in chronology[
                        "amendments"
                    ]:

                        st.write(
                            "• " + item
                        )

                else:

                    st.write(
                        "No amendments identified."
                    )


            with col3:

                st.markdown(
                    "### 📚 Frameworks"
                )

                if frameworks:

                    for item in frameworks:

                        st.write(
                            "• " + item
                        )

                else:

                    st.write(
                        "None identified."
                    )


            with col4:

                st.markdown(
                    "### 📌 Current Policy"
                )

                st.write(
                    document_name
                )


            # ==================================================
            # STAKEHOLDER IMPACT
            # ==================================================

            st.header(
                "👥 Stakeholder Impact"
            )

            stakeholders = eria_result[
                "stakeholder_impact"
            ]


            # --------------------------------------------------
            # STAKEHOLDER CARDS
            # --------------------------------------------------

            stakeholder_items = list(
                stakeholders.items()
            )


            for row_start in range(
                0,
                len(stakeholder_items),
                2
            ):

                row_items = stakeholder_items[
                    row_start:row_start + 2
                ]

                columns = st.columns(
                    len(row_items)
                )


                for column, (
                    stakeholder,
                    data
                ) in zip(
                    columns,
                    row_items
                ):

                    with column:

                        st.markdown(
                            f"### 👤 "
                            f"{stakeholder.replace('_', ' ').title()}"
                        )


                        # Benefits
                        st.markdown(
                            "**✅ Benefits**"
                        )

                        benefits = data.get(
                            "benefits",
                            []
                        )

                        if benefits:

                            for item in benefits:

                                st.write(
                                    "• " + item
                                )

                        else:

                            st.write(
                                "No benefits identified."
                            )


                        # Constraints
                        st.markdown(
                            "**⚠️ Constraints**"
                        )

                        constraints = data.get(
                            "constraints",
                            []
                        )

                        if constraints:

                            for item in constraints:

                                st.write(
                                    "• " + item
                                )

                        else:

                            st.write(
                                "No constraints identified."
                            )


                st.divider()


            # ==================================================
            # RISKS & IMPLEMENTATION
            # ==================================================

            st.header(
                "⚠️ Risks & Implementation Challenges"
            )

            risks = eria_result[
                "risk_and_implementation"
            ]

            for section, items in risks.items():

                if items:

                    st.subheader(
                        section.replace(
                            "_", " "
                        ).title()
                    )

                    for item in items:

                        st.write(
                            "• " + item
                        )


            # ==================================================
            # IMPACT ASSESSMENT
            # ==================================================

            st.header(
                "📅 Impact Assessment"
            )

            impacts = eria_result[
                "impact_assessment"
            ]

            impact_columns = st.columns(3)

            impact_titles = {
                "short_term_0_1_year":
                    "🟢 Short Term (0–1 Year)",

                "medium_term_1_5_years":
                    "🟡 Medium Term (1–5 Years)",

                "long_term_over_5_years":
                    "🔵 Long Term (>5 Years)"
            }


            for column, (
                section,
                items
            ) in zip(
                impact_columns,
                impacts.items()
            ):

                with column:

                    st.subheader(
                        impact_titles.get(
                            section,
                            section.replace(
                                "_", " "
                            ).title()
                        )
                    )

                    if items:

                        for item in items:

                            st.write(
                                "• " + item
                            )

                    else:

                        st.write(
                            "No information identified."
                        )


            # ==================================================
            # POSITIVES
            # ==================================================

            st.header(
                "✅ Positives"
            )

            positives = eria_result[
                "positives"
            ]

            if positives:

                for item in positives:

                    st.write(
                        "• " + item
                    )

            else:

                st.info(
                    "No positive points identified."
                )


            # ==================================================
            # NEGATIVES
            # ==================================================

            st.header(
                "❌ Negatives / Constraints"
            )

            negatives = eria_result[
                "negatives"
            ]

            if negatives:

                for item in negatives:

                    st.write(
                        "• " + item
                    )

            else:

                st.info(
                    "No negative points identified."
                )


            # ==================================================
            # OPPORTUNITIES
            # ==================================================

            st.header(
                "💡 Opportunities"
            )

            opportunities = eria_result[
                "opportunities"
            ]

            if opportunities:

                for item in opportunities:

                    st.write(
                        "• " + item
                    )

            else:

                st.info(
                    "No opportunities identified."
                )


            # ==================================================
            # RECOMMENDATIONS
            # ==================================================

            st.header(
                "📋 Recommendations"
            )

            recommendations = eria_result[
                "recommendations"
            ]

            for stakeholder, items in recommendations.items():

                st.subheader(
                    stakeholder.replace(
                        "_", " "
                    ).title()
                )

                if items:

                    for item in items:

                        st.write(
                            "• " + item
                        )

                else:

                    st.write(
                        "No recommendations identified."
                    )


        # =====================================================
        # JSON ERROR
        # =====================================================

        except json.JSONDecodeError:

            st.error(
                "Gemini returned an invalid JSON response."
            )

            st.text_area(
                "Raw Gemini Response",
                result_text
            )


        # =====================================================
        # GENERAL ERROR
        # =====================================================

        except Exception as error:

            st.error(
                f"An error occurred: {error}"
            )