import os
from openai import OpenAI
from decouple import config
import logging

logger = logging.getLogger(__name__)

def ask_ai_question(prompt, candidate_name=None, job_title=None, company_name=None, timeout=None):
    """Ask AI question using NVIDIA Llama-3.3-Nemotron-Super-49B-v1 model"""
    try:
        api_key = config('NVIDIA_API_KEY')
    except:
        logger.error("NVIDIA_API_KEY not found in environment variables")
        raise ValueError("NVIDIA_API_KEY is required for LLM functionality")
        
    if not api_key:
        logger.error("NVIDIA_API_KEY is empty")
        raise ValueError("NVIDIA_API_KEY cannot be empty")
        
    candidate_name = candidate_name or "the candidate"
    job_title = job_title or "Software Developer" 
    company_name = company_name or "Our Company"
        
    if not prompt or not prompt.strip():
        logger.error("Empty prompt provided to AI function")
        return f"Hey {candidate_name}! Great to meet you. What brings you here today?"
            
    # Optimized system prompt for NVIDIA Llama-3.3-Nemotron
    system_prompt = f"""
You're having a casual, friendly conversation with {candidate_name}. You're genuinely curious about them as a person.

CORE INSTRUCTIONS:
1. Talk naturally - no formal introductions or titles
2. Keep responses SHORT (1-2 sentences maximum)
3. Show genuine interest in what they share
4. Ask follow-up questions that feel organic
5. Be warm, encouraging, and relatable

CONVERSATION STYLE:
- React authentically to what they say
- Ask about their passions and experiences
- Keep it light and engaging
- Show you're really listening

GOOD EXAMPLES:
"Oh wow, that sounds really cool! What got you into that?"
"Nice! I bet that was quite an experience. What was the best part?"
"That's awesome! How long have you been working on that?"

AVOID:
- Formal interview language
- Robotic responses
- Multiple questions at once
- Any labels or prefixes

Just be yourself and have a genuine conversation.
"""
                
    try:
        # Initialize NVIDIA client
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
            timeout=timeout or 10.0
        )
        
        logger.info(f"Making NVIDIA Llama-3.3-Nemotron API call")
        
        completion = client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=80,
            stream=False,
            stop=["\n\n", "Candidate:", "You:", "Interviewer:", "Response as", "Here's my", "As Sarah", "Sarah responds", "*", "(", "Warm"]
        )
        
        raw_response = completion.choices[0].message.content
        cleaned_response = clean_text(raw_response)
        
        logger.info(f"NVIDIA Llama-3.3-Nemotron response successful, length: {len(cleaned_response)}")
        return cleaned_response
        
    except Exception as e:
        logger.error(f"NVIDIA API Error: {type(e).__name__}: {str(e)}")
        raise RuntimeError(f"Failed to get response from NVIDIA Llama-3.3-Nemotron model: {str(e)}")

def clean_text(text):
    """Clean AI response and keep it short and direct"""
    import re
    
    # Remove ALL meta-language and stage directions
    text = re.sub(r'^(Response as Sarah|Sarah\'s response|As Sarah|Here\'s my response|Sarah responds|Warm Smile|\*.*?\*)[:.]?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*.*?\*', '', text)  # Remove any *actions*
    text = re.sub(r'\(.*?\)', '', text)  # Remove (stage directions)
    
    # Remove speaker labels and formatting
    text = re.sub(r'^(Sarah|Interviewer|AI):\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[*#`_>\\-]+', '', text)
    text = re.sub(r'["""''′`]', '', text)
    
    # Clean whitespace and bullets
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^\d+\.\s*', '', text)
    text = re.sub(r'^[-•]\s*', '', text)
    
    # Keep responses SHORT - max 2 sentences
    sentences = text.split('. ')
    if len(sentences) > 2:
        text = '. '.join(sentences[:2]) + '.'
    
    # Ensure proper punctuation
    if text and not text.endswith(('.', '!', '?')):
        text += '.'
        
    return text

