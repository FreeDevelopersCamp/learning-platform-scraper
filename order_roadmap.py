import openai
import time

openai.api_key = "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"

def order_roadmap():
    # Load the roadmap data from the file
    with open('roadmap_data.txt', 'r') as file:
        raw_text = file.read()

    # Simple sorting logic
    roadmap_topics = raw_text.split('\n')
    organized_roadmap = sorted(roadmap_topics)  # This is a basic alphabetical sort

    # Output or save the organized roadmap
    print('\n'.join(organized_roadmap))

if __name__ == "__main__":
    order_roadmap()
