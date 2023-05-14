from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

# Check if CUDA is available on pc
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

text2 = "Each generation was a rehearsal of the one before, so that that family gradually formed the repetitive pattern of a Greek fret, interrupted only once in two centuries by a nine-year-old boy who had taken a look at his prospects, tied a string around his neck with a brick to the other end, and jumped from a footbridge into two feet of water. Courage aside, he had that family's tenacity of purpose, and drowned, a break in the pattern quickly obliterated by the calcimine of silence."
text3 = " That's what it is, this arrogance, in this flamenco music this same arrogance of suffering, listen. The strength of it's what's so overpowering, the self-sufficiency that's so delicate and tender without an instant of sentimentality. With infinite pity, but refusing pity. It's a precision of suffering, he went on, abruptly working his hand in the air as though to shape it there, --the tremendous tension of violence all enclosed in a framework...in a pattern that doesn't pretend to any other level but its own, do you know what I mean? He barely glanced at her to see if she did.--It's the privacy, the exquisite sense of privacy about it, he said speaking more rapidly, --it's the sense of privacy that most popular expressions of suffering don't have, don't dare have, that's what makes it arrogant. "
# Creating a summarization pipeline using the default model ("sshleifer/distilbart-cnn-12-6")
summarizer = pipeline("summarization")
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
summarizer = pipeline(
    "summarization",
    model=model, tokenizer=tokenizer,
    framework="tf", device=device,
    max_length=500, min_length=400,
    num_beams=4, length_penalty=2.0,
    early_stopping=True, no_repeat_ngram_size=2,
    num_return_sequences=1,
    top_p=0.92, top_k=40,
    temperature=0.8,
)
summary_text = summarizer(text3)[0]['summary_text']
print(summary_text)