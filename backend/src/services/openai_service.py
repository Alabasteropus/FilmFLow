import os
from openai import OpenAI, OpenAIError

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',  # Update to 'gpt-4' if accessible
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        generated_text = response.choices[0].message.content.strip()
        return generated_text
    except OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
