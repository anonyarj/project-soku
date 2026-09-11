\# Project Soku



Project Soku is a privacy-first personal AI assistant designed to run locally on a user's device.



\## Current Features



\- Local LLM inference using Ollama

\- Phi-3 language model

\- Voice input through microphone

\- Local speech-to-text using Faster Whisper

\- Text-to-speech responses

\- Multi-turn conversation memory during a session

\- Offline-first architecture



\## Current Flow



User Voice

↓

Microphone

↓

Faster Whisper

↓

Text

↓

Ollama + Phi-3

↓

AI Response

↓

Text-to-Speech

↓

Soku speaks



\## Project Goal



The long-term goal is to build a personalized AI assistant that can:



\- Wake using "Hey Soku"

\- Remember user preferences locally

\- Control desktop applications

\- Perform computer actions

\- Connect to Android devices

\- Control phone functions with permission

\- Support multiple languages including Nepali

\- Integrate with specialized applications

\- Keep personal data stored locally

\- Run offline whenever possible



\## Technologies



\- Python

\- Ollama

\- Phi-3

\- Faster Whisper

\- SpeechRecognition

\- PyAudio

\- pyttsx3



\## Status



Early development.



Current milestone:



Voice → Local Speech Recognition → Local LLM → Spoken Response

