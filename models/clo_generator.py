"""
CLO Generator Module
This module uses NLP techniques to generate Course Learning Outcomes (CLOs) from course content.
"""

import re
import random

class CLOGenerator:
    """Class for generating CLOs from course content."""

    def __init__(self):
        """Initialize the CLO generator with action verbs."""
        # Define action verbs for CLOs
        self.action_verbs = [
            # Knowledge and Understanding
            'define', 'describe', 'identify', 'know', 'label', 'list', 'match', 'name',
            'outline', 'recall', 'recognize', 'select', 'state', 'memorize', 'repeat',
            'record', 'relate', 'reproduce', 'retrieve', 'comprehend', 'convert', 'defend',
            'distinguish', 'estimate', 'explain', 'extend', 'generalize', 'give examples',
            'infer', 'interpret', 'paraphrase', 'predict', 'rewrite', 'summarize', 'translate',
            'classify', 'discuss', 'illustrate', 'recognize', 'report', 'express', 'locate',

            # Application and Analysis
            'apply', 'change', 'compute', 'construct', 'demonstrate', 'discover', 'manipulate',
            'modify', 'operate', 'predict', 'prepare', 'produce', 'relate', 'show', 'solve',
            'use', 'implement', 'execute', 'complete', 'examine', 'classify', 'experiment',
            'calculate', 'illustrate', 'practice', 'analyze', 'break down', 'compare', 'contrast',
            'diagram', 'deconstruct', 'differentiate', 'discriminate', 'distinguish', 'identify',
            'illustrate', 'infer', 'outline', 'relate', 'select', 'separate', 'categorize',
            'criticize', 'experiment', 'question', 'test', 'examine', 'inspect', 'debate',

            # Evaluation and Creation
            'appraise', 'argue', 'assess', 'attach', 'choose', 'compare', 'defend', 'estimate',
            'evaluate', 'judge', 'predict', 'rate', 'select', 'support', 'value', 'critique',
            'justify', 'measure', 'recommend', 'review', 'score', 'coordinate', 'prioritize',
            'monitor', 'verify', 'assemble', 'construct', 'create', 'design', 'develop',
            'formulate', 'generate', 'hypothesize', 'invent', 'make', 'originate', 'plan',
            'produce', 'write', 'compose', 'devise', 'forecast', 'organize', 'propose',
            'set up', 'synthesize', 'compile', 'author', 'investigate'
        ]

        # Educational domains
        self.domains = ['cognitive', 'affective', 'psychomotor']

    def _get_domain(self):
        """
        Determine an appropriate educational domain.

        Returns:
            str: Educational domain
        """
        # Most educational content falls into the cognitive domain
        domain_weights = [0.9, 0.05, 0.05]  # Higher weight for cognitive domain

        return random.choices(self.domains, weights=domain_weights, k=1)[0]

    def _get_clo_template(self):
        """
        Get a CLO template.

        Returns:
            str: CLO template
        """
        templates = [
            "Upon successful completion of this course, students will be able to {verb} {main_keyword} and related concepts such as {supporting_keywords}.",
            "After completing this course, students will be able to {verb} {main_keyword} including {supporting_keywords}.",
            "Students will be able to {verb} {main_keyword} and {supporting_keywords} upon completion of this course.",
            "Upon successful completion of this course, students will be able to {verb} the principles of {main_keyword} in relation to {supporting_keywords}.",
            "After completing this course, students will be able to {verb} how {main_keyword} relates to {supporting_keywords}.",
            "Students will be able to {verb} the concepts of {main_keyword} and {supporting_keywords} upon completion of this course.",
            "Upon successful completion of this course, students will be able to {verb} {main_keyword} techniques to solve problems related to {supporting_keywords}.",
            "After completing this course, students will be able to {verb} {main_keyword} in various contexts involving {supporting_keywords}.",
            "Students will be able to {verb} {main_keyword} principles to address challenges in {supporting_keywords}.",
            "Upon successful completion of this course, students will be able to {verb} {main_keyword} systems in terms of {supporting_keywords}.",
            "After completing this course, students will be able to {verb} the relationships between {main_keyword} and {supporting_keywords}.",
            "Students will be able to {verb} {main_keyword} components and their connections to {supporting_keywords}."
        ]

        return random.choice(templates)

    def _select_action_verb(self):
        """Select a random action verb."""
        return random.choice(self.action_verbs)

    def generate_clos(self, keywords, num_clos=5):
        """
        Generate Course Learning Outcomes (CLOs) based on the extracted keywords.

        Args:
            keywords (list): List of keywords extracted from the course content
            num_clos (int): Number of CLOs to generate

        Returns:
            list: Generated CLOs
        """
        clos = []

        # Group keywords into related concepts
        # In a real implementation, this would use more sophisticated clustering
        keyword_groups = [keywords[i:i+5] for i in range(0, min(len(keywords), num_clos*5), 5)]

        for i, keyword_group in enumerate(keyword_groups[:num_clos]):
            # Select an action verb
            action_verb = self._select_action_verb()

            # Get a CLO template
            template = self._get_clo_template()

            # Create a CLO
            main_keyword = keyword_group[0]
            supporting_keywords = ', '.join(keyword_group[1:]) if len(keyword_group) > 1 else "related concepts"

            # Format the CLO using the template
            clo = template.format(
                verb=action_verb,
                main_keyword=main_keyword,
                supporting_keywords=supporting_keywords
            )

            # Determine the domain (mostly cognitive for academic content)
            domain = self._get_domain()

            clos.append({
                'clo': clo,
                'action_verb': action_verb,
                'domain': domain,
                'keywords': keyword_group
            })

        return clos

    def extract_skills(self, keywords, clos, num_skills=10):
        """
        Extract relevant skills based on the keywords and generated CLOs.

        Args:
            keywords (list): List of keywords extracted from the course content
            clos (list): Generated CLOs
            num_skills (int): Number of skills to extract

        Returns:
            list: Extracted skills
        """
        skills = []

        # Combine all keywords from CLOs
        all_clo_keywords = []
        for clo in clos:
            all_clo_keywords.extend(clo['keywords'])

        # Use remaining keywords not used in CLOs
        remaining_keywords = [kw for kw in keywords if kw not in all_clo_keywords]

        # If not enough remaining keywords, use some from the CLOs
        if len(remaining_keywords) < num_skills:
            remaining_keywords.extend(all_clo_keywords[:num_skills-len(remaining_keywords)])

        # Generate skills (for demonstration, we'll use a template approach)
        skill_templates = [
            "Proficiency in {}",
            "Knowledge of {}",
            "Ability to work with {}",
            "Understanding of {}",
            "Experience with {}"
        ]

        for i in range(min(num_skills, len(remaining_keywords))):
            template = skill_templates[i % len(skill_templates)]
            skill = template.format(remaining_keywords[i])
            skills.append(skill)

        return skills
