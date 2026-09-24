import gradio as gr
import json
import os
from engineering_team.tools import initialize_training_rag
from engineering_team.crew import EngineeringTeamCrew

def upskilling_portal(training_doc, target_tech, developer_profile):
    if not training_doc or not target_tech.strip() or not developer_profile.strip():
        return "⚠️ Please fill out all fields: upload a document, specify target tech, and outline the team profile.", None
        
    try:
        # 1. Parse the uploaded file dynamically into our Chroma Vector DB
        initialize_training_rag(training_doc.name)
        
        # 2. Map input variables directly to the keys defined in tasks.yaml
        inputs = {
            'target_technology': target_tech,
            'developer_current_profile': developer_profile
        }
        
        # 3. Fire off the autonomous multi-agent crew execution loop
        crew_output = EngineeringTeamCrew().crew().kickoff(inputs=inputs)
        
        # 4. Extract the strictly typed JSON data dictionary generated via our Pydantic model
        data = crew_output.json_dict
        
        # 5. Render an elegant Markdown visualization for the dashboard view
        track_icons = {"ACCELERATED": "⚡", "STANDARD": "📘", "FOUNDATIONAL_REQUIRED": "🧱"}
        icon = track_icons.get(data.get('training_track_classification'), "📋")
        
        markdown_ui = f"""
        # 🎓 Corporate Technical Curriculum Intelligence Report
        
        ## {icon} Recommended Track: **{data.get('training_track_classification')}**
        * **Target Core Difficulty Tier:** `{data.get('difficulty_rating')}`
        
        ### 🚨 Missing Prerequisites / Knowledge Gaps:
        """
        for prereq in data.get('missing_prerequisites', []):
            markdown_ui += f"\n* {prereq}"
            
        markdown_ui += f"""
        
        ### 📅 Week-by-Week Technical Training Syllabus:
        {data.get('week_by_week_syllabus')}
        """
        
        # 6. Save data as an exportable JSON file artifact for local downloads
        output_file_name = "generated_upskilling_curriculum.json"
        with open(output_file_name, "w") as out:
            json.dump(data, out, indent=4)
            
        return markdown_ui, output_file_name
        
    except Exception as e:
        return f"🚨 Multi-Agent Orchestration Failure: {str(e)}", None

# Design layout architecture optimized for both desktop viewports and mobile vertical stacking
with gr.Blocks(title="L&D Upskilling Crew Blueprint") as demo:
    gr.Markdown("# 🏢 Autonomous Corporate L&D Program Architect Crew")
    gr.Markdown("Ingests internal legacy specifications, fetches real-time technological documentation, and builds tailored developer bootcamps using an **Agentic RAG pipeline**.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📂 Training Program Parameters")
            doc_file = gr.File(label="Upload Internal Tech Policy / Architecture Overview (.txt)", file_types=[".txt"])
            tech_input = gr.Textbox(label="Target Technology Migration Stack", placeholder="e.g., FastStream Kafka microservices, CrewAI multi-agent frameworks")
            profile_input = gr.Textbox(label="Current Developer Team Experience Baseline", lines=4, placeholder="e.g., 5 mid-level engineers proficient in writing synchronous Django REST APIs, minimal async or messaging experience.")
            submit_btn = gr.Button("Build Upskilling Strategy", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 🤖 Program Architecture Terminal")
            analysis_md = gr.Markdown(value="System status: Idle. Awaiting inputs...")
            download_action = gr.File(label="Download Structured JSON Syllabus Object File")
            
    submit_btn.click(
        fn=upskilling_portal,
        inputs=[doc_file, tech_input, profile_input],
        outputs=[analysis_md, download_action]
    )

if __name__ == "__main__":
    demo.launch()
