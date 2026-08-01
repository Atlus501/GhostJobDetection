import requests
from schemas.requests import TestRequest

test_payload = TestRequest(
    company = "Relativity",
    position = "Software Engineer",
    description = """
        As a Software Engineer, you will build and operate backend services that power Relativity’s generative AI platform, aiR. You will work at the intersection of distributed systems, cloud infrastructure, and applied AI, helping to deliver reliable, scalable systems that sit on the critical path of AI-powered workflows.

        This role reports to the Manager of Software Engineering and provides the opportunity to work on multi-region, multi-cloud systems that handle large-scale AI traffic and complex orchestration challenges.
        """,
    responsibilities = """
        What You’ll Do

        Design and build performant, scalable, and secure backend services with a strong focus on quality, not just meeting requirements
        Collaborate with a software development team to deliver high-quality, reliable systems that operate at massive scale
        Develop and maintain systems that support high-throughput AI workloads, including asynchronous job orchestration and distributed processing
        Write comprehensive unit and integration tests supported by static analysis and thoughtful test strategy development
        Contribute to improving engineering processes by recommending enhancements to tools, workflows, and practices
        Participate in pair programming to improve software quality and share design and implementation knowledge
        Contribute to building systems that route and manage AI traffic efficiently while maintaining reliability and fairness across workloads
        """,
    requirements = """
        Bachelor’s degree in Computer Science or a related field, or equivalent practical experience
        Experience building backend services using languages such as C#, Python, or similar
        Understanding of software engineering disciplines and the ability to work across multiple layers of the application stack
        Strong foundational knowledge of distributed systems, scalability, and backend service design

        Preferred

        Understanding of DevOps principles and experience with tools such as GitHub Actions
        Experience working with large language model (LLM) APIs or generative AI systems
        Experience designing and building scalable systems in Azure or other cloud platforms
        Experience with Kubernetes, serverless technologies, and cloud-native architectures
        Familiarity with domain-driven design and event-driven architecture
        Experience with AI-driven development practices or AI-assisted coding tools
        Awareness of emerging technology trends and their practical application in engineering
        """,
    salary = "$79,000 and $119,000",
    company_description = """
        WHO WE ARE
        Relativity is a leading legal data intelligence company building technology that helps users organize data, discover the truth, and act on it with confidence. Our AI-powered, cloud platform, RelativityOne, transforms massive volumes of complex information into actionable insights for litigation, investigations, regulatory inquiries, data breach responses, and other high-stakes legal work where accuracy and trust are crucial.
        The world’s largest law firms, corporations, and government agencies rely on Relativity’s legal AI software to securely surface and manage the most relevant and impactful information in their matters. Beyond our commercial impact, we’re deeply committed to expanding access to technology for academic institutions through Relativity Academic and supporting pro bono legal work through Justice for Change.
        """,
    miscellaneous_benefits = """
        Competitive salary, health and retirement programs, wellness resources, discretionary time off (DTO), parental leave for primary and secondary caregivers, company-wide breaks, home office stipend, and an equity program.
        """,
    days_opened = 35,
    post_on_website = True,
    hiring_timeline = False,
    hiring_manager_listed = False,
)

#tests the endpoint for calculating the probability of an output
x = requests.post(url='http://127.0.0.1:8000/test', json=test_payload.model_dump())

print(x.json())