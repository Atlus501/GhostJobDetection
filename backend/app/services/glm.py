from zai import ZaiClient

from app.config.settings import settings

"""
Class for connecting with GLM to evalute job posting vaguness
"""
class GLM:
    """
    Constructor for the GLM class
    """
    def __init__(self):
        self.model_name = settings.GLM_MODEL
        self.client = ZaiClient(api_key=settings.ZAI_API)

    """
    Function for rating job vagueness
    """
    def rate_job(self, job : Job):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": f"You are an expert in the job market for ghost job detection. Using your expertise, \
                                please evaluate the vagueness/realisticness of following information for the job posting based on what is \
                                typically written for the position. After your analysis, please rate how likely the position \
                                is ghost job based on how vague, unrealistic, or miscellaneous anomolies of the job description based on a scale of 0 to 10. \
                                0 being that this position is almost guaranteed to not be a ghost job. 10 being that this position is almost guaranteed to be a ghost job.\
                                When giving your final evaluation, always state your final rating at the end of the response, and precede your final rating with the phrase \"Final Rating: \"  \
                                Company : {job.company} \
                                Position : {job.position} \
                                Salary : {job.salary} \
                                Job Description: {job.description}\
                                Miscellaneous Benefits : {job.miscellaneous_benefits} \
                                Requirements : {job.requirements} \
                                Company Description : {job.company_description} \
                                Responsibilities : {job.responsibilities} \
                                "
                },
            ],
            thinking={
                "type": "enabled",  # Optional: "disabled" or "enabled", default is "enabled"
            },
            max_tokens=4096,
            temperature=0.6,
        )

        return response.choices[0].message.content