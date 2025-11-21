"""
Script to generate training data from official BNS Chapter XVII data
"""
import sys
import os
sys.path.append('backend')

from backend.app.services.training_data_generator import TrainingDataGenerator

def main():
    print("Generating training data from official BNS Chapter XVII...")
    
    # Use clean BNS data
    bns_file = "data/bns_data/bns_ch17_clean.json"
    output_dir = "data/training_data"
    
    try:
        generator = TrainingDataGenerator(bns_file)
        generator.save_training_data(output_dir)
        print("Training data generation completed successfully!")
        
    except Exception as e:
        print(f"Error generating training data: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)