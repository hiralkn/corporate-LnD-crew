from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from engineering_team.tools import query_learning_tool

# 1. Define the Pydantic Data Model for predictable, typed JSON responses
class UpskillingProgramReport(BaseModel):
    training_track_classification: str = Field(..., description="Must be ACCELERATED, STANDARD, or FOUNDATIONAL_REQUIRED.")
    difficulty_rating: str = Field(..., description="Recommended difficulty tier: Beginner, Intermediate, or Advanced.")
    missing_prerequisites: list[str] = Field(..., description="Key libraries or foundational concepts the team must learn first.")
    week_by_week_syllabus: str = Field(..., description="A comprehensive Markdown-formatted multi-week curriculum complete with mini-projects.")

@CrewBase
class EngineeringTeamCrew():
    """EngineeringTeam L&D Upskilling Orchestrator"""
    
    # Links to your edited agents.yaml and tasks.yaml
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def curriculum_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_analyst'],
            tools=[query_learning_tool], # Enforces the agent to use the RAG query layer
            verbose=True
        )

    @agent
    def tech_trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_trend_researcher'],
            tools=[], # Removing SerperDevTool removes the final heavy web dependency
            verbose=True
        )


    @agent
    def training_program_director(self) -> Agent:
        return Agent(
            config=self.agents_config['training_program_director'],
            verbose=True
        )

    @task
    def curriculum_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_analysis_task']
        )

    @task
    def tech_trend_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['tech_trend_research_task']
        )

    @task
    def program_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['program_generation_task'],
            output_json=UpskillingProgramReport # Forces the final agent to strictly structure its output
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
