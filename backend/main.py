"""
KrishOpus Backend v4.0 - COMPLETE & PRODUCTION READY
✅ Enhanced TemplateAnalyzer (multi-strategy section extraction)
✅ Ultra SmartDocumentBuilder (page 2 deletion + header/footer preservation)
✅ SessionManager integration
✅ Preview + Chat Refinement (FIXED - ACTUALLY UPDATES DOCUMENT)
✅ Enhanced debug logging for chat
"""


import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


# Import modules
from modules.groq_client import GroqClient
from modules.content_generator import ContentGenerator
from modules.document_builder_template import SmartDocumentBuilder
from modules.session_manager import SessionManager
from modules.template_analyzer import TemplateAnalyzer


# Initialize FastAPI
app = FastAPI(title="KrishOpus API v4.0", version="4.0.0")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize components
print("\n" + "="*60)
print("🎓 KrishOpus Backend v4.0 - PRODUCTION READY")
print("   ✅ Enhanced Template Analysis")
print("   ✅ Ultra Smart Document Building")
print("   ✅ Preview + Chat Refinement (FIXED)")
print("="*60 + "\n")


try:
    session_manager = SessionManager()
    groq_client = GroqClient()
    content_generator = ContentGenerator(groq_client)
    template_analyzer = TemplateAnalyzer()
    document_builder = SmartDocumentBuilder()
    
    print("✅ All components initialized successfully!\n")
    
except Exception as e:
    print(f"❌ Initialization error: {e}")
    raise


# Ensure directories exist
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# =============================================================================
# MODELS
# =============================================================================


class ChatRequest(BaseModel):
    document_id: str
    user_prompt: str


# =============================================================================
# HEALTH CHECK
# =============================================================================


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "4.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "enhanced_template_analysis",
            "ultra_document_building",
            "header_footer_preservation",
            "preview_mode",
            "chat_refinement_fixed",
            "session_management",
            "debug_logging"
        ],
        "active_sessions": session_manager.get_active_sessions_count()
    }


# =============================================================================
# GENERATE ASSIGNMENT (Returns JSON preview)
# =============================================================================


