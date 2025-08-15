# Your AI powered language parent: Allo Prof!

The best way to learn a language is immersion: speaking with and listening to native speakers. But most people struggle with this, when learning a foreign language as an adult it's difficult to avoid feelings of embarassment, or to put off actually speaking for when you are "good enough". That's where Allo Prof steps in, you can start speaking, listening, writing and reading right off the bat at your own level. Working with the tutor, you can build your confidence in expressing yourself and understanding a language so that when you get a chance to engage with it in real life, you are ready to shine. 

Allo Prof is an LLM based language tutor, which will adaptively learn your ability in a second language and tailor its content to your level. Currently in development.

## Stage 1: Minimum Viable Product

- [x] Set up basic language chatbot with OpenAI API. 
- [x] Basic profile data structures.
- [ ] Implement adaptive logic - start with user input level, then change according to mistakes and acquired knowledge.
- [x] Save conversation history.
- [x] Feedback reports at the end of conversations.

## Stage 2: Simple UI

- [ ] Implement voice input.
- [ ] Add TTS for LLM output.
- [ ] Simple interface in Streamlit.
- [ ] Options: Choose difficulty level (slightly above, below or equal to my level), select unfamiliar words
- [ ] Set up proper database to store profiles and conversations (SQLite, MongoDB?).

## Stage 3: Add features

- [ ] Implement SRS: words learned in lessons should come up in later sessions.
- [ ] Topics: Allow users to choose from a few topics or decide their own.
- [ ] Adaptive learning: Adjust depending on vocab, comprehension rate. (Look into L2 literature for this step).
- [ ] Anki integration: Save new vocab and grammar for Anki study.
