"""
Training Pipeline for SLM Entity Extraction and Template Response Formation
Uses official BNS Chapter XVII data for training
"""
import json
import asyncio
from typing import List, Dict, Any, Tuple
from pathlib import Path
import logging
from datetime import datetime

from .training_data_generator import TrainingDataGenerator
from .ollama_service import OllamaService

logger = logging.getLogger(__name__)


class SLMTrainingPipeline:
    """Training pipeline for SLM using official BNS data"""
    
    def __init__(self, bns_data_path: str, output_dir: str):
        self.bns_data_path = bns_data_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_generator = TrainingDataGenerator(bns_data_path)
        self.ollama_service = OllamaService()
        
        self.training_results = {
            "entity_extraction": {"accuracy": 0.0, "examples": []},
            "template_response": {"quality": 0.0, "examples": []}
        }
    
    async def run_full_training_pipeline(self):
        """Run the complete training pipeline"""
        logger.info("Starting SLM training pipeline...")
        
        # Step 1: Generate training data from official BNS data
        logger.info("Step 1: Generating training data from BNS Chapter XVII")
        await self.generate_training_data()
        
        # Step 2: Test Ollama connection
        logger.info("Step 2: Testing Ollama connection")
        connection_test = self.ollama_service.test_connection()
        if connection_test["status"] == "error":
            raise Exception(f"Ollama connection failed: {connection_test['message']}")
        
        # Step 3: Train entity extraction
        logger.info("Step 3: Training entity extraction")
        await self.train_entity_extraction()
        
        # Step 4: Train template response formation
        logger.info("Step 4: Training template response formation")
        await self.train_template_response()
        
        # Step 5: Evaluate and save results
        logger.info("Step 5: Evaluating results")
        await self.evaluate_and_save_results()
        
        logger.info("Training pipeline completed successfully!")
    
    async def generate_training_data(self):
        """Generate training data from official BNS data"""
        try:
            # Generate entity extraction data
            entity_data = self.data_generator.generate_entity_extraction_training_data(100)
            entity_file = self.output_dir / "entity_extraction_training.json"
            
            with open(entity_file, 'w', encoding='utf-8') as f:
                json.dump(entity_data, f, indent=2, ensure_ascii=False)
            
            # Generate template response data
            template_data = self.data_generator.generate_template_response_training_data()
            template_file = self.output_dir / "template_response_training.json"
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated {len(entity_data)} entity extraction examples")
            logger.info(f"Generated {len(template_data)} template response examples")
            
        except Exception as e:
            logger.error(f"Training data generation failed: {e}")
            raise
    
    async def train_entity_extraction(self):
        """Train entity extraction using few-shot prompting"""
        logger.info("Training entity extraction with few-shot examples...")
        
        # Load training data
        entity_file = self.output_dir / "entity_extraction_training.json"
        with open(entity_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        
        # Test entity extraction on validation samples
        validation_samples = training_data[:10]  # Use first 10 for validation
        
        correct_extractions = 0
        total_samples = len(validation_samples)
        
        for i, sample in enumerate(validation_samples):
            user_query = sample["user_query"]
            expected_entities = sample["extracted_entities"]
            
            try:
                # Extract entities using Phi-3
                extracted_entities = self.ollama_service.extract_entities(user_query)
                
                # Evaluate accuracy
                accuracy = self._evaluate_entity_extraction(expected_entities, extracted_entities)
                
                if accuracy > 0.7:  # Consider 70%+ as correct
                    correct_extractions += 1
                
                # Store example for analysis
                self.training_results["entity_extraction"]["examples"].append({
                    "query": user_query,
                    "expected": expected_entities,
                    "extracted": extracted_entities,
                    "accuracy": accuracy
                })
                
                logger.info(f"Entity extraction {i+1}/{total_samples} - Accuracy: {accuracy:.2f}")
                
            except Exception as e:
                logger.error(f"Entity extraction failed for sample {i+1}: {e}")
        
        # Calculate overall accuracy
        overall_accuracy = correct_extractions / total_samples if total_samples > 0 else 0
        self.training_results["entity_extraction"]["accuracy"] = overall_accuracy
        
        logger.info(f"Entity extraction training completed. Accuracy: {overall_accuracy:.2f}")
    
    async def train_template_response(self):
        """Train template response formation"""
        logger.info("Training template response formation...")
        
        # Load training data
        template_file = self.output_dir / "template_response_training.json"
        with open(template_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        
        # Test template response generation
        validation_samples = training_data[:5]  # Use first 5 for validation
        
        quality_scores = []
        
        for i, sample in enumerate(validation_samples):
            legal_analysis = sample["legal_analysis"]
            expected_response = sample["citizen_friendly_response"]
            
            try:
                # Generate response using Phi-3
                generated_response = self.ollama_service.format_legal_response(legal_analysis)
                
                # Evaluate quality (simple heuristics)
                quality_score = self._evaluate_response_quality(expected_response, generated_response)
                quality_scores.append(quality_score)
                
                # Store example
                self.training_results["template_response"]["examples"].append({
                    "legal_analysis": legal_analysis,
                    "expected": expected_response,
                    "generated": generated_response,
                    "quality": quality_score
                })
                
                logger.info(f"Template response {i+1}/{len(validation_samples)} - Quality: {quality_score:.2f}")
                
            except Exception as e:
                logger.error(f"Template response failed for sample {i+1}: {e}")
        
        # Calculate average quality
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        self.training_results["template_response"]["quality"] = avg_quality
        
        logger.info(f"Template response training completed. Average quality: {avg_quality:.2f}")
    
    def _evaluate_entity_extraction(self, expected: Dict, extracted: Dict) -> float:
        """Evaluate entity extraction accuracy"""
        if not expected or not extracted:
            return 0.0
        
        total_score = 0.0
        category_count = 0
        
        for category in expected.keys():
            if category in extracted:
                expected_items = set(expected[category])
                extracted_items = set(extracted[category])
                
                if expected_items:
                    # Calculate intersection over union
                    intersection = len(expected_items & extracted_items)
                    union = len(expected_items | extracted_items)
                    category_score = intersection / union if union > 0 else 0
                else:
                    # If no expected items, perfect if no extracted items
                    category_score = 1.0 if not extracted_items else 0.0
                
                total_score += category_score
                category_count += 1
        
        return total_score / category_count if category_count > 0 else 0.0
    
    def _evaluate_response_quality(self, expected: str, generated: str) -> float:
        """Evaluate response quality using simple heuristics"""
        if not expected or not generated:
            return 0.0
        
        # Simple quality metrics
        quality_score = 0.0
        
        # Check for key sections
        key_sections = ["Legal", "Next Steps", "Important", "Action"]
        section_score = sum(1 for section in key_sections if section.lower() in generated.lower())
        quality_score += (section_score / len(key_sections)) * 0.3
        
        # Check for disclaimers
        disclaimers = ["consult", "lawyer", "preliminary", "qualified"]
        disclaimer_score = sum(1 for disclaimer in disclaimers if disclaimer.lower() in generated.lower())
        quality_score += min(disclaimer_score / len(disclaimers), 1.0) * 0.3
        
        # Check response length (should be informative but not too long)
        length_score = 1.0 if 100 < len(generated) < 1000 else 0.5
        quality_score += length_score * 0.2
        
        # Check for structure (bullet points, sections)
        structure_score = 1.0 if ('**' in generated or '1.' in generated) else 0.5
        quality_score += structure_score * 0.2
        
        return min(quality_score, 1.0)
    
    async def evaluate_and_save_results(self):
        """Evaluate final results and save training report"""
        
        # Create comprehensive training report
        report = {
            "training_date": datetime.now().isoformat(),
            "bns_data_source": str(self.bns_data_path),
            "ollama_model": self.ollama_service.model,
            "results": self.training_results,
            "recommendations": self._generate_recommendations()
        }
        
        # Save training report
        report_file = self.output_dir / "training_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save detailed examples
        examples_file = self.output_dir / "training_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump({
                "entity_extraction_examples": self.training_results["entity_extraction"]["examples"],
                "template_response_examples": self.training_results["template_response"]["examples"]
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Training report saved to {report_file}")
        logger.info(f"Training examples saved to {examples_file}")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on training results"""
        recommendations = []
        
        entity_accuracy = self.training_results["entity_extraction"]["accuracy"]
        response_quality = self.training_results["template_response"]["quality"]
        
        if entity_accuracy < 0.7:
            recommendations.append("Entity extraction accuracy is below 70%. Consider refining prompts or adding more training examples.")
        
        if response_quality < 0.7:
            recommendations.append("Response quality is below 70%. Consider improving template structures and examples.")
        
        if entity_accuracy > 0.8 and response_quality > 0.8:
            recommendations.append("Training results are good. System is ready for integration testing.")
        
        recommendations.append("Continue monitoring performance with real user queries.")
        recommendations.append("Consider periodic retraining with new legal scenarios.")
        
        return recommendations
    
    def create_production_config(self) -> Dict[str, Any]:
        """Create production configuration based on training results"""
        return {
            "entity_extraction": {
                "temperature": 0.1,
                "confidence_threshold": 0.7,
                "max_tokens": 500
            },
            "template_response": {
                "temperature": 0.2,
                "max_tokens": 800,
                "include_disclaimers": True
            },
            "training_metrics": {
                "entity_accuracy": self.training_results["entity_extraction"]["accuracy"],
                "response_quality": self.training_results["template_response"]["quality"]
            }
        }


# Example usage function
async def run_training_pipeline():
    """Run the complete training pipeline"""
    pipeline = SLMTrainingPipeline(
        bns_data_path="D:/Python Programs/FINAL_PROJECT/data/bns_data/bns_ch17.json",
        output_dir="D:/Python Programs/FINAL_PROJECT/data/training_data"
    )
    
    await pipeline.run_full_training_pipeline()
    return pipeline.create_production_config()


if __name__ == "__main__":
    # Run training pipeline
    asyncio.run(run_training_pipeline())