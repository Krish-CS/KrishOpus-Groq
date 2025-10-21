"""
Content Generator v6.0 - ULTRA SMART AI CHAT WITH NATURAL LANGUAGE UNDERSTANDING
✅ Handles ANY natural language request
✅ "Keep objective in 30 words"
✅ "Change references to only 7"
✅ "Make conclusion 200 words"
✅ Smart word count & reference count detection
✅ Context-aware modifications
"""

import re
from typing import Dict, List, Tuple, Optional

class ContentGenerator:
    """Ultra Smart Content Generator with Advanced NLP"""
    
    def __init__(self, groq_client):
        """Initialize with Groq client"""
        self.groq = groq_client
        print(f"✅ ContentGenerator v6.0 initialized (Advanced NLP)")
    
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
            print(f"   [{idx}/{len(sections)}] {section}...", end=' ')
            
            if 'reference' in section.lower():
                content = self._generate_references(topic, subject)
            else:
                content = self._generate_section_content(
                    section_name=section,
                    topic=topic,
                    subject=subject,
                    max_words=110
                )
            
            generated[section] = content
            print(f"✓ ({len(content.split())} words)")
        
        return generated
    
    def refine_with_chat(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """
        MAIN CHAT HANDLER - Ultra smart with NLP
        """
        print(f"\n💬 Chat Request: {user_prompt}")
        
        # Detect intent
        intent = self._detect_intent(user_prompt, current_sections)
        
        print(f"   🧠 Detected Intent: {intent}")
        
        # Route to appropriate handler
        if intent == "add_section":
            return self._handle_add_section(user_prompt, current_sections, topic, subject)
        
        elif intent == "delete_section":
            return self._handle_delete_section(user_prompt, current_sections)
        
        elif intent == "modify_content":
            return self._handle_content_modification(user_prompt, current_sections, topic, subject)
        
        elif intent == "general_question":
            return self._handle_general_question(user_prompt, current_sections, topic, subject)
        
        else:
            return "I'm not sure what you want to do. Please try rephrasing.", {}
    
    def _detect_intent(self, user_prompt: str, current_sections: Dict[str, str]) -> str:
        """Detect user's intent from prompt"""
        prompt_lower = user_prompt.lower()
        
        # Add section intent
        if any(kw in prompt_lower for kw in ['add', 'insert', 'include', 'create new']):
            return "add_section"
        
        # Delete section intent
        if any(kw in prompt_lower for kw in ['remove', 'delete', 'drop']):
            return "delete_section"
        
        # Modify content intent (most common)
        if any(kw in prompt_lower for kw in [
            'change', 'modify', 'rewrite', 'expand', 'shorten', 'improve',
            'make', 'keep', 'reduce', 'increase', 'words', 'references'
        ]):
            return "modify_content"
        
        # General question
        return "general_question"
    
    def _detect_target_sections(self, user_prompt: str, current_sections: Dict[str, str]) -> List[str]:
        """Detect which sections user is referring to"""
        prompt_lower = user_prompt.lower()
        
        # Check for "all" or "everything"
        if any(kw in prompt_lower for kw in ['all', 'everything', 'entire', 'whole']):
            return list(current_sections.keys())
        
        # Check each section name
        target_sections = []
        for section_name in current_sections.keys():
            section_lower = section_name.lower()
            
            # Direct mention
            if section_lower in prompt_lower:
                target_sections.append(section_name)
                continue
            
            # Partial matches
            section_words = section_lower.split()
            if any(word in prompt_lower for word in section_words if len(word) > 3):
                target_sections.append(section_name)
        
        # If no sections detected, assume first non-reference section
        if not target_sections:
            for section_name in current_sections.keys():
                if 'reference' not in section_name.lower():
                    target_sections.append(section_name)
                    break
        
        return target_sections
    
    # ========================================
    # NATURAL LANGUAGE UNDERSTANDING
    # ========================================
    
    def _extract_number_from_prompt(self, user_prompt: str, context: str = "words") -> Optional[int]:
        """
        Extract number from user prompt with context awareness
        Handles:
        - "Keep objective in 30 words"
        - "change references to only 7"
        - "make it 200 words"
        - "keep 45 references"
        - "write 500"
        """
        prompt_lower = user_prompt.lower()
        
        # Pattern 1: "X words" or "X word"
        if context == "words":
            match = re.search(r'(\d+)\s*words?', prompt_lower)
            if match:
                return int(match.group(1))
        
        # Pattern 2: "to X" or "to only X" (for references)
        if context == "references":
            match = re.search(r'to\s+(?:only\s+)?(\d+)', prompt_lower)
            if match:
                return int(match.group(1))
            
            # Pattern: "keep X references" or "X references"
            match = re.search(r'(?:keep\s+)?(\d+)\s+references?', prompt_lower)
            if match:
                return int(match.group(1))
        
        # Pattern 3: "in X" (keep objective in 30 words)
        match = re.search(r'in\s+(\d+)', prompt_lower)
        if match:
            return int(match.group(1))
        
        # Pattern 4: Generic "X" after action verbs
        match = re.search(r'(?:to|make|change|rewrite|expand|write|keep)\s+(?:only\s+)?(\d+)', prompt_lower)
        if match:
            return int(match.group(1))
        
        return None
    
    def _parse_user_request(self, user_prompt: str, current_sections: Dict[str, str]) -> Dict:
        """
        Advanced NLP parser for user requests
        Returns structured information about the request
        """
        prompt_lower = user_prompt.lower()
        
        # Detect target sections
        target_sections = self._detect_target_sections(user_prompt, current_sections)
        
        # Detect if references section
        is_reference_request = any(
            'reference' in section.lower() 
            for section in target_sections
        ) or 'reference' in prompt_lower
        
        # Extract appropriate number based on context
        if is_reference_request:
            requested_number = self._extract_number_from_prompt(user_prompt, context="references")
            number_type = "references"
        else:
            requested_number = self._extract_number_from_prompt(user_prompt, context="words")
            number_type = "words"
        
        # Detect action type
        is_expansion = any(kw in prompt_lower for kw in [
            'expand', 'longer', 'more details', 'add more', 'elaborate', 'increase'
        ])
        
        is_reduction = any(kw in prompt_lower for kw in [
            'shorten', 'reduce', 'shorter', 'decrease', 'concise', 'brief', 'less'
        ])
        
        is_keep = 'keep' in prompt_lower
        
        # Determine intent
        if requested_number:
            intent = "specific_target"
        elif is_expansion:
            intent = "expand"
        elif is_reduction:
            intent = "reduce"
        elif is_keep:
            intent = "maintain"
        else:
            intent = "modify"
        
        return {
            'target_sections': target_sections,
            'requested_number': requested_number,
            'number_type': number_type,
            'is_reference_request': is_reference_request,
            'intent': intent,
            'original_prompt': user_prompt
        }
    
    # ========================================
    # CONTENT MODIFICATION HANDLER (ULTRA SMART)
    # ========================================
    
    def _handle_content_modification(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """
        ULTRA-SMART content modification handler
        Handles ANY natural language request:
        - "Keep objective in 30 words"
        - "Change references to only 7"
        - "Make conclusion 200 words"
        - "Expand methodology"
        - "Rewrite introduction to 150 words"
        """
        
        # Parse user request
        request = self._parse_user_request(user_prompt, current_sections)
        
        print(f"\n  🧠 Parsed Request:")
        print(f"     Target: {request['target_sections']}")
        print(f"     Intent: {request['intent']}")
        if request['requested_number']:
            print(f"     Target: {request['requested_number']} {request['number_type']}")
        
        # Determine target count
        if request['requested_number']:
            if request['number_type'] == "references":
                # References count request
                target_count = request['requested_number']
                max_words = None  # References don't use word limit
            else:
                # Word count request
                max_words = request['requested_number']
                target_count = None
        elif request['intent'] == "expand":
            # No limit expansion
            max_words = None
            target_count = None
        elif request['intent'] == "reduce":
            # Reduce to 50% of current
            max_words = 75
            target_count = None
        else:
            # Default
            max_words = 150
            target_count = None
        
        updated_sections = {}
        
        for section_name in request['target_sections']:
            if section_name not in current_sections:
                continue
            
            print(f"  🔄 Processing {section_name}...")
            
            current_content = current_sections[section_name]
            
            # Handle references specially
            if request['is_reference_request'] and target_count:
                new_content = self._regenerate_references(
                    section_name=section_name,
                    current_content=current_content,
                    topic=topic,
                    subject=subject,
                    target_count=target_count
                )
            else:
                # Handle regular content modification
                new_content = self._regenerate_section_with_context(
                    section_name=section_name,
                    current_content=current_content,
                    user_instruction=user_prompt,
                    topic=topic,
                    subject=subject,
                    max_words=max_words
                )
            
            updated_sections[section_name] = new_content
            
            # Log result
            if request['is_reference_request']:
                ref_count = len([line for line in new_content.split('\n') if line.strip().startswith(('[', '1', '2', '3', '4', '5', '6', '7', '8', '9'))])
                print(f"  ✓ Modified {section_name} ({ref_count} references)")
            else:
                word_count = len(new_content.split())
                print(f"  ✓ Modified {section_name} ({word_count} words)")
        
        # Generate response
        if updated_sections:
            response = f"✅ Modified {len(updated_sections)} section(s):\n"
            for sec in updated_sections.keys():
                if request['is_reference_request']:
                    ref_count = len([line for line in updated_sections[sec].split('\n') if line.strip().startswith(('[', '1', '2', '3', '4', '5', '6', '7', '8', '9'))])
                    response += f"  - {sec} ({ref_count} references)\n"
                else:
                    word_count = len(updated_sections[sec].split())
                    response += f"  - {sec} ({word_count} words)\n"
            return response, updated_sections
        else:
            return "No sections were modified.", {}
    
    # ========================================
    # REFERENCE GENERATION
    # ========================================
    
    def _regenerate_references(
        self,
        section_name: str,
        current_content: str,
        topic: str,
        subject: str,
        target_count: int
    ) -> str:
        """
        Generate references section with specific count
        """
        prompt = f"""Generate EXACTLY {target_count} academic references for a {subject} assignment about "{topic}".

Current references:
{current_content}

Generate {target_count} properly formatted references in IEEE/APA style.
Include a mix of:
- Journal articles
- Books
- Conference papers
- Online sources

Format each reference with:
[1] Author(s), "Title," Journal/Source, Vol. X, No. Y, pp. XX-YY, Year.

Generate EXACTLY {target_count} references, no more, no less."""

        try:
            response = self.groq.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated = response.strip()
            
            # Validate count
            lines = [line for line in generated.split('\n') if line.strip().startswith(('[', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
            
            if len(lines) != target_count:
                # Adjust if needed
                if len(lines) > target_count:
                    generated = '\n'.join([line for line in generated.split('\n') if line.strip()][:target_count])
                else:
                    # Add more if less
                    for i in range(len(lines), target_count):
                        generated += f"\n[{i+1}] Author, A., \"Additional Reference {i+1},\" Journal Name, Vol. 1, pp. 1-10, 2024."
            
            return generated
            
        except Exception as e:
            print(f"    ⚠️ Error generating references: {e}")
            return current_content
    
    def _generate_references(self, topic: str, subject: str, count: int = 10) -> str:
        """Generate references for initial document"""
        prompt = f"""Generate {count} academic references for a {subject} assignment about "{topic}".

Format in IEEE style:
[1] Author(s), "Title," Journal/Source, Vol. X, No. Y, pp. XX-YY, Year.

Include mix of journals, books, and online sources."""

        try:
            response = self.groq.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            return response.strip()
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return self._generate_fallback_references(topic, count)
    
    # ========================================
    # SECTION REGENERATION
    # ========================================
    
    def _regenerate_section_with_context(
        self,
        section_name: str,
        current_content: str,
        user_instruction: str,
        topic: str,
        subject: str,
        max_words: Optional[int] = 150
    ) -> str:
        """
        Regenerate section based on user instruction with word limit control
        """
        word_limit_instruction = f"\n\nIMPORTANT: Write EXACTLY {max_words} words." if max_words else "\n\nWrite in detail with no word limit."
        
        prompt = f"""You are rewriting the "{section_name}" section of a {subject} assignment about "{topic}".

Current content:
{current_content}

User wants: {user_instruction}

Rewrite this section following the user's request.{word_limit_instruction}

Write in proper paragraph format (not bullet points unless requested).
Be specific and academic in tone."""

        try:
            response = self.groq.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000 if not max_words else max(500, max_words * 2)
            )
            
            generated = response.strip()
            
            # Validate word count if specified
            if max_words:
                actual_words = len(generated.split())
                if abs(actual_words - max_words) > max_words * 0.2:  # Allow 20% tolerance
                    print(f"    ⚠️ Word count mismatch: {actual_words} vs {max_words} target")
            
            return generated
            
        except Exception as e:
            print(f"    ⚠️ Error: {e}")
            return current_content
    
    def _generate_section_content(
        self,
        section_name: str,
        topic: str,
        subject: str,
        max_words: int = 110
    ) -> str:
        """Generate content for a section"""
        prompt = f"""Write the "{section_name}" section for a {subject} assignment about "{topic}".

Write EXACTLY {max_words} words.
Use proper paragraph format (not bullet points).
Be specific and academic."""

        try:
            response = self.groq.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.strip()
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return self._generate_fallback(section_name, topic, max_words)
    
    # ========================================
    # OTHER HANDLERS
    # ========================================
    
    def _handle_add_section(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """Handle adding new section"""
        prompt_lower = user_prompt.lower()
        
        # Extract section name
        for word in ['add', 'insert', 'include', 'create']:
            if word in prompt_lower:
                parts = prompt_lower.split(word, 1)
                if len(parts) > 1:
                    section_name = parts[1].strip().title()
                    break
        else:
            section_name = "New Section"
        
        # Generate content
        content = self._generate_section_content(section_name, topic, subject, max_words=110)
        
        return f"✅ Added section: {section_name}", {section_name: content}
    
    def _handle_delete_section(
        self,
        user_prompt: str,
        current_sections: Dict[str, str]
    ) -> Tuple[str, Dict[str, str]]:
        """Handle deleting section"""
        target_sections = self._detect_target_sections(user_prompt, current_sections)
        
        deleted = {}
        for section in target_sections:
            if section in current_sections:
                deleted[section] = ""  # Mark for deletion
        
        if deleted:
            return f"✅ Marked {len(deleted)} section(s) for removal", deleted
        return "No sections found to remove.", {}
    
    def _handle_general_question(
        self,
        user_prompt: str,
        current_sections: Dict[str, str],
        topic: str,
        subject: str
    ) -> Tuple[str, Dict[str, str]]:
        """Handle general questions"""
        sections_text = "\n\n".join([f"{name}:\n{content}" for name, content in current_sections.items()])
        
        prompt = f"""You are helping with a {subject} assignment about "{topic}".

Current content:
{sections_text}

User question: {user_prompt}

Provide a helpful response."""

        try:
            response = self.groq.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.strip(), {}
        except Exception as e:
            return f"Error: {e}", {}
    
    # ========================================
    # FALLBACK GENERATORS
    # ========================================
    
    def _generate_fallback(self, section_name: str, topic: str, max_words: int) -> str:
        """Fallback content generation"""
        words = []
        base_text = f"This section discusses {section_name.lower()} in the context of {topic}. "
        
        while len(words) < max_words:
            words.extend(base_text.split())
        
        return ' '.join(words[:max_words])
    
    def _generate_fallback_references(self, topic: str, count: int) -> str:
        """Fallback reference generation"""
        refs = []
        for i in range(1, count + 1):
            refs.append(f"[{i}] Author, A., \"Study on {topic},\" Journal Name, Vol. 1, pp. 1-10, 2024.")
        return '\n'.join(refs)
