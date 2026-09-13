from schemas.match_result import (
    MatchResult,
    SkillMatch
)


class MatchEngine:

    def calculate(
        self,
        required_skills: list[str],
        candidate_text: str,
        job_text: str
    ) -> MatchResult:

        candidate_lower = candidate_text.lower()

        skill_matches = []

        for skill in required_skills:

            skill_lower = skill.lower()

            if skill_lower in candidate_lower:

                evidence_level = "strong"

                score = 100

                evidence = [
                    f"简历中明确出现技能：{skill}"
                ]

            else:

                evidence_level = "none"

                score = 0

                evidence = []

            skill_matches.append(
                SkillMatch(
                    skill=skill,
                    evidence_level=evidence_level,
                    evidence=evidence,
                    score=score
                )
            )

        if required_skills:

            skill_score = (
                sum(
                    item.score
                    for item in skill_matches
                )
                / len(required_skills)
            )

        else:

            skill_score = 0

        project_evidence_score = self._project_score(
            candidate_text
        )

        responsibility_score = self._responsibility_score(
            candidate_text,
            job_text
        )

        experience_score = 70

        education_score = 70

        semantic_score = 70

        overall_score = (
            skill_score * 0.30
            + responsibility_score * 0.20
            + project_evidence_score * 0.20
            + experience_score * 0.10
            + education_score * 0.05
            + semantic_score * 0.15
        )

        gaps = [
            item.skill
            for item in skill_matches
            if item.score == 0
        ]

        verification_items = [
            f"需要验证：{skill}"
            for skill in gaps
        ]

        if overall_score >= 85:

            recommendation = "strong_match"

        elif overall_score >= 70:

            recommendation = "match"

        elif overall_score >= 55:

            recommendation = "interview_verify"

        else:

            recommendation = "weak_match"

        return MatchResult(
            overall_score=round(
                overall_score,
                1
            ),
            skill_score=round(
                skill_score,
                1
            ),
            responsibility_score=round(
                responsibility_score,
                1
            ),
            project_evidence_score=round(
                project_evidence_score,
                1
            ),
            experience_score=experience_score,
            education_score=education_score,
            semantic_score=semantic_score,
            skill_matches=skill_matches,
            strengths=[
                item.skill
                for item in skill_matches
                if item.score >= 80
            ],
            gaps=gaps,
            verification_items=verification_items,
            recommendation=recommendation
        )

    def _project_score(
        self,
        candidate_text: str
    ) -> float:

        keywords = [
            "项目",
            "实现",
            "开发",
            "负责",
            "部署",
            "系统"
        ]

        count = sum(
            1
            for keyword in keywords
            if keyword in candidate_text
        )

        return min(
            100,
            count * 15
        )

    def _responsibility_score(
        self,
        candidate_text: str,
        job_text: str
    ) -> float:

        keywords = [
            "开发",
            "RAG",
            "Agent",
            "Python",
            "工具调用"
        ]

        matches = sum(
            1
            for keyword in keywords
            if keyword in candidate_text
            and keyword in job_text
        )

        if not keywords:
            return 0

        return min(
            100,
            matches / len(keywords) * 100
        )