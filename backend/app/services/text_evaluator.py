from schemas.job import Job

"""
Class for connecting with GLM to evalute job posting vaguness
"""
class TextEvaluator:
    """
    Constructor for the GLM class
    """
    def __init__(self, llm):
        self.llm = llm

    """
    Function for rating job vagueness
    """
    async def rate_job(self, job : Job):
        system_prompt = """You are a senior recruitment auditor specialized in detecting ghost jobs (fake, outdated, or non-viable job postings).
            Your task is to analyze the provided job posting against a standardized risk rubric and determine a Ghost Job Likelihood Score from 0.0 to 10.0.

            ### SCORING RUBRIC (Sum applicable risk points):
            1. Salary Transparency:
            - Missing or listed as "N/A" / "Competitive": +1.5 points
            - Unrealistically high or extreme range (e.g., $30,000 - $300,000): +2.0 points
            2. Role Definition & Responsibilities:
            - Extremely generic/copy-pasted bullet points (< 3 specific technical tools or key deliverables): +2.0 points
            - Mismatch between Position Title and actual Responsibilities: +2.0 points
            3. Company & Context:
            - Missing or overly generic Company Description: +1.5 points
            - Absence of specific team, project, or domain context: +1.0 point
            4. Requirements & Anomalies:
            - Contradictory experience requirements (e.g., "Entry-Level" requiring 5+ years experience): +2.0 points
            - Overly vague or missing requirements: +1.0 point

            ### OUTPUT FORMAT:
            You MUST respond with a valid JSON object matching this schema exactly. Do not include markdown formatting outside the JSON block.
            Do not format your response with ANYTHING else. It must purely be a string that looks like a JSON object with the following structure:

            {
            "reasoning": "Brief step-by-step breakdown evaluating salary, responsibilities, company details, and requirements.",
            "risk_factors": ["List of specific flags detected, if any"],
            "final_rating": 0.0
            }
        """

        user_prompt = USER_PROMPT = f"""Evaluate the following job posting:
            - Position: {job.position or 'Not Provided'}
            - Salary: {job.salary or 'Not Provided'}
            - Company Description: {job.company_description or 'Not Provided'}
            - Job Description: {job.description or 'Not Provided'}
            - Responsibilities: {job.responsibilities or 'Not Provided'}
            - Requirements: {job.requirements or 'Not Provided'}
            - Miscellaneous Benefits: {job.miscellaneous_benefits or 'Not Provided'}
            """

        response = await self.llm.message(system_prompt, user_prompt)
        return response