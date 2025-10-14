"""
Content Generator v5.0 - ULTRA SMART AI CHAT
✅ Detects section-specific vs all-sections changes
✅ Handles content expansion (removes word limit)
✅ Handles content rewriting (with context)
✅ Updates document properly
✅ Default = paragraphs (bullets only on request)
"""

import re
from typing import Dict, List, Tuple, Optional



class ContentGenerator:
    """Ultra Smart Content Generator with AI-powered chat"""
    
    def __init__(self, groq_client):
        """Initialize with Groq client"""
        self.groq = groq_client
        print(f"✅ ContentGenerator initialized (AI-powered chat)")
    
    
    def generate_full_assignment(
        self,
        topic: str,
        subject: str,
        sections: List[str],
        word_count: int = 3000,
        temperature: float = 0.7
    ) -> Dict[str, str]:
        """Generate complete assignment"""
        print(f"\n🤖 Generating content (110 words max per section)...")
        print(f"   Topic: {topic}")
        print(f"   Subject: {subject}\n")
        
        generated = {}
        
        for idx, section in enumerate(sections, 1):
            print(f"   [{idx}/{len(sections)}] {section}...", end=" ")
            
            if 'reference' in section.lower():
                content = self._generate_dynamic_references(topic, subject, count=8)
            else:
                content = self._generate_section_content(
                    section_name=section,
                    topic=topic,
                    subject=subject,
                    max_words=110,
                    temperature=temperature
                )
            
            word_count_actual = len(content.split())
            print(f"✓ ({word_count_actual} words)")
            
            generated[section] = content
        
        print(f"\n✅ Content generation complete!\n")
        return generated
    
    
    def _generate_section_content(
        self,
        section_name: str,
        topic: str,
        subject: str,
        max_words: int,
        temperature: float
    ) -> str:
        """Generate section content"""
        
        prompt = self._build_prompt(section_name, topic, subject, max_words)
        
        try:
            response = self.groq.generate_text(
                prompt=prompt,
                temperature=temperature,
                max_tokens=500
            )
            
            content = self._clean_text(response, section_name)
            
            # ENFORCE MAX LENGTH
            words = content.split()
            if len(words) > max_words:
                content = ' '.join(words[:max_words]) + '.'
            
            return content
            
        except Exception as e:
            print(f"\n   ✗ Error: {e}")
            return self._generate_fallback(section_name, topic, subject)
    
    
    def _build_prompt(self, section_name: str, topic: str, subject: str, max_words: int) -> str:
        """Build section-specific prompt"""
        
        section_lower = section_name.lower()
        
        base_req = f"""CRITICAL REQUIREMENTS:
- Write EXACTLY {max_words} words (NO MORE, NO LESS)
- Professional academic style
- Specific to "{topic}" in {subject}
- Clear, detailed, well-structured
- NO section heading
- NO meta-text like "Here is..."
- Start directly with content
- Write as FLOWING PARAGRAPHS (NOT bullet points)"""
        
        if any(kw in section_lower for kw in ['descriptive', 'headline', 'introduction', 'overview']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Introduce {topic} comprehensively
- Explain importance and relevance
- Provide context and background

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['objective', 'aim', 'purpose', 'goal']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- State 3-5 clear objectives
- Explain what this aims to achieve
- Be specific and measurable

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['problem', 'analysis', 'challenge', 'issue']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Identify key problems/challenges
- Explain root causes
- Analyze impacts

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['solution', 'methodology', 'approach', 'implementation']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Present solutions/methodologies
- Explain implementation steps
- Discuss advantages

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['technology', 'statistics', 'data', 'technical']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Discuss relevant technologies/tools
- Provide technical details
- Explain applications

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['result', 'finding', 'outcome']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Present key results/findings
- Analyze significance
- Discuss implications

Write EXACTLY {max_words} words:"""

        elif any(kw in section_lower for kw in ['conclusion', 'summary']):
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Summarize main points
- Draw conclusions
- Suggest future directions

Write EXACTLY {max_words} words:"""

        else:
            return f"""Write the {section_name} section for an assignment on "{topic}" in {subject}.

{base_req}
- Comprehensive coverage
- Detailed and specific

Write EXACTLY {max_words} words:"""
    
    
    def _generate_dynamic_references(self, topic: str, subject: str, count: int = 8) -> str:
        """Generate AI references with specific count"""
        
        prompt = f"""Generate exactly {count} realistic academic references for a research paper on "{topic}" in {subject}.

REQUIREMENTS:
- Generate EXACTLY {count} references (NO MORE, NO LESS)
- Use realistic APA citation format
- Include proper authors (realistic names), years (2020-2024), titles, publishers, DOIs
- Make titles highly relevant to "{topic}"
- Use realistic journal/conference names in {subject} field
- Format each reference properly
- DO NOT number them
- DO NOT include "References" heading

Generate EXACTLY {count} references:"""
        
        try:
            response = self.groq.generate_text(
                prompt=prompt,
                temperature=0.8,
                max_tokens=count * 120
            )
            
            references = response.strip()
            references = re.sub(r'^\d+\.\s*', '', references, flags=re.MULTILINE)
            
            return references
            
        except Exception as e:
            print(f"\n   ✗ Error: {e}")
            return f"""Smith, J. (2024). {topic}: A Review. Journal of {subject}, 45(3), 234-256."""
    
    
    def _clean_text(self, text: str, section_name: str) -> str:
        """Clean AI-generated text"""
        
        patterns = [
            r'^Here is.*?:',
            r'^This is.*?:',
            r'^\*\*.*?\*\*:?',
            r'Please let me know.*$',
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        section_lower = section_name.lower()
        if text.lower().startswith(section_lower):
            text = text[len(section_name):].strip().lstrip(':').strip()
        
        text = text.strip().strip('"').strip("'").strip()
        text = ' '.join(text.split())
        
        return text
    
    
    def _generate_fallback(self, section_name: str, topic: str, subject: str) -> str:
        """Fallback content"""
        return f"The {section_name.lower()} examines {topic} in {subject}."
    
    
    def refine_via_chat(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """
        ULTRA SMART AI CHAT - Analyzes intent and updates document
        
        Handles:
        - Reference count changes ("20 references", "40 references")
        - Style changes ("bullet points", "arrow bullets", "paragraphs")
        - Content rewriting ("change objective to...", "rewrite conclusion")
        - Content expansion ("make longer", "add more details", "expand")
        - Section-specific changes ("change objective", "update conclusion")
        """
        
        print(f"\n💬 Smart chat: {user_prompt[:80]}...")
        
        prompt_lower = user_prompt.lower()
        
        # PRIORITY 1: Reference count changes
        if 'reference' in prompt_lower and any(word in prompt_lower for word in ['want', 'need', 'make', 'generate', 'give', 'add', 'create']):
            return self._handle_reference_count_change(user_prompt, current_sections, topic, subject)
        
        # PRIORITY 2: Style changes (bullets, arrows, paragraphs)
        style_keywords = ['bullet', 'point', 'list', 'numbered', 'paragraph', 'style', 'format', 'arrow']
        if any(kw in prompt_lower for kw in style_keywords):
            return self._handle_style_change(user_prompt, current_sections, topic, subject)
        
        # PRIORITY 3: Content changes (rewrite, expand, change)
        content_keywords = ['change', 'rewrite', 'modify', 'update', 'expand', 'add more', 'make longer', 'more details', 'improve', 'enhance']
        if any(kw in prompt_lower for kw in content_keywords):
            return self._handle_content_modification(user_prompt, current_sections, topic, subject)
        
        # PRIORITY 4: Generic response (no changes)
        return self._handle_generic_chat(user_prompt, current_sections, topic, subject)
    
    
    def _handle_reference_count_change(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """Handle reference count changes"""
        
        numbers = re.findall(r'\d+', user_prompt)
        if not numbers:
            return "Please specify how many references (e.g., '20 references')", {}
        
        ref_count = int(numbers[0])
        print(f"   🔄 Generating {ref_count} references...")
        
        new_refs = self._generate_dynamic_references(topic, subject, count=ref_count)
        
        updated_sections = {}
        for section_name in current_sections.keys():
            if 'reference' in section_name.lower():
                updated_sections[section_name] = new_refs
                print(f"   ✓ Generated {ref_count} references")
                break
        
        if updated_sections:
            return f"✅ Generated {ref_count} references successfully!", updated_sections
        else:
            return "⚠ References section not found", {}
    
    
    def _handle_style_change(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """Handle style transformation"""
        
        prompt_lower = user_prompt.lower()
        
        # Detect target sections
        target_sections = self._detect_target_sections(user_prompt, current_sections)
        
        # Detect style
        if 'arrow' in prompt_lower:
            target_style = 'arrow_bullets'
            bullet_char = '→'
        elif 'star' in prompt_lower:
            target_style = 'star_bullets'
            bullet_char = '★'
        elif 'numbered' in prompt_lower or 'number' in prompt_lower:
            target_style = 'numbered_list'
            bullet_char = None
        elif 'paragraph' in prompt_lower:
            target_style = 'paragraph'
            bullet_char = None
        else:
            target_style = 'bullet_points'
            bullet_char = '•'
        
        updated_sections = {}
        
        for section_name in target_sections:
            if 'reference' in section_name.lower():
                print(f"   ⏭ Skipping {section_name} (references cannot be styled)")
                continue
            
            if section_name in current_sections:
                print(f"   🔄 Transforming {section_name} to {target_style}...")
                
                new_content = self._transform_content_style(
                    content=current_sections[section_name],
                    section_name=section_name,
                    topic=topic,
                    subject=subject,
                    target_style=target_style,
                    bullet_char=bullet_char
                )
                
                updated_sections[section_name] = new_content
        
        if updated_sections:
            response = f"✅ Transformed {len(updated_sections)} section(s) to {target_style.replace('_', ' ')}:\n"
            for sec in updated_sections.keys():
                response += f"   - {sec}\n"
            return response, updated_sections
        else:
            return "No sections were transformed.", {}
    
    
    def _handle_content_modification(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """
        Handle content modification (rewrite, expand, change)
        **NO WORD LIMIT** when user asks for more content
        """
        
        prompt_lower = user_prompt.lower()
        
        # Detect target sections
        target_sections = self._detect_target_sections(user_prompt, current_sections)
        
        # Detect if expansion requested
        is_expansion = any(kw in prompt_lower for kw in ['expand', 'longer', 'more details', 'add more', 'elaborate'])
        
        # Set word limit (remove limit if expansion requested)
        max_words = None if is_expansion else 150
        
        updated_sections = {}
        
        for section_name in target_sections:
            if 'reference' in section_name.lower():
                continue
            
            if section_name in current_sections:
                print(f"   🔄 Modifying {section_name}...")
                
                current_content = current_sections[section_name]
                
                # Generate new content based on user request
                new_content = self._regenerate_section_with_context(
                    section_name=section_name,
                    current_content=current_content,
                    user_instruction=user_prompt,
                    topic=topic,
                    subject=subject,
                    max_words=max_words
                )
                
                updated_sections[section_name] = new_content
                print(f"   ✓ Modified {section_name} ({len(new_content.split())} words)")
        
        if updated_sections:
            response = f"✅ Modified {len(updated_sections)} section(s):\n"
            for sec in updated_sections.keys():
                word_count = len(updated_sections[sec].split())
                response += f"   - {sec} ({word_count} words)\n"
            return response, updated_sections
        else:
            return "No sections were modified.", {}
    
    
    def _regenerate_section_with_context(
        self,
        section_name: str,
        current_content: str,
        user_instruction: str,
        topic: str,
        subject: str,
        max_words: Optional[int] = None
    ) -> str:
        """Regenerate section content based on user instruction"""
        
        word_limit_text = f"Write approximately {max_words} words." if max_words else "No word limit - write as much as needed to fully address the instruction."
        
        prompt = f"""Current content for {section_name} section (about {topic} in {subject}):

{current_content}

User instruction: {user_instruction}

Task: Rewrite this section following the user's instruction.

REQUIREMENTS:
- Professional academic style
- {word_limit_text}
- Keep topic focus on "{topic}" in {subject}
- NO section heading
- NO meta-text
- Write as FLOWING PARAGRAPHS (not bullet points unless specifically requested)

Rewrite now:"""
        
        try:
            response = self.groq.generate_text(
                prompt=prompt,
                temperature=0.7,
                max_tokens=max_words * 5 if max_words else 1500
            )
            
            return self._clean_text(response, section_name)
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return current_content
    
    
    def _detect_target_sections(self, user_prompt: str, current_sections: Dict[str, str]) -> List[str]:
        """Detect which sections user wants to modify"""
        
        prompt_lower = user_prompt.lower()
        
        # Check if "all" or "everything"
        if any(kw in prompt_lower for kw in ['all', 'everything', 'entire', 'whole']):
            return list(current_sections.keys())
        
        # Check for specific section mentions
        target_sections = []
        for section_name in current_sections.keys():
            if section_name.lower() in prompt_lower:
                target_sections.append(section_name)
        
        # If no specific sections detected, apply to all (except references)
        if not target_sections:
            target_sections = [s for s in current_sections.keys() if 'reference' not in s.lower()]
        
        return target_sections
    
    
    def _transform_content_style(
        self,
        content: str,
        section_name: str,
        topic: str,
        subject: str,
        target_style: str,
        bullet_char: str = None
    ) -> str:
        """Transform content to target style"""
        
        if target_style == 'paragraph':
            instruction = "Convert to flowing paragraphs (110-150 words). Professional academic style."
        elif target_style == 'numbered_list':
            instruction = "Convert to 5-7 numbered points. Each 15-20 words. Format as '1. ', '2. ', etc."
        elif bullet_char:
            instruction = f"Convert to 5-7 bullet points. Each 15-20 words. Start each with '{bullet_char} '. NO numbering."
        else:
            instruction = "Convert to 5-7 bullet points. Each 15-20 words. Start each with '• '. NO numbering."
        
        prompt = f"""Current content for {section_name} (about {topic} in {subject}):

{content}

Task: {instruction}

CRITICAL:
- Maintain all key information
- Professional academic style
- Use EXACT format specified
- NO section heading
- NO meta-text

Transform now:"""
        
        try:
            response = self.groq.generate_text(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return content
    
    
    def _handle_generic_chat(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """Handle generic chat (no document changes)"""
        
        context = f"Topic: {topic}\nSubject: {subject}\n\nCurrent sections:\n"
        for section, content in current_sections.items():
            context += f"\n{section}: {content[:100]}...\n"
        
        prompt = f"""{context}

User question: {user_prompt}

Provide a helpful response about the document or suggestions for changes."""
        
        try:
            response = self.groq.generate_text(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.strip(), {}
            
        except Exception as e:
            return f"Error: {str(e)}", {}