@app.post("/api/generate")
async def generate_assignment(
    template: UploadFile = File(...),
    topic: str = Form(...),
    subject: str = Form(...),
    word_count: int = Form(3000),
    temperature: float = Form(0.7)
):
    """
    Generate assignment content using Enhanced TemplateAnalyzer
    Returns: JSON with sections for preview
    """
    try:
        print(f"\n📝 New Generation Request:")
        print(f"   Topic: {topic}")
        print(f"   Subject: {subject}")
        print(f"   Word Count: {word_count}")
        print(f"   Temperature: {temperature}")
        
        # Validate file type
        if not template.filename.endswith('.docx'):
            raise HTTPException(status_code=400, detail="Only DOCX templates are supported")
        
        # Save uploaded template
        template_path = UPLOAD_DIR / f"template_{uuid.uuid4().hex}.docx"
        with open(template_path, "wb") as f:
            shutil.copyfileobj(template.file, f)
        
        print(f"✅ Template saved: {template_path.name}")
        
        # STEP 1: Analyze template using Enhanced TemplateAnalyzer
        print("\n📋 Analyzing template with Enhanced TemplateAnalyzer...")
        sections = template_analyzer.analyze_template(str(template_path))
        print(f"✅ Extracted {len(sections)} sections: {sections}")
        
        # STEP 2: Generate content for each section
        print("\n🤖 Generating content with Groq AI...")
        generated_content = content_generator.generate_full_assignment(
            topic=topic,
            subject=subject,
            sections=sections,
            word_count=word_count,
            temperature=temperature
        )
        
        # STEP 3: Create session
        document_id = session_manager.create_session(
            topic=topic,
            subject=subject,
            sections=generated_content,
            template_path=str(template_path)
        )
        
        print(f"✅ Session created: {document_id}")
        print(f"✅ Generation complete!\n")
        
        # Calculate total words
        total_words = sum(len(str(content).split()) for content in generated_content.values())
        
        # Return JSON for preview
        return {
            "success": True,
            "document_id": document_id,
            "topic": topic,
            "subject": subject,
            "sections": generated_content,
            "total_words": total_words,
            "section_count": len(generated_content),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Generation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# =============================================================================
# GET PREVIEW (Get current document state)
# =============================================================================


@app.get("/api/preview/{document_id}")
async def get_preview(document_id: str):
    """Get current document preview"""
    try:
        session = session_manager.get_session(document_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Document session not found or expired")
        
        total_words = sum(len(str(content).split()) for content in session["sections"].values())
        
        return {
            "success": True,
            "document_id": document_id,
            "topic": session["topic"],
            "subject": session["subject"],
            "sections": session["sections"],
            "total_words": total_words,
            "section_count": len(session["sections"]),
            "created_at": session.get("created_at"),
            "chat_history_count": len(session.get("chat_history", []))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Preview error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# CHAT REFINEMENT - **WITH ENHANCED DEBUG LOGGING**
# =============================================================================


@app.post("/api/chat")
async def chat_refinement(request: ChatRequest):
    """
    Refine content via AI chat
    **FIXED: Now actually updates the document session**
    **ENHANCED: Debug logging to see what's happening**
    """
    try:
        print(f"\n💬 Chat refinement request:")
        print(f"   Document: {request.document_id}")
        print(f"   Prompt: {request.user_prompt}")
        
        session = session_manager.get_session(request.document_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Document session not found")
        
        print(f"   📊 Session state BEFORE chat:")
        print(f"      Available sections: {list(session['sections'].keys())}")
        
        # Get AI response and updated sections
        response_text, updated_sections = content_generator.refine_via_chat(
            user_prompt=request.user_prompt,
            current_sections=session["sections"],
            topic=session["topic"],
            subject=session["subject"]
        )
        
        # **ENHANCED DEBUG LOGGING**
        print(f"\n   📊 Chat Response Analysis:")
        print(f"      Response Text: {response_text[:150]}{'...' if len(response_text) > 150 else ''}")
        print(f"      Updated Sections: {list(updated_sections.keys()) if updated_sections else 'None (generic chat)'}")
        print(f"      Sections Modified: {len(updated_sections) if updated_sections else 0}")
        
        # **CRITICAL FIX: Update session with modified sections**
        if updated_sections:
            print(f"\n   🔄 Updating session with {len(updated_sections)} modified sections...")
            
            # Update the session sections with new content
            for section_name, new_content in updated_sections.items():
                old_word_count = len(session["sections"].get(section_name, "").split())
                new_word_count = len(new_content.split())
                
                session["sections"][section_name] = new_content
                
                print(f"      ✓ {section_name}: {old_word_count} → {new_word_count} words")
            
            # Save updated session
            session_manager.update_sections(request.document_id, updated_sections)
            print(f"   ✅ Session updated successfully!")
        else:
            print(f"   ℹ️ No sections updated (generic chat response)")
        
        # Add chat message to history
        session_manager.add_chat_message(request.document_id, "user", request.user_prompt)
        session_manager.add_chat_message(request.document_id, "assistant", response_text)
        
        print(f"   📝 Chat history updated\n")
        
        # Return updated sections so frontend can refresh
        return {
            "success": True,
            "response": response_text,
            "updated_sections": updated_sections if updated_sections else None,
            "sections_modified": len(updated_sections) if updated_sections else 0,
            "current_sections": session["sections"],  # ← Return full updated content
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Chat error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# FINALIZE & DOWNLOAD
# =============================================================================


@app.post("/api/finalize/{document_id}")
async def finalize_document(document_id: str):
    """
    Create final DOCX file using Ultra SmartDocumentBuilder
    ✅ Deletes page 2
    ✅ Preserves headers/footers
    ✅ Adds formatted content
    """
    try:
        print(f"\n📥 Finalizing document: {document_id}")
        
        session = session_manager.get_session(document_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Document session not found")
        
        # Build document using Ultra SmartDocumentBuilder
        print(f"📄 Building with Ultra SmartDocumentBuilder...")
        print(f"   ✅ Page 2 deletion enabled")
        print(f"   ✅ Header/footer preservation enabled")
        
        result = document_builder.generate_from_template(
            template_path=session["template_path"],
            topic=session["topic"],
            user_data={},
            generated_content=session["sections"],
            output_format="docx"
        )
        
        if result['status'] != 'success':
            raise HTTPException(status_code=500, detail=result['message'])
        
        output_path = Path(result['output_path'])
        filename = output_path.name
        
        # Move to outputs directory
        final_path = OUTPUT_DIR / filename
        if output_path.exists():
            shutil.move(str(output_path), str(final_path))
        
        file_size = final_path.stat().st_size
        
        print(f"✅ Document finalized: {filename}")
        print(f"   Size: {file_size / 1024:.1f} KB\n")
        
        return {
            "success": True,
            "document_id": document_id,
            "filename": filename,
            "download_url": f"/api/download/{filename}",
            "file_size": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Finalization error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# DOWNLOAD FILE
# =============================================================================


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download generated document"""
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"📥 Download requested: {filename}")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Download error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# CLEANUP (Optional - for production)
# =============================================================================


@app.post("/api/cleanup/{document_id}")
async def cleanup_session(document_id: str):
    """Manually cleanup session and template file"""
    try:
        success = session_manager.delete_session(document_id)
        
        if success:
            return {
                "success": True,
                "message": f"Session {document_id} cleaned up successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# STARTUP & SHUTDOWN EVENTS
# =============================================================================


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("\n🚀 KrishOpus Backend Started!")
    print(f"   📁 Upload Directory: {UPLOAD_DIR.absolute()}")
    print(f"   📁 Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"   🌐 API Docs: http://localhost:8000/docs")
    print()


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n👋 KrishOpus Backend Shutting Down...")
    
    # Cleanup expired sessions
    session_manager.cleanup_expired_sessions()
    print("✅ Cleanup complete")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting KrishOpus Backend v4.0")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


