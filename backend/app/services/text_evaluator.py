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
        message = f"You are an expert in the job market for ghost job detection. Using your expertise, \
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


        response = await llm.message(message)
        return response