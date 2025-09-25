from flask import Blueprint, jsonify, request
from src.models.database import db, AITool
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

ai_tool_bp = Blueprint('ai_tool', __name__, url_prefix='/api/ai-tools')

@ai_tool_bp.route('', methods=['GET'])
def get_all_tools():
    """Get all AI tools"""
    tools = AITool.query.all()
    
    # Format response
    result = {
        'tools': [
            {
                'id': tool.id,
                'name': tool.name,
                'description': tool.description,
                'tool_type': tool.tool_type,
                'api_endpoint': tool.api_endpoint
            } for tool in tools
        ]
    }
    
    return jsonify(result)

@ai_tool_bp.route('/<int:tool_id>', methods=['GET'])
def get_tool(tool_id):
    """Get a specific AI tool by ID"""
    tool = AITool.query.get_or_404(tool_id)
    
    # Format response
    result = {
        'id': tool.id,
        'name': tool.name,
        'description': tool.description,
        'tool_type': tool.tool_type,
        'api_endpoint': tool.api_endpoint
    }
    
    return jsonify(result)

@ai_tool_bp.route('/<int:tool_id>/use', methods=['POST'])
@jwt_required()
def use_tool(tool_id):
    """Use an AI tool"""
    user_id = get_jwt_identity()
    
    # Check if tool exists
    tool = AITool.query.get_or_404(tool_id)
    
    # Get data from request
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'message': 'Prompt is required'}), 400
    
    prompt = data.get('prompt')
    code = data.get('code', '')
    language = data.get('language', '')
    
    # Simulate AI tool response (in production, this would use OpenAI API)
    try:
        if tool.tool_type == 'generate_code':
            # Generate code based on prompt
            generated_code = "// Generated code based on: " + prompt + "\n"
            generated_code += "// Language: " + language + "\n\n"
            generated_code += "// This is a simulated response\n"
            generated_code += "function example() {\n"
            generated_code += "  console.log('Hello, world!');\n"
            generated_code += "  // TODO: Implement actual functionality\n"
            generated_code += "}"
            
            result = {
                'generated_code': generated_code,
                'language': language
            }
            
        elif tool.tool_type == 'debug_code':
            # Debug code
            debug_result = "Analysis of your code:\n\n"
            debug_result += "1. Issue found: Missing semicolon on line 3\n"
            debug_result += "2. Potential bug: Variable 'data' used before declaration\n"
            debug_result += "3. Recommendation: Add error handling for edge cases\n\n"
            debug_result += "Fixed code:\n```" + language + "\n"
            debug_result += code.replace('function', 'function fixed') + "\n```"
            
            result = {
                'debug_result': debug_result
            }
            
        elif tool.tool_type == 'explain_code':
            # Explain code
            explanation = "Explanation of the provided " + language + " code:\n\n"
            explanation += "1. This code defines a function that does X\n"
            explanation += "2. It uses Y algorithm to process input\n"
            explanation += "3. The main logic is in the loop at lines 5-10\n"
            explanation += "4. It returns Z as the final result"
            
            result = {
                'explanation': explanation
            }
            
        elif tool.tool_type == 'convert_code':
            # Convert code between languages
            target_language = data.get('target_language', '')
            if not target_language:
                return jsonify({'message': 'Target language is required for code conversion'}), 400
            
            converted_code = "// Converted from " + language + " to " + target_language + "\n\n"
            converted_code += "// This is a simulated conversion\n"
            converted_code += "function convertedExample() {\n"
            converted_code += "  console.log('Converted code');\n"
            converted_code += "  // TODO: Implement actual functionality\n"
            converted_code += "}"
            
            result = {
                'converted_code': converted_code,
                'original_language': language,
                'target_language': target_language
            }
            
        else:
            return jsonify({'message': 'Invalid tool type'}), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'message': f'Error using AI tool: {str(e)}'}), 500

