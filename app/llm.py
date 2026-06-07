from app.schemas.models import IncidentClassification
import re

class MockResponse:
    def __init__(self, content):
        self.content = content


class MockStructuredLLM:

    def invoke(self, incident):

        incident = incident.lower()

        if "deployment" in incident:

            version_match = re.search(
        r'v\d+\.\d+\.\d+',
        incident)

            version = (
                version_match.group()
                if version_match
                else "unknown"
            )

            return IncidentClassification(
                severity="P1",
                category="deployment",
                entities=[version]
            )

        elif "database" in incident:
            return IncidentClassification(
                severity="P1",
                category="database",
                entities=["postgres"]
            )

        elif "dns" in incident:
            return IncidentClassification(
                severity="P2",
                category="network",
                entities=["dns"]
            )

        elif "disk" in incident:
            server_match = re.search(
                r'server\d+',
                incident
            )

            server = (
                server_match.group()
                if server_match
                else "unknown"
            )
            return IncidentClassification(
                severity="P2",
                category="infra",
                entities=[server]
            )
        elif "customer-portal" in incident:
            service_match = re.search(
                r'customer-[a-z-]+',
                incident
            )

            service = (
                service_match.group()
                if service_match
                else "unknown"
            )
            return IncidentClassification(
                severity="P3",
                category="application",
                entities=[service]
            )
        return IncidentClassification(
            severity="P3",
            category="application",
            entities=["unknown"]
        )


class MockLLM:

    def invoke(self, prompt):

        return MockResponse(
            """
            1. Verify issue
            2. Restart service
            3. Validate metrics
            4. Monitor system
            """
        )

    def with_structured_output(self, schema):

        return MockStructuredLLM()


llm = MockLLM()