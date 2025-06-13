"""
Simplified AI assistant without heavy ML dependencies for Replit compatibility.
"""
import logging
import os
from typing import Dict, Any, List
from models import ScrapedContent
from app import db

logger = logging.getLogger(__name__)

def simple_search(question: str, top_k: int = 5) -> List[Dict]:
    """
    Simple text-based search through scraped content using basic keyword matching.
    """
    try:
        # Split question into keywords
        keywords = question.lower().split()
        
        # Query database for content containing keywords
        content_items = ScrapedContent.query.all()
        
        results = []
        for item in content_items:
            content_lower = item.content.lower()
            title_lower = (item.title or "").lower()
            
            # Count keyword matches
            score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    score += content_lower.count(keyword)
                if keyword in title_lower:
                    score += title_lower.count(keyword) * 2  # Title matches weighted higher
            
            if score > 0:
                results.append({
                    'content': item.content[:500] + "..." if len(item.content) > 500 else item.content,
                    'title': item.title,
                    'url': item.url,
                    'score': score
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
        
    except Exception as e:
        logger.error(f"Error in simple search: {e}")
        return []

def generate_fallback_answer(question: str, image_base64: str = None) -> Dict[str, Any]:
    """
    Generate a fallback answer using only search results when AI is unavailable.
    """
    search_results = simple_search(question)
    
    if search_results:
        # Create answer from top search results
        answer_parts = ["Based on the available course materials:\n\n"]
        links = []
        
        for i, result in enumerate(search_results[:3], 1):
            answer_parts.append(f"{i}. {result['content'][:200]}...")
            links.append({
                'title': result['title'] or 'Course Material',
                'url': result['url'],
                'relevance': min(result['score'] / 10, 1.0)
            })
        
        answer_parts.append("\n\nPlease refer to the linked materials for more detailed information.")
        
        return {
            'answer': '\n'.join(answer_parts),
            'links': links,
            'source': 'search_fallback'
        }
    else:
        return {
            'answer': "I couldn't find specific information about your question in the available course materials. Please try rephrasing your question or contact your instructor for assistance.",
            'links': [],
            'source': 'no_results'
        }

def answer_question(question: str, image_base64: str = None) -> Dict[str, Any]:
    """
    Answer a student question using simple search and OpenAI.
    """
    try:
        # Check if OpenAI API key is available
        openai_key = os.environ.get('OPENAI_API_KEY')
        
        if openai_key:
            # Try using OpenAI with search context
            search_results = simple_search(question)
            
            try:
                import openai
                client = openai.OpenAI(api_key=openai_key)
                
                # Prepare context from search results
                context = ""
                if search_results:
                    context = "\n\n".join([f"- {result['content'][:300]}" for result in search_results[:3]])
                
                # Create prompt
                prompt = f"""You are a helpful teaching assistant for a data science course. Answer the student's question based on the provided course materials.

Course Materials Context:
{context}

Student Question: {question}

Please provide a clear, helpful answer. If the context doesn't contain enough information, acknowledge this and provide general guidance."""

                # Handle image if provided
                messages = [{"role": "user", "content": prompt}]
                
                if image_base64:
                    messages = [{
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                            }
                        ]
                    }]
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                
                # Prepare links from search results
                links = []
                for result in search_results[:5]:
                    links.append({
                        'title': result['title'] or 'Course Material',
                        'url': result['url'],
                        'relevance': min(result['score'] / 10, 1.0)
                    })
                
                return {
                    'answer': answer,
                    'links': links,
                    'source': 'openai_with_search'
                }
                
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                # Fall back to search-only answer
                return generate_fallback_answer(question, image_base64)
        else:
            # No OpenAI key available, use search-only
            return generate_fallback_answer(question, image_base64)
            
    except Exception as e:
        logger.error(f"Error in answer_question: {e}")
        return {
            'answer': "I'm sorry, but I'm experiencing technical difficulties. Please try again later or contact your instructor for assistance.",
            'links': [],
            'source': 'error'
        }

def rank_and_filter_links(links: List[Dict], question: str, answer: str) -> List[Dict]:
    """
    Rank and filter links based on relevance to the question and answer.
    """
    # Simple ranking based on existing relevance scores
    return sorted(links, key=lambda x: x.get('relevance', 0), reverse=True)[:5]

def initialize_simple_data():
    """
    Initialize the database with sample data if needed.
    """
    try:
        if ScrapedContent.query.count() == 0:
            logger.info("Initializing database with sample course content...")
            
            sample_content = [
                {
                    'title': 'Introduction to Data Science',
                    'content': 'Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data.',
                    'url': 'https://example.com/intro-ds',
                    'content_type': 'course'
                },
                {
                    'title': 'Machine Learning Basics',
                    'content': 'Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.',
                    'url': 'https://example.com/ml-basics',
                    'content_type': 'course'
                },
                {
                    'title': 'Python for Data Analysis',
                    'content': 'Python is a powerful programming language for data analysis. Key libraries include pandas for data manipulation, numpy for numerical computing, and matplotlib for visualization.',
                    'url': 'https://example.com/python-data',
                    'content_type': 'course'
                }
            ]
            
            for content_data in sample_content:
                content = ScrapedContent(
                    title=content_data['title'],
                    content=content_data['content'],
                    url=content_data['url'],
                    content_type=content_data['content_type']
                )
                db.session.add(content)
            
            db.session.commit()
            logger.info("Sample content added to database")
            
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")