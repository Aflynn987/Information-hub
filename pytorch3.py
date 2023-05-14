import re
import string
import nltk
import torch
from nltk.tokenize import sent_tokenize
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

nltk.download('punkt')
device = 0 if torch.cuda.is_available() else -1

# Define preprocessing function
def preprocess(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove digits
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize sentences
    sentences = sent_tokenize(text)
    # Remove short sentences
    sentences = [s for s in sentences if len(s) > 20]
    return sentences

# Define postprocessing function
def postprocess(summary):
    # Remove leading/trailing whitespace
    summary = summary.strip()
    # Capitalize first letter
    summary = summary[0].upper() + summary[1:]
    # Add period if missing
    if summary[-1] not in ['.', '!', '?']:
        summary += '.'
    return summary

# Load model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define summarization pipeline
summarizer = pipeline(
    "summarization",
    model=model, tokenizer=tokenizer,
    framework="tf", device=device,
    max_length=150, min_length=50,
    num_beams=4, length_penalty=2.0,
    early_stopping=True, no_repeat_ngram_size=2,
    num_return_sequences=1,
    top_p=0.92, top_k=40,
    temperature=0.8,
)

# Load text and preprocess
text = """One month after the United States began what has become a troubled rollout of a national COVID
 vaccination campaign, the effort is finally gathering real steam.
Close to a million doses -- over 951,000, to be more exact -- made their way into the arms of Americans in the past 24 hours,
 the U.S. Centers for Disease Control and Prevention reported Wednesday. 
 That's the largest number of shots given in one day since the rollout began and a big jump from the previous day,
  when just under 340,000 doses were given, CBS News reported.
That number is likely to jump quickly after the federal government on Tuesday gave states the OK to vaccinate anyone
 over 65 and said it would release all the doses of vaccine it has available for distribution. Meanwhile, a number of
  states have now opened mass vaccination sites in an effort to get larger numbers of people inoculated,
   CBS News reported."""
sentences = preprocess(text)

# Generate summaries for each sentence
summaries = []
for sentence in sentences:
    summary_text = summarizer(text)[0]['summary_text'].decode('utf-8')
    summary = postprocess(summary_text)
    summaries.append(summary)

# Join summaries into a single text
summary_text = ' '.join(summaries)

# Print summary
print(summary_text)