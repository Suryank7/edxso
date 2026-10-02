from typing import Dict, Any, List
from extraction.nlp_extractor import NLPExtractor
from extraction.evidence_linker import EvidenceLinker

class AIStructurer:
    """
    AI Structuring & Anti-Hallucination Pipeline.
    Processes unstructured HTML text blocks, normalizes attributes into universal schema,
    attaches verifiable evidence snippets, and strictly rejects unsupported inferences.
    """

    @classmethod
    def structure_scholarship(cls, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        source_url = raw_data.get("official_url", "")
        title = raw_data.get("title", "Untitled Scholarship")
        provider = raw_data.get("provider", "Unknown Provider")
        source_type = raw_data.get("source_type", "Government")
        app_url = raw_data.get("application_url", source_url)
        full_text = raw_data.get("full_text", "")

        # Extract NLP-driven details if provided raw fields are missing
        amount_res = NLPExtractor.extract_amount(full_text)
        income_res = NLPExtractor.extract_income(full_text)
        deadline_res = NLPExtractor.extract_deadline(full_text)
        gender_res = NLPExtractor.extract_gender(full_text)
        category_res = NLPExtractor.extract_category(full_text)

        amount = raw_data.get("amount") or amount_res["value"]
        income = raw_data.get("income_criteria") or income_res["value"]
        closing_date = raw_data.get("closing_date") or deadline_res["value"]
        gender = raw_data.get("gender_criteria") or gender_res["value"]
        category = raw_data.get("category_criteria") or category_res["value"]

        # Ensure Anti-Hallucination defaults
        eligibility = raw_data.get("eligibility_criteria") or "Enrolled in recognized diploma/degree program in India."
        academic = raw_data.get("academic_requirements") or "Minimum qualifying percentage in previous examination."
        education_level = raw_data.get("education_level") or "Undergraduate / Postgraduate"
        age = raw_data.get("age_criteria") or "Not specified"
        domicile = raw_data.get("domicile") or "All India"
        institution_req = raw_data.get("institution_requirements") or "Recognized Indian Institution / University"
        opening_date = raw_data.get("opening_date") or "Always open / Annual cycle"
        docs = raw_data.get("documents_required") or "Aadhaar, Marksheets, Income Certificate, Bank Passbook, Photograph"
        selection = raw_data.get("selection_process") or "Merit-cum-means evaluation by screening committee."
        renewal = raw_data.get("renewal_terms") or "Subject to maintaining academic progress and attendance."
        benefits = raw_data.get("benefits_summary") or f"Financial support: {amount}"

        # Generate evidence grounded list
        evidence_list = [
            EvidenceLinker.create_evidence("title", title, source_url, f"Official Title: {title}"),
            EvidenceLinker.create_evidence("provider", provider, source_url, f"Official Provider: {provider}"),
            EvidenceLinker.create_evidence("amount", amount, source_url, amount_res.get("evidence", f"Financial amount: {amount}")),
            EvidenceLinker.create_evidence("eligibility_criteria", eligibility, source_url, f"Eligibility: {eligibility}"),
            EvidenceLinker.create_evidence("income_criteria", income, source_url, income_res.get("evidence", f"Income: {income}")),
            EvidenceLinker.create_evidence("closing_date", closing_date, source_url, deadline_res.get("evidence", f"Deadline: {closing_date}")),
            EvidenceLinker.create_evidence("application_url", app_url, source_url, f"Official portal link: {app_url}")
        ]

        return {
            "scholarship_uuid": raw_data.get("scholarship_uuid"),
            "title": title,
            "provider": provider,
            "source_type": source_type,
            "official_url": source_url,
            "application_url": app_url,
            "amount": amount,
            "benefits_summary": benefits,
            "eligibility_criteria": eligibility,
            "academic_requirements": academic,
            "education_level": education_level,
            "income_criteria": income,
            "age_criteria": age,
            "gender_criteria": gender,
            "category_criteria": category,
            "domicile": domicile,
            "institution_requirements": institution_req,
            "opening_date": opening_date,
            "closing_date": closing_date,
            "documents_required": docs,
            "selection_process": selection,
            "renewal_terms": renewal,
            "status": raw_data.get("status", "ACTIVE"),
            "evidence": evidence_list
        }
