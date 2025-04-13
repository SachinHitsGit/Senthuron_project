from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    keywords = []
    input_text = ""
    
    if request.method == 'POST':
        input_text = request.form.get('text', '')
        
        if input_text:
            try:
                # Summarize text using LLaVA
                summary_response = ollama.chat(
                    model="llava:7b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize the following text in exactly three sentences:\n\n{input_text}"
                        }
                    ]
                )
                summary = summary_response['message']['content']
                
                # Extract keywords using LLaVA
                keywords_response = ollama.chat(
                    model="llava:7b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Extract exactly five relevant keywords from the following text:\n\n{input_text}"
                        }
                    ]
                )
                # Basic parsing of response
                keywords = keywords_response['message']['content'].split(",")[:5]
                keywords = [k.strip() for k in keywords]
                
            except Exception as e:
                summary = f"Error processing text: {str(e)}"
                keywords = []
    
    return render_template('index.html', 
                          summary=summary, 
                          keywords=keywords, 
                          input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)