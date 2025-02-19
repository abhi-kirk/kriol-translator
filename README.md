# English <-> Belizean Kriol Translator
Building an offline english <-> belizean kriol language translator on a raspberry pi. 

## Objectives
- To understand sequence-to-sequence language modeling with Transformers. 
- Solve unique challenges with data scraping and language model training specific to translation models. 
- Possibly build a performant, offline and portable translation device. 

## Product Workflow
1. Raspberry Pi connected with microphone and (small, portable) speakers. 
2. Switch on the Pi enables English -> Kriol or Kriol -> English translation. 
3. User speech captured by the microphone. 
4. ML inference steps (assuming english to kriol translation mode):
   1. English speech converted to english text. 
   2. English text translated to kriol text. 
   3. Kriol text converted to kriol speech. 
5. Translated speed output from the speakers. 

## Challenges
- Belizean Kriol is mostly a spoken language in the small country of Belize. Hence, not a lot of data exists for english-kriol translated text for use in language modeling.
- Language models are usually huge in size; hence may not fit in a small microcontroller memory. 

## Modeling
- English speech to english text: Use a pretrained mini-version of a well known speech-to-text model. Can be done later. 
- English text to Kriol text: 
  - Scrape kriol-english pairs from wherever possible. Utilize chatGPT as well as human translators to enhance dataset. 
  - Train a sequence-to-sequence langauge model from scratch to get baseline metrics. 
  - Use a pretrained multi-lingual translation model, and fine-tune it with eng-kriol pairs. 
- Kriol text to kriol speech: ?