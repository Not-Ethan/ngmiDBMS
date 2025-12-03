from src.llm_driver.llm_driver import LLMDriver
from src.llm_driver.agents.agents import LLMProvider, ModelNames
from src.llm_driver.schemas.response_schemas import SkillExtractionResponseSchema
from src.services.resume_service.resume_parser import ResumeParser
from src.database import db
from typing import List
import os
import shutil

class ResumeService:
    def __init__(self):
        self.llm_driver = LLMDriver(model_name=ModelNames.GPT_4O_MINI, provider=LLMProvider.OPENAI, response_model=SkillExtractionResponseSchema, temperature=0.6)
        self.parser = ResumeParser()

    def extract_skills(self, resume_text: str) -> List[str]:
        return self.llm_driver.extract_skils(resume_text=resume_text)
    
    def parse_resume(self, file_path: str) -> str:
        return self.parser._clean_text(self.parser._load_pdf(file_path))
    
    def upload_resume(self, user_id: int, file_path: str) -> int:
        
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        new_path = os.path.join(uploads_dir, f"{user_id}_{file_name}")
        shutil.copy2(file_path, new_path)
        
        raw_text = self.parse_resume(new_path)
        
        result = db.execute_one(
            "INSERT INTO Resumes (user_id, file_name, file_path, raw_text) VALUES (%s, %s, %s, %s) RETURNING resume_id",
            (user_id, file_name, new_path, raw_text)
        )
        resume_id = result['resume_id']
        
        skills = self.extract_skills(raw_text)
        for skill_name in skills:
            skill_result = db.execute_one(
                "INSERT INTO Skills (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING skill_id",
                (skill_name.lower(),)
            )
            if not skill_result:
                skill_result = db.execute_one("SELECT skill_id FROM Skills WHERE name = %s", (skill_name.lower(),))
            
            skill_id = skill_result['skill_id']
            
            db.execute(
                "INSERT INTO ResumeSkills (resume_id, skill_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (resume_id, skill_id)
            )
        
        return resume_id

    @staticmethod
    def get_user_resumes(user_id: int):
        return db.execute(
            "SELECT resume_id, file_name, uploaded_at FROM Resumes WHERE user_id = %s ORDER BY uploaded_at DESC",
            (user_id,)
        )

    @staticmethod   
    def get_resume_details(resume_id: int):
        resume = db.execute_one(
            "SELECT * FROM Resumes WHERE resume_id = %s",
            (resume_id,)
        )

        if resume:
            skills = db.execute(
                """SELECT s.name FROM Skills s 
                JOIN ResumeSkills rs ON s.skill_id = rs.skill_id 
                WHERE rs.resume_id = %s""",
                (resume_id,)
            )
            resume['skills'] = [skill['name'] for skill in skills]
        
        return resume