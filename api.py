from flask import request, jsonify
import base64
import time
import json
import logging
from app import app, db
from models import QuestionAnswer

logger = logging.getLogger(__name__)

@app.route('/api/', methods=['POST'])
def handle_question():
    """
    Main API endpoint to handle student questions.
    Expected JSON format:
    {
        "question": "What model should I use?",
        "image": "base64_encoded_image_data"  # optional
    }
    """
    start_time = time.time()
    
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        question = data.get('question', '').strip()
        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400
        
        image_base64 = data.get('image')
        
        # Validate image if provided
        if image_base64:
            try:
                # Validate base64 format
                base64.b64decode(image_base64)
            except Exception:
                return jsonify({
                    "error": "Invalid base64 image data"
                }), 400
        
        logger.info(f"Processing question: {question[:100]}...")
        
        # Import AI assistant here to avoid circular imports
        try:
            from ai_assistant_simple import answer_question
            result = answer_question(question, image_base64)
        except ImportError:
            # Fallback if AI assistant not available
            result = {
                "answer": "I'm sorry, but the AI assistant is currently unavailable. Please try again later.",
                "links": [],
                "response_time": 0.0
            }
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Store in database for analytics
        try:
            qa_record = QuestionAnswer(
                question=question,
                answer=result['answer'],
                links=json.dumps(result['links']),
                has_image=bool(image_base64),
                response_time=response_time
            )
            db.session.add(qa_record)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
        
        logger.info(f"Question answered in {response_time:.2f} seconds")
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        logger.error(error_msg)
        
        return jsonify({
            "error": error_msg
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "message": "TDS Virtual TA API is running"
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get API usage statistics.
    """
    try:
        total_questions = QuestionAnswer.query.count()
        questions_with_images = QuestionAnswer.query.filter_by(has_image=True).count()
        
        if total_questions > 0:
            avg_response_time = db.session.query(db.func.avg(QuestionAnswer.response_time)).scalar()
        else:
            avg_response_time = 0.0
        
        return jsonify({
            "total_questions": total_questions,
            "questions_with_images": questions_with_images,
            "average_response_time": round(avg_response_time, 2) if avg_response_time else 0.0
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            "error": "Unable to retrieve statistics"
        }), 500